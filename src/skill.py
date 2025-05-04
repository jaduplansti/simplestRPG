from random import randint;
from copy import deepcopy;

class Skill:
  def __init__(self, name, desc, energy, rank, level = 0):
    self.name = name;
    self.energy = energy;
    self.rank = rank
    self.level = level;
    self.desc = desc;
    
  def deductEnergy(self, character, n):
    character.energy = max(0, character.energy - n);
    
  def use(self, combat_handler = None, attacker = None, defender = None):
    SKILLS[self.name]["action"](self, combat_handler, attacker, defender);
    self.deductEnergy(attacker, self.energy);
    
  def to_dict(self):
    return {
      "name": self.name,
      "energy": self.energy,
      "level": self.level,
      "desc" : self.desc,
      "rank" : self.rank,
      };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);
    
def action_normal_damage(skill, combat_handler, attacker, defender): # generic skill attack
  if combat_handler.attack_handler.handleBlock(attacker, defender) is True:
      return;  
      
  if skill.name == "crimson edge": # this is just a placeholder
    combat_handler.ui.panelPrint(f"{attacker.name} unleashed a crimson edge!");
    for n in range(1, 100):
      combat_handler.ui.panelPrint(f"[bold red]DEALT 10 DAMAGE! {n}x[reset]");
      attacker.attackEnemy(10);
      
def action_normal_defense(skill, combat_handler, attacker, defender):
  if skill.name == "parry":
    attacker.giveStatus("parrying", 2);

def action_normal_item(skill, combat_handler, attacker, defender):
  if skill.name == "mind sword":
    if attacker.equipItem(Item("imaginary sword", rarity = "undefined", bodypart = "right arm")) != False:
      combat_handler.ui.panelNormalPrint(f"{attacker.name} focused, drawing his a fictional sword with his hand!");
      combat_handler.ui.panelNormalPrint(f"{attacker.name} used mind sword succesfully!");
      attacker.attack_style = "imaginary blade";

def getSkill(name):  
  try:
    return deepcopy(SKILLS[name]["skill"]);
  except KeyError:
    return None;
    
SKILLS = {
  "crimson edge" : {
     "skill" : Skill("crimson edge", "a hundred slashes dealing 10 damage each", 50, "D"), 
     "action" : action_normal_damage
    },
  "parry" : {
    "skill" : Skill("parry", "inflicts a parrying status", 5, "E"), 
    "action" : action_normal_defense
  },
};

