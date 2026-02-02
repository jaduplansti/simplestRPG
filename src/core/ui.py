import builtins;

from rich import print, box
from rich.align import Align;
from os import system;

from random import choices, uniform, choice, randint;
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
from interface.animation import Animator;

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import string;

from interface.art import ARTS;
import termios;

class InputController:
  def __init__(self):
    self._fd = sys.stdin.fileno()
    self._orig_attrs = termios.tcgetattr(self._fd)
    self._erase_char = self._orig_attrs[6][termios.VERASE]

  def disableInput(self):
    new_attrs = termios.tcgetattr(self._fd)
    new_attrs[3] &= ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(self._fd, termios.TCSADRAIN, new_attrs)

  def enableInput(self):
    # flush any buffered keystrokes before restoring
    termios.tcflush(self._fd, termios.TCIFLUSH)
    restored = termios.tcgetattr(self._fd)
    restored[3] |= (termios.ECHO | termios.ICANON)
    restored[6][termios.VERASE] = self._erase_char
    termios.tcsetattr(self._fd, termios.TCSADRAIN, restored)

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
    self.input_handler = InputController();
    self.strings = {};
    self.dialogues = {};
    self.loadJson();
  
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
  
  def loadJson(self):
    """loads json files into their corresponding attribute"""
    with open(sys.path[0] + "/strings/game_strings.json", "r") as file:
      self.strings = json.load(file);
    with open(sys.path[0] + "/strings/dialogues.json", "r") as file:
      self.dialogues = json.load(file);
    
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
  
  def getDialogue(self, key, subkey, n, rand = False):
    try:
      if n is None: dialogues = self.dialogues[key][subkey];
      else: dialogues = self.dialogues[key][subkey][n];
      if rand is True and isinstance(dialogues, list): return choice(dialogues);
      else: return dialogues;
    except KeyError:
      return None;
      
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
    
  def panelPrint(self, s, alignment = None, title = "", color = "white", expand = True, centered = False, joint = False, box_style = box.SQUARE):
    """prints a panel."""
    if centered is True: self.normalPrint(Align.center(Panel(Text().from_markup(s, justify = alignment), title = title, border_style = color, expand = expand, box = box_style)));
    else: self.normalPrint(Panel(Text().from_markup(s, justify = alignment), title = title, border_style = color, expand = expand, box = box_style));
    
    if joint is True:
      self.normalPrint(Align.center("||"));
      self.normalPrint(Align.center("||"));
    else: self.newLine();
  
  def panelAnimatedPrintClear(self, text, title):
    panel = self.panelAnimatedPrint(text, title);
    panel_lines = len(self.console.render_lines(panel))
    self.clearLine(panel_lines + 1);
    
  def panelAnimatedPrint(self, text, title, box_type = box.SQUARE):
    """
    typewriter effect inside a panel.
    
    Parameters:
    text, a string to be printed,
    title, a title.
    
    Usage:
    ui.panelAnimatedPrint("help me!", "error")
    """
    if self.game.player.bodyparts["head"] is False:
      text = "[bold red]you cant see.[reset]";
      title = "";

    self.input_handler.disableInput();
    current_text = ""
    formatted_text = Text.from_markup(text)
    panel = Panel("", title=title, border_style=choices(["red", "green", "blue", "cyan", "magenta", "yellow", "bright_blue", "bright_magenta", "bright_cyan"])[0], box = box_type)
    with Live(panel, console=self.console, refresh_per_second=60) as live:
      for n, ch in enumerate(formatted_text):
        panel.renderable = formatted_text[0:n + 1];
        live.update(panel);
        sleep(self.game.settings["type speed"]);
    self.newLine();
    sleep(self.game.settings["delay speed"]);
    self.input_handler.enableInput();
    return panel;
    
  def animatedPrintFile(self, key, n, args):
	  formatted_s = self.getString(key, n).format(*args);
	  self.animatedPrint(formatted_s);
  
  def panelAnimatedPrintFile(self, key, n, args, title):
	  formatted_s = self.getString(key, n).format(*args);
	  self.panelAnimatedPrint(formatted_s, title);
  
  def animatedPrint(self, s, punc = False):
    self.input_handler.disableInput();
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
    self.input_handler.enableInput();

  def printDialogue(self, name, s):
    if not isinstance(s, list): self.animatedPrint(f"[bold]{name}[reset]: {s}", punc = True);
    else: self.animatedPrint(f"[bold]{name}[reset]: {choices(s)[0]}", punc = True);
  
  def printDialogueFile(self, name, key, subkey, n = None, rand = False, args = []):
    try:
      formatted_s = self.getDialogue(key, subkey, n, rand).format(*args);
      self.printDialogue(name, formatted_s);
    except AttributeError:
      return None;
      
  def printTreeMenu(self, title, options): 
    if len(options) == 0: return;
    
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
  
  def getKey(self, s = "", end = "\n"):
    key = readkey();
    self.clearLine(1);
    return key;
    
  def awaitKey(self):
    self.normalPrint("([bold red]press anything to continue[reset])");
    self.getKey();
    
  def input(self, s = ""):
    _input = input(s + " > ");
    return _input;
    
  def getInput(self, completer = None, num = False):
    if completer is None: _input = Prompt.ask(f"[yellow](enter command)[reset] ⤵\n\n");
    else: 
      #if randint(1, 3) == 1: self.normalPrint("[bold yellow]hint: when (⚠) is besides the input prompt that means pressing the (TAB) or (⇆) key autocompletes.[reset]\n");
      _input = prompt("(⚠) (enter command) ↙\n\n: ", completer = WordCompleter(completer), complete_while_typing = False);
    self.newLine();
    if num is True and _input.isdigit() is False: return -1;
    elif num is True: return int(_input);
    self.clearStdinBuffer();
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
    if not self.game.isPlayer(character) and character.boss is True: 
      name += " ([bold blue]boss[reset])";

    if character.stats["health"] / character.stats["max health"] > 0.6:
      color = "green";
    elif character.stats["health"] / character.stats["max health"] > 0.3:
      color = "yellow";
    else: color = "red";
    
    health_bar = self.showBar(character.stats["health"], character.stats["max health"], 6, color);
    energy_bar = self.showBar(character.energy, character.max_energy, 6, "blue");
    hunger_bar = self.showBar(character.hunger, 100, 6, "purple");

    for status in character.status:
      if character.status[status][0] is True:
        symbol = "";
        if status in ["blocking", "parrying"]: symbol = "⬆";
        else: symbol = "⬇";
        statuses += (f"([bold purple]{status}[reset] [bold green]{character.status[status][1] - 1}x[reset] {symbol})");
   
    self.normalPrint(f"{name} HP: [bold green]{round(character.stats["health"])}[reset]/[bold green]{character.stats["max health"]}[reset]\n([bold red]{(character.stats["health"] / character.stats["max health"])*100:.2f}%[reset]) {health_bar}")
    self.normalPrint(f"Energy: [bold cyan]{round(character.energy)}[reset]/[bold cyan]{character.max_energy}[reset]\n([bold green]{(character.energy / character.max_energy)*100:.2f}%[reset]) {energy_bar}")
    if self.game.isPlayer(character): self.normalPrint(f"Hunger: [bold cyan]{round(character.hunger)}[reset]/[bold cyan]{100}[reset]\n([bold green]{(character.hunger / 100)*100:.2f}%[reset]) {hunger_bar}\n")
    else: self.normalPrint("");
    if statuses != "": self.normalPrint(f"{statuses}\n");
    
  def showHeader(self, title, ch):
    header = "";
    for _ in range(len(title)):
      header += ch;
    self.randomizeColorPrint(f"{header}\n{title}\n{header}\n");
  
  def showSeperator(self, ch, title=None):
    width, _ = self.getSize();
    
    if title:
      title = f" {title} ";
      if len(title) >= width: title = title[:width - 4] + "...";
      side = (width - len(title)) // 2;
      line = ch * side + title + ch * (width - side - len(title));
    else:
      line = ch * width;
    self.randomizeColorPrint(line + "\n");
    
  def showStatus(self, msg, n, spinner = "dots"):
    self.input_handler.disableInput();
    with self.console.status(msg, spinner = spinner) as status:
      sleep(n);
    self.input_handler.enableInput();

  def showQuest(self, name):
    quest = self.game.player.quests[name]["obj"];
    self.panelPrint(quest.desc, "center", quest.name);
  
  def printArtPanel(self, art):
    panel = Panel(
      Text(ARTS[art].strip("\n"), justify="center"),
      padding=(1, 4),
      expand=False,
      box=box.ROUNDED
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
  
  def getRandomKeys(self, n):
    keys = [];
    for _ in range(n):
      keys.append(choice(string.ascii_letters).lower());
    return keys;
  
  def moveCursorUp(self, n=1):
    # ANSI escape code to move cursor up by n lines
    builtins.print(f"\033[{n}A", end="");
    
  def flush(self):
    sys.stdout.flush();
  
  def getChoice(self, dialogues):
    try:
      for index, option in enumerate(dialogues):
        print(f"{index + 1}. {option}");
      self.newLine();
      chosen_dialogue = int(self.input("say"));
      self.newLine();
      return chosen_dialogue;
    except ValueError:
      return 0;