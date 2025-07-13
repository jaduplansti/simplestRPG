from random import randint, choices;
from copy import deepcopy;

class Skill:
  def __init__(self, name, desc, energy, rank, level = 0, passive = False):
    self.name = name;
    self.energy = energy;
    self.rank = rank
    self.level = level;
    self.desc = desc;
    self.passive = passive;
    
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
    if (attacker.stats["health"] < defender.stats["health"]) and combat_handler.game.isPlayer(attacker):
      combat_handler.ui.panelPrint(f"user's health is lower than the enemy, this will sacrifice 20% max health in return, proceed (yes/no)", "center", "Warning", "red");
      if combat_handler.ui.getInput() == "n": return;
      attacker.stats["max health"] = round(attacker.stats["max health"] * 0.8);
    combat_handler.ui.printDialogue(attacker.name, "thy soul is stained..");
    combat_handler.ui.printDialogue(attacker.name, "this stained soul shall be cleansed.");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] reaches out their hand, grasping [yellow]{defender.name}'s[reset] soul and crushing it.", "soul shatter");
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, 9999);
    attacker.attackEnemy(dmg);
    
  elif combat_handler.attack_handler.handleBlock(attacker, defender) is True:
      return;  
      
  elif skill.name == "crimson edge": # this is just a placeholder
    combat_handler.ui.panelPrint(f"{attacker.name} unleashed a crimson edge!");
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, 500);
    for n in range(1, 100):
      combat_handler.ui.panelPrint(f"[bold red]DEALT 5 DAMAGE! {n}x[reset]");
      attacker.attackEnemy(5);
  
def action_normal_defense(skill, combat_handler, attacker, defender):
  if skill.name == "parry":
    attacker.giveStatus("parrying", 5);

def action_passive(skill, combat_handler, attacker, defender):
  if skill.name == "hyper precision" and combat_handler.previous_action in ["attack", "atk"]:
    if randint(1, 2) == randint(1, 2):
      defender.status["blocking"] = [False, 0];
      combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] focused into a hyper focus state, breaking {defender.name}'s block", title = skill.name);
  
  elif skill.name == "flowing blade" and attacker.status["blocking"][0] is True and attacker.status["parrying"][0] is True:
    attacker.status["blocking"] = [False, 0];
    defender.giveStatus("stunned", 2);
    
def action_passive_buff(skill, combat_handler, attacker, defender):
  if skill.name == "hyper precision":
    pass;

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
    "skill" : Skill("parry", "inflicts a parrying status", 12, "D"), 
    "action" : action_normal_defense
  },
  "hyper precision" : {
    "skill" : Skill("hyper precision", "you see flaws in every stance, your attacks have a 50% to block break!", 0, "D+", passive = True), 
    "action" : action_passive
  },
  "flowing blade" : {
    "skill" : Skill("flowing blade", "the ultimate defense, when you are both blocking and parrying, you apply 2 stacks of stun and reset your stance.", 0, "C", passive = True), 
    "action" : action_passive
  },
};

