from objects.character import Character;
from random import randint, choices, choice;
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
    self.energy = self.max_energy;
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
      else: self.stats[stat] += 6;
  
  def shouldMove(self):
    if (self.stats["health"] < self.enemy.stats["health"]) and (abs(self.zone - self.enemy.zone) < 2) and (randint(1, 3) == 1):
      return "retreat";
    elif (abs(self.zone - self.enemy.zone) > 1) and randint(1, 2) == 1:
      return "advance";
    return None;
  
  def targetPart(self):
    active_parts = [part for part, is_ok in self.bodyparts.items() if is_ok];
    return f"target {choice(active_parts)}";

  def __getAction(self, ui):
    _move = self.shouldMove();
    if _move != None: return _move;
    #action = self.customAction(ui);
    #if action != None: return action;
    if randint(1, 4) == 1: return self.targetPart();

    if self.status["blocking"][0] is True:
      return choices(["taunt", ""])[0];
    elif self.stats["health"] <= self.stats["max health"] * 0.20:
      return choices(["flee", "block", ""], [self.flee_chance, self.block_chance, 0.5])[0];
    else: return choices(["attack", "block"], [self.attack_chance, self.block_chance])[0];
  
  def getAction(self, ui): # clean this up next update
    _move = self.__getAction(ui);
    try:
      if randint(1, 3) == 1 and _move not in ["retreat", "advance"]: ui.printDialogueFile(self.name, self.name, _move, None, True);
    except KeyError:
      pass;
    return _move;
    
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
    npc.max_energy += 5;
    npc.energy = npc.max_energy;
    
  for loot in loots:
    npc.putLoot(loot[0], loot[1]);
  
  return npc;
  
def getNPC(name):
  return deepcopy(NPCS[name]);
  
NPCS = {
  "slime": createNpc("slime", level = [1, 5], basic_actions = [0.8, 0.2, 0, 0], any_loot = True),
  "goblin": createNpc("goblin", level = [3, 7], basic_actions = [0.8, 0.2, 0, 0], any_loot = True),
  "rat": createNpc("rat", level = [2, 6], basic_actions = [0.75, 0.25, 0, 0], any_loot = True),
  "wolf": createNpc("wolf", level = [4, 8], basic_actions = [0.7, 0.3, 0, 0], any_loot = True),
  "bandit": createNpc("bandit", level = [5, 9], basic_actions = [0.7, 0.25, 0.05, 0], any_loot = True),
  "skeleton": createNpc("skeleton", level = [6, 10], basic_actions = [0.7, 0.2, 0.1, 0], any_loot = True),
  "azaroth": createNpc("azaroth", boss = True, level = [100, 200], basic_actions = [0.9, 0.1, 0, 0], any_loot = True),
  "goblin chief": createNpc("goblin chief", boss = True, level = [20, 25], basic_actions = [0.9, 0.1, 0, 0], any_loot = True),
  "dark slime": createNpc("dark slime", boss = True, level = [15, 20], basic_actions = [0.9, 0.1, 0, 0], any_loot = True),
};