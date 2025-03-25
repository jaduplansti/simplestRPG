from enemy import Enemy, getEnemyByName;
from random import randint, choices, uniform;
from player import Player;

from attack import AttackHandler;

class CombatHandler:
  def __init__(self, attacker, game):
    self.attacker = attacker;
    self.defender = None;
    self.game = game;
    self.ui = game.ui;
    self.attack_handler = AttackHandler(self);
    
  def initiateCombat(self, name):
    self.defender = getEnemyByName(name);
    self.attacker.enemy = self.defender;
    self.defender.enemy = self.attacker; # sets the enemy of the enemy to player
  
  def tryBlockBreak(self, attacker, defender, dmg):
    if dmg >= defender.stats["health"]:
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} was so strong, they broke through {self.ui.coloredString(defender.name, "yellow")}'s defense!");
      self.ui.animatedPrint(f"{self.ui.coloredString(defender.name, "yellow")} couldn't block {self.ui.coloredString(attacker.name, "yellow")}'s attack.");
      return True;
    return False;
  
  def handleAttack(self, attacker, defender):
    self.attack_handler.handleAttack(attacker, defender);
    
  def tryModifyHit(self, attacker, dmg):
    result = choices(["critical", "lucky hit", None], [attacker.stats["luck"], 0.05, 0.5])[0];
    if result == "critical":
      multiplier = round(uniform(1.1, 2), 2);
      self.ui.randomAnimatedPrint(
        [f"{self.ui.coloredString(attacker.name, "yellow")} aims for a weak spot.", f"{self.ui.coloredString(attacker.name, "yellow")} found an opening!"]
      );
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} will now deal a {self.ui.coloredString("CRITICAL HIT!", "red")} {self.ui.coloredString(multiplier, "green")}x damage.");
      return round(dmg * multiplier);
    
    elif result == "lucky hit":
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} is feeling lucky, {self.ui.coloredString("LUCKY HIT!", "cyan")} {self.ui.coloredString("10", "green")}x damage.");
      return dmg * 10;
      
    else:
      return dmg
   
  def tryLevelUpAfterWin(self):
    self.ui.showLevelUp(self.attacker);
  
  def giveLoot(self):
    item = self.defender.getLoot();
    if item != None:
      self.attacker.addItemToInventory(item);
      self.ui.animatedPrint(f"{self.ui.coloredString("you", "yellow")} have obtained {self.ui.coloredString(item.name, "blue")} ({self.ui.rarityPrint(item)})!");
    
  def giveExp(self):
    exp_gain = (self.defender.level * 100) / randint(2, 5);
    self.ui.animatedPrint(f"{self.ui.coloredString("you", "yellow")} gained {self.ui.coloredString(exp_gain, "green")} exp!");
    self.attacker.exp += exp_gain;
    
  def handleDeath(self):
    if self.defender.isDead() is True:
      self.ui.animatedPrint(f"{self.ui.coloredString("you", "yellow")} have killed {self.ui.coloredString(self.defender.name, "yellow")}!");
      self.giveExp();  
      self.tryLevelUpAfterWin();
      self.giveLoot();
    elif self.attacker.isDead() is True:
      self.ui.animatedPrint(f"{self.ui.coloredString(self.defender.name, "yellow")} has killed {self.ui.coloredString("you", "yellow")}!");
      self.attacker.stats["health"] = self.attacker.stats["max health"];
    else:
      return False;
    return True;
  
  def handleFlee(self, attacker, defender):
    random_event = choices(["ran", "grabbed"])[0];
    
    if random_event == "grabbed":
      dmg = attacker.stats["health"] / 2;
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} tried to flee from {self.ui.coloredString(defender.name, "yellow")}, but {self.ui.coloredString(defender.name, "red")} grabbed them!");
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} recieved {self.ui.coloredString(dmg, "red")} dmg!");
      attacker.giveDamage(dmg);
    else:
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} ran away from {self.ui.coloredString(defender.name, "yellow")}!");
    
    return random_event;
  
  def handleOption(self, option, attacker, defender):
    if option == "attack":
      self.handleAttack(attacker, defender);
    elif option == "block":
      attacker.status["blocking"] = True;
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} gets ready to {self.ui.coloredString("block", "red")}!")
    elif option == "inventory" and isinstance(attacker, Player):
      self.game.useInventory();
    elif option == "stats" and isinstance(attacker, Player):
      self.ui.showPlayerStats(attacker);
    elif option == "flee" and attacker.stats["health"] <= (attacker.stats["max health"] * 0.25):
      return self.handleFlee(attacker, defender);
  
  def getOption(self, auto):
    if auto is False:
      return self.ui.getInput();
    else:
      return choices(["attack", "block", "flee"], [0.8, 0.3, 0.1])[0];
      
  def combatLoop(self, auto = False): # optimize and refactor formatting colors
    option = None;
    while True:
      self.ui.showCombatMenu(self.attacker);
      option = self.getOption(auto);
      enemy_option = choices(["attack", "block", "flee"], [self.defender.attack_chance, self.defender.defend_chance, 0.01])[0]; # improve this later
      
      self.ui.clear();
      self.ui.normalPrint("----------------");
      self.ui.normalPrint(" ⚔️ Combat Log ⚔️");
      self.ui.normalPrint("----------------\n");
    
      outcome = self.handleOption(option, self.attacker, self.defender);
      if self.handleDeath() is True or outcome == "ran":
        break;
      outcome = self.handleOption(enemy_option, self.defender, self.attacker);

      if self.handleDeath() is True or outcome == "ran":
        break;
      
      if auto is False:
        self.ui.awaitKey();