from player import Player;
from ui import UI;
from combat import CombatHandler;

class Game:
  def __init__(self):
    self.player = Player("jaduplansti");
    self.ui = UI(self);
  
  def packEvent(self, value, event):
    return {"value" : value, "event" : event};
    
  def handleMainMenu(self):
    while True:
      self.ui.showMainMenu();
      option = self.ui.getInput().lower();
      
      if option == "start":
        self.handleHomeMenu();
      elif option == "quit":
        return;
  
  def handleStatQueryMenu(self, character):
    while True:
      self.ui.showStatsQueryMenu();
      option = self.ui.getInput();
      
      if option == "stats":
        self.ui.showStatsMenu(character);
      elif option == "evaluation":
        self.ui.showStatsEvaluationMenu(character);
      elif option == "rank":
        self.ui.showStatsRankMenu(character);
      elif option == "back":
        return;
        
      self.ui.awaitKey();
      
  def handleHomeMenu(self):
    while True:
      self.ui.showHomeMenu();
      option = self.ui.getInput();
    
      if option == "go outside":
        pass;
      elif option == "stats":
        self.handleStatQueryMenu(self.player);
      elif option == "practice":
        combat_handler = CombatHandler(self);
        combat_handler.initiateFightNpc(self.player, "slime");
      