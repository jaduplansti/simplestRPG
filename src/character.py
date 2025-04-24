from random import randint, uniform
from item import Item, removeEquipment;
from skill import Skill;
from copy import deepcopy;
import json;

class Character:
  def __init__(self, name):
    self.name = name
    self.level = 1
    self.exp = 0;
    self.position = 0;
    
    self.location = "home";
    self.money = 1
    self.energy = 100
    self.berserk = False;

    self.status = {
      "blocking" : [False, 0],
      "stunned" : [False, 0],
      "bleeding" : [False, 0],
      "parrying" : [False, 0],
    }
    
    self.stats = {
      "health": 100,
      "max health": 100,
      "strength": randint(5, 10),
      "defense": randint(5, 10),
      "luck": 0.3,
    }
    
    self.equipment = {"head": None, "chest": None, "left arm": None, "right arm": None, "boots": None}
    
    self.attack_style = "basic"
    self._class = None;
    
    self.inventory = {}
    self.skills = {}
    self.magic = {}
    
    self.addSkill(Skill("crimson edge", 10));
    self.addItemToInventory(Item("health potion"), 100);
    
  def to_dict(self):
    return {
      "name": self.name,
      "level": self.level,
      "exp": self.exp,
      "position": self.position,
      "location": self.location,
      "money": self.money,
      "energy": self.energy,
      "status": self.status,
      "berserk": self.berserk,
      "stats": self.stats,
      "equipment": {k: v.to_dict() if v else None for k, v in self.equipment.items()},
      "attack_style": self.attack_style,
      "_class": self._class,
      "skills": self.skills,
      "magic": self.magic,
      "skills": {k: v.to_dict() if v else None for k, v in self.skills.items()},
      "inventory": {
        name: {
          "item": item_data["item"].to_dict(),
          "amount": item_data["amount"]
        } for name, item_data in self.inventory.items()
      },
    }

  @classmethod
  def from_dict(cls, data):
    char = cls(data["name"])
    char.level = data["level"]
    char.exp = data["exp"]
    char.position = data["position"]
    char.location = data["location"]
    char.money = data["money"]
    char.energy = data["energy"]
    char.status = data["status"]
    char.berserk = data["berserk"]
    char.stats = data["stats"]
    char.equipment = {
      k: Item.from_dict(v) if v else None for k, v in data["equipment"].items()
    }
    char.skills = {
       k: Skill.from_dict(v) if v else None for k, v in data["skills"].items()
    }
    char.attack_style = data["attack_style"]
    char._class = data["_class"]
    char.inventory = {
      name: {
        "item": Item.from_dict(item_data["item"]),
        "amount": item_data["amount"]
      } for name, item_data in data["inventory"].items()
    }
    char.magic = data["magic"]
    return char;

  def save(self, filename="character_save.json"):
    with open(filename, "w") as f:
      json.dump(self.to_dict(), f, indent=2)

  @classmethod
  def load(cls, filename="character_save.json"):
    with open(filename, "r") as f:
      data = json.load(f)
      return cls.from_dict(data)
    
  def rerollStats(self):
    for stat in self.stats:
      if stat != "health":
        self.stats[stat] = randint(1, 10)
  
  def itemExists(self, item):
    return item in self.inventory
      
  def addItemToInventory(self, item, n = 1):
    for _ in range(0, n):
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
  
  def equipItem(self, item):
    if self.isEquipped(item) != True:
      self.equipment[item.bodypart] = deepcopy(item);
      return True;
    return False;
  
  def useEquipment(self, bodypart, n):
    brokens = [];
    for part in bodypart:
      if self.equipment[part] != None and self.equipment[part].handleDurability(n) is True: 
        brokens.append(self.equipment[part].name)
        removeEquipment(self, part);
    return brokens;
    
  def giveDamage(self, dmg):
    self.stats["health"] -= min(self.stats["health"], dmg)
    
  def attackEnemy(self, dmg):
    self.enemy.giveDamage(dmg);
    
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
        self.stats[stat] += 50;
        self.stats["health"] = self.stats["max health"];
      elif stat == "luck":
        self.stats[stat] = round(self.stats[stat] + 0.0001, 4)
      else:
        self.stats[stat] += 2
        
  def isDead(self):
    return self.stats["health"] <= 0
  
  def setLocation(self, location):
    self.location = location
  
  def healPlayer(self, heal):
    self.stats["health"] = min(self.stats["health"] + heal, self.stats["max health"])
  
  def isEquipped(self, item):
    if self.equipment[item.bodypart] != None and self.equipment[item.bodypart].name == item.name: 
      return True;
    return False;
    
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
  
  def getFatigueMultiplier(self):
    if self.energy <= 25:
      return 0.25;
    elif self.energy <= 50:
      return 0.5;
    elif self.energy <= 75:
      return 0.8;
    return 1;
      
  def deductEnergy(self):
    self.energy = max(0, self.energy - 5);

  def giveStatus(self, status, n):
    try:
      self.status[status][0] = True;
      self.status[status][1] += n;
    except KeyError:
      pass;
  
  def addSkill(self, skill):
    self.skills.update({skill.name : skill});
  
  def skillExists(self, skill):
    return skill in self.skills;
      