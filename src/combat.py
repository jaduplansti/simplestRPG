from enemy import Enemy, getEnemyByName;
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
    enemy = getEnemyByName(name, character);
    self.attacker = character
    self.attacker.enemy = enemy;
    
    self.defender = enemy;
    self.defender.enemy = self.attacker;
    self.attacker.status["blocking"] = False; # temporary fix
    
    self.game.handleCombatInitiateMenu(self);
  
  def __handleWin(self):
    if self.tryBerserkNpc(self.defender) is False:
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
    if item != None:
      won.addItemToInventory(item);
      self.ui.animatedPrint(f"[bold yellow]{won.name}[reset] acquired a [underline cyan]{item.name}[reset]!");
      
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
    
    self.ui.panelPrint(f"([blue]-{attacker.getFatigueMultiplier() * 100}%[reset]) stat output.");
  
  def tryBerserkNpc(self, npc):
    if randint(1, 8) == randint(1, 8) and npc.berserk is False:
      self.ui.animatedPrint(f"a mysterious aura covers [red]{npc.name}[reset]");
      self.ui.animatedPrint(f"[yellow]{npc.name}[reset] goes [red]Berserk[reset]!");
      self.ui.panelPrint("[blue]ALL STATS[reset] [green](x1.5)[reset]");
      npc.goBerserk();
      return True;
    return False;
    
  def checkDeath(self):
    if self.attacker.stats["health"] <= 0:
      self.ui.animatedPrint(f"[yellow]{self.defender.name}[reset] killed [yellow]{self.attacker.name}[reset]");
    elif self.defender.stats["health"] <= 0:
      self.ui.animatedPrint(f"[yellow]{self.attacker.name}[reset] killed [yellow]{self.defender.name}[reset]");
      won = self.__handleWin();
      if won is False: return False;
    else:
      return False;
      
    self.ui.awaitKey();
    return True;
   
  def handleOption(self, option, attacker, defender):
    self.ui.showStatus("processing move", 1);
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
    elif option == "items":
      self.game.handleUseItem(self);
    else:
      self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] did nothing.");
    
    attacker.deductEnergy();
  
  def handleCombatNpc(self, auto = False):
    while True:
      self.menu.showCombatMenu(self, self.attacker);
      option = self.ui.getInput();
      enemy_option = choices(["attack", "block", "flee", "taunt"], [self.defender.attack_chance, self.defender.block_chance, self.defender.flee_chance, self.defender.taunt_chance])[0];
      
      self.ui.clear();
      self.ui.showHeader("Combat Logs", "=");
      self.ui.showSeperator("-");
      
      ran = self.handleOption(option, self.attacker, self.defender);
      self.ui.showSeperator("-");

      if self.checkDeath() is True or ran is True:
        break;
      
      ran = self.handleOption(enemy_option, self.defender, self.attacker);
      self.ui.showSeperator("*");
      
      if isinstance(self.defender, Enemy):
        if self.defender.berserk is True: self.defender.giveDamage(self.defender.stats["max health"] * 0.2)
        
      if self.checkDeath() is True or ran is True:
        break;
      
      self.ui.showSeperator("-");
      self.ui.awaitKey();