from random import randint, choices, uniform;

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
    attacker.giveStatus("blocking", 2);
    
class TauntHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
  
  def __handle_outcome(self, attacker, defender):
    if defender.name == "slime": self.ui.panelAnimatedPrintFile("taunt success response", "debuff slime", [defender.name], "slime");
    else: self.ui.panelAnimatedPrintFile("taunt success response", "debuff", [defender.name], defender.name);
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
      **self.createDamage("slam", 0, ["defense", "strength"]),
      **self.createDamage("slash", 30, ["strength"], 2),
      **self.createDamage("thrust", 25, ["strength", "defense"], 1.5),
      **self.createDamage("iron reversal", 30, ["strength"], 2),
      **self.createDamage("blade dance", 20, ["strength"], 1.5),
      **self.createDamage("push", 5, ["defense"], 2, "defender"),
      **self.createDamage("poke", 10, ["strength"], 0.8),
    }
   
  def createDamage(self, name, basedmg, stats, multiplier = 1, origin = "attacker", ignores = []):
    return {name : {"origin" : origin, "dmg" : basedmg, "stats" : stats, "multiplier" :  multiplier, "ignores" : ignores}};
  
  def reduceDamage(self, dmg, defender):
    return max(0, dmg - defender.stats.get("defense"));
  
  def attemptCritical(self, dmg, attacker):
    if choices(["crit", None], [attacker.stats["luck"], 0.5])[0] == "crit":
      multiplier = round(uniform(1.1, attacker.stats["luck"] * 10), 1);
      self.ui.panelPrint(f"[bold red]CRITICAL HIT![reset] [green]({multiplier}x)[reset]");
      return dmg * multiplier;
    return dmg;
     
  def __calculate(self, damage, attacker, defender):
    total_damage = damage.get("dmg");
    for stat in damage.get("stats"):
      if damage.get("origin") == "attacker":
        total_damage += attacker.stats.get(stat);
      else:
        total_damage += defender.stats.get(stat);
    return self.attemptCritical(total_damage * damage.get("multiplier"), attacker) * attacker.getFatigueMultiplier();
   
  def calculateDamage(self, name, attacker, defender):
    damage = self.attack_damages.get(name);
    total_damage = round(self.reduceDamage(self.__calculate(damage, attacker, defender), defender));
    if total_damage >= defender.stats["max health"]: self.ui.panelPrint("[bold green]BRILLIANT![reset]"); # might remove this in the future
    return total_damage;
    
class AttackHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.damage_handler = DamageHandler(combat_handler);
    self.taunt_handler = TauntHandler(combat_handler);
    self.defense_handler = DefenseHandler(combat_handler);
    self.ui = self.combat_handler.ui;
  
  def consumeEquipment(self, character, parts, dmg):
    for broken in character.useEquipment(parts, dmg):
      self.ui.animatedPrint(f"[red]{broken} was broken![reset]");
      
  def handleBlock(self, attacker, defender):
    if attacker.status["blocking"][0] is True:
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] dropped their block");
      attacker.status["blocking"] = [False, 0];
      return True;

    if defender.status["blocking"][0] is True:
      self.ui.panelAnimatedPrintFile("block", "successful block", [defender.name, attacker.name], "block");
      self.ui.panelPrint(f"[purple](DAMAGE BLOCKED)[reset]");
      defender.status["blocking"] = [False, 0];
      return True;
    return False;
  
  def __basic_style(self, attacker, defender):
    move = choices(["punch", "strong punch", "double punch", "slam"])[0];
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg);
    self.ui.panelAnimatedPrintFile("basic style", move, [attacker.name, defender.name, dmg], move);

  def __sword_style(self, attacker, defender):
    move = choices(["slash", "thrust", "iron reversal", "blade dance"])[0];
    if move == "iron reversal" : self.defense_handler.handleBlock(attacker, defender);
    elif move == "blade dance": attacker.stats["defense"] += 2; # balancs this lmao
    
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg);
    self.ui.panelAnimatedPrintFile("sword style", move, [attacker.name, defender.name, dmg], move);
    
    self.consumeEquipment(attacker, ["left arm", "right arm"], dmg - attacker.stats["strength"]);
    if randint(1, 2) == randint(1, 2): defender.giveStatus("bleeding", 2);
    
  def __debug_style(self, attacker, defender):
    self.ui.panelAnimatedPrint(f"[cyan]{attacker.name}[reset] deleted [yellow]{defender.name}[reset], dealt [bold purple]∞[reset] damage", "delete");
    attacker.attackEnemy(99999999999999999);
  
  def __dirty_style(self, attacker, defender):
    move = choices(["push", "poke"])[0];
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg);
    self.ui.panelAnimatedPrintFile("dirty style", move, [attacker.name, defender.name, dmg], move);
    
    if move == "push": defender.giveStatus("stunned", 2);
    
  def handleAttack(self, attacker, defender):
    if self.handleBlock(attacker, defender) is True:
      return;
    
    if attacker.attack_style == "basic": self.__basic_style(attacker, defender);
    elif attacker.attack_style == "debug": self.__debug_style(attacker, defender);
    elif attacker.attack_style == "swordsman": self.__sword_style(attacker, defender);
    elif attacker.attack_style == "dirty": self.__dirty_style(attacker, defender);
