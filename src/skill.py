from random import randint;

class Skill:
  def __init__(self, name, energy, level = 0):
    self.name = name;
    self.energy = energy;
    self.level = level;
    
  def use(self, combat_handler = None, attacker = None, defender = None):
    SKILLS[self.name](self, combat_handler, attacker, defender);
 
  def to_dict(self):
    return {
      "name": self.name,
      "energy": self.energy,
      "level": self.level,
      };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);
    
def action_normal_damage(skill, combat_handler, attacker, defender): # generic skill attack
  if skill.name == "crimson edge": # this is just a placeholder
    defender.giveStatus("stunned", 100);
    defender.giveStatus("bleeding", 100);

SKILLS = {
  "crimson edge" : action_normal_damage,
};