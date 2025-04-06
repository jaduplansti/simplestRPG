from player import Player;
from ui import UI;
from combat import CombatHandler;

from multiplayer import MultiplayerHandler;
from menu import Menu;
from random import choices;

tutorial = True;

class Game:
  def __init__(self):
    self.player = Player("");
    self.ui = UI(self);
    self.menu = Menu(self);
    self.multiplayer_handler = MultiplayerHandler(self);
  
  def handleUseItem(self):
    if len(self.player.inventory) <= 0:
      self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] bag is empty right now, nothing to use.");
      return;
      
    self.menu.showItemsMenu(self.player);
    option = self.ui.getInput().lower();
    
    if self.player.itemExists(option):
      self.player.getItem(option).use(self);
      
  def handleSleep(self):
    if self.player.energy >= 75:
      self.ui.animatedPrintFile("sleep", "cant sleep", [self.player.name]);
      return;
      
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] sees their bed and gets ready to sleep.");
    self.ui.barPrint("[blue]Energy[reset]", self.player.energy, 100, speed = 0.1);
    self.ui.animatedPrintFile("sleep", "rested", [self.player.name]);
    self.ui.panelPrint(f"[bold blue]ENERGY[reset] ([green]+100[reset])");
    self.player.energy = 100;
  
  def handleName(self):
    self.ui.clear();
    self.ui.panelPrint("your name? : ");
    self.player.name = self.ui.getInput();

  def handleMainMenu(self):
    self.handleName();
    while True:
      self.menu.showMainMenu();
      option = self.ui.getInput().lower();
      
      if option == "start":
        self.handleHomeMenu();
      elif option == "quit":
        return;
  
  def handleHomeMenu(self):
    while True:
      self.menu.showHomeMenu();
      option = self.ui.getInput();
    
      if option == "items":
        self.handleUseItem();
      elif option == "stats":
        self.menu.showStatsMenu(self.player);
      elif option == "practice":
        global tutorial;
        if tutorial is False:
          self.handleCombatTutorial();
          tutorial = True;
        combat_handler = CombatHandler(self);
        combat_handler.initiateFightNpc(self.player, choices(["slime", "skeleton", "goblin", "clone", "deity"])[0]);
        continue;
      elif option == "sleep":
        self.handleSleep();
      elif option == "ascend": # for testing purposes
        self.ui.animatedPrint("this will take a few seconds, please wait as you break the limits...");
        self.player.exp = 999999 * 999999;
        self.player.tryLevelUp();
      self.ui.awaitKey();
        
  def handleCombatInitiateMenu(self, combat_handler):
    while True:
      self.menu.showCombatInitiateMenu();
      option = self.ui.getInput();
      
      if option == "fight":
       return combat_handler.handleCombatNpc();
      elif option == "bail":
        break;
      elif option == "talk":
        pass;
      
      self.ui.awaitKey();
      
  def handleCombatTutorial(self):
    self.ui.clear();
    self.ui.animatedPrint(f"[green]{self.player.name}[reset] in [underline]simplestRPG[reset] there are 4 main actions.");
    self.ui.animatedPrint("these are [yellow]attack[reset], [blue]block[reset], [purple]taunt[reset], [red]flee[reset].");
    self.ui.animatedPrint("[yellow]attack[reset] deals damage to enemies and may vary depending on the player class and attack style.");
    
    self.ui.animatedPrint("attacks are automatically reduced by enemy defense, however if the opponents defense is too high.");
    self.ui.panelAnimatedPrintFile("damage handler", "no damage", ["joe", "kevin"], "reduced dmg");
    self.ui.animatedPrint("attacks may also ignore enemy defense.");
    self.ui.panelAnimatedPrintFile("damage handler", "defense ignored", ["joe", "kevin"], "no dmg");
    
    self.ui.awaitKey();
    self.ui.clear();
    self.ui.animatedPrint("[blue]block[reset] completely nullifies the damage incoming, which only applies to physical attacks.");
    self.ui.animatedPrint("blocking is useful especially for strategies.");
    
    self.ui.panelAnimatedPrintFile("block", "blocking", ["joe", "kevin"], "blocking");
    self.ui.panelAnimatedPrintFile("block", "blocking", ["joe", "kevin"], "blocking");
    self.ui.panelAnimatedPrintFile("basic style", "strong punch", ["kevin", "joe", 0], "blocked");
    self.ui.animatedPrint("as you can see the damage has been zeroed.");
   
    self.ui.awaitKey();
    self.ui.clear();
    self.ui.animatedPrint("[purple]taunt[reset] is a strategic move to reduce opponents stats.");
    self.ui.animatedPrint("taunting will get buffed soon.");
    
    self.ui.panelAnimatedPrintFile("taunt", "debuff", ["joe", "kevin"], "taunt");
    self.ui.awaitKey();
    self.ui.clear();
    self.ui.animatedPrint("[red]flee[reset] is a viable option, npcs tend to spam this move especially when their below 25% health.");
    
    self.ui.awaitKey();
    self.ui.clear();

