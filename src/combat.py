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
    self.handleCombatNpc();
  
  def giveExp(self, won, lost):
    won.exp += round((lost.level * 100) / randint(1, 3));
  
  def giveLoot(self, won, lost): # fix add inventory to enemy
    won.addItemToInventory(lost.getLoot());
    
  def handleAuto(self, auto):
    if auto is True:
      return choices(["attack", "block"])[0];
    return self.ui.getInput();
  
  def handleOption(self, option, attacker, defender):
    if option == "attack":
      self.attack_handler.handleAttack(attacker, defender);
    elif option == "block":
      pass;
  
  def checkDeath(self):
    if self.attacker.stats["health"] <= 0:
      self.ui.normalPrint("you lost");
    elif self.defender.stats["health"] <= 0:
      self.ui.normalPrint("npc lost");
    else:
      return False;
    self.ui.awaitKey();
    return True;
    
  def handleCombatNpc(self, auto = False):
    while True:
      self.ui.showCombatMenu(self, self.attacker);
      option = self.handleAuto(auto);
      enemy_option = choices(["attack", "block"], [self.defender.attack_chance, self.defender.block_chance])[0];
      
      self.ui.clear();
      self.ui.showHeader("Combat Logs", "=");
      self.ui.showSeperator("-");
      
      self.handleOption(option, self.attacker, self.defender);
      self.ui.showSeperator("-");

      if self.checkDeath() is True:
        break;
      
      self.handleOption(enemy_option, self.defender, self.attacker);
      self.ui.showSeperator("-");
      
      self.ui.showHealthBar(self.attacker);
      self.ui.showHealthBar(self.defender);

      if self.checkDeath() is True:
        break;
      
      self.ui.showSeperator("-");
      self.ui.awaitKey();