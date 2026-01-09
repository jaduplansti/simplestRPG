from rich.panel import Panel;
from rich.live import Live;
from curtsies import Input;
from random import randint, choice;
from mechanics.combat import CombatHandler;
from objects.npc import NPCS;
from time import sleep;

TRAPS = ["spike_trap", "poison_trap"];

class Dungeon:
  def __init__(self, game, map_explorer):
    self.game = game;
    self.ui = game.ui;
    self.player = game.player;
    self.map_explorer = map_explorer;
    self.floor = 0;
    self.current_map = [];
    self.maps = [];
    self.saved_positions = [];
    self.old_position = None;

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
          self.current_map[y][x] = "wall"
  
      elif preset == 2:
        length = randint(2, 5)
        for i in range(length):
          nx = x + i
          if nx < width - 1 and canPlaceWall(y, nx):
            self.current_map[y][nx] = "wall"
  
      else:
        length = randint(2, 5)
        for i in range(length):
          ny = y + i
          if ny < height - 1 and canPlaceWall(ny, x):
            self.current_map[ny][x] = "wall"
  
  def generateStair(self, width, height):
    sy = randint(1, height - 2);
    sx = randint(1, width - 2);
    self.current_map[sy][sx] = "stairDown";

    while True:
      uy = randint(1, height - 2);
      ux = randint(1, width - 2);
      if self.current_map[uy][ux] == None:
        self.current_map[uy][ux] = "stairUp";
        break;
  
  def generateEnemy(self, width, height):
    for n in range(randint(1, self.floor + 1)):
      uy = randint(1, height - 2);
      ux = randint(1, width - 2);
      
      enemy = choice(list(NPCS));
      self.current_map[uy][ux] = enemy;
  
  def generateTrap(self, width, height):
    for n in range(self.floor + 1):
      uy = randint(1, height - 2);
      ux = randint(1, width - 2);
      
      trap = choice(TRAPS);
      self.current_map[uy][ux] = trap;

  def generateMap(self, width, height):
    self.generateBlank(width, height);
    self.generateBorder(width, height);
    self.generateRandomWalls(width, height);
    self.generateTrap(width, height);
    self.generateEnemy(width, height);
    self.generateStair(width, height);
    
  def findTile(self, tile):
    for y in range(len(self.current_map)):
      for x in range(len(self.current_map[y])):
        if self.current_map[y][x] == tile:
          return [y, x];
    return None;
    
  def goDown(self):
    self.maps.append(self.current_map);
    self.saved_positions.append(self.player.position);
    self.floor += 1;
  
    self.generateMap(20, 10);
  
    stair = self.findTile("stairUp");
    if stair:
      y, x = stair;
      placed = False;
      for dy, dx in [(0,-1),(0,1),(-1,0),(1,0)]:
        ny, nx = y + dy, x + dx;
        if 0 <= ny < len(self.current_map) and 0 <= nx < len(self.current_map[0]):
          if self.current_map[ny][nx] == None:
            self.player.position = [ny, nx];
            placed = True;
            break;
      if not placed:
        self.player.position = [1, 1];
    else:
      self.player.position = [1, 1];
    self.current_map[self.player.position[0]][self.player.position[1]] = "plr";
    self.explore();
    
  def goUp(self):
    if self.maps:
      self.current_map = self.maps.pop();
      self.player.position = self.saved_positions.pop();
      self.floor -= 1;
      self.explore();
    else:
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
    self.map_explorer.placePlayer(self.player.position, self.current_map);
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
            live.update(Panel(self.map_explorer.render(self.current_map, dungeon = self)), refresh=True);
    
    if self.game.player.stats["health"] <= 0:
      self.dungeonFail();
    elif interacted[0] == "inventory":
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
    elif interacted[0] in TRAPS:
      self.checkTrapped(interacted[0]);
      self.explore();
  
  def dungeonFail(self):
    self.player.position = self.old_position;
    self.game.exploration_handler.explore();
  
  def checkTrapped(self, trap):
    if trap == "spike_trap":
      self.player.giveDamage(self.game.player.stats["max health"] * 0.1);
    if trap == "poison_trap":
      self.player.giveStatus("poisoned", 3)
      
  def handleEncounter(self, interacted, enemy):
    combat_handler = CombatHandler(self.game);
    combat_handler.initiateFightNpc(self.player, enemy);
    self.ui.awaitKey();
    if combat_handler.won != self.player.name: self.explore();
    self.current_map[interacted[1][0]][interacted[1][1]] = None;
    self.explore();
    
  def enter(self):
    self.old_position = self.player.position;
    self.player.position = [1, 1];
    self.generateMap(20, 10);
    self.explore();