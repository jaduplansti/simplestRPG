from random import randint;

#todo: probably add a seperate handleAttack for npcs

class AttackHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
  
  def doBlock(self, attacker, defender, dmg):
    if defender.status["blocking"] is False:
      return;
    elif dmg >= defender.stats["health"]:
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} was so strong, they broke through {self.ui.coloredString(defender.name, "yellow")}'s defense!");
      defender.status["blocking"] = False;
      return;
    
    damage_blocked = max(0, dmg - defender.stats["defense"]);
    self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} tried to hit {self.ui.coloredString(defender.name, "yellow")}, but they blocked and reduced it to {self.ui.coloredString(damage_blocked, "red")} damage!");
    attacker.attackEnemy(damage_blocked)
    defender.status["blocking"] = False;
    
  def handleAttack(self, attacker, defender): # execute predefined combos
    # self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} slipped and recieved {self.ui.coloredString(slip_dmg, "red")} damage!");

    if attacker.status["blocking"] is True:
      self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} dropped their guard!");
      attacker.status["blocking"] = False;
    
    elif attacker.attack_style == "basic":
      combo_preset = randint(1, 2);
      
      if combo_preset == 1:
        punch_dmg = self.combat_handler.tryModifyHit(attacker, 2 + attacker.stats["strength"]);
        self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} threw a normal punch at {self.ui.coloredString(defender.name, "yellow")}, dealt {self.ui.coloredString(punch_dmg, "blue")} dmg!");
        self.doBlock(attacker, defender, punch_dmg);
        
        strong_punch_dmg = self.combat_handler.tryModifyHit(attacker, punch_dmg * 1.2);
        self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} released all their strength at {self.ui.coloredString(defender.name, "yellow")}, dealt {self.ui.coloredString(strong_punch_dmg, "red")} dmg!");
        self.doBlock(attacker, defender, strong_punch_dmg);
   
        attacker.attackEnemy(punch_dmg);
        attacker.attackEnemy(strong_punch_dmg);
      
      elif combo_preset == 2:
        uppercut_dmg = self.combat_handler.tryModifyHit(attacker,  5 + attacker.stats["strength"]);
        self.ui.animatedPrint(f"{self.ui.coloredString(attacker.name, "yellow")} threw a uppercut at {self.ui.coloredString(defender.name, "yellow")}, dealt {self.ui.coloredString(uppercut_dmg, "blue")} dmg!");
        self.doBlock(attacker, defender, uppercut_dmg);
        attacker.attackEnemy(uppercut_dmg);

    