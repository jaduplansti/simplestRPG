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
    self.ui.clear()
    self.ui.animatedPrint(f"[yellow]{character.name}[reset] calls out [green](STATUS)[reset]")
    self.ui.animatedPrint(f"[blue]Level: {character.level}[reset] | [cyan]XP: {character.exp}/{character.level * 100}[reset]")
    self.ui.animatedPrint(f"[yellow]{character.name}[reset] has [red]{character.stats['health']} HP[reset] / [red]{character.stats['max health']} HP[reset]")
    if character.stats['health'] < 0.3 * character.stats['max health']:
        self.ui.animatedPrint(f"[bold red]Warning: Low health![/reset] Consider healing soon.")
    elif character.stats['health'] < 0.6 * character.stats['max health']:
        self.ui.animatedPrint(f"[orange]Caution: Health is getting low.[reset]")
    self.ui.animatedPrint(f"[yellow]{character.name}[reset] has [magenta]{character.energy} Energy[reset]")
    self.ui.animatedPrint(f"[yellow]{character.name}[reset] has [blue]{character.stats['strength']} Strength[reset]")
    self.ui.animatedPrint(f"[yellow]{character.name}[reset] has [green]{character.stats['defense']} Defense[reset]")
    self.ui.animatedPrint(f"[yellow]{character.name}[reset] has [purple]{character.stats['luck'] * 100}% Luck[reset]")
  
  def showMainMenu(self):
    self.ui.clear();
    self.ui.normalPrint("×××××××××××××××");
    self.ui.normalPrint("× [bold cyan]simplestRpg[reset] ×");
    self.ui.normalPrint("×××××××××××××××");
    self.ui.normalPrint("\n• version [green]2.0[reset] •\n")

    self.ui.printTreeMenu("(options)\n", ["[green]start[reset]", "[yellow]quit[reset]"]);
    
  def showHomeMenu(self):
    self.ui.clear();
    self.ui.normalPrint("••••••••••••••");
    self.ui.normalPrint("• [italic yellow]Your House[reset] •");
    self.ui.normalPrint("••••••••••••••\n");
    
    self.ui.normalPrint("× [green]stats[reset]");
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
    