from submenu import SubMenu;

class Home(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    self.max_page = 2;
    
  def showHouseMenu(self):
    self.ui.clear();
    self.ui.showSeperator("-");
    self.game.menu.showPlayerMenu();
    self.ui.showSeperator("-");
    
    self.ui.normalPrint("•••••••••••••");
    self.ui.normalPrint("• [italic yellow]Your Home[reset] •");
    self.ui.normalPrint("•••••••••••••\n");
    
    self.ui.normalPrint(f"(page {self.page})\n");
    if self.page == 1:
      self.ui.normalPrint("≈ [green]stats[reset]");
      self.ui.normalPrint("≈ [cyan]items[reset]");
      self.ui.normalPrint("≈ [purple]practice[reset]");
      self.ui.normalPrint("≈ [blue]gear[reset]");
      self.ui.normalPrint("≈ [yellow]next[reset]\n");
    else:
      self.ui.normalPrint("≈ [magenta]go outside[reset]");
      self.ui.normalPrint("≈ [blue]sleep[reset]");
      self.ui.normalPrint("≈ [blue]quest[reset]");
      self.ui.normalPrint("≈ [green]settings[reset]");
      self.ui.normalPrint("≈ [yellow]back[reset]\n");
    
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