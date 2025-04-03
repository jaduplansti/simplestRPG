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

class UI:
  def __init__(self, game):
    self.game = game;
    self.console = Console();
    self.strings = {};
    self.loadStrings();
  
  def beep(self):
    system("echo -n -e \a");
    
  def clear(self):
    system("clear");
  
  def disableEcho(self):
    system("stty -echo");
  
  def enableEcho(self):
    system("stty echo");
  
  def clearStdinBuffer(self):
    while select.select([sys.stdin], [], [], 0.1)[0]:
      sys.stdin.read(1);
  
  def loadStrings(self):
    with open(str(Path.home()) + "/simplestRPG/src/game_strings.json", "r") as file:
      self.strings = json.load(file);
  
  def getString(self, key, n):
    if isinstance(self.strings[key][n], list):
      return choices(self.strings[key][n])[0];
    return self.strings[key][n];
    
  def normalPrint(self, s, center = False):
    if center is True:
      print(Align.center(s));
    else:
      print(s);
  
  def barPrint(self, s, n, n_max, speed = 0.01):
    self.disableEcho();
    with Progress(TextColumn(f"({s}): "), BarColumn()) as progress:
      for _ in progress.track(range(n, n_max)):
        sleep(speed);
    self.newLine();
    self.enableEcho();
    
  def panelPrint(self, s):
    self.normalPrint(Panel(s));
    self.newLine();
  
  def panelAnimatedPrint(self, text, title, type_speed=0.05):
    self.disableEcho();
    current_text = ""
    formatted_text = Text.from_markup(text)
    panel = Panel("", title=title, border_style=choices(["red", "green", "blue", "cyan", "magenta", "yellow", "bright_blue", "bright_magenta", "bright_cyan"])[0])
    with Live(panel, console=self.console, refresh_per_second=60) as live:
      for n, ch in enumerate(formatted_text):
        panel.renderable = formatted_text[0:n];
        live.update(panel);
        self.beep();
        sleep(type_speed);
    self.newLine();
    sleep(2);
    self.enableEcho();
    self.clearStdinBuffer();
    
  def animatedPrintFile(self, key, n, args, delay=2):
	  formatted_s = self.getString(key, n).format(*args);
	  self.animatedPrint(formatted_s, delay);
  
  def panelAnimatedPrintFile(self, key, n, args, title, type_speed = 0.05):
	  formatted_s = self.getString(key, n).format(*args);
	  self.panelAnimatedPrint(formatted_s, title, type_speed);
  
  def animatedPrint(self, s, delay=1):
    self.disableEcho();
    parsed_s = Text.from_markup(s)
    print("~ ", end = "");
    for ch in parsed_s:
      print(ch, end='', flush=True)
      self.beep();
      sleep(uniform(0.01, 0.06));
    self.newLine();
    self.newLine();
    sleep(delay);
    self.enableEcho();
    self.clearStdinBuffer();
  
  def printTreeMenu(self, title, options): 
    tree = Tree(title);
    for option in options:
      tree.add(option);
    print(tree);
    self.newLine();
    
  def randomizeColorPrint(self, s, center = False):
    colored_string = "";
    for ch in s:
      random_color = choices(["red", "blue", "yellow", "green", "cyan", "magenta"])[0];
      colored_string += f"[{random_color}]{ch}[reset]";
    self.normalPrint(colored_string, center);
  
  def newLine(self):
    print("");
  
  def awaitKey(self):
    self.normalPrint("(press enter to continue)\n");
    self.getInput();
    self.newLine();
    
  def getInput(self):
    _input = Prompt.ask();
    self.newLine();
    return _input;
  
  def showHealthBar(self, character):
	  name = character.name
	  current_hp = character.stats["health"]
	  max_hp = character.stats["max health"]
	  current_hp = max(0, min(current_hp, max_hp))

	  health_percentage = current_hp / max_hp
	  bar_length = 6
	  filled_length = int(health_percentage * bar_length)

	  if health_percentage > 0.6:
		  color = "green"
	  elif health_percentage > 0.3:
		  color = "yellow"
	  else:
		  color = "red"

	  health_bar = f"[{color}]" + "█" * filled_length + "░" * (bar_length - filled_length) + "[/]"
	  self.normalPrint(f"{name} HP: {round(current_hp)}/{max_hp}\n({health_percentage*100:.2f}%) {health_bar}\n")
	
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
    