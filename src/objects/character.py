from random import randint, uniform
from objects.item import Item, Equipment, getItem, itemToEquipment, equipmentToItem;
from objects.skill import Skill, getSkill;
from copy import deepcopy;
from objects.character_class import Class;
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
    self.hunger = 100;
    
    self.berserk = False;
    self.zone = 5;
    self.direction = "forward";
    
    self.points = 20;
    self.title = "unawakened";
    self.status = {
      "blocking" : [False, 0],
      "stunned" : [False, 0],
      "poisoned" : [False, 0],
      "bleeding" : [False, 0],
      "parrying" : [False, 0],
      "karma" : [False, 0],
      "countering": [False, 0]
    }
    
    self.stats = {
      "health": 100,
      "max health": 100,
      "strength": randint(5, 10),
      "defense": randint(5, 10),
      "dexterity": randint(5, 10),
      "luck": 0.3,
    }
    
    self.equipment = {"head": None, "chest": None, "left arm": None, "right arm": None, "boots": None}
    self.bodyparts = {"head" : True, "arms" : True, "legs": True};
    
    
    self.attack_style = "basic"
    self._class = Class("Classless");
    
    self.inventory = {}
    self.skills = {}
    self.magic = {}
    
    self.guild_info = {};
    self.area_data = {};
    self.commonly_used_skills = [];
    
    self.story_progress = 0;
    
  def to_dict(self):
    return {
     "name": self.name,
      "level": self.level,
      "exp": self.exp,
      "position": self.position,
      "location": self.location,
      "money": self.money,
      "energy": self.energy,
      "hunger": self.hunger,
      "status": self.status,
      "guild info": self.guild_info,
      "berserk": self.berserk,
      "stats": self.stats,
      "equipment": {k: v.to_dict() if v else None for k, v in self.equipment.items()},
      "attack_style": self.attack_style,
      "_class": self._class.to_dict(),
      "skills": self.skills,
      "points": self.points,
      "title": self.title,
      "magic": self.magic,
      "area_data": self.area_data,
      "story_progress": self.story_progress,
      "bodyparts": self.bodyparts,
      "skills": {k: v.to_dict() if v else None for k, v in self.skills.items()},
      "inventory": {
          name: {
            "item": [item_obj.to_dict() for item_obj in item_data["item"]], 
            "amount": item_data["amount"]
          } for name, item_data in self.inventory.items()
      }
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
    char.hunger = data["hunger"]
    char.status = data["status"]
    char.berserk = data["berserk"]
    char.stats = data["stats"]
    char.guild_info = data["guild info"]
    char.points = data["points"]
    char.title = data["title"]
    char.area_data = data["area_data"]
    char.equipment = {
      k: Equipment.from_dict(v) if v else None for k, v in data["equipment"].items()
    }
    char.skills = {
       k: Skill.from_dict(v) if v else None for k, v in data["skills"].items()
    }
    char.attack_style = data["attack_style"]
    char._class = Class.from_dict(data["_class"]);
    char.inventory = {
      name: {
        "item": [Item.from_dict(item_dict) for item_dict in item_data["item"]], 
        "amount": item_data["amount"]
      } for name, item_data in data["inventory"].items()
    }

    char.magic = data["magic"]
    char.story_progress = data["story_progress"]
    char.bodyparts = data["bodyparts"];
    return char;

  def save(self):
    with open(f"saves/{self.name}.save", "w") as f:
      json.dump(self.to_dict(), f, indent=2)

  @classmethod
  def load(cls, name):
    with open(f"saves/{name}.save", "r") as f:
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
      if self.getTotalItems() >= 50:
        return -1;
        
      if self.itemExists(item.name):
        self.inventory[item.name]["item"].append(item);
        self.inventory[item.name]["amount"] += 1
      else:
        self.inventory[item.name] = {"amount": 1, "item": [item]}
    
  def getAmountOfItem(self, item):
    return self.inventory[item]["amount"]
  
  def getTotalItems(self):
    count = 0;
    for item in self.inventory: count += self.inventory[item]["amount"];
    return count;
    
  def getItem(self, item):
    return self.inventory[item]["item"][-1];
  
  def usedItem(self, item):
    if self.getAmountOfItem(item) <= 1:
      del self.inventory[item]
    else:
      self.inventory[item]["item"].pop();
      self.inventory[item]["amount"] -= 1
  
  def unequipItem(self, bodypart, game):
    item = equipmentToItem(self.equipment[bodypart]);
    if self.addItemToInventory(item, 1) == -1: return -1;
    self.equipment[bodypart].removeEquipment(self, game);
    
  def equipItem(self, item):
    if self.isOccupied(item.bodypart) != True:
      self.equipment[item.bodypart] = itemToEquipment(item);
      return True;
    return False;
  
  def useEquipment(self, bodypart, n, game):
    brokens = [];
    for part in bodypart:
      if self.equipment[part] != None and self.equipment[part].handleDurability(n) is True: 
        brokens.append(self.equipment[part].name)
        self.equipment[part].removeEquipment(self, game);
    return brokens;
    
  def giveDamage(self, dmg):
    self.stats["health"] -= min(self.stats["health"], dmg)
    
  def giveExp(self, exp):
    self.exp += exp
  
  def canLevelUp(self):
    return self.exp >= (self.level * 100)
  
  def tryLevelUp(self): 
    leveled_up = False
    while self.canLevelUp():
      if (self.level % 5) == 0: self.energy += 1;
      self.exp -= (self.level * 100)
      self.level += 1
      self.points += 2;
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
  
  def isOccupied(self, bodypart):
    if self.equipment[bodypart] != None: return True;
    else: return False;
    
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
    self.energy = max(0, self.energy - 10);

  def giveStatus(self, status, n):
    try:
      self.status[status][0] = True;
      self.status[status][1] += n + 1;
    except KeyError:
      pass;
  
  def addSkill(self, skill):
    self.skills.update({skill.name : skill});
  
  def skillExists(self, skill):
    return skill in self.skills;
  
  def removeSkill(self, skill_name):
    try:
      del self.skills[skill_name];
    except KeyError:
      pass;
      
  def clearStatus(self):
    for status in self.status: self.status[status] = [False, 0];
    
  def attackEnemy(self, dmg, combat_handler = None):
    self.dmg = dmg;
    if combat_handler != None: # clean this up. 
      combat_handler.attack_handler.consumeEquipment(self.enemy, ["chest"], dmg * 0.8);
      combat_handler.attack_handler.handlePassiveSkills("damage", self.enemy, self);
      combat_handler.notifyDurability(self.enemy, ["chest"]);
      if hasattr(self.enemy, "shadow"): self.enemy.shadow = 0;
    
    self.enemy.giveDamage(self.dmg);
    
    try:
      if combat_handler != None and combat_handler.game.isPlayer(self.enemy) != True and randint(1, 2) == 1: 
        if self.enemy.stats["health"] <= 0 and getattr(self.enemy, "announce_death", False) is False: 
          setattr(self.enemy, "announce_death", True);
          combat_handler.ui.printDialogueFile(self.enemy.name, self.enemy.name, "death", None, True);
        else: combat_handler.ui.printDialogueFile(self.enemy.name, self.enemy.name, "hurt", None, True);
    except KeyError:
      pass;
      
  def hasAreaData(self, area, info):
    try:
      self.area_data[area][info];
      return True;
    except KeyError:
      return False;
  
  def hasItems(self, items):
    for item_name in items:
      if item_name not in self.inventory or self.inventory[item_name]["amount"] <= 0:
        return False;
    return True
  
  def getWeight(self):
    weight = 0;
    for item in self.inventory:
      weight += self.getItem(item).weight * self.getAmountOfItem(item);
    for slot in self.equipment:
      if self.equipment[slot] != None: weight += getItem(self.equipment[slot].name).weight;
    return round(weight);
  
  def fixParts(self):
    for bodypart in self.bodyparts:
      self.bodyparts[bodypart] = True;
  
  def addCommonSkill(self, skill_name):
    if skill_name in self.commonly_used_skills: return;
    if len(self.commonly_used_skills) >= 3: self.commonly_used_skills.pop(0);
    self.commonly_used_skills.append(skill_name);