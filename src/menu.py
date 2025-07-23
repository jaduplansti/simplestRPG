from rich.table import Table;
from rich import print, box;

class Menu():
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
  
  def showPlayerMenu(self):
    self.ui.console.print(f"[yellow]{self.game.player.name}[reset] ([green]level {self.game.player.level}[reset])\n", justify = "center");
    self.ui.normalPrint(f"× ([cyan]{len(self.game.player.inventory)} items[reset]) ([purple]{len(self.game.player.skills)} skills[reset])\n");
    self.ui.normalPrint("× [underline bold magenta]check status for more details.[reset]\n");
  
  def showQuestMenu(self, character):
    self.ui.animatedPrint(f"[blue]==QUESTS==[reset]");
    for quest_name in character.quests:
      quest = character.quests[quest_name];
      self.ui.panelPrint(f"{quest["obj"].desc}", "center", f"{quest_name} ({quest["kills"]})");
      
  def showItemsMenu(self, character):
    if character.getTotalItems() < 50: self.ui.animatedPrint(f"[magenta]{character.name}[reset] is carrying [green]{len(character.inventory)}[reset]({character.getTotalItems()}) item(s)");
    else: self.ui.animatedPrint(f"[bold red]INVENTORY FULL[reset]");
    
    for name in character.inventory:
      item = character.inventory[name];
      self.ui.normalPrint(f"- [underline yellow]{name}[reset] [purple]({item["amount"]}x)[reset]");
      for info in item["item"][-1].__dict__: 
        if info != "name": self.ui.normalPrint(f"  • [bold green]{info.capitalize()}[reset] ({item["item"][-1].__dict__[info]})");
      self.ui.newLine();
    self.ui.normalPrint("[bold yellow]you can close the bag by typing 'close'[reset]\n");
      
  def showSkillsMenu(self, character):
    self.ui.animatedPrint(f"[magenta]==SKILLS==[reset]");
    for skill_name in character.skills:
      skill = character.skills[skill_name];
      if skill.passive is False: self.ui.panelPrint(f"[bold yellow]{skill_name}[reset] ([magenta]{skill.rank}[reset])\n[underline]{skill.desc}, consumes {skill.energy} energy and {skill.range} range[reset]", "center");
      else: self.ui.panelPrint(f"[bold yellow]{skill_name}[reset] ([cyan]PASSIVE[reset]) ([green]{skill.rank}[reset])\n[underline]{skill.desc}", "center");

  def showStatsMenu(self, character):
    info = f"[green]name[reset]: [bold yellow]{character.name}[reset]\n[blue]level[reset]: {character.level} ({character.exp}/{100 * character.level})\n";
    info += f"[yellow]title[reset]: {character.title}\n";
    info += f"[red]health[reset]: {character.stats["health"]}/{character.stats["max health"]}\n";
    info += f"[blue]energy[reset]: {character.energy}\n";
    info += f"[purple]hunger[reset]: {character.hunger}\n";
    info += f"[bold]points[reset]: [green]{character.points}[reset]\n\n"
    
    info += f"[green]stats[reset]:\n"
    for stat in character.stats:
      info += f"  [yellow]{stat}[reset]: {character.stats[stat]}\n";
   
    info += "\n[cyan]skills[reset]:\n";
    for skill in character.skills:
      info += f"  [yellow]{skill}[reset] ({character.skills[skill].rank})\n";
      
    info.rstrip("\n");
    self.ui.panelPrint(info, title = "status", color = "cyan");
   
  def showEquipmentMenu(self, character):
    self.ui.animatedPrint("[bold purple]=== EQUIPMENT ===[reset]");
    
    for part in character.equipment:
      item = character.equipment[part];
      if item != None: self.ui.panelPrint(f"[yellow]{item.name}[reset] ([bold cyan]{round(item.getDurability())}%[reset])", "center", f"{part}");
      else: self.ui.panelPrint("[cyan]EMPTY[reset]", "center", f"{part}");
    self.ui.normalPrint("[yellow]hint: specify the body part to select, type close to exit.[red]\n");
    
  def showMainMenu(self):
    self.ui.clear();
    self.ui.normalPrint("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈");
    self.ui.normalPrint("≈ [bold cyan]simplestRpg[reset] ≈");
    self.ui.normalPrint("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈");

    self.ui.normalPrint("\n• version [green]2.6.7[reset] ([bold red]DEBUG[reset]) •\n")
    self.ui.printTreeMenu("(options)\n", ["[green]start[reset]", "[yellow]quit[reset]"]);
    
  def showCombatInitiateMenu(self):
    self.ui.clear();
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] encounters a [cyan]{self.game.player.enemy.name}[cyan]!");
    self.ui.printTreeMenu("[green](options)[reset]\n", ["[red]fight[reset]", "[red]bail[reset]", "[purple]talk[reset]"]);
    self.showTip();
    if self.game.player.level + 3 < self.game.player.enemy.level: self.ui.panelPrint(f"[red]LEVEL GAP (you < 3)[reset]!", "center");

  def showCombatMenu(self, combat_handler, character):
    self.ui.clear();
    self.ui.showHeader(f"{character.name} vs {character.enemy.name}", "≈");
    
    self.ui.showSeperator("+");
    
    self.ui.normalPrint("≈ [yellow]attack[reset]");
    self.ui.normalPrint("≈ [cyan]block[reset]");
    self.ui.normalPrint("≈ [blue]taunt[reset]");
    self.ui.normalPrint("≈ [green]items[reset]");
    self.ui.normalPrint("≈ [magenta]skills[reset]");
    
    if character.stats["health"] <= character.stats["max health"] * 0.25:
      self.ui.normalPrint("≈ [red]flee[reset]");
    self.ui.newLine();
    
    self.ui.showSeperator("-");
    self.ui.panelPrint(f"POSITION: [yellow]{character.zone}[reset] - [cyan]{character.enemy.zone}[reset]", "center");
    self.ui.showSeperator("-");
    self.ui.showCombatBar(character);
    self.ui.showCombatBar(character.enemy);
    
  def showTip(self):
    self.ui.panelAnimatedPrintFile("tips", "tips", [], "tips");
  
  def showSettingsMenu(self):
    self.ui.clear();
    self.ui.showHeader("Settings", ".");
    self.ui.normalPrint(f"• [yellow]type speed[reset] : {self.game.settings["type speed"]}");
    self.ui.normalPrint(f"• [cyan]delay speed[reset] : {self.game.settings["delay speed"]}");
    self.ui.newLine();
  
    