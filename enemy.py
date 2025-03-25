from random import randint, uniform, choices;
from item import Item;

class Enemy():
  def __init__(self, name):
    self.name = name;
    self.level = 0;
    self.enemy = None;
    
    self.loot = [None];
    self.loot_chance = [0.5];
    
    self.attack_chance = 0;
    self.defend_chance = 0;
    
    self.status = {
      "blocking" : False,
    }
    
    self.stats = {
      "health" : 100,
      "max health" : 100,
      "strength" : 0,
      "defense" : 0,
      "luck" : round(uniform(0.1, 0.5), 4),
    }
    
    self.attack_style = None;
    
  def getLoot(self):
    return choices(self.loot, self.loot_chance)[0];
  
  def putLoot(self, item, chance):
    self.loot.append(item);
    self.loot_chance.append(chance);
    
  def giveDamage(self, dmg):
    self.stats["health"] -= max(0, dmg);
    
  def attackEnemy(self, dmg):
    self.enemy.giveDamage(dmg);
  
  def isDead(self):
    if self.stats["health"] <= 0:
      return True;
    return False;
  
  def getIncreasedStat(self):
    return self.level * 2;
    
def getEnemyByName(name):
  if name == "slime":
    slime = Enemy("slime");
    slime.level = randint(1, 5);
    
    slime.stats["health"] = 50;
    slime.stats["max health"] = 50;
    slime.stats["strength"] = randint(6, 8) + slime.getIncreasedStat();
    slime.stats["defense"] = randint(2, 5) + slime.getIncreasedStat();
    
    slime.attack_chance = 0.5;
    slime.defend_chance = 0;
    slime.attack_style = "basic";

    slime.putLoot(Item("wooden sword", rarity = "common",  bodypart = "left arm"), 0.8);
    slime.putLoot(Item("health potion", rarity = "common"), 0.1);
    return slime;
    
  elif name == "goblin":
    goblin = Enemy("goblin");
    goblin.level = randint(1, 5);
    goblin.stats["health"] = 100;
    goblin.stats["max health"] = 100;
    goblin.stats["strength"] = randint(8, 12) + goblin.getIncreasedStat();
    goblin.stats["defense"] = randint(8, 15) + goblin.getIncreasedStat();
    
    goblin.attack_chance = 0.8;
    goblin.defend_chance = 0.5;
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
    skeleton.defend_chance = 0.1;
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
    baker.defend_chance = 0.5;
    baker.attack_style = "basic";
    return baker;