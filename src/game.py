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
  
  def handleSleep(self):
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] sees their bed and gets ready to sleep.");
    self.ui.barPrint("[blue]Energy[reset]", self.player.energy, 100, speed = 0.1);
    self.ui.animatedPrintFile("sleep", "rested", [self.player.name]);
    self.ui.panelPrint(f"[bold blue]ENERGY[reset] ([green]+100[reset])");
    self.player.energy = 100;
    
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
  
  def handleHomeMenu(self):
    while True:
      self.menu.showHomeMenu();
      option = self.ui.getInput();
    
      if option == "go outside":
        pass;
      elif option == "stats":
        self.menu.showStatsMenu(self.player);
      elif option == "practice":
        combat_handler = CombatHandler(self);
        combat_handler.initiateFightNpc(self.player, choices(["slime", "goblin"])[0]);
        continue;
      elif option == "sleep":
        if self.player.energy >= 75:
          self.ui.animatedPrintFile("sleep", "cant sleep", [self.player.name]);
        else: 
          self.handleSleep();
      self.ui.awaitKey();
        
  def handleCombatInitiateMenu(self, combat_handler):
    while True:
      self.menu.showCombatInitiateMenu();
      option = self.ui.getInput();
      
      if option == "fight":
        combat_handler.handleCombatNpc();
        return;
      elif option == "bail":
        pass;
      elif option == "talk":
        pass;
      
      self.ui.awaitKey();
        