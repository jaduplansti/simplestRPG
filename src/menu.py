from rich.table import Table;
from rich import print, box;

import art;

class Menu():
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
  
  def showItemsMenu(self, character):
    self.ui.animatedPrint(f"([magenta]{character.name}[reset] is carrying [green]{len(character.inventory)}[reset] item(s))");
    for name in character.inventory:
      item = character.inventory[name];
      self.ui.normalPrint(f"- [underline yellow]{name}[reset] [purple]({item["amount"]}x)[reset]");
      for info in item["item"].__dict__: 
        if info != "name": self.ui.normalPrint(f"  • [bold green]{info.capitalize()}[reset] ({item["item"].__dict__[info]})");
      self.ui.newLine();
    self.ui.normalPrint("[bold yellow]you can close the bag by typing 'close'[reset]\n");
      
  def showSkillsMenu(self, character):
    self.ui.animatedPrint(f"[magenta]==SKILLS==[reset]");
    for skill_name in character.skills:
      skill = character.skills[skill_name];
      self.ui.normalPrint(f"- [bold yellow]{skill_name}[reset]");
      for info in skill.__dict__: 
        if info != "name": self.ui.normalPrint(f"  - [bold green]{info.capitalize()}[reset] ({skill.__dict__[info]})");
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
    
    self.showEquipmentMenu(character);
    
  def showEquipmentMenu(self, character):
    self.ui.animatedPrint("[bold purple]=== EQUIPMENT ===[reset]");
    for part in character.equipment:
      if character.equipment[part] != None: self.ui.normalPrint(f"[bold magenta]{part}[reset] -> [italic yellow]{character.equipment[part].name}[reset] ([cyan]{character.equipment[part].rarity}[reset]) ([green]{character.equipment[part].durability}[reset]%)\n");
      else: self.ui.normalPrint(f"[purple]{part}[reset] -> [yellow]Empty[reset]\n");
    
  def showMainMenu(self):
    self.ui.clear();
    self.ui.normalPrint("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈");
    self.ui.normalPrint("≈ [bold cyan]simplestRpg[reset] ≈");
    self.ui.normalPrint("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈");

    self.ui.normalPrint("\n• version [green]2.5.1[reset] •\n")
    self.ui.printTreeMenu("(options)\n", ["[green]start[reset]", "[yellow]quit[reset]"]);
    
  def showCombatInitiateMenu(self):
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] encounters a [cyan]{self.game.player.enemy.name}[cyan]!");
    self.ui.printTreeMenu("[green](options)[reset]\n", ["[red]fight[reset]", "[red]bail[reset]", "[purple]talk[reset]"]);
    self.showTip();
    
  def showCombatMenu(self, combat_handler, character):
    self.ui.clear();
    self.ui.showHeader(f"{character.name} vs {character.enemy.name}", "≈");
    
    self.ui.showCombatBar(character);
    self.ui.showCombatBar(character.enemy);
    self.ui.showSeperator("+");
    
    self.ui.normalPrint("≈ [yellow]attack[reset]");
    self.ui.normalPrint("≈ [cyan]block[reset]");
    self.ui.normalPrint("≈ [blue]taunt[reset]");
    self.ui.normalPrint("≈ [green]items[reset]");
    self.ui.normalPrint("≈ [magenta]skills[reset]");

    if character.stats["health"] <= character.stats["max health"] * 0.25:
      self.ui.normalPrint("≈ [red]flee[reset]");
    self.ui.newLine();
    
  def showTip(self):
    self.ui.panelAnimatedPrintFile("tips", "tips", [], "tips");
  
  def showSettingsMenu(self):
    self.ui.clear();
    self.ui.showHeader("Settings", ".");
    self.ui.normalPrint(f"• [yellow]type speed[reset] : {self.game.settings["type speed"]}");
    self.ui.normalPrint(f"• [cyan]delay speed[reset] : {self.game.settings["delay speed"]}");
    self.ui.normalPrint(f"• [purple]audio[reset] : {self.game.audio_handler.enabled}");
    self.ui.newLine();
    

