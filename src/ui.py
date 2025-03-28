from rich import print, box;
from rich.align import Align;
from os import system;

from random import choices;
from rich.prompt import Prompt;
from rich.text import Text;

from rich.table import Table;
from time import sleep;
import sys;

import select;
import json;
import shutil;

class UI:
  def __init__(self, game):
    self.game = game;
    self.strings = {};
    self.loadStrings();
    
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
    with open("game_strings.json", "r") as file:
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
  
  def animatedPrint(self, key, n, args, type_speed = 0.01, delay = 1, center = False):
    self.disableEcho();
    formatted_s = self.getString(key, n).format(*args)
    parsed_s = Text.from_markup(formatted_s);
    
    for ch in parsed_s:
      print(ch, end = "");
      sleep(type_speed)
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
    _ = input(">");
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
	  self.normalPrint(f"{name} HP: {current_hp}/{max_hp}\n({health_percentage*100:.2f}%) {health_bar}\n")
	
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
    self.showStatsMenu(character1);
    self.normalPrint("vs");
    self.showStatsMenu(character2);

  def showMainMenu(self):
    self.clear();
    self.normalPrint("×××××××××××××××");
    self.normalPrint("× [bold cyan]simplestRpg[reset] ×");
    self.normalPrint("×××××××××××××××\n");
    
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
    
    self.normalPrint("× [yellow]go outside[reset]");
    self.normalPrint("× [purple]practice[reset]");
    self.normalPrint("× [cyan]stats[reset]");
    self.normalPrint("× [green]items[reset]\n");
    
  def showCombatMenu(self, combat_handler, character):
    self.clear();
    self.showHeader(f"{character.name} vs {character.enemy.name}", "×");
    
    self.showHealthBar(character);
    self.showHealthBar(character.enemy);
    self.showSeperator("+");
    
    self.normalPrint("× [yellow]attack[reset]");
    self.normalPrint("× [cyan]block[reset]");
    self.normalPrint("× [green]items[reset]");
      
    if character.stats["health"] <= character.stats["max health"] * 0.25:
      self.normalPrint("× [red]flee[reset]");
    self.newLine();