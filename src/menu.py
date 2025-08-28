from rich.table import Table;
from rich import print, box;
from art import ARTS;

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
      self.ui.panelPrint(f"{quest.desc}", "center", f"{quest_name} ({quest.progress})");
 
  def showItemDetails(self, character, name):
    item = character.getItem(name);
    self.ui.panelPrint(f"[yellow]{item.name}[reset] ([green]{item.rarity}[reset]) ([blue]{item.rank}[reset])\n\n{item.desc}\n\nAmount: {character.getAmountOfItem(name)}\nWeight: {item.weight} kg\nSlot: {item.bodypart}\nDurability: {item.durability}/{item.max_durability}", "center", "item details");

    self.ui.normalPrint("≈ [green]use[reset]");
    self.ui.normalPrint("≈ [red]drop[reset]");
    self.ui.normalPrint("≈ [yellow]back[reset]\n");
  
  def showItemsMenu(self, character):
    items = "";
    for name in character.inventory:
      items += f"> [yellow]{name}[reset] ([green]{character.getAmountOfItem(name)}[reset])\n";
    items = items.rstrip();
    self.ui.animatedPrint(f"[cyan]===INVENTORY===[reset]");
    self.ui.panelPrint(items, title = f"ITEMS ({character.getTotalItems()})");
    self.ui.normalPrint(f"[yellow]hint: select an item by typing its name or type close to exit[reset]\n");
    
  def showSkillDetails(self, character, name):
    skill = character.skills[name];
    if skill.passive is False: self.ui.panelPrint(f"[yellow]{skill.name}[reset] ([green]{skill.rank}[reset]) ([blue]{skill.energy}[reset] mp)\n\n{skill.desc}\n\nRange: {skill.range} (↘↙↗↘)\nStyle: {skill._style}", "center", "skill details");
    else: self.ui.panelPrint(f"[yellow]{skill.name}[reset] ([green]{skill.rank}[reset]) ([yellow]PASSIVE[reset])\n\n{skill.desc}\n\nRange: {skill.range} (↘↙↗↘)\nClass: {skill._class}", "center", "skill details");

    if skill.passive != True: self.ui.normalPrint("≈ [green]use[reset]");
    self.ui.normalPrint("≈ [yellow]back[reset]\n");

  def showSkillsMenu(self, character):
    self.ui.animatedPrint(f"[magenta]==SKILLS==[reset]");
    skills = "";
    for skill_name in character.skills:
      skill = character.skills[skill_name];
      skills += f"💠 [bold]{skill_name}[reset]\n   Rank: [green]{skill.rank}[reset]\n   Energy: [blue]{skill.energy}[reset]\n\n";
    skills = skills.rstrip("\n");
    self.ui.panelPrint(skills, title = "skills");
      
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
  
  def showEquipmentDetails(self, character, part):
    item = character.equipment[part];
    if item != None: self.ui.panelPrint(f"[underline yellow]{item.name} ({round(item.getDurability())}%)[reset]\n\n{item.desc}\n\n{item.formatBonus()}", "center", "item details");
    else: self.ui.panelPrint(f"[underline yellow]empty[reset]\n\ntheres nothing here..", "center", "item details");

    if item != None: self.ui.normalPrint("≈ [red]unequip[reset]");
    self.ui.normalPrint("≈ [yellow]back[reset]\n");

  def showMainMenu(self):
    self.ui.clear();
    self.ui.normalPrint("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈");
    self.ui.normalPrint("≈ [bold cyan]simplestRpg[reset] ≈");
    self.ui.normalPrint("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈");

    self.ui.normalPrint("\n• version [green]2.7.1[reset] ([bold blue]ALPHA[reset]) •\n")
    self.ui.printTreeMenu("(options)\n", ["[green]start[reset]", "[yellow]quit[reset]"]);
    
  def showCombatInitiateMenu(self):
    self.ui.clear();
    try:
      self.ui.printArtPanel(ARTS[self.game.player.enemy.name]);
    except KeyError:
      pass;
      
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] encounters a [cyan]{self.game.player.enemy.name}[cyan]!");
    self.ui.printTreeMenu("[green](options)[reset]\n", ["[red]fight[reset]", "[red]bail[reset]", "[purple]talk[reset]"]);
    self.showTip();
    if self.game.player.level + 3 < self.game.player.enemy.level: self.ui.panelPrint(f"[red]LEVEL GAP (you < 3)[reset]!", "center");

  def showCombatMenu(self, combat_handler, character):
    self.ui.clear();
    self.ui.showHeader(f"{character.name} vs {character.enemy.name}", "≈");
    
    self.ui.showSeperator("+");
    
    self.ui.normalPrint("≈ [yellow]attack[reset] (🗡)");
    self.ui.normalPrint("≈ [cyan]block[reset] (🛑)");
    self.ui.normalPrint("≈ [blue]taunt[reset] (🖕)");
    self.ui.normalPrint("≈ [green]items[reset] (💼)");
    self.ui.normalPrint("≈ [magenta]skills[reset] (💥)");
    
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
    self.ui.normalPrint(f"• [red]delete[reset]");
    self.ui.newLine();
  
  def showStatAllocateMenu(self, stat):
    self.ui.panelPrint(f"{stat} ({self.game.player.stats[stat]})\npoints: {self.game.player.points}", "center");
    self.ui.normalPrint("[yellow]press (w/s) to allocate or deallocate points, press (enter) to close[reset]\n");