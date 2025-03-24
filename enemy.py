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
  
  def getLoot(self):
    return choices(self.loot, self.loot_chance)[0];
  
  def putLoot(self, item, chance):
    self.loot.append(item);
    self.loot_chance.append(chance);
    
  def giveDamage(self, dmg):
    self.stats["health"] -= dmg;
    
  def attackEnemy(self, dmg):
    self.enemy.giveDamage(dmg);
  
  def isDead(self):
    if self.stats["health"] <= 0:
      return True;
    return False;
  
def getEnemyByName(name):
  if name == "slime":
    slime = Enemy("slime");
    slime.level = 1;
    slime.stats["health"] = 10;
    slime.stats["max health"] = 10;
    slime.stats["strength"] = 1;
    slime.stats["defense"] = 1;
    
    slime.attack_chance = 0.5;
    slime.defend_chance = 0;

    slime.putLoot(Item("wooden sword", rarity = "uncommon"), 0.6);
    slime.putLoot(Item("condom", rarity = "epic"), 0.1);
    return slime;
    
  elif name == "goblin":
    goblin = Enemy("goblin");
    goblin.level = randint(2, 5);
    goblin.stats["health"] = 20;
    goblin.stats["max health"] = 20;
    goblin.stats["strength"] = randint(2, 5);
    goblin.stats["defense"] = randint(2, 5);
    
    goblin.attack_chance = 0.8;
    goblin.defend_chance = 0.5;

    return goblin;
    
  elif name == "skeleton":
    skeleton = Enemy("skeleton");
    skeleton.level = randint(3, 5);
    skeleton.stats["health"] = 5;
    skeleton.stats["max health"] = 5;
    skeleton.stats["strength"] = 10;
    skeleton.stats["defense"] = 1;
    
    skeleton.attack_chance = 0.9;
    skeleton.defend_chance = 0.1;
    
    return skeleton;
  
  elif name == "baker":
    baker = Enemy("baker");
    baker.level = 15;
    
    baker.stats["health"] = 100;
    baker.stats["max health"] = 100;
    baker.stats["strength"] = 10;
    baker.stats["defense"] = 6;
    
    baker.attack_chance = 0.5;
    baker.defend_chance = 0.5;

    return baker;