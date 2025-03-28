from random import randint, choices;

#todo: probably add a seperate handleAttack for npcs
class CriticalHandler:
  def __init__(self):
    pass;

class ComboHandler:
  def __init__(self):
    pass;
   
class DefenseHandler:
  def __init__(self):
    pass;

class StatusEffectHandler:
  def __init__(self):
    pass;
    
class DamageHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
    self.game = self.combat_handler.game;
    
  def reduceDamageByDefense(self, dmg, attacker, defender):
    event = choices([None, "defense_ignored"])[0];
    if event == "defense_ignored":
      self.ui.animatedPrintFile("damage handler", "defense ignored", [attacker.name, defender.name]);
      return dmg;
    elif dmg - defender.stats["defense"] <= 0:
      self.ui.animatedPrintFile("damage handler", "no damage", [attacker.name, defender.name]);
      return 0;
    return dmg - defender.stats["defense"];
    
  def calculateDamage(self, name, attacker, defender):
    fatigue_multiplier = attacker.getFatigueMultiplier();
    
    if name == "punch":
      dmg = self.reduceDamageByDefense(attacker.stats["strength"], attacker, defender) * fatigue_multiplier;
      return max(dmg, 0);
      
    elif name == "strong punch":
      dmg = self.reduceDamageByDefense(attacker.stats["strength"] * 1.3, attacker, defender) * fatigue_multiplier;
      return max(dmg, 0);

class AttackHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.damage_handler = DamageHandler(combat_handler);
    self.ui = self.combat_handler.ui;
    
  def handleAttack(self, attacker, defender):
    if attacker.attack_style == "basic":
      preset = randint(1, 2);
      if preset is 1:
        dmg = self.damage_handler.calculateDamage("punch", attacker, defender);
        self.ui.animatedPrintFile("basic style", "normal punch", [attacker.name, defender.name, dmg]);
        attacker.attackEnemy(dmg);
      elif preset is 2:
        dmg = self.damage_handler.calculateDamage("strong punch", attacker, defender);
        self.ui.animatedPrintFile("basic style", "strong punch", [attacker.name, defender.name, dmg]);
        attacker.attackEnemy(dmg);
  
