from player import Player;
from ui import UI;
from combat import CombatHandler;

from menu import Menu;
from random import choices;
import os;

from exploration import Exploration, AREAS;
from time import sleep;
from subprocess import run;

from item import getItem, ITEMS;
from skill import getSkill, Skill, SKILLS;
from enemy import ENEMIES;

from audio import AudioHandler;
import sys;

from copy import deepcopy;
from animation import Animator;

class Tutorial:
  """This class handles the tutorial"""
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    self.player = game.player;
  
  def askSkip(self):
    self.ui.animatedPrint("skip tutorial? ([cyan]y[reset]/[red]n[reset])");
    if self.ui.getInput() == "y": return True;
    
  def start(self):
    if self.askSkip(): return;
    self.ui.showSeperator("-");
    self.ui.printDialogue("???", f"welcome [yellow]{self.player.name}[reset]...");
    self.ui.printDialogue("???", f"this game requires [bold]fast reading skills[reset], for a better experience");
    self.ui.panelAnimatedPrintFile("sword style", "blade dance", [self.player.name, "dummy", 2], "blade dance");
    self.ui.printDialogue("???", f"the example above is a [yellow]action log[reset] and is common in simplestRPG");
    self.ui.printDialogue("???", f"some of the important words are [yellow]highlighted[reset] with colors");
    self.ui.printDialogue("???", f"[green]read the log carefully, enter when done[reset]!");
    self.ui.printDialogue("system", f"current type speed: {self.game.settings["type speed"]}");
    self.ui.awaitKey();
   
    self.ui.clear();
    self.ui.printDialogue("???", f"great work, [yellow]{self.player.name}[reset]!");
    self.ui.printDialogue("???", f"the next step is learning how to type commands!");
    self.ui.printDialogue("???", f"[yellow]simplestRPG[reset] was primarily made for android (termux) users, where there is an [bold cyan]on-screen keyboard[reset]");
    self.ui.printDialogue("???", f"one problem is.. The keyboard takes up screen space, especially on mobile phones!");
    self.ui.printDialogue("???", f"the solution is to hide the keyboard!, press the [blue]back button[reset] on your phone!");
    self.ui.printDialogue("???", f"then press the [blue]screen[reset] on your phone to open the keyboard.");
    self.ui.printDialogue("???", f"[yellow]you may skip this part on desktop, tablet and etc.[reset]");
    self.ui.awaitKey();
  
    self.ui.clear();
    self.ui.printDialogue("???", f"the next part is [purple]scrolling[reset]!");
    self.ui.printDialogue("???", f"ill print a ton of action logs, try scrolling up!");
    self.ui.printDialogue("???", f"[green]enter when ready[reset]!");
    self.ui.awaitKey();
    for n in range(1, 6): self.ui.panelAnimatedPrintFile("sword style", "iron reversal", [self.player.name, "dummy", 999], "iron reversal");
    self.ui.awaitKey();
    self.ui.printDialogue("???", f"did you scroll properly? make sure to scroll through action logs!");
    self.ui.awaitKey();

    self.ui.clear();
    self.ui.printDialogue("???", f"finally, we have [green]commands[reset]!");
    self.ui.printDialogue("???", f"in [yellow]simplestRPG[reset], there are no [red]buttons[reset]");
    self.ui.printDialogue("???", f"you can interact with the game by typing [yellow]highlighted[reset] commands using your keyboard.");
    self.ui.printDialogue("???", f"lets try one right now!");
    self.ui.printTreeMenu("commands", ["hi", "hello", "wassup"]);
    self.ui.printDialogue("???", f"remember [underline green]type the command[reset], not click!");
    command = self.ui.getInput();
    
    if command in ["hi", "hello", "wassup"]:
      self.ui.printDialogue("???", f"well done!, remember close your keyboard after typing!");
    else:
      self.ui.printDialogue("???", f"uh..., you typed [red]{command}[reset]?");
      self.ui.printDialogue("???", f"you got it wrong! but its fine, just close your keyboard..");
    self.ui.awaitKey();
    
    self.ui.clear();
    self.ui.printDialogue("???", "lets try another one shall we?");
    self.ui.normalPrint("≈ [blue]hi[reset]");
    self.ui.normalPrint("≈ [green]hello[reset]");
    self.ui.normalPrint("≈ [red]bye[reset]\n");
    command = self.ui.getInput();
    
    if command in ["hi", "hello", "bye"]:
      self.ui.printDialogue("???", f"fantastic!, you did great");
    else:
      self.ui.printDialogue("???", f"damn, you have to work on your typing skills!");
    self.ui.awaitKey();
    
    self.ui.clear();
    self.ui.printDialogue("???", f"one last thing, before we end this basic tutorial.");
    self.ui.printDialogue("???", f"there are [yellow]quick time[reset] events, where you have to type quickly!");
    self.ui.printDialogue("???", f"lets try one shall we?, press enter any time to start!");
    self.ui.awaitKey();
    
    if self.ui.getInputWithTimeout("type (pineapple) quickly!", 10) == f"pineapple": 
      self.ui.newLine();
      self.ui.printDialogue("???", f"[yellow]great job!, truly a keyboard wizard[reset]!");
    else: 
      self.ui.newLine();
      self.ui.printDialogue("???", f"oh. you need to practice speed typing!");
    self.ui.printDialogue("???", f"i set the time limit for 10 seconds just in case, but for other events it might be...");
    self.ui.printDialogue("???", f"around 1.5 seconds or maybe 3-7 seconds, honestly it depends.");
    self.ui.printDialogue("???", f"well thats all for the tutorial, i wish you luck!");
    self.game.givePlayerItem("starter chest");
    self.ui.awaitKey();
    
    self.startCombat();
    
  def startCombat(self):
    self.ui.clear();
    self.ui.printDialogue("???", f"lets test your skills shall we?");
    self.ui.printDialogue("???", f"here take some exp..");
    self.ui.showStatus("leveling up!, take a seat", 5);
    
    player_backup = deepcopy(self.game.player);
    self.game.givePlayerExp(999999);
    self.game.handlePlayerLevelUp();
    
    self.ui.printDialogue("???", f"are you ready?");
    self.ui.normalPrint("([yellow]yes[reset]) | ([green]yeah[reset])\n");
    self.ui.getInput();
    
    combat_handler = CombatHandler(self.game)
    combat_handler.initiateFightNpc(self.game.player, "fallen knight");
    
    self.game.player = player_backup;

    if combat_handler.won == self.game.player.name:
      self.ui.printDialogue("???", f"impressive, here take this!");
      self.game.givePlayerItem("wooden sword");
      self.game.givePlayerItem("peasant tunic");
      self.game.givePlayerItem("bread", 5);
      self.game.givePlayerItem("health potion", 5);
    else:
      self.ui.printDialogue("???", f"uh.. how did you fail?");
      self.game.givePlayerItem("skill book");
      self.game.givePlayerItem("strength potion", 10);

    self.ui.awaitKey();
    
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
    self.audio_handler = AudioHandler(self);
    self.animator = Animator(self);
    
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
  
  def handleQuit(self):
    """Handles quitting, stops audio player and enables echoing."""
    self.ui.enableEcho();
    self.audio_handler.popTracks();
    os._exit(0);
  
  def handleQuest(self):
    self.ui.clear();
    self.menu.showQuestMenu(self.player);
  
  def handleEquipmentDetail(self, part):
    while True:
      self.ui.clear();
      self.menu.showEquipmentDetails(self.player, part);
      option = self.ui.getInput();
      
      if option == "unequip" and self.player.equipment[part] != None:
        if self.player.unequipItem(part, self) != -1: 
          self.ui.panelPrint(f"[bold cyan]UNEQUIPPED[reset]", "center", part, "purple");
        else: self.ui.panelPrint(f"[bold res] UNEQUIP FAILED[reset]", "center", part, "red");  
        return;
      elif option == "back":
        return;
        
      self.ui.awaitKey();
      self.ui.clear();
      
  def handleEquipment(self, combat_handler = None):
    while True:
      self.ui.clear();
      self.menu.showEquipmentMenu(self.player);
      option = self.ui.getInput();
      
      try:
        if option == "close": return;
        self.handleEquipmentDetail(option);
      except KeyError as e:
        self.ui.animatedPrint(f"[bold red]{option} not a bodypart[reset]");
      self.ui.awaitKey();
  
  def handleItemDetail(self, name, combat_handler = None):
    while self.player.itemExists(name):
      self.ui.clear();
      self.menu.showItemDetails(self.player, name);
      option = self.ui.getInput();
      
      if option == "use":
        self.player.getItem(name).use(self, self.player, combat_handler);
      elif option == "drop":
        self.player.usedItem(name);
        continue;
      elif option == "back":
        return;
        
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
      option = self.ui.getInput();
     
      if option == "close": return;
      elif option == "gear": self.handleEquipment(combat_handler);
      elif self.player.itemExists(option): 
        self.handleItemDetail(option, combat_handler);
        continue;
      else: self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] does not have [yellow]{option}[reset]");
      self.ui.awaitKey();
  
  def handleSkillDetail(self, skill, combat_handler = None, attacker = None, defender = None):
    while True:
      self.ui.clear();
      self.menu.showSkillDetails(self.player, skill);
      option = self.ui.getInput();
      
      if option == "use" and attacker.skills[skill].passive != True:
        if attacker.energy >= attacker.skills[skill].energy: 
          attacker.skills[skill].use(combat_handler, attacker, defender);
          return;
        else: self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] does not have enough energy to use [green]{skill}[reset]!");
      elif option == "back":
        return -1;
        
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
      self.ui.clear();
      self.menu.showSkillsMenu(attacker);
      skill = self.ui.getInput();
      
    if attacker.skillExists(skill) is True:
       if self.handleSkillDetail(skill, combat_handler, attacker, defender) == -1: return self.handleUseSkill(None, combat_handler, attacker, defender);
    else:
      pass;
      
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
    self.audio_handler.play("start.wav");
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
    
    elif option == "delete":
      self.handleDelete();
      
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
      self.ui.console.log("git  installed!");
      return;
    except Exception:
      return;
      
  def handleLoad(self):
    """Handles load files in /saves"""
    
    self.ui.clear();
    self.ui.showHeader("Save Slots", "#");
    
    if os.path.exists(sys.path[0] + "/saves") != True:
      self.handleName();
      Tutorial(self).start();
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
        #Tutorial(self).startCombat();
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
  
  def handleDelete(self):
    try:
      os.remove(f"saves/{self.player.name}.save");
      self.ui.animatedPrint(f"[cyan]deleted {self.player.name} (OK)[reset]")
      self.handleQuit();
    except FileNotFoundError:
      self.ui.panelPrint("FAILED TO DELETE", "center", "settings");
      
  def giveQuest(self, name):
    if self.player.giveQuest(name) != -1:
      self.ui.panelPrint(f"[bold yellow]{name}[reset]\n{self.player.quests[name].desc}", "center", title = "QUEST RECEIVED");
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
            raise KeyError(f"'{stat}'  a valid stat")
          
          if stat == "luck":
            raise ValueError("Luck cannot be increased");
          
          if amount <= 0 or amount > self.player.points:
            raise ValueError("Invalid amount")
            
          self.player.stats[stat] += amount
          self.player.points -= amount
          
        except Exception as e: self.ui.panelPrint(str(e), "center", "system", "red")
        self.ui.awaitKey()
      else: break;
 
  def getItems(self):
    return ITEMS;
    
  def getSkills(self):
    return SKILLS;
    
  def giveStatus(self, status, n):
    CombatHandler(self).attack_handler.status_handler.afflict(self.player, status, n);
  
  def isPlayer(self, char):
    return isinstance(char, Player);
  
  def giveStyle(self, char, style, announce = True):
    self.removeStyle(char);
    char.attack_style = style;
    self.evolveStyle(char);
    if announce is True: self.ui.animatedPrint(f"[yellow]{char.name}[reset] switched to [bold magenta]{char.attack_style}[reset] style!");
    for skill in SKILLS:
      if SKILLS[skill]["skill"]._class == char.attack_style: self.giveSkill(char, skill);
    if char.attack_style == "swordsman": self.giveSkill(char, "parry")
    elif char.attack_style == "cleric": self.giveSkill(char, "blunt recovery");

  def removeStyle(self, char):
    for skill in SKILLS:
      if SKILLS[skill]["skill"]._class == char.attack_style: char.removeSkill(skill);
    char.attack_style = "basic";
  
  def evolveStyle(self, char):
    pass;
    #if char.attack_style == "swordsman" >= 10: char.attack_style = "duelist";
    