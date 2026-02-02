from random import choices, uniform;

class DamageHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
    self.game = self.combat_handler.game;
    
    self.attack_damages = {
      # basic moves
      **self.createDamage("punch", 5, ["strength"], _range = 1),
      **self.createDamage("strong punch", 6, ["strength"], _range = 1),
      **self.createDamage("double punch", 4, ["strength", "dexterity"], _range = 1),
      **self.createDamage("slam", 0, ["defense", "strength"], _range = 1),
      
      # sword1 moves
      **self.createDamage("slash", 13, ["strength"], _range = 2),
      **self.createDamage("thrust", 15, ["strength", "defense"], _range = 3),
      **self.createDamage("iron reversal", 15, ["strength"], _range = 1),
      **self.createDamage("blade dance", 20, ["strength"], _range = 2),
    }
   
  def createDamage(self, name, basedmg, stats, multiplier = 1, origin = "attacker", ignores = [], _range = 1):
    return {name : {"origin" : origin, "dmg" : basedmg, "stats" : stats, "multiplier" :  multiplier, "ignores" : ignores, "range" : _range}};
  
  def reduceDamage(self, dmg, defender):
    return max(0, dmg - defender.stats.get("defense"));
  
  def __getCritChance(self, attacker):
    if getattr(attacker, "true_crit", False) is True:
      attacker.true_crit = False;
      return 1;
    else: return min(attacker.stats["luck"], 0.7); # Ensure luck is max 0.7 (70%)
  
  def __getCritMultiplier(self, attacker):
    if getattr(attacker, "next_crit_multiplier", 1) > 1:
      crit = getattr(attacker, "next_crit_multiplier", 1);
      attacker.next_crit_multiplier = 0;
      return crit;
    else: return round(uniform(1.1, attacker.stats["luck"] * 10), 1); 
  
  def __handleCritMessage(self, crit_chance, multiplier):
    if crit_chance == 1: self.game.animator.animatePerfectCritical(multiplier);
    else: self.game.animator.animateCritical(multiplier);

  def attemptCritical(self, dmg, attacker):
    crit_chance = self.__getCritChance(attacker);
    if choices(["crit", None], [crit_chance, 1 - crit_chance])[0] == "crit":
        multiplier = self.__getCritMultiplier(attacker);
        if multiplier > 2.0: self.game.audio_handler.play("critical_hit2.wav");
        else: self.game.audio_handler.play("critical_hit1.wav");
        self.__handleCritMessage(crit_chance, multiplier);
        return dmg * multiplier;
    return dmg;
    
  def __calculate(self, damage, attacker, defender):
    total_damage = damage.get("dmg") + attacker.getWeight();
    for stat in damage.get("stats"):
      if damage.get("origin") == "attacker":
        total_damage += attacker.stats.get(stat);
      else:
        total_damage += defender.stats.get(stat);
    multiplier = self.combat_handler.attack_handler.gore_handler.getMultiplier(defender);
    return self.attemptCritical(total_damage * damage.get("multiplier") * multiplier, attacker) * attacker.getFatigueMultiplier();
  
  def __calculateDmg(self, dmg, attacker):
    return (self.attemptCritical(dmg, attacker) * self.combat_handler.attack_handler.gore_handler.getMultiplier(attacker.enemy)) * attacker.getFatigueMultiplier();
  
  def calculateDamage(self, name, attacker, defender, dmg = 0, ignore_defense = False):
    total_damage = 0;
    if name != None: 
      damage = self.attack_damages.get(name);
      if ignore_defense is False: total_damage = round(self.reduceDamage(self.__calculate(damage, attacker, defender), defender));
      else: total_damage = round(self.__calculate(damage, attacker, defender));
    else: 
      if ignore_defense is False: total_damage = round(self.reduceDamage(self.__calculateDmg(dmg, attacker), defender));
      else: total_damage = round(self.__calculateDmg(dmg, attacker));

    ratio = total_damage / defender.stats["max health"]
    if ratio >= 100: self.ui.panelPrint("[bold]BOUNDLESS![reset]")
    elif ratio >= 50: self.ui.panelPrint("[bold red]TRANSCENDENT![reset]")
    elif ratio >= 10: self.ui.panelPrint("[bold green]BRILLIANT![reset]")
    elif ratio >= 5: self.ui.panelPrint("[bold yellow]FANTASTIC![reset]")
    elif ratio >= 2: self.ui.panelPrint("[bold blue]EXCELLENT![reset]")
    elif ratio >= 1.5: self.ui.panelPrint("[bold cyan]GREAT![reset]")
    elif 0.99 <= ratio <= 1.01: self.ui.panelPrint("[bold yellow]IMPRESSIVE![reset]")
    return total_damage;
    