import string;
from player import Player;
from random import randint, choice, choices, uniform;

class Style:
  def __init__(self):
    pass;

class StyleHandler:
  def __init__(self, game, combat_handler):
    self.game = game;
    self.combat_handler = combat_handler;
    self.attack_handler = combat_handler.attack_handler;
    self.ui = game.ui;
    
    self.styles = {
      **self.__register_style("swordsman", self.__swordsman_style),
      **self.__register_style("archer", self.__archer_style),
      **self.__register_style("basic", self.__basic_style),
      **self.__register_style("cleric", self.__cleric_style),
      **self.__register_style("thief", self.__thief_style),
      **self.__register_style("dirty", self.__dirty_style),
    }
  
  def __register_style(self, name, handler):
    return {name : {
      "handler" : handler,
    }}
  
  def __basic_style(self, attacker, defender):
    # move selection and verification
    move = choices(["punch", "strong punch", "double punch", "slam"])[0];
    if self.attack_handler.validateAttack(attacker, defender, move) != True: return;
    
    # sound effects
    if move == "punch": self.game.audio_handler.play(f"punch{randint(1, 2)}.wav");
    elif move == "strong punch": self.game.audio_handler.play("strong_punch.wav");
    elif move == "slam" : pass;
    elif move == "double punch": 
      self.game.audio_handler.play(f"punch{randint(1, 2)}.wav");
      self.game.audio_handler.play(f"punch{randint(1, 2)}.wav");
    
    # damage calculation and output logs 
    dmg = self.attack_handler.damage_handler.calculateDamage(move, attacker, defender);
    self.ui.panelAnimatedPrintFile("basic style", move, [attacker.name, defender.name, dmg], move);
    attacker.attackEnemy(dmg, self.combat_handler);
  
  def __swordsman_style(self, attacker, defender):
    # move selection and verification
    move = choices(["slash", "thrust", "iron reversal", "blade dance"])[0];
    if self.attack_handler.validateAttack(attacker, defender, move) != True: return;
    if self.__swordMiniGame(move, attacker, defender) is False: return;
    
    # sound effects
    if move == "slash": self.game.audio_handler.play(f"slash{randint(1, 2)}.wav");
    elif move == "thrust": self.game.audio_handler.play(f"thrust{randint(1, 2)}.wav");
    elif move == "iron reversal": self.game.audio_handler.play(f"iron_reversal.wav");
    elif move == "blade dance": 
      self.game.audio_handler.play(f"{choices(["slash", "thrust"])[0]}{randint(1, 2)}.wav");
      self.game.audio_handler.play(f"{choices(["slash", "thrust"])[0]}{randint(1, 2)}.wav");
      self.game.audio_handler.play(f"{choices(["slash", "thrust"])[0]}{randint(1, 2)}.wav");

    # move buffs
    if move == "iron reversal" : self.attack_handler.defense_handler.giveBlock(attacker, defender);
    elif move == "blade dance": attacker.stats["defense"] += 0.5; # balance this lmao
    
    # damage calculation and output logs 
    dmg = self.attack_handler.damage_handler.calculateDamage(move, attacker, defender);
    self.ui.panelAnimatedPrintFile("sword style", move, [attacker.name, defender.name, dmg], move);
    attacker.attackEnemy(dmg, self.combat_handler);
    
    # status effects, durability consumption and mechanic
    self.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], dmg * 0.1);
    if randint(1, 2) == randint(1, 2): defender.giveStatus("bleeding", 2);
    self.swordMechanic(attacker, defender);
  
  def __archer_style(self, attacker, defender):
    # check for ammo (wooden arrow)
    if not attacker.itemExists("wooden arrow"):
      self.ui.panelPrint("[bold red]NO ARROWS[reset]", "center", "bow");
      return;
      
    # move selection and verification
    move = choices(["quick shot", "half draw", "arrow throw"])[0];
    if self.attack_handler.validateAttack(attacker, defender, move) != True: return;
    if self.__bowMiniGame(move, attacker, defender) is False: return;
    
    # damage calculation and output logs 
    dmg = self.attack_handler.damage_handler.calculateDamage(move, attacker, defender);
    self.ui.panelAnimatedPrintFile("bow style", move, [attacker.name, defender.name, dmg], move);
    attacker.attackEnemy(dmg, self.combat_handler);
    
    # status effects, durability consumption and mechanic
    self.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], dmg * 0.01);
    attacker.usedItem("wooden arrow");
    if randint(1, 2) == randint(1, 2): defender.giveStatus("bleeding", 2);

  def __dirty_style(self, attacker, defender):
    # move selection and verification
    move = choices(["push", "poke"])[0];
    if self.attack_handler.validateAttack(attacker, defender, move) != True: return;
    
    # damage calculation and output logs 
    dmg = self.attack_handler.damage_handler.calculateDamage(move, attacker, defender);
    self.ui.panelAnimatedPrintFile("dirty style", move, [attacker.name, defender.name, dmg], move);
    attacker.attackEnemy(dmg, self.combat_handler);
    
    # move buffs
    if move == "push": defender.giveStatus("stunned", 3);
    elif move == "poke": defender.giveStatus("bleeding", 3);
  
  def __cleric_style(self, attacker, defender):
    # move verification
    if self.attack_handler.validateAttack(attacker, defender, "heal override") != True: return;
    #self.ui.printDialogue(attacker.name, "repent..");
    
    # damage calculation and output logs 
    dmg = self.attack_handler.damage_handler.calculateDamage("heal override", attacker, defender);
    dmg = dmg * max(defender.status["karma"][1], 1);
    attacker.stats["health"] = min(attacker.stats["health"] + (dmg * 0.5), attacker.stats["max health"]);
    
    defender.giveStatus("karma", 2);
    self.ui.panelAnimatedPrintFile("cleric style", "heal override", [attacker.name, defender.name, dmg], "heal override");
    attacker.attackEnemy(dmg, self.combat_handler);
  
  def __thief_style(self, attacker, defender):
    # move selection and verification
    move = choices(["stab", "feint", "chain"])[0]; # todo back stab mechanic
    if self.attack_handler.validateAttack(attacker, defender, move) != True: return;
    
    # shadow mechanic
    if hasattr(attacker, "shadow"): 
      attacker.shadow += 5;
      if attacker.shadow >= 20: self.ui.animatedPrint(f"[purple] yóu yóu yôuxh2vé s_hdów [reset]")
      else: self.ui.animatedPrint(f"shadow gained!");
      self.ui.panelPrint(self.ui.showBar(attacker.shadow, 25, 4, "purple"), "center");
    else: attacker.shadow = 1;
    
    # damage calculation and output logs 
    dmg = self.backstabMechanic(move, attacker, defender);
    self.ui.panelAnimatedPrintFile("thief style", move, [attacker.name, defender.name, round(dmg * (attacker.shadow * 0.1))], move);
    attacker.attackEnemy(dmg * (attacker.shadow * 0.1), self.combat_handler);
    
    # status effects, durability consumption and mechanic
    self.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], (dmg * (attacker.shadow * 0.1)) * 0.05);
    if move == "stab": defender.giveStatus("poisoned", 3);
    elif move == "feint": attacker.giveStatus("parrying", 1);
    elif move == "chain" and attacker.equipment["right arm"] != None: self.__thief_style(attacker, defender);
    
    # shadow release mechanic
    if attacker.shadow >= 25: 
      attacker.shadow = 1;
      self.ui.printDialogue(attacker.name, "release!");
      self.ui.animatedPrint(f"[purple]{attacker.name}'s shadow dissipates..[reset]")
  
  def backstabMechanic(self, move, attacker, defender):
    dmg = 0;
    if attacker.zone in [defender.zone - 1, defender.zone + 1]: 
      dmg = self.attack_handler.damage_handler.calculateDamage(move, attacker, defender, ignore_defense = True);
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] goes for a backstab!");
    else: dmg = self.attack_handler.damage_handler.calculateDamage(move, attacker, defender);
    return dmg;
    
  def swordMechanic(self, attacker, defender):
    if self.combat_handler.getOpponentTurnOption(attacker) == "block" and defender.status["stunned"][0] is False:
      self.ui.animatedPrint(f"[yellow]{defender.name}[reset] let their guard down!");
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] grabs [yellow]{defender.name}[reset]!");
      self.ui.printDialogue(defender.name, "augh..");
      defender.giveStatus("stunned", 2);
      
    elif defender.status["bleeding"][1] > 3:
      defender.status["bleeding"] = [False, 0];
      dmg = round(defender.stats["max health"] * uniform(0.3, 0.6));
      self.ui.printDialogue(attacker.name, "scatter!");
      self.ui.panelAnimatedPrint(f"[yellow]{defender.name}'s[reset] injuries throb in pain, permanently dealing [red]{dmg}[reset] damage!", "injury");
      attacker.attackEnemy(dmg);
  
  def __swordMiniGame(self, move, attacker, defender):
    if not isinstance(attacker, Player) or randint(1, 3) == randint(1, 3): return True;
    
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
      correct_answer = round(defender.stats["strength"]) - round(attacker.stats["defense"]);
      self.ui.animatedPrint(f"iron reversal, [bold green]{round(defender.stats["strength"])} - {round(attacker.stats["defense"])}[reset]?");
      answer = self.ui.getInput();
      try:
        if int(answer) != correct_answer:
          self.ui.panelPrint("[bold red]FAILED TO REVERSE[reset]");
          return False;
        return True;
      except ValueError:
        self.ui.panelPrint("[bold red]THATS NOT A NUMBER[reset]");
        return False;
    else: return True;
    
  def __bowMiniGame(self, move, attacker, defender):
    if not isinstance(attacker, Player): return True;
    
    if move == "quick shot":
      if self.ui.getInputWithTimeout("type (q) to quickly shoot a arrow", 1.4) == "q": 
        self.ui.newLine();
        return True;
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
    