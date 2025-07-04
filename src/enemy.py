from random import randint, uniform, choices;
from item import Item;
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
        self.stats[stat] += 20;
        self.stats["health"] = self.stats["max health"];
      elif stat == "luck": self.stats[stat] += 0.001;
      else: self.stats[stat] += 1;
        
  def getAction(self):
    if self.status["blocking"][0] is True:
      return choices(["taunt", None])[0];
    elif self.stats["health"] <= self.stats["max health"] * 0.25:
      return choices(["flee", "block", None], [self.flee_chance, self.block_chance, 0.5])[0];
    else: return choices(["attack", "block"], [self.attack_chance, self.block_chance])[0];
  
def createEnemy(name, level, stats : dict, attack_style : str, action_chances : list, loots : list):
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
  
  enemy.attack_style = attack_style;
  for loot in loots:
    enemy.putLoot(loot[0], loot[1]);
  return enemy;
  
    
def getEnemyByName(name, plr = None):
  if name == "slime":
    return createEnemy(
      "slime", randint(3, 4), {"strength" : 4}, "basic", [0.7, 0.2, 0.01, 0.01],
      [
        [Item("wooden sword", rarity = "common",  bodypart = "right arm", durability = 1000), 0.8]
      ]
    );
  elif name == "goblin":
    return createEnemy(
      "goblin", randint(5, 8), {"strength" : 10, "defense" : 20}, "basic", [0.7, 0.1, 0.5, 0.01],
      [
        [Item("wooden sword", rarity = "common",  bodypart = "right arm", durability = 1000), 0.8],
        [Item("health potion", rarity = "common"), 0.8],
        [Item("health potion", rarity = "uncommon"), 0.5],
      ]
    );
  elif name == "orc":
    return createEnemy(
      "orc", randint(8, 13), {"strength" : 25, "defense" : 40}, "swordsman", [0.7, 0.1, 0.5, 0.01],
      [
        [Item("wooden sword", rarity = "common",  bodypart = "right arm", durability = 1000), 0.8],
        [Item("health potion", rarity = "common"), 0.8],
        [Item("health potion", rarity = "uncommon"), 0.5],
      ]
    );
  elif name == "skeleton":
    return createEnemy(
      "skeleton", randint(9, 15), {"strength" : 20, "defense" : 10}, "basic", [0.7, 0.1, 0.5, 0.01],
      [
        [Item("wooden sword", rarity = "common",  bodypart = "right arm", durability = 1000), 0.8],
        [Item("health potion", rarity = "common"), 0.8],
        [Item("health potion", rarity = "uncommon"), 0.5],
      ]
    );
  elif name == "bandit":
    return createEnemy(
      "bandit", randint(10, 18), {"strength" : 15, "defense" : 10}, "dirty", [0.7, 0.1, 0.5, 0.01],
      [
        [Item("wooden sword", rarity = "common",  bodypart = "right arm", durability = 1000), 0.8],
        [Item("health potion", rarity = "common"), 0.8],
        [Item("health potion", rarity = "uncommon"), 0.5],
      ]
    );
    

    
