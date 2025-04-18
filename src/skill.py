from random import randint;

class Skill:
  def __init__(self, name, energy, level = 0):
    self.name = name;
    self.energy = energy;
    self.level = level;
  
  def deductEnergy(self, character, n):
    character.energy = max(0, character.energy - n);
    
  def use(self, combat_handler = None, attacker = None, defender = None):
    SKILLS[self.name](self, combat_handler, attacker, defender);
    self.deductEnergy(attacker, self.energy);
    
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
    combat_handler.ui.panelPrint(f"{attacker.name} unleashed a crimson edge!");
    for n in range(1, 100):
      combat_handler.ui.panelPrint(f"[bold red]DEALT 10 DAMAGE! {n}x[reset]");
      attacker.attackEnemy(10);
      
def action_normal_defense(skill, combat_handler, attacker, defender):
  if skill.name == "parry":
    attacker.giveStatus("parrying", 2);
    
SKILLS = {
  "crimson edge" : action_normal_damage,
  "parry" : action_normal_defense,
};