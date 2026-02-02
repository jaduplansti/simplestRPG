from rich import box;
from world.dungeon import TRAPS;

class MapExplorer:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    self.under_player = None;
    
  def getSymbol(self, obj):
    if obj is None:
      return "[dim].[reset]";
    if "path" in obj:
      return " ";
    elif obj == "wall":
      return "#";
    elif obj == "wall2":
      return "[dim]#[reset]";
    elif obj == "water":
      return "[blue]≈[reset]"
    elif obj == "tree":
      return "[green]T[reset]";
    elif obj == "bush":
      return "[green]&[reset]";
    elif obj == "rock":
      return "[dim]O[reset]";
    elif obj == "plr":
      return "[yellow]Y[reset]";
    elif obj == "home":
      return "H";
    elif obj == "shop":
      return "[cyan]S[reset]";
    elif obj == "dungeon":
      return "D";
    elif obj == "stairDown":
      return "[green]=[reset]";
    elif obj == "stairUp":
      return "[dim green]^[reset]";
    elif obj == "slime":
      return "[green]s[reset]";
    elif obj == "wolf":
      return "[red]w[reset]"
    elif obj == "skeleton":
      return "[dim]s[reset]"
    elif obj == "bandit":
      return "[yellow]в[reset]";
    elif obj == "rat":
      return "[green]r[reset]"
    elif obj == "goblin":
      return "[bold green]g[reset]";
    elif obj == "azaroth":
      return "[red]A[reset]";
    elif obj == "dark slime":
      return "[magenta]S[reset]";
    elif obj == "goblin chief":
      return "[green]G[reset]";
    elif obj == "spike_trap":
      return "∆";
    elif obj == "poison_trap":
      return "[dim green]~[reset]"
    else:
      return "?";

  def render(self, smap, dungeon=None, vision_radius=2):
    rendered = ""
    
    if dungeon is None: vision_radius = 10;
    px = py = None
    for i, row in enumerate(smap):
      for j, obj in enumerate(row):
        if obj == "plr":
          px, py = i, j
          break
      if px is not None:
        break
  
    for x, row in enumerate(smap):
      for y, obj in enumerate(row):
        if px is not None and abs(px - x) <= vision_radius and abs(py - y) <= vision_radius:
          rendered += self.getSymbol(obj)
        else:
          rendered += " "
      rendered += "\n"
  
    if dungeon is None:
      return f"{self.exploreBar(smap)}\n\n{rendered}"
    else:
      return f"{self.dungeonBar(smap, dungeon)}\n\n{rendered}"
      
  def placePlayer(self, pos, smap):
    x, y = pos;
    self.under_player = smap[x][y];
    smap[x][y] = "plr";
    self.game.player.position = [x, y];

  def interact(self, smap):
    x, y = self.game.player.position;
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
      nx = x + dx;
      ny = y + dy;
      if 0 <= nx < len(smap) and 0 <= ny < len(smap[0]):
        obj = smap[nx][ny];
        if obj != None and obj != "wall":
          return (obj, [nx, ny]);
    return None;

  def movePlayer(self, key, smap, dungeon = None):
    x, y = self.game.player.position;
    nx = x;
    ny = y;

    if key == "a":
      ny -= 1;
    elif key == "d":
      ny += 1;
    elif key == "w":
      nx -= 1;
    elif key == "s":
      nx += 1;
    elif key == "\n":
      return self.interact(smap);
    else:
      return None;

    if nx < 0 or ny < 0 or nx >= len(smap) or ny >= len(smap[0]):
      return None;
    
    if smap[nx][ny] != None and "path" in smap[nx][ny]:
      self.game.exploration_handler.changeMap(smap[nx][ny]);
      return None;
      
    if smap[nx][ny] != None and (smap[nx][ny] not in TRAPS) and (smap[nx][ny] not in ["grass", "water", "bush"]):
      return None;

    old_object = smap[nx][ny];
    smap[x][y] = self.under_player;
    self.under_player = smap[nx][ny];
    self.game.player.position = [nx, ny];
    smap[nx][ny] = "plr";
    
    if dungeon != None and old_object in TRAPS: 
      dungeon.checkTrapped(old_object);
      self.under_player = None;

  def exploreBar(self, smap):
    hp = self.game.player.stats["health"];
    max_hp = self.game.player.stats["max health"];
    gold = self.game.player.money;
    x, y = self.game.player.position;

    bar_len = 10;
    filled = int(hp / max_hp * bar_len) if max_hp > 0 else 0;
    empty = bar_len - filled;
    hp_bar = "[green]" + "█" * filled + "[dim]" + "█" * empty + "[reset]";

    nearby = [];
    for dx, dy, name in [(0, -1, "Left"), (0, 1, "Right"), (-1, 0, "Up"), (1, 0, "Down")]:
      nx = x + dx;
      ny = y + dy;
      if 0 <= nx < len(smap) and 0 <= ny < len(smap[0]):
        obj = smap[nx][ny];
        if obj != None and obj != "wall":
          nearby.append(f"{self.getSymbol(obj)} {obj.capitalize()}");

    nearby_line = "  ".join(nearby) if nearby else "[dim]None[reset]";
    line1 = f"HP: {hp_bar} {hp}/{max_hp}   Gold: {gold}   Pos: ({x}, {y})";
    line2 = f"Nearby: {nearby_line}";

    return line1 + "\n" + line2;
    
  def dungeonBar(self, smap, dungeon):
    stats = self.game.player.stats;
  
    hp = stats["health"];
    max_hp = stats["max health"];
  
    energy = self.game.player.energy;
    max_energy = self.game.player.max_energy;
  
    hunger = self.game.player.hunger;
    max_hunger = 100;
  
    level = self.game.player.level
    floor = dungeon.floor;
  
    x, y = self.game.player.position;
  
    bar_len = 10;
  
    hp_filled = int(hp / max_hp * bar_len) if max_hp > 0 else 0;
    en_filled = int(energy / max_energy * bar_len) if max_energy > 0 else 0;
    hu_filled = int(hunger / max_hunger * bar_len) if max_hunger > 0 else 0;
    
    if self.game.player.hunger <= 20:
      hu_bar = "[red]" + "█" * hu_filled + "[dim]" + "█" * (bar_len - hu_filled) + "[reset]";
    else:
      hu_bar = "[yellow]" + "█" * hu_filled + "[dim]" + "█" * (bar_len - hu_filled) + "[reset]";

    hp_bar = "[green]" + "█" * hp_filled + "[dim]" + "█" * (bar_len - hp_filled) + "[reset]";
    en_bar = "[cyan]" + "█" * en_filled + "[dim]" + "█" * (bar_len - en_filled) + "[reset]";
  
    nearby = [];
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
      nx = x + dx;
      ny = y + dy;
      if 0 <= nx < len(smap) and 0 <= ny < len(smap[0]):
        obj = smap[nx][ny];
        if obj != None and obj != "wall":
          nearby.append(f"{self.getSymbol(obj)} {obj.capitalize()}");
  
    nearby_line = "  ".join(nearby) if nearby else "[dim]None[reset]";
  
    if self.game.player.energy <= self.game.player.max_energy * 0.2:
      line1 = f"HP {hp_bar} {hp}/{max_hp}\nEN {en_bar} {energy}/{max_energy} ([bold green]DANGER[reset])";
    else:
      line1 = f"HP {hp_bar} {hp}/{max_hp}\nEN {en_bar} {energy}/{max_energy}";
    
    if self.game.player.hunger <= 20:
      line2 = f"HU {hu_bar} {hunger}/{max_hunger} ([bold red]LOW[reset])\nLv {level} Floor {floor}";
    else:
      line2 = f"HU {hu_bar} {hunger}/{max_hunger}\nLv {level} Floor {floor}";
    
    line3 = f"Nearby: {nearby_line}";
  
    return line1 + "\n" + line2 + " " + line3;
  
  def findObject(self, name, smap):
    for y in smap:
      for x in y:
        if x == name:
          return True;
    return False;