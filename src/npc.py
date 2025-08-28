from character import Character;
from random import randint, choices;
from copy import deepcopy;

class NPC(Character):
  def __init__(self, name):
    super().__init__(name);
    self.loot = [];
    self.loot_chance = [];
    self.fightable = True;
    self.boss = False;
    
    self.attack_chance = 0;
    self.block_chance = 0;
    self.flee_chance = 0;
    self.taunt_chance = 0;
    
    self.custom_actions = {};
   
  def createCustomAction(self, name, chance, actions, action_chance, threshold):
    return {
      name : {
        "chance" : chance,
        "actions": actions,
        "action_chance" : action_chance,
        "threshold": threshold,
      }
    };
  
  def checkCustomCondition(self, name):
    try:
      if self.custom_actions[name]["chance"] > 0: return True;
      return False;
    except KeyError:
      return False;
      
  def getLoot(self):
    if len(self.loot) == 0: return None;
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
  
  def move(self, away = False):
    if not away:
      if self.enemy.zone < self.zone:
        return choices(["move backward", None], [0.8, 0.2])[0];
      elif self.enemy.zone > self.zone:
        return choices(["move forward", None], [0.8, 0.2])[0];
    else:
      if self.enemy.zone < self.zone:
        return choices(["move forward", None], [0.8, 0.2])[0];
      elif self.enemy.zone > self.zone:
        return choices(["move backward", None], [0.8, 0.2])[0];
    return choices(["move backward", "move forward", None], [0.4, 0.4, 0.2])[0];
  
  def shouldMove(self):
    if (self.stats["health"] < self.enemy.stats["health"]) and (abs(self.zone - self.enemy.zone) < 2) and (randint(1, 3) == 1):
      return self.move(True);
    elif (abs(self.zone - self.enemy.zone) > 1) and randint(1, 2) == 1:
      return self.move(False);
    return None;
 
  def customAction(self, ui):
    if self.checkCustomCondition("recover") and choices([None, True], [1 - self.custom_actions["recover"]["chance"], self.custom_actions["recover"]["chance"]]):
      if self.stats["health"] < self.stats["max health"] * self.custom_actions["recover"]["threshold"]: return choices(self.custom_actions["recover"]["actions"], self.custom_actions["recover"]["action_chance"]);
    
  def getAction(self, ui):
    _move = self.shouldMove();
    if _move != None: return _move;
    action = self.customAction(ui);
    if action != None: return action;
    
    if self.status["blocking"][0] is True:
      return choices(["taunt", ""])[0];
    elif self.stats["health"] <= self.stats["max health"] * 0.20:
      return choices(["flee", "block", ""], [self.flee_chance, self.block_chance, 0.5])[0];
    else: return choices(["attack", "block"], [self.attack_chance, self.block_chance])[0];

def createNpc(
  name,
  boss = False,
  loots = [],
  basic_actions = [],
  custom_actions = [],
):
  npc = NPC(name);
  npc.boss = boss;
  
  npc.attack_chance = basic_actions[0];
  npc.block_chance = basic_actions[1];
  npc.block_chance = basic_actions[2];
  npc.flee_chance = basic_actions[3];
  
  for loot in loots:
    npc.putLoot(loot[0], loot[1]);
    
  for action in custom_actions:
    npc.createCustomAction(action[0], action[1], action[2], action[3], action[4]);
  return npc;
  
def getNPC(name):
  return deepcopy(NPCS[name]);
  
NPCS = {
  "slime" : createNpc("slime", basic_actions = [0.8, 0.2, 0, 0]),
  "goblin" : createNpc("goblin", basic_actions = [0.8, 0.2, 0, 0])
};