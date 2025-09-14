from objects.npc import NPC, getNPC;
from random import randint, choices;
from mechanics.handlers import AttackHandler;

from time import time;

class CombatHandler:
  def __init__(self, game):
    self.game = game;
    self.ui = self.game.ui;
    self.menu = self.game.menu;
    self.attack_handler = AttackHandler(self);
    
    self.attacker = None;
    self.defender = None;
    self.enemy_option = ""; # temporary solution
    self.player_option = "";
    
    self.previous_action = "";
    self.won = None;
    
  def initiateFightNpc(self, character, name):
    self.game.audio_handler.play("battle_start.wav");
    self.game.animator.transition();
    
    npc = getNPC(name);
    self.attacker = character;
    self.attacker.enemy = npc;
    
    self.defender = npc;
    self.defender.enemy = self.attacker;
    self.attacker.clearStatus();
    
    self.attacker.zone = randint(1, 8);
    self.defender.zone = randint(1, 8);
    
    self.game.handleCombatInitiateMenu(self);
  
  def __handleWin(self):
    if self.tryBerserkNpc(self.defender) is False:
      if self.defender.boss is True: self.ui.panelPrint("BOSS DEFEATED", "center", "combat");
      self.giveExp(self.attacker, self.defender);
      self.handleLevelUp(self.attacker);
      self.giveLoot(self.attacker, self.defender);
      self.won = self.attacker.name;
      return True;
    return False;
    
  def giveExp(self, won, lost):
    exp_gain = round((lost.level * 100) / randint(1, 3));
    self.ui.animatedPrint(f"[yellow]{won.name}[reset] felt an energy surging from within, gained [italic green]{exp_gain}[reset] exp!");
    won.exp += exp_gain;
  
  def handleLevelUp(self, won):
    old_level = won.level;
    if won.tryLevelUp() is True:
      self.ui.animatedPrint(f"[yellow]{won.name}[reset] feels a surge of [blue]power[reset], [yellow]{won.name}[reset], leveled up!");
      self.ui.panelPrint(f"level [yellow]{old_level}[reset] -> [green]{won.level}[reset]");
      
  def giveLoot(self, won, lost):
    item = lost.getLoot();
    if item != None: self.game.givePlayerItem(item.name, 1);
    earned = randint(5, 10) * lost.level;
    self.ui.animatedPrint(f"[yellow]{won.name}[reset] earned [green]{earned}[reset] gold!");
    won.money += earned;
   
  def notifyDurability(self, attacker, parts):
    if not self.game.isPlayer(attacker):
      return;
       
    for part in parts:
      item = attacker.equipment[part];
      if item is None: continue;
      durability_ratio = item.durability / item.max_durability;

      if durability_ratio <= 0.1: self.ui.animatedPrint(f"[bold]{item.name}[reset] is on the verge of {choices(["[yellow]cracking[reset]", "[magenta]shattering[reset]", "[cyan]breaking[reset]"])[0]}!");
      elif durability_ratio <= 0.4: self.ui.animatedPrint(f"[bold]{item.name}[reset] is close to {choices(["[yellow]cracking[reset]", "[magenta]shattering[reset]", "[cyan]breaking[reset]"])[0]}!");
      elif durability_ratio <= 0.6: self.ui.animatedPrint(f"[bold]{item.name}[reset] appears to have small {choices(["[yellow]dents[reset]", "[magenta]cracks[reset]", "[cyan]damaged materials[reset]"])[0]}!");

  def handleFatigue(self, attacker):
    if attacker.energy <= 10:
      self.ui.panelAnimatedPrint(f"[red]{attacker.name} passes out from exhaustion.[reset]", "fatigue");
      attacker.stats["health"] = 0;
      return "passed out";
    elif attacker.energy <= 25 and not isinstance(attacker, NPC):
      self.ui.panelAnimatedPrintFile("fatigue handler", "exhausted", [attacker.name], "fatigue");
    else:
      return False;
    
    self.ui.panelPrint(f"([blue]-{attacker.getFatigueMultiplier() * 100}%[reset]) stat output.");
  
  def handleHunger(self, attacker):
    if attacker.hunger <= 10 and self.game.isPlayer(attacker):
      self.ui.panelAnimatedPrintFile("hunger handler", "starved", [attacker.name], "hunger");
    elif attacker.hunger <= 25 and self.game.isPlayer(attacker):
      self.ui.panelAnimatedPrintFile("hunger handler", "very hungry", [attacker.name], "hunger");
    else:
      return False;
  
  def useHunger(self, attacker):
    if attacker.hunger > 10 and attacker.berserk != True:
      attacker.stats["health"] = min(attacker.stats["max health"], attacker.stats["health"] + (attacker.hunger * 0.2));
      attacker.energy = min(100, attacker.energy + (attacker.hunger * 0.2));
      attacker.hunger = max(0, attacker.hunger - 2);
    else:
      attacker.stats["health"] -= round(attacker.stats["health"] * 0.02);
      attacker.energy -= round(attacker.energy * 0.02);

  def tryBerserkNpc(self, npc):
    if randint(1, 7) == randint(1, 7) and npc.berserk is False:
      self.ui.animatedPrint(f"a mysterious aura covers [red]{npc.name}[reset]");
      self.ui.animatedPrint(f"[yellow]{npc.name}[reset] goes [red]Berserk[reset]!");
      self.ui.panelPrint("[blue]ALL STATS[reset] [green](1.5x)[reset]");
      npc.goBerserk();
      return True;
    return False;
  
  def checkDeath(self):
    self.attack_handler.handlePassiveSkills("death", self.attacker, self.defender);
    self.attack_handler.handlePassiveSkills("death", self.defender, self.attacker);
    self.game.player.trackQuest(self.game, self);
    if self.attacker.stats["health"] <= 0:
      self.ui.animatedPrint(f"[yellow]{self.defender.name}[reset] killed [yellow]{self.attacker.name}[reset]");
      self.won = self.defender.name;
    elif self.defender.stats["health"] <= 0:
      self.ui.animatedPrint(f"[yellow]{self.attacker.name}[reset] killed [yellow]{self.defender.name}[reset]");
      won = self.__handleWin();
      if won is False: return False;
    else:
      return False;
    return True;
  
  def setCurrentTurnOption(self, attacker, option):
    if self.game.isPlayer(attacker): self.player_option = option;
    else: self.enemy_option = option;
  
  def getCurrentTurnOption(self, attacker):
    if self.game.isPlayer(attacker): return self.player_option;
    else: return self.enemy_option;
  
  def getOpponentTurnOption(self, attacker):
    if self.game.isPlayer(attacker): return self.enemy_option;
    else: return self.player_option;
  
  def storeAction(self, option):
    self.previous_action = option;
  
  def isHit(self, direction, n, attacker, defender):
    if attacker.zone == defender.zone: return True;
    elif direction == "backward" and defender.zone in range(attacker.zone - 1, attacker.zone - n - 1, -1): return True;
    elif direction == "forward" and defender.zone in range(attacker.zone + 1, attacker.zone + n + 1): return True;
    else: return False;
  
  def lockTarget(self, attacker, defender):
    if attacker.zone < defender.zone: 
      attacker.direction = "forward";
      defender.direction = "backward";
    elif attacker.zone > defender.zone: 
      attacker.direction = "backward";
      defender.direction = "forward";
    else:
      pass;
      
  def move(self, offset, direction, attacker):
    if direction == "backward" and attacker.zone - offset > 0 : attacker.zone -= offset;
    elif direction == "forward" and attacker.zone - offset < 10 : attacker.zone += offset;
  
  def handleCombatOption(self, option, attacker, defender):
    if option in ["attack", "atk"]:
      self.attack_handler.handleAttack(attacker, defender);
    elif option in ["block", "blk"]:
      self.attack_handler.defense_handler.giveBlock(attacker, defender);
      self.ui.panelAnimatedPrintFile("block", "blocking", [attacker.name, defender.name], "block");
    elif option == "taunt":
      self.attack_handler.taunt_handler.handleTaunt(attacker, defender);
    else: return -1;
  
  def handleInteractOption(self, option, attacker, defender):
    if option == "items": self.game.handleUseItem(self);
    elif option == "skills": self.game.handleUseSkill(None, self, attacker, defender);
    else: return -1;
    
  def handleMovementOption(self, option, attacker, defender):
    if option == "advance":
      self.move(1, attacker.direction, attacker);
      self.ui.panelAnimatedPrintFile("movement", "advance", [attacker.name], f"([yellow]{attacker.zone}[reset])");
    elif option == "retreat":
      self.move(1, defender.direction, attacker);
      self.ui.panelAnimatedPrintFile("movement", "retreat", [attacker.name], f"([red]{attacker.zone}[reset])");
    elif option == "dash":
      self.move(2, attacker.direction, attacker);
      self.game.animator.animateDash();
      self.ui.panelAnimatedPrintFile("movement", "dash", [attacker.name], ">>");
      
    else: return -1;
    
  def handleOption(self, option, attacker, defender):
    self.ui.showStatus("processing move", 1, "clock");
    self.handleHunger(attacker);
    
    if self.handleFatigue(attacker) == "passed out":
      return "passed out";
      
    if self.handleCombatOption(option, attacker, defender) != -1: return;
    elif self.handleInteractOption(option, attacker, defender) != -1: return;
    elif self.handleMovementOption(option, attacker, defender) != -1: return;
    else:
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] did nothing.");
      self.setCurrentTurnOption(attacker, "");
      
    self.useHunger(attacker);
    attacker.deductEnergy();
  
  def handleCombatNpc(self, auto = False):
    while True:
      self.menu.showCombatMenu(self, self.attacker);
      self.player_option = self.ui.getInput();
      self.storeAction(self.player_option);
      
      self.ui.clear();
      self.ui.showHeader("Combat Logs", "=");
      self.ui.showSeperator("×");
      self.attack_handler.status_handler.handleStatus(self.attacker, self.defender);
      
      self.lockTarget(self.attacker, self.defender);
      if self.attack_handler.status_handler.turn_passed is False: ran = self.handleOption(self.player_option, self.attacker, self.defender);
      self.ui.showSeperator("×");

      if self.checkDeath() is True or (self.player_option == "flee" and self.attacker.status["stunned"][0] is False):
        break;
      
      self.enemy_option = self.defender.getAction(self.ui);
      self.storeAction(self.enemy_option);
      self.attack_handler.status_handler.handleStatus(self.defender, self.attacker);
      
      self.lockTarget(self.attacker, self.defender);
      if self.attack_handler.status_handler.turn_passed is False: ran = self.handleOption(self.enemy_option, self.defender, self.attacker);
      self.ui.showSeperator("*");

      if isinstance(self.defender, NPC):
        if self.defender.berserk is True: self.defender.giveDamage(self.defender.stats["max health"] * 0.2)
        
      if self.checkDeath() is True or (self.enemy_option == "flee" and self.defender.status["stunned"][0] is False): break;
      self.ui.showSeperator("-");
      self.ui.awaitKey();
 
  def handleSpare(self, won, lost):
    self.ui.animatedPrint(f"[yellow]{lost.name}[reset] is asking for mercy!");
    self.ui.printDialogue(lost.name, "...");
    self.ui.normalPrint("([red]skill[reset]) or ([cyan]mercy[resey])\n");
    # todo here