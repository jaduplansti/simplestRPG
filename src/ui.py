from rich import print
from rich.align import Align;
from os import system;

from random import choices, uniform;
from rich.prompt import Prompt;
from rich.text import Text;

from time import sleep;
import sys;

import select;
import json;
import shutil;

from pathlib import Path;
from rich.panel import Panel;
from rich.progress import Progress, TextColumn, BarColumn;

import time;
from rich.console import Console;
from rich.live import Live;

from rich.tree import Tree;
from readchar import readkey;

from timedinput import timedinput;

class UI:
  """
  This class handles User Interface, mainly serving as a wrapper for rich.
  
  Attributes:
  game, an instance of the Game class.
  console, an instance of the rich.console.Console class.
  strings, a dictionary holding the strings in game_strings.json.
  
  Usage:
  ui = UI(Game())
  """
  
  def __init__(self, game):
    self.game = game;
    self.console = Console();
    self.strings = {};
    self.loadStrings();
  
  def beep(self):
    """prints the beep escape character, i should rewrite this."""
    system("echo -n -e \a");
    
  def clear(self):
    """clear duh"""
    system("clear");
  
  def disableEcho(self):
    """a way to disable input echo, highly not compatible with other platforms."""
    system("stty -echo");
  
  def enableEcho(self):
    """see disableEcho()."""
    system("stty echo");
  
  def clearStdinBuffer(self):
    """clears the input buffer, often paired with disableEcho(), idek if this works."""
    while select.select([sys.stdin], [], [], 0.1)[0]:
      sys.stdin.read(1);
  
  def loadStrings(self):
    """loads game_strings.json into self.strings, note: rewrite this."""
    with open(str(Path.home()) + "/simplestRPG/src/game_strings.json", "r") as file:
      self.strings = json.load(file);
  
  def getString(self, key, n):
    """
    used to get a certain string in self.strings
    
    Parameters:
    key, a string containing the first key,
    n, a string containing the second key,
    
    Returns:
    this method may return a list of strings or a singular string.
    
    Usage:
    ui.getString("sword style", "iron reversal")
    """
    
    if isinstance(self.strings[key][n], list):
      return choices(self.strings[key][n])[0];
    return self.strings[key][n];
    
  def normalPrint(self, s):
    """ print. """
    print(s);
  
  def barPrint(self, s, n, n_max, speed = 0.01):
    """
    prints a rich progress bar.
    
    parameters:
    s, a string holding a name e.g health, energy, username.
    n, an integer holding the current value.
    n_max, the limit of n.
    speed, i forgot wth.
    
    Usage:
    ui.barPrint("health", 50, 100)
    """
    
    self.disableEcho();
    with Progress(TextColumn(f"({s}): "), BarColumn()) as progress:
      for _ in progress.track(range(n, n_max)):
        sleep(speed);
    self.newLine();
    self.enableEcho();
    
  def panelPrint(self, s):
    """prints a panel."""
    self.normalPrint(Panel(s));
    self.newLine();
  
  def panelAnimatedPrint(self, text, title):
    """
    typewriter effect inside a panel.
    
    Parameters:
    text, a string to be printed,
    title, a title.
    
    Usage:
    ui.panelAnimatedPrint("help me!", "error")
    """
    
    self.disableEcho();
    current_text = ""
    formatted_text = Text.from_markup(text)
    panel = Panel("", title=title, border_style=choices(["red", "green", "blue", "cyan", "magenta", "yellow", "bright_blue", "bright_magenta", "bright_cyan"])[0])
    with Live(panel, console=self.console, refresh_per_second=60) as live:
      for n, ch in enumerate(formatted_text):
        panel.renderable = formatted_text[0:n + 1];
        live.update(panel);
        self.beep();
        sleep(self.game.settings["type speed"]);
    self.newLine();
    sleep(self.game.settings["delay speed"]);
    self.enableEcho();
    self.clearStdinBuffer();
    
  def animatedPrintFile(self, key, n, args):
	  formatted_s = self.getString(key, n).format(*args);
	  self.animatedPrint(formatted_s);
  
  def panelAnimatedPrintFile(self, key, n, args, title):
	  formatted_s = self.getString(key, n).format(*args);
	  self.panelAnimatedPrint(formatted_s, title);
  
  def animatedPrint(self, s):
    self.disableEcho();
    parsed_s = Text.from_markup(s)
    print("~ ", end = "");
    for ch in parsed_s:
      print(ch, end='', flush=True)
      self.beep();
      sleep(self.game.settings["type speed"]);
    self.newLine();
    self.newLine();
    sleep(self.game.settings["delay speed"]);
    self.enableEcho();
    self.clearStdinBuffer();
  
  def printTreeMenu(self, title, options): 
    tree = Tree(title);
    for option in options:
      tree.add(option);
    print(tree);
    self.newLine();
    
  def randomizeColorPrint(self, s):
    colored_string = "";
    for ch in s:
      random_color = choices(["red", "blue", "yellow", "green", "cyan", "magenta"])[0];
      colored_string += f"[{random_color}]{ch}[reset]";
    self.normalPrint(colored_string);
  
  def newLine(self):
    print("");
  
  def getKey(self):
    return readkey();
    
  def awaitKey(self):
    self.normalPrint("(type anything to continue)\n");
    self.getInput(); # yeah
    self.newLine();
    
  def getInput(self):
    _input = Prompt.ask();
    self.newLine();
    return _input;
  
  def getInputWithTimeout(self, msg, n):
    self.normalPrint(msg + "\n");
    try:
      return timedinput(f": ", timeout = n);
    except:
      return "";
      
  def showBar(self, n, total, bar_length, color):
    n = max(0, min(n, total))
    filled_length = int(n / total * bar_length) if total > 0 else 0
    return f"[{color}]" + "◼" * filled_length + "◻" * (bar_length - filled_length) + "[reset]"
    
  def showCombatBar(self, character):
    color = "";
    statuses = "";
    name = character.name;
    
    if character.berserk is True:
      name += " ([bold red]berserk[reset])";
      
    if character.stats["health"] / character.stats["max health"] > 0.6:
      color = "green";
    elif character.stats["health"] / character.stats["max health"] > 0.3:
      color = "yellow";
    else: color = "red";
    
    health_bar = self.showBar(character.stats["health"], character.stats["max health"], 6, color);
    energy_bar = self.showBar(character.energy, 100, 6, "blue");

    for status in character.status:
      if character.status[status][0] is True:
        symbol = "";
        if status in ["blocking"]: symbol = "⬆";
        else: symbol = "⬇";
        statuses += (f"([bold purple]{status}[reset] [bold green]{character.status[status][1]}x[reset] {symbol})");
    
    self.normalPrint(f"{name} HP: [bold green]{round(character.stats["health"])}[reset]/[bold green]{character.stats["max health"]}[reset]\n([bold red]{(character.stats["health"] / character.stats["max health"])*100:.2f}%[reset]) {health_bar}")
    self.normalPrint(f"Energy: [bold cyan]{round(character.energy)}[reset]/[bold cyan]{100}[reset]\n([bold green]{(character.energy / 100)*100:.2f}%[reset]) {energy_bar}\n")
    if statuses != "": self.normalPrint(f"{statuses}\n");
    
  def showHeader(self, title, ch):
    header = "";
    for _ in range(len(title)):
      header += ch;
    self.randomizeColorPrint(f"{header}\n{title}\n{header}\n");
  
  def showSeperator(self, ch):
    seperator = "";
    for _ in range(shutil.get_terminal_size().columns):
      seperator += ch;
    self.randomizeColorPrint(seperator + "\n");
  
  def showStatus(self, msg, n, spinner = "dots"):
    with self.console.status(msg, spinner = spinner) as status:
      sleep(n);
  