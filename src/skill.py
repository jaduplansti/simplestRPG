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
  if skill.name == "soul shatter":
    if (attacker.stats["health"] < defender.stats["health"]):
      combat_handler.ui.panelPrint(f"user's health is lower than the enemy, this will sacrifice 20% max health in return, proceed (yes/no)", "center", "Warning", "red");
      if combat_handler.ui.getInput() == "n": return;
      attacker.stats["max health"]  *= 0.8;
    combat_handler.ui.printDialogue(attacker.name, "thy soul is stained..");
    combat_handler.ui.printDialogue(attacker.name, "this stained soul shall be cleansed.");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] reaches out their hand, grasping [yellow]{defender.name}'s[reset] soul and crushing it.", "soul shatter");
    attacker.attackEnemy(999999);
    
  elif combat_handler.attack_handler.handleBlock(attacker, defender) is True:
      return;  
      
  elif skill.name == "crimson edge": # this is just a placeholder
    combat_handler.ui.panelPrint(f"{attacker.name} unleashed a crimson edge!");
    for n in range(1, 100):
      combat_handler.ui.panelPrint(f"[bold red]DEALT 5 DAMAGE! {n}x[reset]");
      attacker.attackEnemy(5);
 
def action_normal_defense(skill, combat_handler, attacker, defender):
  if skill.name == "parry":
    attacker.giveStatus("parrying", 2);

def getSkill(name):  
  try:
    return deepcopy(SKILLS[name]["skill"]);
  except KeyError:
    return None;
    
SKILLS = {
  "crimson edge" : {
     "skill" : Skill("crimson edge", "a hundred slashes dealing 5 damage each", 50, "D"), 
     "action" : action_normal_damage
    },
  "soul shatter" : {
     "skill" : Skill("soul shatter", "a divine technique capable of crushing the soul of the enemy, cannot be blocked or nullified", 80, "S+"), 
     "action" : action_normal_damage
  },
  "parry" : {
    "skill" : Skill("parry", "inflicts a parrying status", 5, "E"), 
    "action" : action_normal_defense
  },
};

