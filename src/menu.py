from rich.table import Table;
from rich import print, box;
from classes import Classes;

import art;

class Menu():
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
  
  def showItemsMenu(self, character):
    self.ui.animatedPrint(f"[magenta]{character.name}[reset] is carrying [green]{len(character.inventory)}[reset] item(s)");
    for name in character.inventory:
      item = character.inventory[name];
      self.ui.normalPrint(f"- [underline yellow]{name}[reset] [purple]({item["amount"]}x)[reset]");
      for info in item["item"].__dict__: 
        if info != "name": self.ui.normalPrint(f"  • [bold green]{info.capitalize()}[reset] ({item["item"].__dict__[info]})");
      self.ui.newLine();
  
  def showStatsMenu(self, character):
    self.ui.clear()
    self.ui.animatedPrint(f"[yellow]{character.name}[reset] focuses...")

    self.ui.animatedPrint(f"[green]=== STATUS ===[reset]")
    self.ui.normalPrint(f"[blue]Level:[reset] [cyan]{character.level}[reset] ([magenta]{character.exp} / {character.level * 100}[reset])\n")
    self.ui.normalPrint(f"[red]Health:[reset] [green]{character.stats['health']}[reset] / [green]{character.stats['max health']}[reset] HP\n")
    self.ui.normalPrint(f"[cyan]Energy:[reset] [blue]{character.energy}[reset]\n")

    self.ui.animatedPrint(f"[green]=== ATTRIBUTES ===[reset]")
    self.ui.normalPrint(f"[blue]Strength:[reset] [red]{character.stats['strength']}[reset] - [underline]Physical power, affects melee damage[reset]\n")
    self.ui.normalPrint(f"[green]Defense:[reset] [yellow]{character.stats['defense']}[reset] - [underline]Reduces damage taken[reset]\n")
    self.ui.normalPrint(f"[purple]Luck:[reset] [cyan]{character.stats['luck'] * 100:.0f}%[reset] - [underline]Affects critical hits and rare events[reset]\n");
    
  def showMainMenu(self):
    self.ui.clear();
    self.ui.normalPrint("×××××××××××××××");
    self.ui.normalPrint("× [bold cyan]simplestRpg[reset] ×");
    self.ui.normalPrint("×××××××××××××××");
    self.ui.normalPrint(art.CASTLE)

    self.ui.normalPrint("\n• version [green]2.1[reset] •\n")
    self.ui.printTreeMenu("(options)\n", ["[green]start[reset]", "[yellow]quit[reset]"]);
    
  def showHomeMenu(self):
    self.ui.clear();
    self.ui.normalPrint("••••••••••••••");
    self.ui.normalPrint("• [italic yellow]Your House[reset] •");
    self.ui.normalPrint("••••••••••••••");
    
    self.ui.normalPrint(art.HOUSE + "\n");
    self.ui.normalPrint("× [green]stats[reset]");
    self.ui.normalPrint("× [cyan]items[reset]");
    self.ui.normalPrint("× [purple]practice[reset]");
    self.ui.normalPrint("× [blue]sleep[reset]\n");
  
  def showYouMenu(self):
    self.ui.clear();
    self.ui.showHeader("YOU", "-");
    
    self.ui.normalPrint("× [cyan]stats[reset]");
    self.ui.normalPrint("× [green]items[reset]");
    self.ui.normalPrint("× [red]back[reset]\n");
  
  def showCombatInitiateMenu(self):
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] encounters a [cyan]{self.game.player.enemy.name}[cyan]!");
    self.ui.printTreeMenu("[green](options)[reset]\n", ["[red]fight[reset]", "[red]bail[reset]", "[purple]talk[reset]"]);
  
  def showCombatMenu(self, combat_handler, character):
    self.ui.clear();
    self.ui.showHeader(f"{character.name} vs {character.enemy.name}", "×");
    
    self.ui.showHealthBar(character);
    self.ui.showHealthBar(character.enemy);
    self.ui.showSeperator("+");
    
    self.ui.normalPrint("× [yellow]attack[reset]");
    self.ui.normalPrint("× [cyan]block[reset]");
    self.ui.normalPrint("× [blue]taunt[reset]");
    self.ui.normalPrint("× [green]items[reset]");
      
    if character.stats["health"] <= character.stats["max health"] * 0.25:
      self.ui.normalPrint("× [red]flee[reset]");
    self.ui.newLine();
    
  def classSelectionMenu(self):
    self.ui.animatedPrint(f"{self.game.player.name}, select your class!");
    self.ui.animatedPrint(f"there are {len(Classes.getAvailableClass(9999))} classes in SimplestRPG.");
  
  def showTip(self):
    self.ui.panelAnimatedPrintFile("tips", "tips", [], "tips");
    
    