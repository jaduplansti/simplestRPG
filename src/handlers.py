from random import randint, choice, choices, uniform;
from player import Player;
from enemy import Enemy;
import string;

class CriticalHandler:
  def __init__(self):
    pass;

class ComboHandler:
  def __init__(self):
    pass;
   
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
    self.ui.animatedPrint(f"[yellow]{attacker.name} feels their sins crawling, punishing for {dmg} damage[reset]!");
    attacker.enemy.attackEnemy(dmg);
    attacker.status["karma"][1] -= 1;
  
  def __parrying(self, attacker, defender):
    self.combat_handler.attack_handler.defense_handler.handleParry(attacker, defender);
    defender.status["parrying"][1] -= 1;
    
  def __blocking(self, attacker, defender):
   defender.status["blocking"][1] -= 1;
   
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
  
  def handleParry(self, attacker, defender):
    if self.combat_handler.getOpponentTurnOption(defender) in ["atk", "attack"]:
      if self.combat_handler.attack_handler.handleRange(None, attacker, defender, 2) is False: return;
      elif defender.status["parrying"][0] is True: return;
      
      if not isinstance(defender, Player) and randint(1, 3) == randint(1, 3): pass;
      elif isinstance(defender, Player) and self.ui.getInputWithTimeout("type (f) to quickly parry!", 1.5) == "f": pass;
      else:
        self.ui.newLine();
        self.ui.panelAnimatedPrint(f"[yellow]{defender.name}[reset] failed to parry!", "parry");
        self.ui.panelPrint("[bold red]PARRY FAILED (-10% energy)[reset]");
        defender.energy -= defender.energy * 0.1;
        return;
        
      self.ui.newLine();
      self.ui.panelAnimatedPrint(f"[yellow]{defender.name}[reset] parried [green]{attacker.name}[reset] with precision!", "parry");
      self.ui.panelPrint("[bold cyan]PARRIED[reset]");
      self.combat_handler.attack_handler.consumeEquipment(defender, ["left arm", "right arm"], defender.stats["strength"] * 0.2);
      self.combat_handler.attack_handler.status_handler.turn_passed = True;
    
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
  
  def __calculateDmg(self, dmg, attacker):
    return self.attemptCritical(dmg, attacker) * attacker.getFatigueMultiplier();
  
  def calculateDamage(self, name, attacker, defender, dmg = 0):
    total_damage = 0;
    if name != None: 
      damage = self.attack_damages.get(name);
      total_damage = round(self.reduceDamage(self.__calculate(damage, attacker, defender), defender));
    else: total_damage = round(self.reduceDamage(self.__calculateDmg(dmg, attacker), defender));

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
      
  def __basic_style(self, attacker, defender):
    move = choices(["punch", "strong punch", "double punch", "slam"])[0];
    if self.validateAttack(attacker, defender, move) != True: return;
    
    if self.__basicMiniGame(move, attacker, defender) is False: return;
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg, self.combat_handler);
    self.ui.panelAnimatedPrintFile("basic style", move, [attacker.name, defender.name, dmg], move);
  
  def __sword_style(self, attacker, defender):
    move = choices(["slash", "thrust", "iron reversal", "blade dance"])[0];
    if self.validateAttack(attacker, defender, move) != True: return;

    if self.__swordMiniGame(move, attacker, defender) is False: return;
    if move == "iron reversal" : self.defense_handler.giveBlock(attacker, defender);
    elif move == "blade dance": attacker.stats["defense"] += 0.5; # balance this lmao
    
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg, self.combat_handler);
    self.ui.panelAnimatedPrintFile("sword style", move, [attacker.name, defender.name, dmg], move);
    
    self.consumeEquipment(attacker, ["left arm", "right arm"], dmg - attacker.stats["strength"]);
    if randint(1, 2) == randint(1, 2): defender.giveStatus("bleeding", 2);
  
  def __bow_style(self, attacker, defender):
    if not attacker.itemExists("wooden arrow"):
      self.ui.panelPrint("[bold red]NO ARROWS[reset]", "center", "bow");
      return;
    move = choices(["quick shot", "half draw", "arrow throw"])[0];
    if self.validateAttack(attacker, defender, move) != True: return;

    if self.__bowMiniGame(move, attacker, defender) is False: return;
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg, self.combat_handler);
    self.ui.panelAnimatedPrintFile("bow style", move, [attacker.name, defender.name, dmg], move);
    
    self.consumeEquipment(attacker, ["left arm", "right arm"], dmg - attacker.stats["strength"]);
    attacker.usedItem("wooden arrow");
    if randint(1, 2) == randint(1, 2): defender.giveStatus("bleeding", 2);
    
  def __dirty_style(self, attacker, defender):
    move = choices(["push", "poke"])[0];
    if self.validateAttack(attacker, defender, move) != True: return;

    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg, self.combat_handler);
    self.ui.panelAnimatedPrintFile("dirty style", move, [attacker.name, defender.name, dmg], move);
    
    if move == "push": defender.giveStatus("stunned", 3);
    elif move == "poke": defender.giveStatus("bleeding", 3);
  
  def __cleric_style(self, attacker, defender):
    if self.validateAttack(attacker, defender, "heal override") != True: return;
    self.ui.printDialogue(attacker.name, "repent..");
    dmg = self.damage_handler.calculateDamage("heal override", attacker, defender);
    dmg = dmg * max(defender.status["karma"][1], 1);
    
    attacker.stats["health"] = min(attacker.stats["health"] + (dmg * 0.5), attacker.stats["max health"]);
    attacker.attackEnemy(dmg, self.combat_handler);
    defender.giveStatus("karma", 2);
    self.ui.panelAnimatedPrintFile("cleric style", "heal override", [attacker.name, defender.name, dmg], "heal override");
  
  def __thief_style(self, attacker, defender):
    move = choices(["stab", "feint", "chain"])[0]; # todo back stab mechanic
    if self.validateAttack(attacker, defender, move) != True: return;
    dmg = self.damage_handler.calculateDamage(move, attacker, defender);
    attacker.attackEnemy(dmg, self.combat_handler);
    self.ui.panelAnimatedPrintFile("thief style", move, [attacker.name, defender.name, dmg], move);
    
    if move == "stab": defender.giveStatus("poisoned", 3);
    elif move == "feint": attacker.giveStatus("parrying", 1);
    
  def __thiefMiniGame(self, move, attacker, defender):
    if not isinstance(attacker, Player): return True;
    
    if move == "chain":
      pass;
      
  def __swordMiniGame(self, move, attacker, defender):
    if not isinstance(attacker, Player): return True;
    
    if move == "blade dance":
      keys = [choice(string.ascii_letters).lower(), choice(string.ascii_letters).lower(), choice(string.ascii_letters).lower()];
      if self.ui.getInputWithTimeout(f"type ({keys[0]}) to quickly 1x", 1.4) != keys[0]: return False;
      self.ui.newLine();
      if self.ui.getInputWithTimeout(f"type ({keys[1]}) quickly 2x", 1.4) != keys[1]: return False;
      self.ui.newLine();
      if self.ui.getInputWithTimeout(f"type ({keys[2]}) quickly 3x", 1.4) != keys[2]: return False;
      self.ui.newLine();
      return True;
    
    elif move == "iron reversal":
      correct_answer = defender.stats["strength"] - attacker.stats["defense"];
      self.ui.animatedPrint(f"iron reversal, [bold green]{defender.stats["strength"]} - {attacker.stats["defense"]}[reset]?");
      answer = self.ui.getInput();
      try:
        if float(answer) != correct_answer:
          self.ui.panelPrint("[bold red]FAILED TO REVERSE[reset]");
          return False;
        return True;
      except KeyError:
        self.ui.panelPrint("[bold red]THATS NOT A NUMBER[reset]");
        return False;
    else: return True;
    
  def __bowMiniGame(self, move, attacker, defender):
    if not isinstance(attacker, Player): return True;
    
    if move == "quick shot":
      if self.ui.getInputWithTimeout("type (q) to quickly shoot a arrow", 1.4) == "q": return True;
      else: self.ui.panelPrint("[red]QUICK SHOT FAILED[reset]");
    
    elif move == "half draw":
      distance = randint(1, 9);
      self.ui.animatedPrint(f"[yellow]draw half![reset], [cyan]divide {distance} by 2[reset]!");
      try:
        answer = self.ui.getInput();
        if float(answer) == (distance / 2): return True;
        else: self.ui.panelPrint("[red]WRONG, SKILL ISSUE[reset]");
      except ValueError: self.ui.panelPrint("[red]MUST BE DECIMALS, (3.5)[reset]");
    else: return True;
    return False;
  
  def __basicMiniGame(self, move, attacker, defender):
    if not isinstance(attacker, Player): return True;
    if move == "slam":
      for n in range(3):
        if self.ui.getKey("press (q)") != "q": return False;
        if self.ui.getKey("press (e)") != "e": return False;
      return True;
      
    else: return True;
    return False;
    
  def handleAttack(self, attacker, defender):
    self.handlePassiveSkills("attack", attacker, defender);

    if attacker.attack_style == "basic": self.__basic_style(attacker, defender);
    elif attacker.attack_style == "swordsman": self.__sword_style(attacker, defender);
    elif attacker.attack_style == "dirty": self.__dirty_style(attacker, defender);
    elif attacker.attack_style == "archer": self.__bow_style(attacker, defender);
    elif attacker.attack_style == "cleric": self.__cleric_style(attacker, defender);
    elif attacker.attack_style == "thief": self.__thief_style(attacker, defender);
