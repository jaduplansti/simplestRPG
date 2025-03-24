from ui import UI;
from player import Player;
from combat import CombatHandler;

from exploration import MoveMenuHandler;
from random import choices;

class Game:
  def __init__(self):
    self.ui = UI();
    self.player = Player("kevin");
    
  def mainMenu(self):
    while True:
      self.ui.showMainMenu();
      option = self.ui.getInput().lower();
      
      if option == "start":
        #self.characterCreation();
        self.homeMenu();
      elif option == "exit":
        return;
        
  def characterCreation(self):
    self.ui.showCharacterCreationTitle();
    self.ui.showDialogue("???", "What is your name hero?");
    name = self.ui.getInput();
    
    self.ui.showDialogue("???", f"So you are {self.ui.coloredString(name, "yellow")}-sama....");
    self.ui.showDialogue("???", "Ummm. i think its a pretty cute name hehe.");
    self.ui.showDialogue("???", f"Im {self.ui.coloredString("hestia", "yellow")}, the goddess of reincarnation.");
    self.ui.showDialogue("hestia", "Anyways, how are you feeling?");
    
    _ = self.ui.dynamicDialogue({
      "like shit" : "[hestia] : Oh.... dont worry! im sure you'll get used it.",
      "good" : f"[hestia] : Thats Great {self.ui.coloredString(name, "yellow")}!",
    });
    
    self.player = Player(name);
    self.ui.showDialogue("hestia", "Uhm im going to display your stats now if you dont mind.");
    self.ui.showPlayerStats(self.player);
    
    self.ui.showDialogue("hestia", "Not bad right?!");
    _ = self.ui.dynamicDialogue({
      "what the fuck" : f"[hestia] : {self.ui.coloredString("Calm Down!", "red")} also it cant be that bad right.",
      "looks good to me" : f"[hestia] : Yayy, im glad you liked your stats.",
    });
    self.ui.showDialogue("hestia", "Unfortunately i dont have the powers to change your stats");
    
  def homeMenu(self):
    while True:
      self.ui.showHomeMenu();
      option = self.ui.getInput();
      
      if option == "move":
        self.goTravel();
      elif option == "inventory":
        self.ui.showInventory(self.player);
      elif option == "stats":
        self.ui.showPlayerStats(self.player);
      elif option == "train":
        self.initiateCombat(choices(["slime", "skeleton", "goblin"])[0]);
      elif option == "exit":
        return;
        
      self.ui.awaitKey();
  
  def goTravel(self):
    move_handler = MoveMenuHandler(self);
    move_handler.homeTravelMenu();
    
  def initiateCombat(self, name):
    combat_handler = CombatHandler(self.player, self);
    combat_handler.initiateCombat(name);
    
    self.ui.compareStats(combat_handler.attacker, combat_handler.defender);
    self.ui.awaitKey();
    
    combat_handler.combatLoop(auto = True);
    