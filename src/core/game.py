from objects.player import Player;
from core.ui import UI;
from mechanics.combat import CombatHandler;

from interface.menu import Menu;
from random import choices, randint;
import os;

from world.exploration import Exploration, AREAS;
from time import sleep;
from subprocess import run;

from objects.item import getItem, ITEMS;
from objects.skill import getSkill, Skill, SKILLS;
from objects.npc import NPC, NPCS;

from core.audio import AudioHandler;
import sys;

from copy import deepcopy;
from interface.animation import Animator;
from objects.character_class import getClass, CLASSES;
from world.story import Story;
 
from mechanics.clock import Clock;

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
    self.story_handler = Story(self);
    self.clock = Clock(self);
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
    
  def handleMenu(self, options : dict, showFun = None, default = None, back = False):
    """
    Creates a generic menu to display.
     
    Parameters:
    options, a dictionary holding the possible option that maps to a function.
    showFun, a function pointer that holds the function to display the options.
    """
    
    while True:
      if showFun != None: showFun();
      option = self.ui.getInput(options);
      
      if option == "help": self.menu.showTip();
      elif option == "quit": self.handleQuit();
      elif options != None and option in options.keys(): options[option]();
      elif back is True and option == "back": return;
      elif default != None: default(option);
      self.ui.awaitKey();
  
  def handleQuit(self):
    """Handles quitting, stops audio player and enables echoing."""
    self.ui.enableEcho();
    self.audio_handler.popTracks();
    self.clock.stopClock();
    os._exit(0);
  
  def handleQuest(self):
    self.ui.clear();
    self.menu.showQuestMenu(self.player);
  
  def handleStart(self):
    """Initializes the game."""
 
    self.ui.clear();
    self.audio_handler.play("start.wav");
    self.handleLoad();
    AREAS[self.player.location]["handler"](self).enter();
    
  def handleMainMenu(self):
    """This is self explanatory"""
    self.animator.animateTitle();
    self.handleMenu({"start" : self.handleStart, "quit" : self.handleQuit}, self.menu.showMainMenu);
  
  def initiateFight(self):
    """Initiates a fight using CombatHandler, see combat.py."""
    npc = choices(list(NPCS))[0];
    #elif self.player.level in range(6, 9): enemy = choices(["orc", "skeleton"])[0];
    #elif self.player.level in range(9, 13): enemy = choices(["elf", "bandit"])[0];
    #else: enemy = choices(["fallen knight", "priest"])[0];
  
    combat_handler = CombatHandler(self);
    combat_handler.initiateFightNpc(self.player, npc);
    
    if randint(1, 3) == 1:
      self.ui.animatedPrint("[red]another enemy appears![reset]");
      self.ui.awaitKey();
      return self.initiateFight();
      
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
      
  def giveQuest(self, name):
    if self.player.giveQuest(name) != -1:
      self.ui.panelPrint(f"[bold yellow]{name}[reset]\n{self.player.quests[name].desc}", "center", title = "QUEST RECEIVED");
    else: return -1;
    
  def givePlayerExp(self, exp):
    self.player.exp += exp;
  
  def givePlayerMoney(self, n):
    self.ui.animatedPrint(f"[yellow]you[reset] earned [green]{n}[reset] gold!");
    self.player.money += n;
    
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
    
  def giveSkill(self, char, name, announce = False):
    if name in char.skills: return;
    skill = getSkill(name);
    char.addSkill(skill);
    if announce is True and skill.passive != True: self.ui.panelPrint(f"[bold yellow]{skill.name}[reset] ([magenta]{skill.rank}[reset])\n[underline]{skill.desc}, consumes {skill.energy} energy[reset]", "center", "Learned");
    elif announce is True and skill.passive is True: self.ui.panelPrint(f"[bold yellow]{skill.name}[reset] ([italic yellow]PASSIVE[reset])\n[underline]{skill.desc}, consumes {skill.energy} energy[reset]", "center", "Learned");

  def getItems(self):
    return ITEMS;
    
  def getSkills(self):
    return SKILLS;
    
  def giveStatus(self, status, n):
    CombatHandler(self).attack_handler.status_handler.afflict(self.player, status, n);
 
  def isPlayer(self, char):
    return isinstance(char, Player);
  
  def giveClass(self, character, name, announce = False):
    if name not in ["swordsman", "peasant"]: return;
    _class = getClass(name);
    character._class = _class;
    
    for stat in _class.stat_bonus["increase"]:
      character.stats[stat[0]] += stat[1];
      if announce is True: self.ui.normalPrint(f"× [yellow]{stat[0]}[reset] went up by [green]{stat[1]}[reset]\n");
    for stat in _class.stat_bonus["decrease"]:
      character.stats[stat[0]] += stat[1];
      if announce is True: self.ui.normalPrint(f"× [yellow]{stat[0]}[reset] went down by [red]{stat[1]}[reset]\n");
    
    if announce is True: self.ui.showStatus("learning skills", 3);
    for skill in _class.skills:
      self.giveSkill(character, skill, announce);
    
  def handleStatAllocate(self, stat):
    allocated_points = 0;
    while True:
      self.ui.clear();
      self.menu.showStatAllocateMenu(stat);
      key = self.ui.getKey();
      
      if key == "w" and self.player.points > 0:
        self.player.stats[stat] += 1;
        self.player.points -= 1;
        allocated_points += 1;
      elif key == "s" and allocated_points > 0:
        self.player.stats[stat] -= 1;
        self.player.points += 1;
        allocated_points -= 1;
      elif key == "\n":
        return;
        
  def handleStatsMenu(self):
    while True:
      self.ui.clear()
      self.menu.showStatsMenu(self.player)
      self.ui.normalPrint("[yellow]hint[reset]: type a stat e.g strength\n");
      stat = self.ui.getInput();
      try:
        if stat == "close": return;
        elif stat not in self.player.stats:
          raise KeyError(f"{stat} does not exist");
        elif stat in ["luck", "health", "max health"]:
          raise ValueError(f"{stat} cannot be increased");
        else:
          self.handleStatAllocate(stat);
          continue;
      except Exception as e: self.ui.panelPrint(str(e), "center", "system", "red")
      self.ui.awaitKey();
      
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
      self.ui.panelPrint(f"level {plr.level} ({plr.exp}/{plr.level * 100})", title = f"{plr.name} ({plr._class.name})", alignment = "center");
    
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
      self.story_handler.progress = self.player.story_progress;
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
    self.player.story_progress = self.story_handler.progress;
    self.player.save();
  
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
      option = self.ui.getInput(list(self.player.inventory));
     
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
        if attacker.skills[skill].use(combat_handler, attacker, defender) == -1: self.ui.animatedPrint(f"[yellow]{attacker.name}[reset] does not have enough energy to use [green]{skill}[reset]!");
        return;
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
      skill = self.ui.getInput(list(attacker.skills));
      
    if attacker.skillExists(skill) is True:
      if self.handleSkillDetail(skill, combat_handler, attacker, defender) == -1: return self.handleUseSkill(None, combat_handler, attacker, defender);
    else:
      pass;
  
  def handleSkillTree(self):
    while True:
      self.menu.showSkillTreeMenu(self.player);
      _option = self.ui.getInput(list(self.player.skills));
      if _option == "close": return;
      elif _option in self.player.skills: self.handleSkillTreeDetails(_option);
      else: self.ui.normalPrint(f"you do not have [yellow]'{_option}'[reset]\n");
      self.ui.awaitKey();
  
  def handleSkillTreeDetails(self, skill_name):
    while True:
      self.menu.showSkillTreeDetailsMenu(self.player, skill_name);
      _option = self.ui.getInput(list(self.player.skills));
      if _option == "back": return;
     
  def handleSleep(self):
    """Handles Sleep, increases Player Health and Player Energy and then Saves."""
    
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.player.name}[reset] sees their bed and gets ready to sleep.");
    self.ui.barPrint("[blue]Energy[reset]", self.player.energy, 100, speed = 0.1);
    self.ui.animatedPrintFile("sleep", "rested", [self.player.name]);
    self.ui.panelPrint(f"[bold blue]ENERGY and HP[reset] RESTORED");

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
    self.giveClass(self.player, "peasant");
    self.story_handler.scene1();
    
  def handleSettings(self):
    """Handles game settings, see self.settings."""
    
    self.menu.showSettingsMenu();
    option = self.ui.getInput();
    
    if option == "type speed" or option == "ts":
      self.ui.normalPrint("set type speed ⤵\n");
      try:
        self.game.settings["type speed"] = float(self.ui.getInput());
      except ValueError:
        self.ui.normalPrint("type speed must be decimal/float ⤴\n");
    
    elif option == "delay speed" or option == "ds":
      self.ui.normalPrint("set delay speed ⤵\n");
      try:
        self.game.settings["delay speed"] = float(self.ui.getInput());
      except ValueError:
        self.ui.normalPrint("delay speed must be decimal/float ⤴\n");
    
    elif option == "delete":
      self.handleDelete();
     
  def handleDelete(self):
    try:
      os.remove(f"saves/{self.player.name}.save");
      self.ui.animatedPrint(f"[cyan]deleted {self.player.name} (OK)[reset]")
      self.handleQuit();
    except FileNotFoundError:
      self.ui.panelPrint("FAILED TO DELETE", "center", "settings");