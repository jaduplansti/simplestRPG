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
    
    self.berserk = False;
    
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
    
def getEnemyByName(name):
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
    
    goblin.attack_chance = 0.8;
    goblin.block_chance = 0.5;
    goblin.attack_style = "basic";
    return goblin;
    
  elif name == "skeleton":
    skeleton = Enemy("skeleton");
    skeleton.level = randint(3, 5);
    skeleton.stats["health"] = 20;
    skeleton.stats["max health"] = 20;
    skeleton.stats["strength"] = randint(10, 15) + skeleton.getIncreasedStat();
    skeleton.stats["defense"] = randint(10, 15) + skeleton.getIncreasedStat();
    
    skeleton.attack_chance = 0.9;
    skeleton.block_chance = 0.1;
    skeleton.attack_style = "basic";
    return skeleton;
  
  elif name == "baker":
    baker = Enemy("baker");
    baker.level = 25;
    
    baker.stats["health"] = 1000;
    baker.stats["max health"] = 1000;
    baker.stats["strength"] = 10 + baker.getIncreasedStat();
    baker.stats["defense"] = 10 + baker.getIncreasedStat();
    
    baker.attack_chance = 0.5;
    baker.block_chance = 0.5;
    baker.attack_style = "basic";
    return baker;