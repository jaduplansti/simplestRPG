from enemy import Enemy, getEnemyByName;
from random import randint, choices;
from handlers import AttackHandler;

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
    
  def initiateFightNpc(self, character, name):
    enemy = getEnemyByName(name, character, self.game);
    self.attacker = character
    self.attacker.enemy = enemy;
    
    self.defender = enemy;
    self.defender.enemy = self.attacker;
    self.attacker.status["blocking"] = [False, 0]; # temporary fix
    
    self.game.handleCombatInitiateMenu(self);
  
  def __handleWin(self):
    if self.tryBerserkNpc(self.defender) is False:
      if self.defender.boss is True: self.ui.panelPrint("BOSS DEFEATED", "center", "combat");
      self.giveExp(self.attacker, self.defender);
      self.handleLevelUp(self.attacker);
      self.giveLoot(self.attacker, self.defender);
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
    won.money += randint(5, 10) * lost.level;
    
  def handleFatigue(self, attacker):
    if attacker.energy <= 10:
      self.ui.panelAnimatedPrint(f"[red]{attacker.name} passes out from exhaustion.[reset]", "fatigue");
      attacker.stats["health"] = 0;
      return "passed out";
    elif attacker.energy <= 25 and not isinstance(attacker, Enemy):
      self.ui.panelAnimatedPrintFile("fatigue handler", "exhausted", [attacker.name], "fatigue");
    elif attacker.energy <= 50 and not isinstance(attacker, Enemy):
      self.ui.panelAnimatedPrintFile("fatigue handler", "fatigued", [attacker.name], "fatigue");
    elif attacker.energy <= 75 and not isinstance(attacker, Enemy):
      self.ui.panelAnimatedPrintFile("fatigue handler", "tired", [attacker.name], "fatigue");
    else:
      return False;
    
    self.ui.panelPrint(f"([blue]-{attacker.getFatigueMultiplier() * 100}%[reset]) stat output.");
  
  def handleHunger(self, attacker):
    if attacker.hunger <= 10:
      self.ui.panelAnimatedPrintFile("hunger handler", "starved", [attacker.name], "hunger");
    elif attacker.hunger <= 25 and not isinstance(attacker, Enemy):
      self.ui.panelAnimatedPrintFile("hunger handler", "very hungry", [attacker.name], "hunger");
    elif attacker.hunger <= 50 and not isinstance(attacker, Enemy):
      self.ui.panelAnimatedPrintFile("hunger handler", "moderately hungry", [attacker.name], "hunger");
    elif attacker.hunger <= 75 and not isinstance(attacker, Enemy):
      self.ui.panelAnimatedPrintFile("hunger handler", "slightly hungry", [attacker.name], "hunger");
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
    if direction == "backward" and attacker.zone - offset >= 0 : attacker.zone -= offset;
    elif direction == "forward" and attacker.zone - offset <= 10 : attacker.zone += offset;

  def handleOption(self, option, attacker, defender):
    self.ui.showStatus("processing move", 1, "clock");
    self.handleHunger(attacker);
    
    if self.handleFatigue(attacker) == "passed out":
      return "passed out";
      
    if option in ["attack", "atk"]:
      if self.attack_handler.handleAttack(attacker, defender) in ["parried"]: return "parry";
    elif option in ["block", "blk"]:
      self.attack_handler.defense_handler.giveBlock(attacker, defender);
      self.ui.panelAnimatedPrintFile("block", "blocking", [attacker.name, defender.name], "block");
    elif option == "taunt":
      self.attack_handler.taunt_handler.handleTaunt(attacker, defender);
    elif option == "flee" and attacker.stats["health"] <= (attacker.stats["max health"] * 0.25): # put in handlers
      if attacker.berserk is True: 
        self.ui.animatedPrint(f"[red]{attacker.name}[reset] tried to run away, but ([red]BERSERK[reset]) pulls them back");
        self.setCurrentTurnOption(attacker, "");
      else: self.ui.animatedPrint(f"[red]{attacker.name}[reset] ran away!");
    elif option == "items":
      self.game.handleUseItem(self);
    elif option == "skills":
      self.game.handleUseSkill(None, self, attacker, defender);
    elif len(option.split(",")) > 1 and option.split(",")[0] == "use" and isinstance(attacker, Enemy):
      if attacker.itemExists(option.split(",")[1].lstrip()) is True: attacker.getItem(option.split(",")[1].lstrip()).use(self.game, attacker, self);
      else: self.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] tried to use a item, but they dont have a {option.split(",")[1].lstrip()}", title = "item");
    elif len(option.split(",")) > 1 and option.split(",")[0] == "perform" and isinstance(attacker, Enemy):
      if attacker.skillExists(option.split(",")[1].lstrip()) is True: attacker.skills[option.split(",")[1].lstrip()].use(self, attacker, defender);
      else: self.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] tried to use a skill, but they haven't learned {option.split(",")[1].lstrip()}", title = "skill");
    elif len(option.split(" ")) > 1 and option.split(" ")[0] == "move":
      direction = option.split(" ")[1];
      if direction.lower() in ["backward", "forward"]: 
        self.move(1, direction, attacker);
        self.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] moved [cyan]{direction}[reset] by a step!", "move");
      else: self.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] moved [cyan]{direction}[reset] but failed!", "move");
    else:
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] did nothing.");
      self.setCurrentTurnOption(attacker, "");
      
    self.useHunger(attacker);
    attacker.deductEnergy();
  
  def handleCombatNpc(self, auto = False):
    while True:
      self.menu.showCombatMenu(self, self.attacker);
      self.player_option = self.ui.getInputWithTimeout("[green](enter action)[reset] ⤵", 15);
      self.storeAction(self.player_option);

      self.ui.clear();
      self.ui.showHeader("Combat Logs", "=");
      self.ui.showSeperator("-");
      self.attack_handler.status_handler.handleStatus(self.attacker, self.defender);
      
      self.lockTarget(self.attacker, self.defender);
      if self.attack_handler.status_handler.turn_passed is False: ran = self.handleOption(self.player_option, self.attacker, self.defender);
      self.ui.showSeperator("-");
      
      if self.checkDeath() is True or (self.player_option == "flee" and self.attacker.status["stunned"] is False):
        break;
      
      self.enemy_option = self.defender.getAction(self.ui);
      self.storeAction(self.enemy_option);
      self.attack_handler.status_handler.handleStatus(self.defender, self.attacker);
      
      self.lockTarget(self.attacker, self.defender);
      if self.attack_handler.status_handler.turn_passed is False: ran = self.handleOption(self.enemy_option, self.defender, self.attacker);
      self.ui.showSeperator("*");

      if isinstance(self.defender, Enemy):
        if self.defender.berserk is True: self.defender.giveDamage(self.defender.stats["max health"] * 0.2)
        
      if self.checkDeath() is True or (self.enemy_option == "flee" and self.defender.status["stunned"] is False): break;
      self.ui.showSeperator("-");
      self.ui.awaitKey();
 