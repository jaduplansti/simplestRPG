from random import choices;
from enemy import Enemy;

class CombatEventHandler:
  def __init__(self, combat_handler):
    self.combat_handler = combat_handler;
    self.ui = self.combat_handler.ui;
  
  def pickEvent(self, events, odds = None):
    if odds is None:
      return choices(events)[0];
    else:
      return choices(events, odds)[0];
      
  def handleEvent(self, attacker, defender, event):
    if isinstance(attacker, Enemy):
      return;
      
    if event == "basic_normal_event":
      self.ui.printTreeMenu("combo", ["chain hit", "block"]);
      option = self.ui.getInput();
      
      if option == "chain hit":
        self.ui.panelAnimatedPrint(f"{attacker.name} followed up with chain hit!", "combo");
        self.combat_handler.attack_handler.handleAttack(attacker, defender);
      elif option == "block":
        self.ui.panelAnimatedPrintFile("block", "blocking", [attacker.name, defender.name], "block");
        self.combat_handler.attack_handler.defense_handler.handleBlock(attacker, defender);
      else:
        pass;
      
    