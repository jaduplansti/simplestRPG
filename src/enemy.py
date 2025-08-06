from random import randint, uniform, choices;
from item import getItem;
from character import Character;

class Enemy(Character):
  def __init__(self, name):
    super().__init__(name);
    self.loot = [None];
    self.loot_chance = [0.5];
    
    self.attack_chance = 0.1;
    self.block_chance = 0.1;
    self.flee_chance = 0.1;
    self.taunt_chance = 0.1;
    
    self.boss = False;
    
  def getLoot(self):
    return choices(self.loot, self.loot_chance)[0];
  
  def putLoot(self, item, chance):
    self.loot.append(item);
    self.loot_chance.append(chance);
  
  def goBerserk(self):
    self.energy = 100;
    for stat in self.stats:
      self.stats[stat] *= 1.5;
    self.stats["health"] = self.stats["max health"];
    self.berserk = True;
  
  def statLevelUp(self):
    for stat in self.stats:
      if stat == "max health":
        self.stats[stat] += 40;
        self.stats["health"] = self.stats["max health"];
      elif stat == "luck": self.stats[stat] += 0.001;
      else: self.stats[stat] += 1;
  
  def move(self, away = False):
    if not away:
      if self.enemy.zone < self.zone:
        return choices(["move backward", None], [0.8, 0.2])[0]
      elif self.enemy.zone > self.zone:
        return choices(["move forward", None], [0.8, 0.2])[0]
    else:
      if self.enemy.zone < self.zone:
        return choices(["move forward", None], [0.8, 0.2])[0]
      elif self.enemy.zone > self.zone:
        return choices(["move backward", None], [0.8, 0.2])[0]
    
    return choices(["move backward", "move forward", None], [0.4, 0.4, 0.2])[0]
    
  def getAction(self, ui):
    if randint(1, 3) == 1:
      _move = self.move(choices([True, False])[0]);
      if _move != None: return _move;
     
    action = self.customAction(ui);
    if action != None: return action;
    
    if self.status["blocking"][0] is True:
      return choices(["taunt", ""])[0];
    elif self.stats["health"] <= self.stats["max health"] * 0.20:
      return choices(["flee", "block", ""], [self.flee_chance, self.block_chance, 0.5])[0];
    else: return choices(["attack", "block"], [self.attack_chance, self.block_chance])[0];

  def customAction(self, ui):
    if self.name == "fallen knight":
      if self.stats["health"] <= self.stats["max health"] * 0.2: 
        return choices(["use, health potion", "perform, parry"])[0];
      else: return choices(["perform, trislash", None])[0];
      
    if self.name == "elf":
      if self.attack_style == "archer" and self.itemExists("wooden sword") and not self.itemExists("wooden arrow"): return "use, wooden sword";
      elif self.attack_style == "archer": return choices(["perform, arrow rain", None], [0.2, 0.8])[0];
      elif self.attack_style == "swordsman": return choices(["perform, parry", "perform, trislash", None], [0.2, 0.2, 0.6])[0];

    if self.name == "priest":
      if self.stats["health"] <= self.stats["max health"] * 0.5 and randint(1, 4) == 1: return "perform, blunt recovery";
      elif randint(1, 4) == randint(1, 4) and self.enemy.stats["health"] >= self.enemy.stats["max health"] * 0.7: return "perform, divine restriction";
      elif randint(1, 3) == randint(1, 3) and self.enemy.status["blocking"][0] is True: return "perform, status wipe";
    
def createEnemy(name, level, stats : dict, attack_style : str, action_chances : list, loots : list, boss = False, game = None, items = None):
  enemy = Enemy(name);
  enemy.level = level;
  
  for stat in stats:
    enemy.stats[stat] = stats[stat];
 
  for _ in range(enemy.level + 1):
    enemy.statLevelUp();
  
  enemy.attack_chance = action_chances[0];
  enemy.block_chance = action_chances[1];
  enemy.flee_chance = action_chances[2];
  enemy.taunt_chance = action_chances[3];
  
  if game != None: game.giveStyle(enemy, attack_style, False);
  else: enemy.attack_style = attack_style;
  
  if items != None:
    for item in items: enemy.addItemToInventory(getItem(item[0]), item[1]);
    
  for loot in loots:
    enemy.putLoot(loot[0], loot[1]);
  enemy.boss = boss;
  return enemy;

def getEnemyByName(name, plr = None, game = None):
  if name == "slime":
    return createEnemy(
      "slime", randint(1, 1), {"strength" : 1}, "basic", [0.7, 0.2, 0.01, 0.01],
      [
        [getItem("wooden sword"), 0.5],
        [getItem("wooden bow"), 0.5],
        [getItem("wooden arrow"), 0.4]
      ]
    );
  elif name == "goblin":
    return createEnemy(
      "goblin", randint(3, 5), {"strength" : 6, "defense" : 6}, "basic", [0.7, 0.1, 0.5, 0.01],
      [
        [getItem("wooden sword"), 0.5],
        [getItem("starter chest"), 0.01],
        [getItem("energy potion"), 0.4],
      ]
    );
  elif name == "orc":
    return createEnemy(
      "orc", randint(6, 8), {"strength" : 12, "defense" : 10}, "swordsman", [0.7, 0.1, 0.5, 0.01],
      [
        [getItem("wooden sword"), 0.5],
        [getItem("starter chest"), 0.01],
        [getItem("scroll of teleport"), 0.01]     
      ]
    );
  elif name == "skeleton":
    return createEnemy(
      "skeleton", randint(6, 8), {"strength" : 15}, "basic", [0.7, 0.1, 0.5, 0.01],
      [
        [getItem("wooden sword"), 0.5],
        [getItem("wooden bow"), 0.5],
        [getItem("wooden arrow"), 0.4]
      ]
    );
  elif name == "bandit":
    return createEnemy(
      "bandit", randint(9, 11), {"strength" : 10, "dexterity": 20}, "dirty", [0.7, 0.1, 0.5, 0.01],
      [
        [getItem("leather gloves"), 0.5],
        [getItem("scroll of teleport"), 0.01]      
      ]
    );
  elif name == "elf":
    return createEnemy(
      "elf", randint(10, 12), {"strength" : 20, "defense" : 20, "dexterity" : 30}, "archer", [0.7, 0.1, 0.5, 0.01],
      [
        [getItem("leather gloves"), 0.5],
        [getItem("scroll of teleport"), 0.01]      
      ],
      game = game,
      items = [
        ["wooden sword", 1],
        ["wooden arrow", randint(3, 7)]
      ],
    );
  elif name == "fallen knight":
    return createEnemy(
      "fallen knight", randint(25, 30), {"strength" : 100, "defense" : 100}, "swordsman", [0.5, 0.4, 0.1, 0],
      [
        [getItem("scroll of instant kill"), 0.1]    
      ],
      True,
      game,
    );
  elif name == "priest":
    return createEnemy(
      "priest", randint(30, 35), {"strength" : 50, "defense" : 200}, "cleric", [0.7, 0.3, 0.1, 0],
      [
        [getItem("bible"), 0.1]    
      ],
      True,
      game,
    );
    
ENEMIES = [
  #"bandit", 
  "slime", 
#   "orc", 
#   "goblin", 
#   "skeleton",
#   "elf",
#   "fallen knight",
#   "priest",
]