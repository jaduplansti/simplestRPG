from enemy import getEnemyByName;
from random import randint, choices;
from handlers import AttackHandler;
from  combatevent import CombatEventHandler;

class CombatHandler:
  def __init__(self, game):
    self.game = game;
    self.ui = self.game.ui;
    self.menu = self.game.menu;
    self.attack_handler = AttackHandler(self);
    
    self.event_handler = CombatEventHandler(self);
    self.attacker = None;
    self.defender = None;
    
  def initiateFightNpc(self, character, name):
    enemy = getEnemyByName(name);
    self.attacker = character
    self.attacker.enemy = enemy;
    
    self.defender = enemy;
    self.defender.enemy = self.attacker;
    self.menu.showStatCompareMenu(self.attacker, self.defender);
    
    self.handleCombatNpc();
  
  def giveExp(self, won, lost):
    exp_gain = round((lost.level * 100) / randint(1, 3));
    self.ui.animatedPrint(f"[yellow]{won.name}[reset] felt an energy surging from within, gained [italic green]{exp_gain}[reset] exp!");
    won.exp += exp_gain;
  
  def handleLevelUp(self, won):
    old_level = won.level;
    if won.tryLevelUp() is True:
      self.ui.animatedPrint(f"[yellow]{won.name}[reset] feels a surge of [blue]power[reset], [yellow]{won.name}[reset], leveled up!");
      self.ui.panelPrint(f"level [yellow]{old_level}[reset] -> [green]{won.level}[reset]");
      
  def giveLoot(self, won, lost): # fix add inventory to enemy
    won.addItemToInventory(lost.getLoot());
  
  def handleFatigue(self, attacker):
    if attacker.energy <= 10:
      self.ui.panelAnimatedPrint(f"[red]{attacker.name} passes out from exhastion.[reset]", "fatigue");
      attacker.stats["health"] = 0;
      return "passed out";
    elif attacker.energy <= 25:
      self.ui.panelAnimatedPrintFile("fatigue handler", "exhausted", [attacker.name], "fatigue");
    elif attacker.energy <= 50:
      self.ui.panelAnimatedPrintFile("fatigue handler", "fatigued", [attacker.name], "fatigue");
    elif attacker.energy <= 75:
      self.ui.panelAnimatedPrintFile("fatigue handler", "tired", [attacker.name], "fatigue");
    else:
      return False;
    
    self.ui.panelPrint(f"([blue]-{self.attacker.getFatigueMultiplier()}[reset]) stat reduction.");
  
  def handleInput(self):
    pass;
    
  def handleOption(self, option, attacker, defender):
    if self.handleFatigue(attacker) == "passed out":
      return True;
      
    if option == "attack":
      self.attack_handler.handleAttack(attacker, defender);
    elif option == "block":
      self.attack_handler.defense_handler.handleBlock(attacker, defender);
      self.ui.panelAnimatedPrintFile("block", "blocking", [attacker.name, defender.name], "block");
    elif option == "taunt":
      self.attack_handler.taunt_handler.handleTaunt(attacker, defender);
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
      if randint(1, 10) == randint(1, 10):
        self.ui.panelPrint(f"[blue]{self.defender.name} refuses to die![reset]");
        self.ui.panelPrint("[yellow]HEALTH[reset] [green](+5)[reset]");
        self.defender.stats["health"] += 5;
        return False;
      else:
        self.giveExp(self.attacker, self.defender);
        self.handleLevelUp(self.attacker);
    else:
      return False;
      
    self.ui.awaitKey();
    self.attacker.stats["health"] = self.attacker.stats["max health"];
    return True;
  
  def handleCombatLocal(self, attacker, defender): # handles multiplayer using pipes, 2 players
    while True:
      self.menu.showCombatMenu(attacker, defender);
      option1 = self.ui.getInput();
      #option2 = self.game.multiplayer_handler
      
  def handleCombatNpc(self, auto = False):
    while True:
      self.menu.showCombatMenu(self, self.attacker);
      option = self.ui.getInput();
      enemy_option = choices(["attack", "block", "flee", "taunt"], [self.defender.attack_chance, self.defender.block_chance, 0.5, 0.5])[0];
      
      self.ui.clear();
      self.ui.showHeader("Combat Logs", "=");
      self.ui.showSeperator("-");
      
      ran = self.handleOption(option, self.attacker, self.defender);
      self.ui.showSeperator("-");

      if self.checkDeath() is True or ran is True:
        break;
      
      ran = self.handleOption(enemy_option, self.defender, self.attacker);
      self.ui.showSeperator("*");
      
      if self.checkDeath() is True or ran is True:
        break;
      
      self.ui.showSeperator("-");
      self.ui.awaitKey();