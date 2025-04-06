from random import randint, uniform, choices;
from item import Item;
from character import Character;

class Enemy(Character):
  def __init__(self, name):
    super().__init__(name);
    self.loot = [None];
    self.loot_chance = [0.5];
    
    self.attack_chance = 0;
    self.block_chance = 0;
    self.flee_chance = 0;
    self.taunt_chance = 0;
  
  def getLoot(self):
    return choices(self.loot, self.loot_chance)[0];
  
  def putLoot(self, item, chance):
    self.loot.append(item);
    self.loot_chance.append(chance);
  
  def goBerserk(self):
    self.energy = 1000;
    for stat in self.stats:
      self.stats[stat] *= 1.5;
    self.stats["health"] = self.stats["max health"];
    self.berserk = True;
    
def getEnemyByName(name, plr = None):
  if name == "slime":
    slime = Enemy("slime");
    slime.level = randint(1, 2);
    
    slime.stats["health"] = 20;
    slime.stats["max health"] = 20;
    slime.stats["strength"] = slime.getIncreasedStat();
    slime.stats["defense"] = slime.getIncreasedStat();
    
    slime.attack_chance = 0.5;
    slime.block_chance = 0;
    slime.attack_style = "basic";

    slime.putLoot(Item("wooden sword", rarity = "common",  bodypart = "left arm"), 0.8);
    slime.putLoot(Item("health potion", rarity = "common"), 0.1);
    return slime;
    
  elif name == "goblin":
    goblin = Enemy("goblin");
    goblin.level = randint(3, 5);
    goblin.stats["health"] = 50;
    goblin.stats["max health"] = 50;
    goblin.stats["strength"] = randint(8, 12) + goblin.getIncreasedStat();
    goblin.stats["defense"] = randint(8, 15) + goblin.getIncreasedStat();
    
    goblin.attack_chance = 0.5;
    goblin.block_chance = 0.1;
    goblin.flee_chance = 0.8;
    goblin.taunt_chance = 0.8;

    goblin.attack_style = "basic";
    return goblin;
    
  elif name == "skeleton":
    skeleton = Enemy("skeleton");
    skeleton.level = randint(3, 5);
    skeleton.stats["health"] = 150;
    skeleton.stats["max health"] = 150;
    skeleton.stats["strength"] = randint(10, 15) + skeleton.getIncreasedStat();
    skeleton.stats["defense"] = randint(10, 15) + skeleton.getIncreasedStat();
    
    skeleton.attack_chance = 0.9;
    skeleton.block_chance = 0.1;
    skeleton.attack_style = "basic";
    return skeleton;
  
  elif name == "clone":
    clone = Enemy("clone");
    clone.level = plr.level;
    
    for stat in plr.stats:
      clone.stats[stat] = plr.stats[stat];
      
    clone.attack_chance = 0.5;
    clone.block_chance = 0.5;
    clone.attack_style = plr.attack_style;
    return clone;
  
  elif name == "deity":
    deity = Enemy("exodus the god of death");
    deity.level = 999999;
    
    for stat in deity.stats:
      deity.stats[stat] = 100 * deity.level
      
    deity.attack_chance = 1;
    deity.block_chance = 0.1;
    deity.attack_style = "debug";
    return deity;