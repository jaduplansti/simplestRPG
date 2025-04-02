from player import Player;
from ui import UI;
from combat import CombatHandler;

from multiplayer import MultiplayerHandler;
from menu import Menu;
from random import choices;

class Game:
  def __init__(self):
    self.player = Player("");
    self.ui = UI(self);
    self.menu = Menu(self);
    self.multiplayer_handler = MultiplayerHandler(self);
    
  def handleMainMenu(self):
    while True:
      self.menu.showMainMenu();
      option = self.ui.getInput().lower();
      
      if option == "start":
        self.ui.panelPrint("your name?, theres no menu for name yet lol: ");
        self.player.name = self.ui.getInput();
        self.handleHomeMenu();
      elif option == "quit":
        return;
  
  def handleStatQueryMenu(self, character):
    while True:
      self.menu.showStatsQueryMenu();
      option = self.ui.getInput();
      
      if option == "stats":
        self.menu.showStatsMenu(character);
      elif option == "evaluation":
        self.menu.showStatsEvaluationMenu(character);
      elif option == "rank":
        self.menu.showStatsRankMenu(character);
      elif option == "back":
        return;
        
      self.ui.awaitKey();
      
  def handleHomeMenu(self):
    while True:
      self.menu.showHomeMenu();
      option = self.ui.getInput();
    
      if option == "go outside":
        pass;
      elif option == "you":
        self.handleYouMenu();
      elif option == "practice":
        combat_handler = CombatHandler(self);
        combat_handler.initiateFightNpc(self.player, choices(["slime", "goblin"])[0]);
      elif option == "sleep":
        if self.player.energy >= 75:
          self.ui.animatedPrintFile("sleep", "cant sleep", [self.player.name]);
        else: # optimize this
          self.ui.clear();
          self.ui.barPrint("[blue]sleeping[reset]", self.player.energy, 100, speed = 0.1);
          self.ui.animatedPrintFile("sleep", "rested", [self.player.name]);
          self.ui.panelPrint(f"[bold blue]ENERGY[reset] ([green]+100[reset])");
          self.player.energy = 100;
        self.ui.awaitKey();
        
  def handleYouMenu(self):
    while True:
      self.menu.showYouMenu();
      option = self.ui.getInput();
    
      if option == "items":
        pass;
      elif option == "stats":
        self.handleStatQueryMenu(self.player);
      elif option == "back":
        return;
      self.ui.awaitKey();