from random import randint, uniform
from item import Item
import json

class Character:
  def __init__(self, name):
    self.name = name
    self.level = 1
    self.exp = 0
    
    self.location = "home"
    self.money = 1
    self.energy = 100
    
    self.status = {"blocking": False}
    
    self.stats = {
      "health": 100,
      "max health": 100,
      "strength": randint(5, 10),
      "defense": randint(5, 10),
      "luck": round(uniform(0.1, 0.4), 4),
    }
    
    self.equipment = {"head": None, "chest": None, "left arm": None, "right arm": None, "boots": None}
    
    self.attack_style = "debug"
    self.inventory = {}
    self.skills = {}
    self.magic = {}
  
  def rerollStats(self):
    for stat in self.stats:
      if stat != "health":
        self.stats[stat] = randint(1, 10)
  
  def itemExists(self, item):
    return item in self.inventory
      
  def addItemToInventory(self, item):
    if self.itemExists(item.name):
      self.inventory[item.name]["amount"] += 1
    else:
      self.inventory[item.name] = {"amount": 1, "item": item}
  
  def getAmountOfItem(self, item):
    return self.inventory[item]["amount"]
  
  def getItem(self, item):
    return self.inventory[item]["item"]
  
  def usedItem(self, item):
    if self.getAmountOfItem(item) <= 1:
      del self.inventory[item]
    else:
      self.inventory[item]["amount"] -= 1
      
  def giveDamage(self, dmg):
    self.stats["health"] -= min(self.stats["health"], dmg)
    
  def attackEnemy(self, dmg):
    self.enemy.giveDamage(dmg)
  
  def giveExp(self, exp):
    self.exp += exp
  
  def canLevelUp(self):
    return self.exp >= (self.level * 100)
  
  def tryLevelUp(self): 
    leveled_up = False
    while self.canLevelUp():
      self.exp -= (self.level * 100)
      self.level += 1
      self.statLevelUp()
      leveled_up = True
    return leveled_up
  
  def statLevelUp(self):
    for stat in self.stats:
      if stat == "max health":
        self.stats[stat] += 10
      elif stat == "luck":
        self.stats[stat] = round(self.stats[stat] + 0.01, 4)
      else:
        self.stats[stat] += 2
        
  def isDead(self):
    return self.stats["health"] <= 0
  
  def setLocation(self, location):
    self.location = location
  
  def healPlayer(self, heal):
    self.stats["health"] = min(self.stats["health"] + heal, self.stats["max health"])
  
  def isEquipped(self, item):
    return self.equipment[item.bodypart] and self.equipment[item.bodypart].name == item.name
    
  def equipItem(self, item):
    if item.bodypart in self.equipment:
      self.equipment[item.bodypart] = item
  
  def getMaxStat(self):
    return 10 * self.level
  
  def getIncreasedStat(self):
    return 2 * self.level
  
  def getColorBasedOnStat(self, stat):
    ratio = self.stats[stat] / self.getMaxStat()
    if ratio <= 0.25:
      return "red"
    elif ratio <= 0.5:
      return "yellow"
    elif ratio <= 1:
      return "green"
    return "cyan"
  
  def getRankBasedOnStat(self, stat):
    ratio = self.stats[stat] / self.getMaxStat()
    
    if ratio <= 0.05: return "E"
    elif ratio <= 0.15: return "F"
    elif ratio <= 0.3: return "D"
    elif ratio <= 0.45: return "C"
    elif ratio <= 0.6: return "B"
    elif ratio <= 0.75: return "A"
    elif ratio <= 0.9: return "S"
    elif ratio <= 1.0: return "S+"
    elif ratio <= 1.15: return "SS"
    elif ratio <= 1.3: return "SS+"
    elif ratio <= 1.5: return "SSS"
    elif ratio <= 1.75: return "SSS+"
    return "???"
  
  def getFatigueMultiplier(self):
    if self.energy <= 25:
      return 0.25
    elif self.energy <= 50:
      return 0.5
    elif self.energy <= 75:
      return 0.8
    return 1
      
  def deductEnergy(self):
    self.energy = max(0, round(self.energy - 5 / self.getFatigueMultiplier()))
  
  def loadData(self, path):
    with open(path, "r") as file:
      data = json.load(file)
      self.name = data["name"]
      self.energy = data["energy"]
      self.stats = data["stats"]
  
  def loadDataFromJson(self, s):
    data = json.loads(s)
    self.name = data["name"]
    self.energy = data["energy"]
    self.stats = data["stats"]
    return self
    
  def getData(self):
    return json.dumps(self.__dict__)
