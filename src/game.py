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
from skill import getSkill, Skill;
from enemy import ENEMIES;
import sys;

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
      if option.isdigit(): option = list(options)[int(option)];
      if option == "help": self.menu.showTip();
      elif option == "quit": self.handleQuit();
      elif option in options.keys(): options[option]();
      self.ui.awaitKey();
  
  def handleQuit(self):
    """Handles quitting, stops audio player and enables echoing."""
    self.ui.enableEcho();
    os._exit(0);
  
  def handleQuest(self):
    self.ui.clear();
    self.menu.showQuestMenu(self.player);
    
  def handleEquipment(self):
    while True:
      self.ui.clear();
      self.menu.showEquipmentMenu(self.player);
      option = self.ui.getInput();
      
      try:
        if option == "close": return;
        if not self.player.isOccupied(option): self.ui.animatedPrint("[red]thats an empty slot..[reset]");
        else: 
          if self.player.unequipItem(option, self) != -1: 
            self.ui.panelPrint(f"[bold cyan]UNEQUIPPED[reset]", "center", option, "purple");
          else: self.ui.panelPrint(f"[bold res] UNEQUIP FAILED[reset]", "center", option, "red");
      except KeyError as e:
        self.ui.animatedPrint(f"[bold red]{option} is not a bodypart[reset]");
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
   
    while True:
      self.ui.clear();   
      self.menu.showItemsMenu(self.player);
      option = self.ui.getInput().lower().split(",");
      count = 1;
      
      try:
        if len(option) > 1: count = int(option[1]);
      except ValueError:
        self.ui.normalPrint("[red bold]the amount must be an integer e.g wooden sword, 2[reset]\n");
        self.ui.awaitKey();
        continue;
        
      for _ in range(0, count):
        if self.player.itemExists(option[0]): self.player.getItem(option[0]).use(self, self.player, combat_handler);
        elif option[0] == "close": 
          return;
        else: 
          self.ui.normalPrint(f"[red underline]{self.player.name} does not have {option[0]}[reset]\n");
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
      if attacker.skills[skill].passive is True: self.ui.animatedPrint("[bold red]cannot use passive skills![reset]");
      elif attacker.energy >= attacker.skills[skill].energy: attacker.skills[skill].use(combat_handler, attacker, defender);
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
    
  def handleName(self, name = None):
    """Gets character name"""
    self.ui.clear();
    if name == None:
      self.ui.panelPrint("your name? : ");
      self.player.name = self.ui.getInput();
    else:
      self.player.name = name;
      
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
    enemy = "";
    if self.player.level in range(1, 6): enemy = choices(["slime", "goblin"])[0];
    elif self.player.level in range(6, 9): enemy = choices(["orc", "skeleton"])[0];
    elif self.player.level in range(9, 13): enemy = choices(["elf", "bandit"])[0];
    else: enemy = choices(["fallen knight", "priest"])[0];

    combat_handler = CombatHandler(self);
    combat_handler.initiateFightNpc(self.player, enemy);
    
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
        self.settings["type speed"] = float(self.ui.getInput());
      except ValueError:
        self.ui.normalPrint("type speed must be decimal/float ⤴\n");
    
    elif option == "delay speed" or option == "ds":
      self.ui.normalPrint("set delay speed ⤵\n");
      try:
        self.settings["delay speed"] = float(self.ui.getInput());
      except ValueError:
        self.ui.normalPrint("delay speed must be decimal/float ⤴\n");
    
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
    
    if os.path.exists(sys.path[0] + "/saves") != True:
      self.handleName();
      return;
     
    player_data = {};
    for save in os.listdir("saves"):
      self.ui.showStatus("fetching", 0.5);
      plr = Player(None).load(save.replace(".save", ""));
      player_data.update({plr.name : plr});
      self.ui.panelPrint(f"level {plr.level} ({plr.exp}/{plr.level * 100})", title = f"{plr.name} ({plr.attack_style})", alignment = "center");
    
    self.ui.animatedPrint("[underline green]pick a character to load, enter a new name to create![reset]")
    option = self.ui.getInput();
    
    if option not in player_data:
      self.ui.animatedPrint(f"character {option} does not exist!");
      self.ui.animatedPrint(f"create {option}? (y/n)");
      if self.ui.getInput().lower() == "y":
        self.handleName(option);
        return;
      else:
        self.handleQuit();
   
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
      self.ui.panelPrint(f"[bold yellow]{name}[reset]\n{self.player.quests[name]["obj"].desc}", "center", title = "QUEST RECEIVED");
    else: return -1;
    
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
    if self.player.addItemToInventory(item, amount) != -1: self.ui.animatedPrint(f"Acquired [bold yellow]{item.name}[reset] ([green]{item.rarity}[reset]) {amount}x");
    else: self.ui.animatedPrint(f"No space left for [bold yellow]{item.name}[reset]");
    
  def giveSkill(self, char, name):
    if name in char.skills: return;
    skill = getSkill(name);
    char.addSkill(skill);
    if isinstance(char, Player): self.ui.panelPrint(f"[bold yellow]{skill.name}[reset] ([magenta]{skill.rank}[reset])\n[underline]{skill.desc}, consumes {skill.energy} energy[reset]", "center", "Learned");
  
  def handleStatsMenu(self):
    while True:
      self.ui.clear()
      self.menu.showStatsMenu(self.player)

      if self.player.points > 0:
        self.ui.normalPrint("[yellow]hint[reset]: type strength, 2 to allocate points to strength\n") 
        option = self.ui.getInput().split(",")
        
        try:
          if len(option) != 2:
            raise ValueError("Invalid input format. Use: stat, amount")

          stat = option[0].strip()
          amount = int(option[1].strip())
          
          if stat not in self.player.stats:
            raise KeyError(f"'{stat}' is not a valid stat")
          
          if stat == "luck":
            raise ValueError("Luck cannot be increased");
          
          if amount <= 0 or amount > self.player.points:
            raise ValueError("Invalid amount")
            
          self.player.stats[stat] += amount
          self.player.points -= amount
          
        except Exception as e: self.ui.panelPrint(str(e), "center", "system", "red")
        self.ui.awaitKey()
      else: break;
 
  def giveStatus(self, status, n):
    CombatHandler(self).attack_handler.status_handler.afflict(self.player, status, n);
  
  def isPlayer(self, char):
    return isinstance(char, Player);
 
  def giveStyle(self, char, style, announce = True):
    char.attack_style = style;
    if announce is True: self.ui.animatedPrint(f"[yellow]{char.name}[reset] switched to [bold magenta]{style}[reset] style!");
    if style == "swordsman": 
      self.giveSkill(char, "parry");
      self.giveSkill(char, "hyper precision");
      self.giveSkill(char, "flowing blade");
      self.giveSkill(char, "trislash");
    elif style == "archer": 
      self.giveSkill(char, "arrow return");
      self.giveSkill(char, "arrow rain");
      self.giveSkill(char, "bow bash");
    elif style == "cleric":
      self.giveSkill(char, "divine protection");
      self.giveSkill(char, "blunt recovery");
      self.giveSkill(char, "status wipe");
      self.giveSkill(char, "divine restriction");

  def removeStyle(self, char):
    if char.attack_style == "swordsman": 
      char.removeSkill("parry");
      char.removeSkill("hyper precision");
      char.removeSkill("flowing blade");
      char.removeSkill("trislash");
    elif char.attack_style == "archer": 
      char.removeSkill("arrow return");
      char.removeSkill("arrow rain");
      char.removeSkill("bow bash");
    elif style == "cleric":
      self.removeSkill(char, "divine protection");
      self.removeSkill(char, "blunt recovery");
      self.removeSkill(char, "status wipe");
      self.removeSkill(char, "divine restriction");

    char.attack_style = "basic";
