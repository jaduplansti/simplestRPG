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
    
  def handleTaunt(self, attacker, defender):
    self.ui.panelAnimatedPrintFile("taunt", "debuff", [attacker.name, defender.name], "taunt");
    if defender.name == "slime":
      self.ui.panelAnimatedPrintFile("taunt success response", "debuff slime", [defender.name], "slime");
    stat = choices(list(defender.stats))[0];
    defender.stats[stat] = max(0, defender.stats[stat] - 0.1);
    self.ui.panelPrint(f"[bold yellow]{stat.upper()}[reset] ([red]-0.1[reset])");
    
class DamageHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
    self.game = self.combat_handler.game;
    
  def reduceDamageByDefense(self, dmg, attacker, defender):
    event = choices([None, "defense_ignored"])[0];
    if event == "defense_ignored":
      self.ui.panelAnimatedPrintFile("damage handler", "defense ignored", [attacker.name, defender.name], attacker.name);
      return round(dmg);
    elif dmg - defender.stats["defense"] <= 0:
      self.ui.panelAnimatedPrintFile("damage handler", "no damage", [attacker.name, defender.name], attacker.name);
      return 0;
    return round(dmg - defender.stats["defense"]);
    
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
    self.taunt_handler = TauntHandler(combat_handler);
    self.defense_handler = DefenseHandler(combat_handler);
    
    self.ui = self.combat_handler.ui;
  
  def handleBlock(self, attacker, defender):
    if attacker.status["blocking"]:
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] dropped their block");
      attacker.status["blocking"] = False;
    elif defender.status["blocking"]:
      self.ui.panelAnimatedPrintFile("block", "successful block", [defender.name, attacker.name], "block");
      self.ui.panelPrint(f"[purple](DAMAGE BLOCKED)[reset]");
      defender.status["blocking"] = False;
    else:
      return False;
    return True;
  
  def handleAttack(self, attacker, defender):
    if self.handleBlock(attacker, defender) is True:
      return;
    
    if attacker.attack_style == "basic":
      preset = randint(1, 3);
      if preset == 1:
        dmg = self.damage_handler.calculateDamage("punch", attacker, defender);
        self.ui.panelAnimatedPrintFile("basic style", "normal punch", [attacker.name, defender.name, dmg], "normal punch");
        attacker.attackEnemy(dmg);
        self.combat_handler.event_handler.handleEvent(attacker, defender, self.combat_handler.event_handler.pickEvent(["basic_normal_event", None], [0.4, 0.6]));
      elif preset == 2:
        dmg = self.damage_handler.calculateDamage("strong punch", attacker, defender);
        self.ui.panelAnimatedPrintFile("basic style", "strong punch", [attacker.name, defender.name, dmg], "strong punch");
        attacker.attackEnemy(dmg);
        ## add reaction event here
      elif preset == 3:
        for n in range(1, 3):
          dmg = self.damage_handler.calculateDamage("strong punch", attacker, defender);
          self.ui.panelAnimatedPrintFile("basic style", "quick combo punch", [attacker.name, defender.name, dmg], f"quick combo {n}", 0.01);
          attacker.attackEnemy(dmg);
    
    elif attacker.attack_style == "debug":
      self.ui.panelAnimatedPrint(f"[cyan]{attacker.name}[reset] deleted [yellow]{defender.name}[reset], dealt [bold purple]∞[reset] damagee", "debug");
      attacker.attackEnemy(99999999999999999);
      self.combat_handler.event_handler.handleEvent(attacker, defender, self.combat_handler.event_handler.pickEvent(["basic_normal_event", None], [0.4, 0.6]));

