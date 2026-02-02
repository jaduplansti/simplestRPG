from rich.panel import Panel;
from rich.live import Live;
from curtsies import Input;
from random import randint, choice;
from mechanics.combat import CombatHandler;
from objects.npc import NPCS;
from time import sleep;

# fix dis shit

TRAPS = ["spike_trap", "poison_trap"];

class Dungeon:
  def __init__(self, game, map_explorer):
    self.game = game;
    self.ui = game.ui;
    self.player = game.player;
    self.map_explorer = map_explorer;
    self.floor = 0;
    self.current_map = [];
    self.old_position = None;
    
    self.cause_of_death = "";
    
  def generateBlank(self, width, height):
    self.current_map = [];
    for y in range(height):
      row = [];
      for x in range(width):
        row.append(None);
      self.current_map.append(row);

  def generateBorder(self, width, height):
    for y in range(height):
      for x in range(width):
        if y == 0 or y == height - 1 or x == 0 or x == width - 1:
          self.current_map[y][x] = "wall";
  
  def generateRandomWalls(self, width, height):
    def canPlaceWall(y, x):
      free = 0
      for dy, dx in [(0,-1),(0,1),(-1,0),(1,0)]:
        ny = y + dy
        nx = x + dx
        if 0 <= ny < height and 0 <= nx < width:
          if self.current_map[ny][nx] is None:
            free += 1
      return free >= 2  # at least 2 exits
  
    for _ in range(randint(5, 10)):
      preset = randint(1, 3)
      y = randint(1, height - 2)
      x = randint(1, width - 2)
  
      if preset == 1:
        if canPlaceWall(y, x):
          self.current_map[y][x] = "wall2"
  
      elif preset == 2:
        length = randint(2, 5)
        for i in range(length):
          nx = x + i
          if nx < width - 1 and canPlaceWall(y, nx):
            self.current_map[y][nx] = "wall2"
  
      else:
        length = randint(2, 5)
        for i in range(length):
          ny = y + i
          if ny < height - 1 and canPlaceWall(ny, x):
            self.current_map[ny][x] = "wall2"
  
  def generateStair(self, width, height):
    sy = randint(1, height - 2);
    sx = randint(1, width - 2);
    self.current_map[sy][sx] = "stairDown";

  def generateEnemy(self, width, height):
    for n in range(randint(1, self.floor + 1)):
      uy = randint(1, height - 2);
      ux = randint(1, width - 2);
      
      while True:
        enemy = choice(list(NPCS));
        if NPCS[enemy].boss is True: continue;
        self.current_map[uy][ux] = enemy;
        break;
        
  def generateTrap(self, width, height):
    for n in range(self.floor + 1):
      uy = randint(1, height - 2);
      ux = randint(1, width - 2);
      
      trap = choice(TRAPS);
      self.current_map[uy][ux] = trap;
  
  def generateBoss(self, width, height):
    uy = randint(1, height - 2);
    ux = randint(1, width - 2);
      
    while True:
      if self.floor == 5: boss = "dark slime";
      elif self.floor == 10: boss = "goblin chief";
      else: boss = None;
      
      self.current_map[uy][ux] = boss;
      break;
    
  def generateMap(self, width, height):
    self.generateBlank(width, height);
    self.generateBorder(width, height);
    if self.floor == 0 or (self.floor % 5) != 0:
      self.generateRandomWalls(width, height);
      self.generateTrap(width, height);
      self.generateEnemy(width, height);
    else:
      self.generateBoss(width, height);
    self.generateStair(width, height);
    
  def findTile(self, tile):
    for y in range(len(self.current_map)):
      for x in range(len(self.current_map[y])):
        if self.current_map[y][x] == tile:
          return [y, x];
    return None;
    
  def goDown(self):
    if self.enemiesRemaining() is True: 
      self.ui.printDialogue(self.game.player.name, "i cant go down yet.. there are enemies left.");
      self.ui.awaitKey();
      self.explore();
      
    self.floor += 1;
    self.generateMap(20, 10);
    position = [randint(1, 8), randint(1, 18)];
    self.player.position = position;
    self.current_map[self.player.position[0]][self.player.position[1]] = "plr";
    self.explore();
    
  def goUp(self):
    self.player.position = self.old_position;
    self.game.exploration_handler.explore();
  
  def moveEnemy(self, width, height, aggro_range=5):
    py, px = self.player.position
  
    for y in range(height):
      for x in range(width):
        if self.current_map[y][x] not in NPCS:
          continue
  
        # not every enemy moves every tick
        if randint(1, 3) != 1:
          continue
  
        # distance to player (square range)
        dist = abs(py - y) + abs(px - x)
  
        if dist <= aggro_range:
          # --- HONE TOWARD PLAYER ---
          dy = 0
          dx = 0
  
          if py > y: dy = 1
          elif py < y: dy = -1
  
          if px > x: dx = 1
          elif px < x: dx = -1
  
          # choose axis randomly to avoid straight lines
          if randint(0, 1) == 0:
            dy = 0
          else:
            dx = 0
        else:
          # --- RANDOM MOVE ---
          dy, dx = choice([(0,-1),(0,1),(-1,0),(1,0)])
  
        ny = y + dy
        nx = x + dx
  
        if 0 <= ny < height and 0 <= nx < width:
          if self.current_map[ny][nx] == None:
            self.current_map[ny][nx] = self.current_map[y][x]
            self.current_map[y][x] = None
    
  def enemyNear(self, width, height):
    y, x = self.player.position
  
    for dy, dx in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
      ny = y + dy
      nx = x + dx
  
      if 0 <= ny < height and 0 <= nx < width:
        if self.current_map[ny][nx] in NPCS:
          return [True, self.current_map[ny][nx], (ny, nx)];
  
    return [False, None];
    
  def explore(self):
    self.ui.showStatus("rendering map!", 0.3);
    self.ui.clear();
    if self.map_explorer.findObject("plr", self.current_map) != True: self.map_explorer.placePlayer(self.game.player.position, self.current_map);

    interacted = None;

    with Input(keynames="curses") as input_generator:
      with Live(Panel(self.map_explorer.render(self.current_map, dungeon = self)), auto_refresh=False) as live:
        while interacted == None and self.game.player.stats["health"] > 0:
          key = input_generator.send(0.01);
          if key: 
            interacted = self.map_explorer.movePlayer(key, self.current_map, dungeon = self);
            if key == "i": interacted = ["inventory"];
            enemyNear = self.enemyNear(20, 10);
            if enemyNear[0] is True:
              interacted = [enemyNear[1], enemyNear[2]];
              break;
            self.moveEnemy(20, 10);
            self.useStats();
            live.update(Panel(self.map_explorer.render(self.current_map, dungeon = self)), refresh=True);
    
    if self.game.player.stats["health"] <= 0:
      self.dungeonFail();
    else: self.handleInteraction(interacted);
    
  def handleInteraction(self, interacted):
    if interacted[0] == "inventory":
      self.game.handleUseItem();
      self.explore();
    elif interacted[0] == "stairUp":
      self.goUp();
    elif interacted[0] == "stairDown":
      self.goDown();
    elif interacted[0] == "chest":
      pass;
    elif interacted[0] in NPCS:
      self.handleEncounter(interacted, interacted[0])
    elif interacted[0] == "wall2":
      y, x = interacted[1];
      self.current_map[y][x] = None;
      self.explore();
    elif interacted[0] in TRAPS:
      self.checkTrapped(interacted[0]);
      self.explore();
    
  def rewardPlayer(self):
    self.ui.clear();
  
    gold_gain = randint(20, 40) * self.floor;
    exp_gain = randint(100, 500) * self.floor;
  
    self.game.player.money += gold_gain;
    self.game.givePlayerExp(exp_gain);
    self.game.player.tryLevelUp();
  
    self.ui.panelPrint(
      f"[yellow]🏆 DUNGEON CLEARED[reset]\n"
      f"────────────────────────\n"
      f"[blue]Floor Reached[reset] : {self.floor}\n"
      f"[yellow]Gold Earned[reset]   : +{gold_gain}g\n"
      f"[green]EXP Gained[reset]    : +{exp_gain} exp\n"
      f"[bold]Cause Of Death[reset] (°)\n ({self.cause_of_death})\n"
    );
  
    self.ui.awaitKey();
    if self.floor == 0: self.ui.printDialogue(self.game.player.name, "ouch, i think i need to get stronger.");
    else: self.ui.printDialogue(self.game.player.name, "that was... not bad, i can do better next time.");
    self.ui.awaitKey();
    
  def dungeonFail(self):
    self.player.position = self.old_position;
    self.rewardPlayer();
    self.game.exploration_handler.explore();
  
  def checkTrapped(self, trap):
    if trap == "spike_trap":
      self.player.giveDamage(self.game.player.stats["max health"] * 0.1);
      if self.game.player.stats["health"] <= 0: self.cause_of_death = "impaled on a iron spike";
    if trap == "poison_trap":
      self.player.giveStatus("poisoned", 3)

  def handleEncounter(self, interacted, enemy):
    combat_handler = CombatHandler(self.game);
    combat_handler.initiateFightNpc(self.player, enemy);
    self.ui.awaitKey();
    if combat_handler.won != self.player.name: 
      self.cause_of_death = f"defeated by [bold yellow]{enemy}![reset]";
      self.dungeonFail();
    self.current_map[interacted[1][0]][interacted[1][1]] = None;
    self.map_explorer.under_player = None;
    self.explore();
    
  def enter(self):
    if self.game.player.stats["health"] <= 0:
      self.game.exploration_handler.explore();
    
    self.old_position = self.player.position;
    self.player.position = [1, 1];
    self.generateMap(20, 10);
    self.explore();
  
  def enemiesRemaining(self):
    for objs in self.current_map:
      for obj in objs:
        if obj in NPCS:
          return True;
    return False;
    
  def useStats(self):
    if self.game.player.stats["health"] <= 10:
      self.cause_of_death = "succumbed to starvation";    
    
    if self.game.player.hunger <= 10:
      self.game.player.stats["health"] = max(0, self.game.player.stats["health"] - 10);
      self.game.player.energy = max(0, self.game.player.energy - 0.5);
    else:
      self.game.player.hunger = max(0, self.game.player.hunger - 1);