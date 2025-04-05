from random import randint, choices;

class CriticalHandler:
  def __init__(self):
    pass;

class ComboHandler:
  def __init__(self):
    pass;
   
class StatusEffectHandler:
  def __init__(self):
    pass;

class DefenseHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
  
  def handleBlock(self, attacker, defender):
    attacker.status["blocking"] = True;
    
class TauntHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
  
  def __handle_outcome(self, attacker, defender):
    if defender.name == "slime":
      self.ui.panelAnimatedPrintFile("taunt success response", "debuff slime", [defender.name], "slime");
    stat = choices(list(defender.stats))[0];
    defender.stats[stat] -= max(0, defender.stats[stat] * 0.05);

  def handleTaunt(self, attacker, defender):
    self.ui.panelAnimatedPrintFile("taunt", "debuff", [attacker.name, defender.name], "taunt");
    self.__handle_outcome(attacker, defender);
    
class DamageHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
    self.game = self.combat_handler.game;
    
    self.attack_damages = {
      **self.createDamage("punch", 10, ["strength"]),
      **self.createDamage("strong punch", 20, ["strength"], 2),
      **self.createDamage("double punch", 10, ["strength"], 2),
      **self.createDamage("slam", 0, ["defense", "strength"], origin = "defender"),
    }
   
  def createDamage(self, name, basedmg, stats, multiplier = 1, origin = "attacker", ignores = []):
    return {name : {"origin" : origin, "dmg" : basedmg, "stats" : stats, "multiplier" :  multiplier, "ignores" : ignores}};
  
  def reduceDamage(self, dmg, defender):
    return max(0, dmg - defender.stats.get("defense"));
  
  def __calculate(self, damage, attacker, defender):
    total_damage = 0;
    for stat in damage.get("stats"):
      if damage.get("origin") == "attacker":
        total_damage += attacker.stats.get(stat);
      else:
        total_damage += defender.stats.get(stat);
    return (total_damage * damage.get("multiplier")) / attacker.getFatigueMultiplier();

  def calculateDamage(self, name, attacker, defender):
    damage = self.attack_damages.get(name);
    return self.reduceDamage(self.__calculate(damage, attacker, defender), defender);
    
class AttackHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.damage_handler = DamageHandler(combat_handler);
    self.taunt_handler = TauntHandler(combat_handler);
    self.defense_handler = DefenseHandler(combat_handler);
    self.ui = self.combat_handler.ui;
  
  def handleBlock(self, attacker, defender):
    if attacker.status.get("blocking", False):
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] dropped their block");
      attacker.status["blocking"] = False;
      return True;

    if defender.status.get("blocking", False):
      self.ui.panelAnimatedPrintFile("block", "successful block", [defender.name, attacker.name], "block");
      self.ui.panelPrint(f"[purple](DAMAGE BLOCKED)[reset]");
      defender.status["blocking"] = False;
      return True;
    return False;
  
  def __basic_style(self, attacker, defender):
    move = choices(["punch", "strong punch", "double punch", "slam"])[0];
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg);
    self.ui.panelAnimatedPrintFile("basic style", move, [attacker.name, defender.name, dmg], move);
    
  def __debug_style(self, attacker, defender):
    self.ui.panelAnimatedPrint(f"[cyan]{attacker.name}[reset] deleted [yellow]{defender.name}[reset], dealt [bold purple]∞[reset] damagee", "debug");
    attacker.attackEnemy(99999999999999999);

  def handleAttack(self, attacker, defender):
    if self.handleBlock(attacker, defender) is True:
      return;
    
    if attacker.attack_style == "basic":
      self.__basic_style(attacker, defender);
    elif attacker.attack_style == "debug":
      self.__debug_style(attacker, defender);
  
  
