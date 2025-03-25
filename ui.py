import colorama;
import subprocess;
from time import sleep;

from random import choices;
from os import system;

class UI:
  def __init__(self):
    colorama.init(); # initialize colorama lib

  def normalPrint(self, s): # same as print
    print(s, end = "\n");
  
  def newLine(self):
    print("");
  
  def __noEcho(self):
    system("stty -echo -icanon");
  
  def __doEcho(self):
    system("stty echo icanon");
  
  def clear_stdin_buffer(self):
    import sys;
    import platform;
    
    if platform.system() == "Windows":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        
  def animatedPrint(self, s, type_speed = 0.008, delay = 0.7, end = "\n"): # type writer effect
    self.__noEcho();
    for ch in s:
      print(ch, end = "", flush = True);
      sleep(type_speed);
    print(end);
    sleep(delay);
    self.__doEcho();
    self.clear_stdin_buffer();
    
  def showDialogue(self, name, s, name_color = "white"): # turns str to a valid colorama color
    print(f"[{self.coloredString(name, name_color)}] : ", end = "");
    self.animatedPrint(s, type_speed = 0.09);
    
  def getColor(self, color):
    if color == "red":
      return colorama.Fore.RED;
    elif color == "green":
      return colorama.Fore.GREEN;
    elif color == "blue":
      return colorama.Fore.BLUE;
    elif color == "yellow":
      return colorama.Fore.YELLOW;
    elif color == "reset":
      return colorama.Style.RESET_ALL;
    elif color == "white":
      return colorama.Fore.WHITE;
    elif color == "cyan":
      return colorama.Fore.CYAN;
    elif color == "magenta":
      return colorama.Fore.MAGENTA;
    else:
      return "err";
  
  def rarityPrint(self, item):
    if item.rarity == "common":
      return self.coloredString("common", "yellow");
    elif item.rarity == "uncommon":
      return self.coloredString("uncommon", "yellow");
    elif item.rarity == "rare":
      return self.coloredString("rare", "blue");
    elif item.rarity == "epic":
      return self.coloredString("epic", "cyan");
      
  def coloredString(self, s, color):
    return f"{self.getColor(color)}{s}{self.getColor("reset")}";
  
  def getInput(self):
    _in = input(">> ");
    self.newLine();
    return _in;
  
  def clear(self):
    subprocess.run(["clear"]);
  
  def awaitKey(self):
    self.normalPrint(self.coloredString("[press enter to continue]\n", "red"));
    self.getInput(); # to stop and wait
    
  def dynamicDialogue(self, dialogues): # where dialogues is a dictionary.
    for s in dialogues.keys():
      self.normalPrint(f"• {s}");
    print("") # new line
    
    _input = self.getInput().lower();
    if _input in dialogues.keys():
      self.animatedPrint(dialogues[_input], type_speed = 0.09);
    return _input;
  
  def randomDialogue(self, name, dialogues):
    self.showDialogue(name, choices(dialogues)[0]);
  
  def randomAnimatedPrint(self, msgs):
    self.animatedPrint(choices(msgs)[0]);
    
  def showBar(self, bar_name, n, max_n, end_str, color = "white", bar_color = "yellow"):
    bar_length = 6;
    filled_length = (n / max_n) * bar_length;
    empty_length = bar_length - filled_length;
    
    filled_bar = self.getColor(color) + "█" * round(filled_length);
    empty_bar = self.getColor("white") + "░" * round(empty_length);
    
    self.normalPrint(f"{self.coloredString(bar_name + " :" , bar_color)} {filled_bar}{empty_bar}{end_str}");
  
  def showStarBar(self, bar_name, n, max_n, end_str, color = "white", bar_color = "yellow"):
    bar_length = 6;
    filled_length = min((n / max_n) * bar_length, bar_length);
    empty_length = bar_length - filled_length;
    
    filled_bar = self.getColor(color) + "★" * round(filled_length);
    empty_bar = self.getColor(color) + "☆" * round(empty_length);
    
    self.normalPrint(f"{self.coloredString(bar_name + " :" , bar_color)} {filled_bar}{empty_bar}{end_str}");
  
  def showHealthBar(self, player):
    self.showBar(
      f"{player.name} health",
      player.stats["health"],
      player.stats["max health"],
      f" ({player.stats["health"]} hp)",
      "green",
    );
  
  def showMainMenu(self):
    self.clear();
    
    self.normalPrint("××××××××××××××××××");
    self.normalPrint(self.coloredString("   Simplest RPG   ", "magenta"));
    self.normalPrint("××××××××××××××××××\n");
    
    self.normalPrint(self.coloredString("{&}={&}={&}={&}={&}\n", "blue"));
     
    self.normalPrint(f"•=({self.coloredString("start", "yellow")})=•")
    self.normalPrint(f"•=({self.coloredString("exit", "red")})=•\n")
    
    self.normalPrint(self.coloredString("{&}={&}={&}={&}={&}\n", "cyan"));

  def showCharacterCreationTitle(self):
    self.clear();
    
    self.normalPrint("🛠️================🛠️");
    self.normalPrint("Character Creation");
    self.normalPrint("🛠️================🛠️\n")
    
  def showPlayerStats(self, player):
    self.normalPrint("{===================}");
    self.normalPrint("        Stats         ");
    self.normalPrint("{===================}\n");
    
    self.normalPrint(f"level {self.coloredString(player.level, "green")}\n");
    self.showBar("(exp)", player.exp, (player.level * 100), f" ({round(player.exp, 2)} exp)", "yellow", "cyan");

    for stat in player.stats:
      if stat == "health":
        self.showBar("(health)", player.stats["health"], player.stats["max health"], f" ({player.stats[stat]} hp)\n", "green", "red");
      else:  
        self.showStarBar(f"({stat})", player.stats[stat], max(player.level * 10, player.stats[stat]), f" ({player.stats[stat]})", "blue", "magenta");
        #self.normalPrint(f"({self.coloredString(stat, "yellow")}) •=• {self.coloredString(player.stats[stat], "green")}");
    self.newLine();
  
  def compareStats(self, player1, player2):
    self.normalPrint("{========================}");
    self.normalPrint("        Comparison        ");
    self.normalPrint("{========================}\n");
    
    self.normalPrint(f"{player1.name}(lv {self.coloredString(player1.level, "yellow")}) <-> {player2.name}(lv {self.coloredString(player2.level, "yellow")})\n");
    for stat in player1.stats: # this assumes the stat of player 1 = player 2
      self.normalPrint(f"({self.coloredString(stat, "yellow")}) •=• {self.coloredString(player1.stats[stat], "blue")} ⚔️ {self.coloredString(player2.stats[stat], "cyan")}");
    self.newLine();
    
  def showHomeMenu(self):
    self.clear()
  
    self.normalPrint("╔══════════════╗");
    self.normalPrint("║     home     ║");
    self.normalPrint("╚══════════════╝\n");
  
    self.normalPrint(f"──> {self.coloredString('~ move ~', 'yellow')}");
    self.normalPrint(f"──> {self.coloredString('~ inventory ~', 'blue')}");
    self.normalPrint(f"──> {self.coloredString('~ stats ~', 'green')}");
    self.normalPrint(f"──> {self.coloredString('~ train ~', 'magenta')}");
    self.normalPrint(f"──> {self.coloredString('~ exit ~', 'red')}\n");

    self.normalPrint("•══════════════•\n");
    
  def showInventory(self, player): # improve this
    if len(player.inventory) <= 0:
      self.animatedPrint(f"you dont have {self.coloredString("items", "red")}!");
      return -1;
    
    for item in player.inventory:
      self.normalPrint(f"({item}) {player.getAmountOfItem(item)}x");
      item_obj = player.getItem(item).__dict__;
      
      for info in item_obj:
        self.normalPrint(f"- {info}: {item_obj[info]}");
      self.newLine();
    
  def showDynamicMenu(self, player):
    self.clear();
    if player.location == "home":
      self.normalPrint("-=============-")
      self.normalPrint("|   Outside   |")
      self.normalPrint("-=============-\n")
        
      self.normalPrint(f"- ({self.coloredString('market', 'yellow')}) is at the north")
      self.normalPrint(f"- ({self.coloredString('forest', 'green')}) is at the west")
      self.normalPrint(f"- ({self.coloredString('go back', 'red')})\n")

      self.normalPrint("-========================-\n")
    
    elif player.location == "market":
      self.normalPrint("|==============|")
      self.normalPrint("|    Market    |")
      self.normalPrint("|==============|\n")
        
      self.normalPrint(f"- ({self.coloredString('forest', 'green')}) is at the west");
      self.normalPrint(f"- ({self.coloredString('bakery', 'magenta')})");
      self.normalPrint(f"- ({self.coloredString('potion stall', 'blue')})");
      self.normalPrint(f"- ({self.coloredString('go back', 'red')})\n");

      self.normalPrint("-========================-\n")
    
    elif player.location == "bakery":
      self.normalPrint("|==============|")
      self.normalPrint("|    Bakery    |")
      self.normalPrint("|==============|\n")
      
      self.randomDialogue("baker", ["good mornin, take a look at my stock!", "howdy, see anything you like?", "welcome buddy, got anything for me?"]);
      self.normalPrint(f"- ({self.coloredString('list foods', 'yellow')})");
      self.normalPrint(f"- ({self.coloredString('buy food', 'blue')})");
      self.normalPrint(f"- ({self.coloredString('sell food', 'green')})");
      
      self.normalPrint(f"- ({self.coloredString('attack', 'red')})");
      self.normalPrint(f"- ({self.coloredString('go back', 'red')})\n");

      self.normalPrint("-========================-\n")
        
  def showCombatMenu(self, player):
    self.clear();
    
    self.normalPrint("-•°•°•°•°•°•-");
    self.normalPrint(f"{player.name} vs {player.enemy.name}");
    self.normalPrint("-•°•°•°•°•°•-\n");
    
    self.showHealthBar(player);
    self.showHealthBar(player.enemy);
    self.newLine();
    
    self.normalPrint("============\n");
    
    self.normalPrint(f"× {self.coloredString("attack", "blue")}");
    self.normalPrint(f"× {self.coloredString("block", "cyan")}");
    self.normalPrint(f"× {self.coloredString("stats", "green")}");
    self.normalPrint(f"× {self.coloredString("inventory", "yellow")}");
    
    if player.stats["health"] <= (player.stats["max health"] * 0.25):
      self.normalPrint(f"× {self.coloredString("flee", "red")}");
    
    self.newLine();
    
  def showLevelUp(self, player):
    previous_level = player.level;
    previous_stats = {key: value for key, value in player.stats.items()};
     
    if player.tryLevelUp() is True:
      self.animatedPrint(f"{self.coloredString("you", "yellow")} have leveled up!, lv {self.coloredString(previous_level, "green")} -> {self.coloredString(player.level, "yellow")}");
      for stat in previous_stats:
        self.normalPrint(f"{self.coloredString(stat, "blue")} : {self.coloredString(previous_stats[stat], "green", )} -> {self.coloredString(player.stats[stat], "yellow")}");
      self.newLine();
      
    
    