from player import Player;
from ui import UI;
from combat import CombatHandler;

from multiplayer import MultiplayerHandler;
from menu import Menu;
from random import choices;

from os import _exit;
#todo refactor game class, improve ui class

class Game:
  def __init__(self):
    self.player = Player("");
    self.ui = UI(self);
    self.menu = Menu(self);
    self.multiplayer_handler = MultiplayerHandler(self);
    
    self.settings = { 
      "type speed" : 0.01,
      "delay speed" : 0.5,
    }
   
  def handleMenu(self, options : dict, showFun = None):
    while True:
      if showFun != None: showFun();
      option = self.ui.getInput();
      if option in options.keys():
        options[option]();
      self.ui.awaitKey();
      
  def handleUseItem(self, combat_handler = None):
    if len(self.player.inventory) <= 0:
      self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] bag is empty right now, nothing to use.");
      return;
      
    self.menu.showItemsMenu(self.player);
    while True:
      option = self.ui.getInput().lower();
      if self.player.itemExists(option):
        self.player.getItem(option).use(self, combat_handler);
      elif option == "":
        break;
  
  def handleUseSkill(self, skill = None, combat_handler = None, attacker = None, defender = None):
    if skill is None:
      self.menu.showSkillsMenu(attacker);
      skill = self.ui.getInput();
    
    if attacker.skillExists(skill) is True:
      if attacker.energy >= attacker.skills[skill].energy: attacker.skills[skill].use(combat_handler, attacker, defender);
      else: self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] does not have enough energy to use [green]{skill}[reset]!");
      
  def handleSleep(self):
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] sees their bed and gets ready to sleep.");
    self.ui.barPrint("[blue]Energy[reset]", self.player.energy, 100, speed = 0.1);
    self.ui.animatedPrintFile("sleep", "rested", [self.player.name]);
    self.ui.panelPrint(f"[bold blue]ENERGY[reset] & [bold green]HEALTH[reset] RESTORED");

    self.player.energy = 100;
    self.player.stats["health"] = self.player.stats["max health"];
    
    self.ui.showStatus("saving", 2);
    self.player.save();
    
  def handleName(self):
    self.ui.clear();
    self.ui.panelPrint("your name? : ");
    self.player.name = self.ui.getInput();
  
  def handleLoad(self):
    try:
      plr = Player.load();
      self.ui.animatedPrint(f"[bold yellow]{plr.name}'s[reset] save was found, load data? [italic green](yes/no)[reset]");
      if self.ui.getInput() == "yes": 
        self.ui.showStatus("loading", 2);
        self.player = plr;
      else: self.handleName();
    except FileNotFoundError:
      self.handleName();
      
  def handleMainMenu(self):
    self.handleMenu({"start" : self.handleHomeMenu, "exit" : _exit}, self.menu.showMainMenu);
  
  def handleHomeMenu(self):
    self.handleLoad();
    self.handleMenu(
      {
       "items" : self.handleUseItem, 
       "stats" : lambda: self.menu.showStatsMenu(self.player),
       "practice" : self.initiateFight,
       "sleep" : self.handleSleep,
       "settings" : self.handleSettings,
      }, 
      self.menu.showHomeMenu
    );
  
  def initiateFight(self):
    combat_handler = CombatHandler(self);
    combat_handler.initiateFightNpc(self.player, choices(["slime", "goblin"])[0]);
    
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
      
  def handleSettings(self):
    self.menu.showSettingsMenu();
    option = self.ui.getInput();
    
    if option == "type speed" or option == "ts":
      self.ui.normalPrint("set type speed ⤵\n");
      try:
        self.settings["type speed"] = int(self.ui.getInput());
      except ValueError:
        self.ui.normalPrint("type speed must be integers ⤴\n");
    
    elif option == "delay speed" or option == "ds":
      self.ui.normalPrint("set delay speed ⤵\n");
      try:
        self.settings["delay speed"] = int(self.ui.getInput());
      except ValueError:
        self.ui.normalPrint("delay speed must be integers ⤴\n");
    
