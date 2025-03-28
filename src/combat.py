from enemy import getEnemyByName;
from random import randint, choices;
from handlers import AttackHandler;

class CombatHandler:
  def __init__(self, game):
    self.game = game;
    self.ui = self.game.ui;
    
    self.attack_handler = AttackHandler(self);
    
    self.attacker = None;
    self.defender = None;
    
  def initiateFightNpc(self, character, name):
    enemy = getEnemyByName(name);
    self.attacker = character
    self.attacker.enemy = enemy;
    
    self.defender = enemy;
    self.defender.enemy = self.attacker;
    self.ui.showStatCompareMenu(self.attacker, self.defender);
    
    self.handleCombatNpc();
  
  def giveExp(self, won, lost):
    exp_gain = round((lost.level * 100) / randint(1, 3));
    self.ui.animatedPrint(f"[yellow]{won.name}[reset] gained [italic green]{exp_gain}[reset] exp!");
    won.exp += exp_gain;
    
  def giveLoot(self, won, lost): # fix add inventory to enemy
    won.addItemToInventory(lost.getLoot());
  
  def handleFatigue(self, attacker):
    if attacker.energy <= 10:
      self.ui.animatedPrint(f"[red]{attacker.name} passes out from exhastion.[reset]");
      self.attacker.stats["health"] = 0;
      return "passed out";
    elif attacker.energy <= 25:
      self.ui.animatedPrintFile("fatigue handler", "exhausted", [attacker.name]);
    elif attacker.energy <= 50:
      self.ui.animatedPrintFile("fatigue handler", "fatigued", [attacker.name]);
    elif attacker.energy <= 75:
      self.ui.animatedPrintFile("fatigue handler", "tired", [attacker.name]);
    else:
      return False;
    
    self.ui.animatedPrint(f"([blue]-{self.attacker.getFatigueMultiplier()}[reset]) stat reduction.");
  
  def handleTaunt(self, attacker, defender):
    self.ui.animatedPrintFile("taunt", "debuff", [attacker.name, defender.name]);
    if defender.name == "slime":
      self.ui.animatedPrintFile("taunt success response", "debuff slime", [defender.name]);
  
  def handleAuto(self, auto):
    if auto is True:
      return choices(["attack", "block"])[0];
    return self.ui.getInput();
  
  def handleOption(self, option, attacker, defender):
    if self.handleFatigue(attacker) == "passed out":
      return True;
      
    if option == "attack":
      self.attack_handler.handleAttack(attacker, defender);
    elif option == "block":
      pass;
    elif option == "taunt":
      self.handleTaunt(attacker, defender);
    elif option == "flee" and attacker.stats["health"] <= (attacker.stats["max health"] * 0.25):
      self.ui.animatedPrint(f"[red]{attacker.name}[reset] ran away!");
      self.ui.awaitKey();
      return True
    else:
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] did nothing.");
    
    attacker.deductEnergy();

  def checkDeath(self):
    if self.attacker.stats["health"] <= 0:
      self.ui.animatedPrint(f"[yellow]{self.defender.name}[reset] killed [yellow]{self.attacker.name}[reset]");
    elif self.defender.stats["health"] <= 0:
      self.ui.animatedPrint(f"[yellow]{self.attacker.name}[reset] killed [yellow]{self.defender.name}[reset]");
      self.giveExp(self.attacker, self.defender);
      attacker.stats["health"] = attacker.stats["max health"]
    else:
      return False;
    self.ui.awaitKey();
    return True;
  
  def handleCombatNpc(self, auto = False):
    while True:
      self.ui.showCombatMenu(self, self.attacker);
      option = self.handleAuto(auto);
      enemy_option = choices(["attack", "block", "flee"], [self.defender.attack_chance, self.defender.block_chance, 0.5])[0];
      
      self.ui.clear();
      self.ui.showHeader("Combat Logs", "=");
      self.ui.showSeperator("-");
      
      ran = self.handleOption(option, self.attacker, self.defender);
      self.ui.showSeperator("-");

      if self.checkDeath() is True or ran is True:
        break;
      
      ran = self.handleOption(enemy_option, self.defender, self.attacker);
      self.ui.showSeperator("-");
      
      self.ui.showHealthBar(self.attacker);
      self.ui.showHealthBar(self.defender);

      if self.checkDeath() is True or ran is True:
        break;
      
      self.ui.showSeperator("-");
      self.ui.awaitKey();