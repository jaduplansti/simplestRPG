import builtins;

from rich import print, box
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

from inputimeout import inputimeout, TimeoutOccurred;
from threading import Thread
from player import Player;

from animation import Animator;

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
  
  def clear(self):
    """clear duh"""
    system("clear");
  
  def clearLine(self, n = 1):
    """clears for n line using escape sequence"""
    for _ in range(n):
      builtins.print("\033[A\033[2K", end = "", flush = True);
    
  def disableEcho(self):
    """a way to disable input echo, highly not compatible with other platforms."""
    if self.game.isTermux() is True: # temporary solution, hey it works!
      system("stty -echo");
  
  def enableEcho(self):
    """see disableEcho()."""
    if self.game.isTermux() is True:
      system("stty echo");
  
  def clearStdinBuffer(self):
    """clears the input buffer, often paired with disableEcho(), idek if this works."""
    while select.select([sys.stdin], [], [], 0.1)[0]:
      sys.stdin.read(1);
  
  def loadStrings(self):
    """loads game_strings.json into self.strings, note: rewrite this."""
    with open(sys.path[0] + "/game_strings.json", "r") as file:
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
      for _ in progress.track(range(int(n), int(n_max))):
        sleep(speed);
    self.newLine();
    self.enableEcho();
    
  def panelPrint(self, s, alignment = None, title = "", color = "white", expand = True, centered = False, joint = False):
    """prints a panel."""
    if centered is True: self.normalPrint(Align.center(Panel(Text().from_markup(s, justify = alignment), title = title, border_style = color, expand = expand)));
    else: self.normalPrint(Panel(Text().from_markup(s, justify = alignment), title = title, border_style = color, expand = expand));
    
    if joint is True:
      self.normalPrint(Align.center("||"));
      self.normalPrint(Align.center("||"));
    else: self.newLine();
    
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
  
  def animatedPrint(self, s, punc = False):
    self.disableEcho();
    parsed_s = Text.from_markup(s)
    print("× ", end = "");
    for ch in parsed_s:
      if punc is True and str(ch) == ".": sleep(0.3);
      elif punc is True and str(ch) == ",": sleep(0.1);
      print(ch, end='', flush=True)
      sleep(self.game.settings["type speed"]);
    self.newLine();
    self.newLine();
    sleep(self.game.settings["delay speed"]);
    self.enableEcho();
    self.clearStdinBuffer();
  
  def printDialogue(self, name, s):
    if not isinstance(s, list): self.animatedPrint(f"{name}: {s}", punc = True);
    else: self.animatedPrint(f"{name}: {choices(s)[0]}", punc = True);

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
  
  def getKey(self, s = ""):
    self.normalPrint(s + "\n");
    return readkey();
  
  def awaitKey(self):
    self.getKey("([bold red]press anything to continue[reset])");
    
  def getInput(self):
    _input = Prompt.ask(f"[yellow](enter command)[reset] ⤵\n\n");
    self.newLine();
    return _input;
  
  def dialogueAsk(self, s):
    _input = Prompt.ask(s + "\n\n");
    self.newLine();
    return _input;
    
  def getInputWithTimeout(self, msg, n):
    self.normalPrint(msg + "\n");
    try:
      return inputimeout(prompt = ": ", timeout = n);
    except TimeoutOccurred:
      return "";
  
  def getEnterWithTimeout(self, msg, n):
    try:
      return inputimeout(prompt = msg, timeout = n);
    except TimeoutOccurred:
      return None;
      
  def showBar(self, n, total, bar_length, color):
    n = max(0, min(n, total))
    filled_length = int(n / total * bar_length) if total > 0 else 0
    return f"[{color}]" + "◼" * filled_length + "◻" * (bar_length - filled_length) + "[reset]"
    
  def showCombatBar(self, character):
    color = "";
    statuses = "";
    name = character.name + f" [green]|lv {character.level}|[reset]";
    
    if character.berserk is True:
      name += " ([bold red]berserk[reset])";
    if not isinstance(character, Player) and character.boss is True: 
      name += " ([bold blue]boss[reset])";

    if character.stats["health"] / character.stats["max health"] > 0.6:
      color = "green";
    elif character.stats["health"] / character.stats["max health"] > 0.3:
      color = "yellow";
    else: color = "red";
    
    health_bar = self.showBar(character.stats["health"], character.stats["max health"], 6, color);
    energy_bar = self.showBar(character.energy, 100, 6, "blue");
    hunger_bar = self.showBar(character.hunger, 100, 6, "purple");

    for status in character.status:
      if character.status[status][0] is True:
        symbol = "";
        if status in ["blocking", "parrying"]: symbol = "⬆";
        else: symbol = "⬇";
        statuses += (f"([bold purple]{status}[reset] [bold green]{character.status[status][1] - 1}x[reset] {symbol})");
    
    self.normalPrint(f"{name} HP: [bold green]{round(character.stats["health"])}[reset]/[bold green]{character.stats["max health"]}[reset]\n([bold red]{(character.stats["health"] / character.stats["max health"])*100:.2f}%[reset]) {health_bar}")
    self.normalPrint(f"Energy: [bold cyan]{round(character.energy)}[reset]/[bold cyan]{100}[reset]\n([bold green]{(character.energy / 100)*100:.2f}%[reset]) {energy_bar}")
    if isinstance(character, Player): self.normalPrint(f"Hunger: [bold cyan]{round(character.hunger)}[reset]/[bold cyan]{100}[reset]\n([bold green]{(character.hunger / 100)*100:.2f}%[reset]) {hunger_bar}\n")
    else: self.normalPrint("");
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
  
  def showQuest(self, name):
    quest = self.game.player.quests[name]["obj"];
    self.panelPrint(quest.desc, "center", quest.name);
  
  def printArtPanel(self, art):
    panel = Panel(
      Text(art.strip("\n"), justify="center"),
      padding=(1, 4),
      expand=False,
      box=box.DOUBLE
    )
    centered_panel = Align.center(panel)
    print(centered_panel);
    self.newLine();
  
  def showDivider(self, s):
    self.console.rule(s);
  
  def getSize(self):
    dimension = shutil.get_terminal_size();
    return [dimension.columns, dimension.lines];
  
  def randomColor(self):
    return choices(["yellow", "green", "red", "cyan"])[0];
    
    