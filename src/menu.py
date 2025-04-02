from rich.table import Table;
from rich import print, box;

class Menu():
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
  
  def showStatsRankMenu(self, character):
    stats_table = Table(f"{character.name} Stats", box = box.DOUBLE);
    stats_table.add_column("Rank");
    for stat in character.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", f"[blue]({character.getRankBasedOnStat(stat)})[reset]");
    self.ui.normalPrint(stats_table);
    self.ui.newLine();

  def showStatsMenu(self, character):
    stats_table = Table(f"{character.name} Stats", box = box.DOUBLE);
    stats_table.add_column("Value");
    for stat in character.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", f"[{character.getColorBasedOnStat(stat)}]{character.stats[stat]}[reset]");
    self.ui.normalPrint(stats_table);
    self.ui.newLine();

  def showStatsEvaluationMenu(self, character):
    stats_table = Table(f"{character.name} Stats", box = box.DOUBLE);
    stats_table.add_column("Evaluation");
    for stat in character.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", self.ui.showStatEvaluation(stat, character.stats[stat], character.level));
    self.ui.normalPrint(stats_table);
    self.ui.newLine();
    
  def showStatCompareMenu(self, character1, character2):
    stats_table = Table(f"Stat", box = box.DOUBLE);
    stats_table.add_column("You");
    stats_table.add_column(f"{character2.name}");
    for stat in character1.stats:
      stats_table.add_row(f"[yellow]{stat}[reset]", f"[{character1.getColorBasedOnStat(stat)}]{character1.stats[stat]}[reset]", f"[{character2.getColorBasedOnStat(stat)}]{character2.stats[stat]}[reset]");
    self.ui.normalPrint(stats_table);
    self.ui.newLine();
    self.ui.awaitKey();
    
  def showMainMenu(self):
    self.ui.clear();
    self.ui.normalPrint("×××××××××××××××");
    self.ui.normalPrint("× [bold cyan]simplestRpg[reset] ×");
    self.ui.normalPrint("×××××××××××××××");
    self.ui.normalPrint("\n• version [green]1.9[reset] •\n")

    self.ui.printTreeMenu("(options)\n", ["[green]start[reset]", "[yellow]quit[reset]"]);
    
  def showStatsQueryMenu(self):
    self.ui.clear();
    self.ui.normalPrint("••••••••••••••");
    self.ui.normalPrint("• [italic yellow]Stat Query[reset] •");
    self.ui.normalPrint("••••••••••••••\n");
    
    self.ui.normalPrint("× [green]stats[reset]");
    self.ui.normalPrint("× [yellow]evaluation[reset]");
    self.ui.normalPrint("× [cyan]rank[reset]");
    self.ui.normalPrint("× [red]back[reset]\n");
 
  def showHomeMenu(self):
    self.ui.clear();
    self.ui.normalPrint("••••••••••••••");
    self.ui.normalPrint("• [italic yellow]Your House[reset] •");
    self.ui.normalPrint("••••••••••••••\n");
    
    self.ui.normalPrint("× [yellow]you[reset]");
    self.ui.normalPrint("× [purple]practice[reset]");
    self.ui.normalPrint("× [blue]sleep[reset]\n");
  
  def showYouMenu(self):
    self.ui.clear();
    self.ui.showHeader("YOU", "-");
    
    self.ui.normalPrint("× [cyan]stats[reset]");
    self.ui.normalPrint("× [green]items[reset]");
    self.ui.normalPrint("× [red]back[reset]\n");

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
    