from submenu import SubMenu;
from random import choices;

class Home(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    self.max_page = 2;
    
    self.info = {};
  
  def showCharacterThoughts(self):
    if self.game.player.stats["health"] <= (self.game.player.stats["max health"] * 0.4):
      self.ui.printDialogue(self.game.player.name, [
        "my wounds hurt...",
        "ugh... i need to recover.",
        "i can't take much more of this.",
        "every step burns.",
        "i'm barely holding on..."
      ])
    elif self.game.player.energy <= 50:
      self.ui.printDialogue(self.game.player.name, [
        "i need sleep...",
        "my body’s giving out.",
        "i should rest soon.",
        "can’t stay awake much longer...",
        "so tired..."
      ])
    elif self.game.player.hunger <= 50:
      self.ui.printDialogue(self.game.player.name, [
        "food... please...",
        "my stomach is grumbling.",
        "i should eat something.",
        "i'm starving here...",
        "i could eat anything right now."
      ])
    else:
      self.ui.normalPrint(f"~ [yellow]{self.game.player.name}[reset] has a moment to think.\n")
    
  def showHouseMenu(self):
    self.ui.clear();
    self.ui.showSeperator("-");
    self.game.menu.showPlayerMenu();
    self.ui.showSeperator("-");
    
    self.ui.normalPrint("•••••••••••••");
    self.ui.normalPrint("• [italic yellow]Your Home[reset] •");
    self.ui.normalPrint("•••••••••••••\n");
    
    self.ui.normalPrint(f"(page {self.page})\n");
    self.showCharacterThoughts();
    
    if self.page == 1:
      self.ui.normalPrint("> [green]stats[reset] (📈)");
      self.ui.normalPrint("> [cyan]items[reset] (💼)");
      self.ui.normalPrint("> [purple]practice[reset] (🤺)");
      self.ui.normalPrint("> [blue]gear[reset] (🪖)");
      self.ui.normalPrint("> [yellow]next[reset] (↪)\n");
    else:
      self.ui.normalPrint("> [magenta]go outside[reset] (🚪)");
      self.ui.normalPrint("> [blue]sleep[reset] (🛌)");
      self.ui.normalPrint("> [blue]quest[reset] (🗒)");
      self.ui.normalPrint("> [green]settings[reset] (🔗)");
      self.ui.normalPrint("> [yellow]back[reset] (↩)\n");
    
  def handleHome(self):
    self.game.handleMenu(
      {
        "items" : self.game.handleUseItem, 
        "stats" : self.game.handleStatsMenu,
        "practice" : self.game.initiateFight,
        "sleep" : self.game.handleSleep,
        "settings" : self.game.handleSettings,
        "gear" : self.game.handleEquipment,
        "quest" : self.game.handleQuest,
        "go outside" : self.game.exploration_handler.explore,
        "next": self.nextPage,
        "back": self.prevPage,
      }, 
      self.showHouseMenu,
    );
    
  def enter(self):
    self.handleHome();