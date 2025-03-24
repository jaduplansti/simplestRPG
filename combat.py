from enemy import Enemy, getEnemyByName;
from random import randint, choices, uniform;

class CombatHandler:
  def __init__(self, attacker, game):
    self.attacker = attacker;
    self.defender = None;
    self.game = game;
    self.ui = game.ui;
    
  def initiateCombat(self, name):
    self.defender = getEnemyByName(name);
    self.attacker.enemy = self.defender;
    self.defender.enemy = self.attacker; # sets the enemy of the enemy to player
  
  def tryBlockBreak(self, attacker, defender, dmg):
    if dmg >= defender.stats["health"]:
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} was so strong, they broke through {self.ui.coloredString(defender.name, "yellow")}'s defense!");
      self.ui.animatedPrint(f"{self.ui.coloredString(defender.name, "yellow")} couldn't block {self.ui.coloredString(attacker.name, "yellow")} attack.");
      return True;
    return False;
    
  def handleAttack(self, attacker, defender, dmg, hit_msg, block_msg):
    random_event = choices([None, "slipped"], [0.8, 0.2])[0];
    
    if attacker.status["blocking"] is True:
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} dropped their block!");
      attacker.status["blocking"] = False;

    elif defender.status["blocking"] is True and self.tryBlockBreak(attacker, defender, dmg) is False:
      self.ui.animatedPrint(block_msg);
      attacker.attackEnemy(max(0, dmg - defender.stats["defense"]));
      defender.status["blocking"] = False;
    
    elif random_event == "slipped":
      slip_dmg = attacker.stats["strength"] / randint(3, 5);
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} slipped and recieved {self.ui.coloredString(slip_dmg, "red")} damage!");
    
    else:
      attacker.attackEnemy(dmg);
      self.ui.animatedPrint(hit_msg);
  
  def tryCriticalHit(self, attacker, dmg):
    result = choices(["critical", None], [attacker.stats["luck"], 0.5])[0];
    if result == "critical":
      multiplier = round(uniform(1.1, 2), 2);
      self.ui.randomAnimatedPrint(
        [f"{self.ui.coloredString(attacker.name, "yellow")} aims for a weak spot.", f"{self.ui.coloredString(attacker.name, "yellow")} found a opening!"]
      );
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} will now deal a {self.ui.coloredString("CRITICAL HIT!", "red")} {self.ui.coloredString(multiplier, "green")}x damage.");
      return round(dmg * multiplier);
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
    else:
      return False;
    return True;
    
  def combatLoop(self, auto = False): # optimize and refactor formatting colors
    option = None;
    while True:
      self.ui.showCombatMenu(self.attacker);
      if auto is False:
        option = self.ui.getInput();
      else:
        option = choices(["attack", "defend"], [0.8, 0.3])[0];
      enemy_option = choices(["attack", "defend"], [self.defender.attack_chance, self.defender.defend_chance])[0]; # improve this later
      
      #==========#
      
      if option == "attack":
        dmg = self.tryCriticalHit(self.attacker, self.attacker.stats["strength"]);
        self.handleAttack(
          self.attacker, 
          self.defender,
          dmg,
          f"{self.ui.coloredString("you", "yellow")} hit {self.ui.coloredString(self.defender.name, "yellow")} and dealt {self.ui.coloredString(dmg, "red")} damage!",
          f"{self.ui.coloredString("you", "yellow")} tried to hit {self.ui.coloredString(self.defender.name, "yellow")}, but they blocked and reduced it to {self.ui.coloredString(max(0, dmg - self.defender.stats["defense"]), "red")} damage!",
        );
      elif option == "defend":
        self.attacker.status["blocking"] = True;
        self.ui.animatedPrint(f"{self.ui.coloredString("you", "yellow")} put your arms up to {self.ui.coloredString("block", "red")}.");
      elif option == "stats":
        self.ui.showPlayerStats(self.attacker);
      #==========# 
      
      if self.handleDeath() is True:
        break;
        
      if enemy_option == "attack":
        dmg = self.tryCriticalHit(self.defender, self.defender.stats["strength"]);
        self.handleAttack(
          self.defender, 
          self.attacker, 
          dmg,
          f"{self.ui.coloredString(self.defender.name, "yellow")} hit {self.ui.coloredString("you", "yellow")} and dealt {self.ui.coloredString(dmg, "red")} damage!",
          f"{self.ui.coloredString(self.defender.name, "yellow")} tried to hit {self.ui.coloredString("you", "yellow")} but {self.ui.coloredString("you", "yellow")} blocked and reduced it to {self.ui.coloredString(max(0, dmg - self.defender.stats["defense"]), "red")} damage!",
        );
      elif enemy_option == "defend":
        self.defender.status["blocking"] = True;
        self.ui.animatedPrint(f"{self.ui.coloredString(self.defender.name, "yellow")} gets ready to {self.ui.coloredString("block", "red")}.");
      
      #==========# 
      
      if self.handleDeath() is True:
        break;
      
      if auto is False:
        self.ui.awaitKey();
