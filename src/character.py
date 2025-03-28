from random import randint, uniform;
from item import Item;

class Character:
  def __init__(self, name):
    self.name = name;
    self.level = 1;
    self.exp = 0;
    
    self.location = "home";
    self.money = 1;
    self.energy = 100;
    
    self.status = {
      "blocking" : False,
    }
    
    self.stats = {
      "health" : 100,
      "max health" : 100,
      "strength" : randint(5, 10),
      "defense" : randint(5, 10),
      "luck" : round(uniform(0.1, 0.5), 4),
    };
    
    self.equipment = {
      "head" : None,
      "chest" : None,
      "left arm" : None,
      "right arm" : None,
      "boots" : None,
    };
    
    self.attack_style = "basic";
    self.inventory = {};
    self.skills = {};
    self.magic = {};
    
  def rerollStats(self):
    for stat in self.stats:
      if stat not in ["health"]:
        self.stats[stat] = randint(1, 10);
  
  def itemExists(self, item):
    try:
      self.inventory[item];
      return True;
    except KeyError:
      return False;
      
  def addItemToInventory(self, item):
    if self.itemExists(item.name) is True:
      self.inventory[item.name]["amount"] += 1;
    else:
      self.inventory.update({
        item.name : {"amount" : 1, "item" : item}
      });
  
  def getAmountOfItem(self, item):
    return self.inventory[item]["amount"];
  
  def getItem(self, item):
    return self.inventory[item]["item"];
  
  def usedItem(self, item):
    if self.getAmountOfItem(item) <= 1:
      del self.inventory[item];
    else:
      self.inventory[item]["amount"] -= 1;
      
  def giveDamage(self, dmg):
    self.stats["health"] -= min(self.stats["health"], dmg);
    
  def attackEnemy(self, dmg):
    self.enemy.giveDamage(dmg);
  
  def giveExp(self, exp):
    self.exp += exp;
  
  def canLevelUp(self):
    if self.exp >= (self.level * 100):
      return True;
    else:
      return False;
  
  def tryLevelUp(self): 
    leveled_up = False;
    while self.canLevelUp() is True:
      self.exp -= (self.level * 100);
      self.level += 1;
      self.statLevelUp();
      leveled_up = True;
    return leveled_up;
  
  def statLevelUp(self):
    for stat in self.stats:
      if stat == "max health":
        self.stats[stat] += 10;
      elif stat == "luck":
        self.stats[stat] = round(self.stats[stat] + 0.01, 4);
      else:
        self.stats[stat] += 2;
        
  def isDead(self):
    if self.stats["health"] <= 0:
      return True;
    return False;
  
  def setLocation(self, location):
    self.location = location;
  
  def healPlayer(self, heal):
    self.stats["health"] = min(self.stats["health"] + heal, self.stats["max health"]);
  
  def isEquipped(self, item):
    if self.equipment[item.bodypart].name == item.name:
      return True;
    return False;
    
  def equipItem(self, item): # todo check if already equipped
    if item.bodypart in self.equipment:
      self.equipment[item.bodypart] = item;
  
  def getMaxStat(self):
    return (10 * self.level);
  
  def getIncreasedStat(self):
    return (2 * self.level);
  
  def getColorBasedOnStat(self, stat):
    if self.stats[stat] <= self.getMaxStat() * 0.25:
      return "red";
    elif self.stats[stat] <= self.getMaxStat() * 0.5:
      return "yellow";
    elif self.stats[stat] <= self.getMaxStat() * 1:
      return "green";
    if self.stats[stat] > self.getMaxStat() * 1:
      return "cyan";
  
  def getRankBasedOnStat(self, stat):
    ratio = self.stats[stat] / self.getMaxStat()
    
    if ratio <= 0.05:
        return "E"
    elif ratio <= 0.15:
        return "F"
    elif ratio <= 0.3:
        return "D"
    elif ratio <= 0.45:
        return "C"
    elif ratio <= 0.6:
        return "B"
    elif ratio <= 0.75:
        return "A"
    elif ratio <= 0.9:
        return "S"
    elif ratio <= 1.0:
        return "S+"
    elif ratio <= 1.15:
        return "SS"
    elif ratio <= 1.3:
        return "SS+"
    elif ratio <= 1.5:
        return "SSS"
    elif ratio <= 1.75:
        return "SSS+"
    else:
        return "???"
    