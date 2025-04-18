from player import Player;
from ui import UI;
from combat import CombatHandler;

from multiplayer import MultiplayerHandler;
from menu import Menu;
from random import choices;

from os import _exit;
from exploration import Exploration, AREAS;
from audio import AudioPlayer;

class Game:
  """ 
  This class handles the interaction between other classes.
  
  Attributes:
  player, an instance of the Player class.
  ui, an instance of the UI class.
  menu, an instance of the Menu class.
  multiplayer_handler, an instance of a experimental local multiplayer.
  exploration_handler, an instance of the Exploration class.
  audio_handler, an instance of the Audio Handler class.
  areas, a dictionary holding the available areas made in exploration.py.
  settings, a dict holding the type speed, delay speed and audio configs.
  
  Usage:
  game = Game()
  game.handleMainMenu()
  """
 
  def __init__(self):
    self.player = Player("");
    self.ui = UI(self);
    self.menu = Menu(self);
    self.multiplayer_handler = MultiplayerHandler(self);
    self.exploration_handler = Exploration(self);
    self.audio_handler = AudioPlayer(self);
    
    self.areas = {};
    
    self.settings = { 
      "type speed" : 0.01,
      "delay speed" : 0.5,
    }
    
  def getArea(self, name):
    """
    Gets an area from the self.areas
    
    Parameters:
    name, a string holding a name of an area.
    
    Returns:
    area, a dictionary holding information of the current area, see exploration.py.
    """
    
    return self.areas.get(name, None);
    
  def handleMenu(self, options : dict, showFun = None):
    """
    Creates a generic menu to display.
    
    Parameters:
    options, a dictionary holding the possible option that maps to a function.
    showFun, a function pointer that holds the function to display the options.
    """
    
    while True:
      if showFun != None: showFun();
      option = self.ui.getInput();
      if option == "help": self.menu.showTip();
      elif option in options.keys(): options[option]();
      self.ui.awaitKey();
      
  def handleUseItem(self, combat_handler = None):
    """
    Handles item usage by displaying the inventory and getting input.
    
    Parameters:
    combat_handler, an instance of the CombatHandler class.
    """
    
    if len(self.player.inventory) <= 0:
      self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] bag is empty right now, nothing to use.");
      return;
      
    self.menu.showItemsMenu(self.player);
    while True:
      option = self.ui.getInput().lower();
      if self.player.itemExists(option): self.player.getItem(option).use(self, combat_handler);
      elif option == "": break;
  
  def handleUseSkill(self, skill = None, combat_handler = None, attacker = None, defender = None):
    """
    Handles skill usage by displaying skills and getting input.
    
    Parameters:
    skill, a string that contains the name of the skill.
    combat_handler, an instance of the CombatHandler class.
    attacker, an instance of the Character class.
    defender, an instance of the Character class.
    """
    
    if skill is None:
      self.menu.showSkillsMenu(attacker);
      skill = self.ui.getInput();
    
    if attacker.skillExists(skill) is True:
      if attacker.energy >= attacker.skills[skill].energy: attacker.skills[skill].use(combat_handler, attacker, defender);
      else: self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] does not have enough energy to use [green]{skill}[reset]!");
      
  def handleSleep(self):
    """Handles Sleep, increases Player Health and Player Energy and then Saves."""
    
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] sees their bed and gets ready to sleep.");
    self.ui.barPrint("[blue]Energy[reset]", self.player.energy, 100, speed = 0.1);
    self.ui.animatedPrintFile("sleep", "rested", [self.player.name]);
    self.ui.panelPrint(f"[bold blue]ENERGY[reset] & [bold green]HEALTH[reset] RESTORED");

    self.player.energy = 100;
    self.player.stats["health"] = self.player.stats["max health"];
    
    self.ui.showStatus("saving", 2, "line");
    self.player.save();
    
  def handleName(self):
    """Gets character name"""
    
    self.ui.clear();
    self.ui.panelPrint("your name? : ");
    self.player.name = self.ui.getInput();
  
  def handleLoad(self):
    """Tries to load character data, otherwise call handleName."""
    
    try:
      self.ui.showHeader("LOAD DATA", "-");
      plr = Player.load();
      self.ui.animatedPrint(f"[bold yellow]{plr.name}'s[reset] save was found, load data? [italic green](yes/no)[reset]");
      if self.ui.getInput() == "yes": 
        self.ui.showStatus("loading", 2, "line");
        self.player = plr;
      else: self.handleName();
    except FileNotFoundError:
      self.handleName();
  
  def handleStart(self):
    """Initializes the game."""
    
    self.ui.clear();
    self.handleLoad();
    AREAS[self.player.location]["handler"](self).enter();
    
  def handleMainMenu(self):
    """This is self explanatory"""
    
    self.handleMenu({"start" : self.handleStart, "exit" : _exit}, self.menu.showMainMenu);
  
  def initiateFight(self):
    """Initiates a fight using CombatHandler, see combat.py."""
    
    combat_handler = CombatHandler(self);
    combat_handler.initiateFightNpc(self.player, choices(["slime", "goblin"])[0]);
    
  def handleCombatInitiateMenu(self, combat_handler):
    """
    Handles combat initiation usually before the actual combat starts.
    
    Parameters:
    combat_handler, an instance of the CombatHandler class.
    
    Returns:
    boolean, this is to leav the initiation menu.
    """
    
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
    """Handles game settings, see self.settings."""
    
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
    
    elif option == "audio":
      self.ui.normalPrint("enable audio ⤵\n");
      enable = self.ui.getInput();
      
      if enable == "true": self.audio_handler.enabled = True;
      elif enable == "false": self.audio_handler.enabled = False;

