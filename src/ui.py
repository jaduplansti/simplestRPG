from rich import print, box;
from rich.align import Align;
from os import system;

from random import choices, uniform;
from rich.prompt import Prompt;
from rich.text import Text;

from rich.table import Table;
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
  
  def panelAnimatedPrint(self, text, title, type_delay=0.05):
    current_text = ""
    formatted_text = Text.from_markup(text)
    panel = Panel("", title=title, border_style=choices(["red", "green", "blue", "cyan", "magenta", "yellow", "bright_blue", "bright_magenta", "bright_cyan"])[0])
    with Live(panel, console=self.console, refresh_per_second=60) as live:
      for n, ch in enumerate(formatted_text):
        panel.renderable = formatted_text[0:n];
        live.update(panel);
        time.sleep(type_delay);
    self.newLine();
    
  def animatedPrintFile(self, key, n, args, delay=1):
	  formatted_s = self.getString(key, n).format(*args);
	  self.animatedPrint(formatted_s, delay);
  
  def panelAnimatedPrintFile(self, key, n, args, title, delay=1):
	  formatted_s = self.getString(key, n).format(*args);
	  self.panelAnimatedPrint(formatted_s, title);
  
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
  
  def showStatEvaluation(self, stat_name, stat_val, level):
    if stat_name == "health" or stat_name == "max health" or stat_name == "luck":
      return "N/A";
    
    bar_length = 6;
    stat_percentage = stat_val / (level * 10);
    filled_length = int(stat_percentage * bar_length)
    
    if stat_val <= (10 * level) * 0.25:
      color = "red";
    elif stat_val <= (10 * level) * 0.5:
      color = "yellow";
    elif stat_val <= (10 * level) * 1:
      color = "green";
    if stat_val > (10 * level) * 1:
      color = "cyan";
      
    evaluation_bar = f"[{color}]" + "★" * filled_length + "☆" * (bar_length - filled_length) + "[/]"
    return evaluation_bar;
    
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
    
  def showStatsRankMenu(self, character):
    stats_table = Table(f"{character.name} Stats", box = box.DOUBLE);
    stats_table.add_column("Rank");
    for stat in character.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", f"[blue]({character.getRankBasedOnStat(stat)})[reset]");
    self.normalPrint(stats_table);
    self.newLine();

  def showStatsMenu(self, character):
    stats_table = Table(f"{character.name} Stats", box = box.DOUBLE);
    stats_table.add_column("Value");
    for stat in character.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", f"[{character.getColorBasedOnStat(stat)}]{character.stats[stat]}[reset]");
    self.normalPrint(stats_table);
    self.newLine();

  def showStatsEvaluationMenu(self, character):
    stats_table = Table(f"{character.name} Stats", box = box.DOUBLE);
    stats_table.add_column("Evaluation");
    for stat in character.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", self.showStatEvaluation(stat, character.stats[stat], character.level));
    self.normalPrint(stats_table);
    self.newLine();
    
  def showStatCompareMenu(self, character1, character2):
    stats_table = Table(f"Stat", box = box.DOUBLE);
    stats_table.add_column("You");
    stats_table.add_column(f"{character2.name}");
    for stat in character1.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", f"[{character1.getColorBasedOnStat(stat)}]{character1.stats[stat]}[reset]", f"[{character2.getColorBasedOnStat(stat)}]{character2.stats[stat]}[reset]");
    self.normalPrint(stats_table);
    self.newLine();
    self.awaitKey();
    
  def showMainMenu(self):
    self.clear();
    self.normalPrint("×××××××××××××××");
    self.normalPrint("× [bold cyan]simplestRpg[reset] ×");
    self.normalPrint("×××××××××××××××");
    self.normalPrint("\n• version [green]1.9[reset] •\n")

    self.normalPrint("× [green]start[reset]");
    self.normalPrint("× [red]quit[reset]\n");
    
  def showStatsQueryMenu(self):
    self.clear();
    self.normalPrint("••••••••••••••");
    self.normalPrint("• [italic yellow]Stat Query[reset] •");
    self.normalPrint("••••••••••••••\n");
    
    self.normalPrint("× [green]stats[reset]");
    self.normalPrint("× [yellow]evaluation[reset]");
    self.normalPrint("× [cyan]rank[reset]");
    self.normalPrint("× [red]back[reset]\n");

  def showHomeMenu(self):
    self.clear();
    self.normalPrint("••••••••••••••");
    self.normalPrint("• [italic yellow]Your House[reset] •");
    self.normalPrint("••••••••••••••\n");
    
    self.normalPrint("× [yellow]you[reset]");
    self.normalPrint("× [purple]practice[reset]");
    self.normalPrint("× [blue]sleep[reset]\n");
  
  def showYouMenu(self):
    self.clear();
    self.showHeader("YOU", "-");
    
    self.normalPrint("× [cyan]stats[reset]");
    self.normalPrint("× [green]items[reset]");
    self.normalPrint("× [red]back[reset]\n");

  def showCombatMenu(self, combat_handler, character):
    self.clear();
    self.showHeader(f"{character.name} vs {character.enemy.name}", "×");
    
    self.showHealthBar(character);
    self.showHealthBar(character.enemy);
    self.showSeperator("+");
    
    self.normalPrint("× [yellow]attack[reset]");
    self.normalPrint("× [cyan]block[reset]");
    self.normalPrint("× [blue]taunt[reset]");
    self.normalPrint("× [green]items[reset]");
      
    if character.stats["health"] <= character.stats["max health"] * 0.25:
      self.normalPrint("× [red]flee[reset]");
    self.newLine();
    