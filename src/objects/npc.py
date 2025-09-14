from objects.character import Character;
from random import randint, choices;
from copy import deepcopy;
from objects.item import getItem, ITEMS;

class NPC(Character):
  def __init__(self, name):
    super().__init__(name);
    self.loot = [];
    self.loot_chance = [];
    self.any_loot = False;
    self.fightable = True;
    self.boss = False;
    
    self.attack_chance = 0;
    self.block_chance = 0;
    self.flee_chance = 0;
    self.taunt_chance = 0;
    
  def getLoot(self):
    if self.any_loot is True: return getItem(choices(list(ITEMS))[0]);
    elif len(self.loot) == 0: return None;
    else: return choices(self.loot, self.loot_chance)[0];
  
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
        self.stats[stat] += 30;
        self.stats["health"] = self.stats["max health"];
      elif stat == "luck": self.stats[stat] += 0.001;
      else: self.stats[stat] += 0.5;
  
  def shouldMove(self):
    if (self.stats["health"] < self.enemy.stats["health"]) and (abs(self.zone - self.enemy.zone) < 2) and (randint(1, 3) == 1):
      return "retreat";
    elif (abs(self.zone - self.enemy.zone) > 1) and randint(1, 2) == 1:
      return "advance";
    return None;
 
  def getAction(self, ui):
    _move = self.shouldMove();
    if _move != None: return _move;
    #action = self.customAction(ui);
    #if action != None: return action;
    
    if self.status["blocking"][0] is True:
      return choices(["taunt", ""])[0];
    elif self.stats["health"] <= self.stats["max health"] * 0.20:
      return choices(["flee", "block", ""], [self.flee_chance, self.block_chance, 0.5])[0];
    else: return choices(["attack", "block"], [self.attack_chance, self.block_chance])[0];

def createNpc(
  name,
  level = 1,
  boss = False,
  any_loot = False,
  loots = [],
  basic_actions = [],
):
  npc = NPC(name);
  npc.boss = boss;
  npc.any_loot = True;
  
  npc.attack_chance = basic_actions[0];
  npc.block_chance = basic_actions[1];
  npc.taunt_chance = basic_actions[2];
  npc.flee_chance = basic_actions[3];
  
  if isinstance(level, list) is True: npc.level = randint(level[0], level[1]);
  else: npc.level = level;
  
  for _ in range(npc.level):
    npc.statLevelUp();
    
  for loot in loots:
    npc.putLoot(loot[0], loot[1]);
    
  return npc;
  
def getNPC(name):
  return deepcopy(NPCS[name]);
  
NPCS = {
  "slime" : createNpc("slime", level = [1, 5], basic_actions = [0.8, 0.2, 0, 0], any_loot = True),
  "goblin" : createNpc("goblin", basic_actions = [0.8, 0.2, 0, 0], any_loot = True),
  "ñayéroÀ" : createNpc("ñayéroÀ", boss = True, level = [20, 50], basic_actions = [0.8, 0.2, 0, 0], any_loot = True),
  "exodus" : createNpc("exodus", boss = True, level = [20, 50], basic_actions = [0.8, 0.2, 0, 0], any_loot = True),
};