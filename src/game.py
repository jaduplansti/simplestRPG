from player import Player;
from ui import UI;
from combat import CombatHandler;

from menu import Menu;
from random import choices;
import os;

from exploration import Exploration, AREAS;
from time import sleep;
from subprocess import run;

from item import getItem;
from skill import getSkill;

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
    self.exploration_handler = Exploration(self);
    
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
      elif option == "quit": self.handleQuit();
      elif option in options.keys(): options[option]();
      self.ui.awaitKey();
  
  def handleConfiguration(self):
    while self.ui.validScreenSize() is False:
      self.ui.clear();
      self.ui.normalPrint(f"[yellow]zoom in your terminal around 20-40 (current width {self.ui.console.width})[reset]\n");
      self.ui.normalPrint(f"[green]you can zoom in by (pinching in) or (ctrl +)[reset]\n");
      sleep(2);
   
  def handleQuit(self):
    """Handles quitting, stops audio player and enables echoing."""
    self.ui.enableEcho();
    os._exit(0);
    
  def handleUseItem(self, combat_handler = None):
    """
    Handles item usage by displaying the inventory and getting input.
    
    Parameters:
    combat_handler, an instance of the CombatHandler class.
    """
    
    if len(self.player.inventory) <= 0:
      self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] bag is empty right now, nothing to use.");
      return;
   
    while True:
      self.ui.clear();   
      self.menu.showItemsMenu(self.player);
      option = self.ui.getInput().lower().split(",");
      count = 1;
      
      try:
        if len(option) > 1: count = int(option[1]);
      except ValueError:
        self.ui.normalPrint("[red bold]the amount must be an integer e.g wooden sword, 2[reset]\n");
      
      for _ in range(0, count):
        if self.player.itemExists(option[0]): self.player.getItem(option[0]).use(self, combat_handler);
        elif option[0] == "close": 
          return;
        else: 
          self.ui.normalPrint(f"[red underline]{self.player.name} does not have {option[0]}[reset]\n");
          self.ui.awaitKey();
          break;
      self.ui.awaitKey();
      
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
    
    self.handleSave();
    
  def handleName(self):
    """Gets character name"""
    
    self.ui.clear();
    self.ui.panelPrint("your name? : ");
    self.player.name = self.ui.getInput();
  
  def handleStart(self):
    """Initializes the game."""
 
    self.ui.clear();
    self.handleLoad();
    AREAS[self.player.location]["handler"](self).enter();
    
  def handleMainMenu(self):
    """This is self explanatory"""
    self.handleMenu({"start" : self.handleStart, "quit" : self.handleQuit}, self.menu.showMainMenu);
  
  def initiateFight(self):
    """Initiates a fight using CombatHandler, see combat.py."""
    
    combat_handler = CombatHandler(self);
    combat_handler.initiateFightNpc(self.player, choices(["goblin"])[0]);
    
  def handleCombatInitiateMenu(self, combat_handler):
    """
    Handles combat initiation usually before the actual combat starts.
    
    Parameters:
    combat_handler, an instance of the CombatHandler class.
    
    Returns:
    boolean, this is to leave the initiation menu.
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
  
  def doUpdate(self):
    """Handles updates using git fetch"""
    
    self.ui.console.log("checking for updates!");
    try:
      run(["git", "fetch"], check = True);
      result = run(["git", "status"], check = True, text = True, capture_output = True);
        
      if "behind" in result.stdout:
        self.ui.console.log("found latest version!");
        run(["git", "pull"]);
        self.ui.console.log("update complete!");
        self.handleQuit();
    except FileNotFoundError:
      self.ui.console.log("git is not installed!");
      return;
    except Exception:
      return;
      
  def handleLoad(self):
    """Handles load files in /saves"""
    
    self.ui.clear();
    self.ui.showHeader("Save Slots", "#");
    
    if os.path.exists("saves") != True:
      self.handleName();
      return;
    
    player_data = {};
    for save in os.listdir("saves"):
      self.ui.showStatus("fetching", 0.5);
      plr = Player(None).load(save.replace(".save", ""));
      player_data.update({plr.name : plr});
      self.ui.panelPrint(f"level {plr.level} ({plr.exp}/{plr.level * 100})", title = plr.name, alignment = "center");
    
    self.ui.animatedPrint("[underline green]pick a character to load, leave it blank to ignore![reset]")
    option = self.ui.getInput();
    
    if option not in player_data:
      self.ui.animatedPrint(f"character {option} does not exist!");
      self.handleName();
      return;
   
    try:
      self.ui.showStatus("loading", 2);
      self.player = player_data[option]
    except KeyError:
      self.handleLoad();
        
  def handleSave(self):
    """saves the current game.player to /saves/{name}.save"""
    
    if os.path.exists("saves") != True:
      os.mkdir("saves");
    
    if os.path.isfile(f"saves/{self.player.name}.save"):
      self.ui.animatedPrint(f"[yellow]save for {self.player.name} already exists!, overwrite? (yes/no)[reset]");
      if self.ui.getInput().lower() != "yes":
        return;
    
    self.ui.showStatus("saving", 2);
    self.player.save();
   
  def giveQuest(self, name):
    if self.player.giveQuest(name) != -1:
      self.ui.normalPrint(f"Quest {name} accepted!");
      
  def givePlayerExp(self, exp):
    self.player.exp += exp;
  
  def handlePlayerLevelUp(self):
    old_level = self.player.level;
    if self.player.tryLevelUp() is True:
      self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] feels a surge of [blue]power[reset], [yellow]{self.player.name}[reset], leveled up!");
      self.ui.panelPrint(f"level [yellow]{old_level}[reset] -> [green]{self.player.level}[reset]");
  
  def isTermux(self):
    return "PREFIX" in os.environ and "/data/data/com.termux/files/usr" in os.environ["PREFIX"];
 
  def givePlayerItem(self, name, amount = 1):
   item = getItem(name);
   self.player.addItemToInventory(item, amount);
   self.ui.animatedPrint(f"Acquired [bold yellow]{item.name}[reset] ([green]{item.rarity})[reset] {amount}x");
 
  def givePlayerSkill(self, name):
   skill = getSkill(name);
   self.player.addSkill(skill);
   self.ui.panelPrint(f"[bold yellow]{skill.name}[reset] ([magenta]{skill.rank}[reset])\n[underline]{skill.desc}, consumes {skill.energy} energy[reset]", "center", "Learned");
