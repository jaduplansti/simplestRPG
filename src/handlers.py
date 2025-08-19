from random import randint, choice, choices, uniform;
from player import Player;
from enemy import Enemy;
import string;

class StatusEffectHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = combat_handler.ui;
    self.turn_passed = False;
    
    self.statuses = {
      "stunned" : self.__stunned,
      "bleeding" : self.__bleeding,
      "poisoned": self.__poisoned,
      "karma": self.__karma,
    };
    
    self.other_status = {
      "parrying" : self.__parrying,
      "blocking" : self.__blocking,
    };
    
  def afflict(self, reciever, status, amount):
    reciever.giveStatus(status, amount);
   
  def deduct(self, reciever, status, amount):
    reciever.status[status][1] -= amount;
  
  def __stunned(self, attacker, defender):
    self.ui.animatedPrint(f"[red]{attacker.name} is stunned and cant move[reset]!");
    attacker.status["stunned"][1] -= 1;
    if randint(1, 3) == randint(1, 3): self.ui.animatedPrint(f"[red]{attacker.name} resisted the stun[reset]!"); # temporary quick nerf
    else: self.turn_passed = True;
    
  def __bleeding(self, attacker, defender):
    dmg = round(attacker.stats["health"] * 0.1);
    self.ui.animatedPrint(f"[red]{attacker.name} is bleeding, receiving {dmg} damage[reset]!");
    attacker.enemy.attackEnemy(dmg);
    attacker.status["bleeding"][1] -= 1;
  
  def __poisoned(self, attacker, defender):
    dmg = round(attacker.stats["health"] * 0.15);
    self.ui.animatedPrint(f"[bold green]{attacker.name} is poisoned, afflicting {dmg} damage[reset]!");
    attacker.enemy.attackEnemy(dmg);
    attacker.status["poisoned"][1] -= 1;
  
  def __karma(self, attacker, defender):
    dmg = round((attacker.stats["health"] * 0.3) * (attacker.level / randint(10, 15)));
    if "divine protection" in attacker.skills:
      self.ui.animatedPrint(f"[yellow]{attacker.name} feels divine energy.., healing for {dmg} health[reset]!");
      attacker.stats["health"] += dmg;
    else:
      self.ui.animatedPrint(f"[yellow]{attacker.name} feels their sins crawling, punishing for {dmg} damage[reset]!");
      attacker.enemy.attackEnemy(dmg);
      self.__karma_punish(attacker, defender);
    attacker.status["karma"][1] -= 1;
  
  def __parrying(self, attacker, defender):
    self.combat_handler.attack_handler.defense_handler.handleParry(attacker, defender);
    defender.status["parrying"][1] -= 1;
    
  def __blocking(self, attacker, defender):
   defender.status["blocking"][1] -= 1;
  
  def __karma_punish(self, attacker, defender):
    if self.combat_handler.previous_action == "taunt":
      self.ui.animatedPrint(f"[yellow]{attacker.name} taunted the divine!, a penalty has been applied!");
      attacker.status["karma"][1] += 10;
      self.turn_passed = True;
    elif self.combat_handler.previous_action == "block":
      self.ui.animatedPrint(f"[yellow]{attacker.name} tried to block...");
      self.ui.printDialogue(defender.name, f"{attacker.name}... you cannot hide from judgement!");
      attacker.stats["defense"] *= 0.8;
      self.turn_passed = True;
      
  def handleStatus(self, attacker, defender):
    self.turn_passed = False;
    
    for status in attacker.status:
      if status in self.statuses and attacker.status[status][0] is True: self.statuses[status](attacker, defender);
    
    for status in defender.status:
      if status in self.other_status and defender.status[status][0] is True: self.other_status[status](attacker, defender);
    
    for status in attacker.status:
      if status in self.statuses and attacker.status[status][1] <= 0 and attacker.status[status][0] != False:
        self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] is no longer [red]{status}[reset]!");
        attacker.status[status][0] = False;
    
    for status in defender.status:
      if status in self.other_status and defender.status[status][1] <= 0 and defender.status[status][0] != False:
        self.ui.animatedPrint(f"[yellow]{defender.name}[reset] is no longer [red]{status}[reset]!");
        defender.status[status][0] = False;
    
class DefenseHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
  
  def giveBlock(self, attacker, defender):
    attacker.giveStatus("blocking", 2);
  
  def giveParry(self, attacker):
    attacker.giveStatus("parrying", 2);
  
  def parryEvent(self, attacker, defender):
    if attacker.stats["health"] <= attacker.stats["max health"] * 0.3 and randint(1, 4) == 1:
      self.ui.animatedPrint(f"{attacker.name} falters, caught by {defender.name}'s flawless parry!")
      self.ui.printDialogue(defender.name, ["Gotcha!", "Surprise!", "Take this!"])
      self.combat_handler.attack_handler.handleAttack(defender, attacker)

    elif attacker.status["parrying"][0] is True:
      self.ui.animatedPrint(f"{defender.name}'s parry sends a shockwave through {attacker.name}'s guard, breaking their stance!")
      attacker.status["parrying"] = [False, 0]
      
  def handleParry(self, attacker, defender):
    if self.combat_handler.getOpponentTurnOption(defender) in ["atk", "attack"] and attacker.status["stunned"][0] is False:
      if self.combat_handler.attack_handler.handleRange(None, attacker, defender, 2) is False: return;
      elif defender.status["stunned"][0] is True: return;
      
      if not isinstance(defender, Player) and randint(1, 3) == randint(1, 3): pass;
      elif isinstance(defender, Player) and self.ui.getEnterWithTimeout("(press [ENTER] to quickly parry!)", 1.5) == "": pass;
      else:
        self.ui.newLine();
        self.ui.panelAnimatedPrintFile("parry", "failed parry", [defender.name, attacker.name], "parry");
        self.ui.panelPrint("[bold red]PARRY FAILED (-10% energy)[reset]");
        defender.energy -= defender.energy * 0.1;
        return;
        
      self.ui.newLine();
      self.combat_handler.game.audio_handler.play("parry.wav");
      self.ui.panelAnimatedPrintFile("parry", "successful parry", [defender.name, attacker.name], "parry");
      self.ui.panelPrint("[bold cyan]PARRIED[reset]");
      self.combat_handler.attack_handler.consumeEquipment(defender, ["left arm", "right arm"], defender.stats["strength"] * 0.1);
      self.combat_handler.attack_handler.status_handler.turn_passed = True;
      self.parryEvent(attacker, defender);
      
  def handleDodge(self, attacker, defender):
    dodge_chance = min(defender.stats["dexterity"] * 0.1, 60); # capped at 60%
    if choices(["dodge", None], [dodge_chance, 100 - dodge_chance])[0] is None: return;
    self.ui.panelAnimatedPrint(f"[yellow]{defender.name}[reset] managed to dodge [yellow]{attacker.name}'s[reset] attack just in time!", "dodge");
    self.ui.panelPrint("[bold magenta]DODGED[reset]");
    return True;
    
class TauntHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
  
  def __handle_outcome(self, attacker, defender):
    if defender.name == "slime": self.ui.panelAnimatedPrintFile("taunt success response", "debuff slime", [defender.name], "slime");
    else: self.ui.panelAnimatedPrintFile("taunt success response", "debuff", [defender.name], defender.name);
    stat = choices(list(defender.stats))[0];
    defender.stats[stat] -= round(max(0, defender.stats[stat] * 0.05));

  def handleTaunt(self, attacker, defender):
    self.ui.panelAnimatedPrintFile("taunt", "debuff", [attacker.name, defender.name], "taunt");
    self.__handle_outcome(attacker, defender);
    
class DamageHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
    self.game = self.combat_handler.game;
    
    self.attack_damages = {
      **self.createDamage("punch", 10, ["strength"], _range = 1),
      **self.createDamage("strong punch", 20, ["strength"], _range = 1),
      **self.createDamage("double punch", 10, ["strength"], _range = 1),
      **self.createDamage("slam", 0, ["defense", "strength"], _range = 1),
      **self.createDamage("slash", 30, ["strength"], _range = 2),
      **self.createDamage("thrust", 25, ["strength", "defense"], _range = 3),
      **self.createDamage("iron reversal", 30, ["strength"], _range = 1),
      **self.createDamage("blade dance", 40, ["strength"], _range = 2),
      **self.createDamage("push", 5, ["defense"], _range = 1, origin = "defender"),
      **self.createDamage("poke", 10, ["strength"], _range = 2),
      **self.createDamage("quick shot", 15, ["strength"], _range = 5),
      **self.createDamage("half draw", 20, ["strength"], _range = 7),
      **self.createDamage("arrow throw", 10, ["strength"], _range = 5),
      **self.createDamage("heal override", 6, ["strength", "dexterity"], _range = 2),
      **self.createDamage("stab", 10, ["strength", "dexterity"], _range = 1),
      **self.createDamage("feint", 5, ["dexterity"], _range = 1),
      **self.createDamage("chain", 15, ["strength"], _range = 1),
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
      return getattr(attacker, "next_crit_multiplier", 1);
    else: return round(uniform(1.1, attacker.stats["luck"] * 10), 1); 
  
  def __handleCritMessage(self, crit_chance, multiplier):
    if crit_chance == 1: self.ui.panelPrint(f"[bold cyan]PERFECT CRITICAL[reset] [green]({multiplier}x)[reset]");
    else: self.ui.panelPrint(f"[bold red]CRITICAL HIT![reset] [green]({multiplier}x)[reset]");

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
    total_damage = damage.get("dmg");
    for stat in damage.get("stats"):
      if damage.get("origin") == "attacker":
        total_damage += attacker.stats.get(stat);
      else:
        total_damage += defender.stats.get(stat);
    return self.attemptCritical(total_damage * damage.get("multiplier"), attacker) * attacker.getFatigueMultiplier();
  
  def __calculateDmg(self, dmg, attacker):
    return self.attemptCritical(dmg, attacker) * attacker.getFatigueMultiplier();
  
  def calculateDamage(self, name, attacker, defender, dmg = 0, ignore_defense = False):
    total_damage = 0;
    if name != None: 
      damage = self.attack_damages.get(name);
      if ignore_defense is False: total_damage = round(self.reduceDamage(self.__calculate(damage, attacker, defender), defender));
      else: total_damage = round(self.__calculate(damage, attacker, defender));
    else: 
      if ignore_defense is False: total_damage = round(self.reduceDamage(self.__calculateDmg(dmg, attacker), defender));
      else: total_damage = round(self.__calculateDmg(dmg, attacker));

    if total_damage > 0:
      ratio = defender.stats["max health"] / total_damage;
      if ratio <= 0.01: self.ui.panelPrint("[bold purple]TRANSCENDENT![reset]");
      elif ratio <= 0.1: self.ui.panelPrint("[bold green]BRILLIANT![reset]");
      elif ratio <= 0.2: self.ui.panelPrint("[bold yellow]FANTASTIC![reset]");
      elif ratio <= 0.5: self.ui.panelPrint("[bold cyan]GREAT![reset]"); 
      elif ratio == 1: self.ui.panelPrint("[bold yellow]IMPRESSIVE![reset]"); 
    return total_damage;
    
class AttackHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.damage_handler = DamageHandler(combat_handler);
    self.taunt_handler = TauntHandler(combat_handler);
    self.defense_handler = DefenseHandler(combat_handler);
    self.status_handler = StatusEffectHandler(combat_handler);
    self.ui = self.combat_handler.ui;
    
  def handlePassiveSkills(self, _type, attacker, defender):
    for skill in attacker.skills:
      if attacker.skills[skill].passive is True and attacker.skills[skill].passive_type == _type:
        attacker.skills[skill].use(self.combat_handler, attacker, defender);
  
  def validateAttack(self, attacker, defender, move, _range = None, ignore_block = False):
    if self.handleRange(move, attacker, defender, _range) is False: return False;
    if self.defense_handler.handleDodge(attacker, defender) is True: return False;
    if ignore_block is False and self.handleBlock(attacker, defender) is True: return False;
    return True;
    
  def consumeEquipment(self, character, parts, dmg):
    for broken in character.useEquipment(parts, dmg, self.combat_handler.game):
      self.ui.animatedPrint(f"[red]{broken} was broken![reset]");
      
  def handleBlock(self, attacker, defender): # move this to defense handler
    if attacker.status["blocking"][0] is True:
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] dropped their block");
      attacker.status["blocking"] = [False, 0];
      return True;

    if defender.status["blocking"][0] is True:
      self.combat_handler.game.audio_handler.play("blocked.wav");
      self.ui.panelAnimatedPrintFile("block", "successful block", [defender.name, attacker.name], "block");
      self.ui.panelPrint(f"[purple](DAMAGE BLOCKED)[reset]");
      defender.status["blocking"] = [False, 0];
      return True;
    return False;
  
  def handleRange(self, move, attacker, defender, _range = None):
    if _range is None: _range = self.damage_handler.attack_damages[move]["range"];
    if self.combat_handler.isHit(attacker.direction, _range, attacker, defender): return True;
    self.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] tried to hit [yellow]{defender.name}[reset] but missed!", "miss");
    self.ui.panelPrint(f"[yellow]MISSED[reset]");
    return False;
  
  def handleAttackBar(self, attacker):
    result = self.combat_handler.game.animator.attackBar();
    self.ui.clearLine(3);
    if result is None: return;
    elif result[1] == result[3]: attacker.true_crit = True;
      
  def handleAttack(self, attacker, defender):
    self.handlePassiveSkills("attack", attacker, defender);
    if self.combat_handler.game.isPlayer(attacker): self.handleAttackBar(attacker);
    self.combat_handler.style_handler.styles[attacker.attack_style]["handler"](attacker, defender);
    