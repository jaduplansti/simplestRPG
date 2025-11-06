from interface.submenu import SubMenu;
from random import choices;
from mechanics.cooking import Cooker;
from world.farm import Farm;

class Home(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    self.max_page = 3;
    
    self.info = {};
    self.cooker = Cooker(self.game);
    self.farm = Farm(self.game);
    
  def showHouseMenu(self):
    self.game.story_handler.handleStory();
    self.ui.clear();

    self.ui.showSeperator("-");
    self.game.menu.showPlayerMenu();
    self.ui.showSeperator("-");
    
    self.ui.normalPrint("•••••••••••••");
    self.ui.normalPrint("• [italic yellow]Your Home[reset] •");
    self.ui.normalPrint("•••••••••••••\n");
    
    self.ui.normalPrint(f"(page {self.page})\n");
    self.ui.normalPrint(f"its currently {"day" if self.game.clock.isDay() else "night"} time.\n");
    
    if self.page == 1:
      self.ui.panelPrint("[green]stats[reset] (📈)\n[cyan]items[reset] (💼)\n[purple]spar[reset] (🤺)\n[blue]gear[reset] (🪖)\n[yellow]next[reset] (↪)",
      "center"
      "commands",
      expand = False,
      centered = True,
      );
     
    elif self.page == 2:
      self.ui.panelPrint("[magenta]travel[reset] (🚪)\n[blue]sleep[reset] (🛌)\n[blue]quest[reset] (🗒)\n[green]settings[reset] (🔗)\n[yellow]next/back[reset] (↪)",
      "center"
      "commands",
      expand = False,
      centered = True,
      );
    
    else:
      self.ui.panelPrint("[cyan]cook[reset] (🍳)\n[yellow]farm[reset] (🌾)\n[blue]skills[reset] (✨)\n[yellow]back[reset] (↩)",
      "center"
      "commands",
      expand = False,
      centered = True,
      );
    
  def handleHome(self):
    self.game.handleMenu(
      {
        "items" : self.game.handleUseItem, 
        "stats" : self.game.handleStatsMenu,
        "spar" : self.game.initiateFight,
        "sleep" : self.game.handleSleep,
        "settings" : self.game.handleSettings,
        "gear" : self.game.handleEquipment,
        "cook" : self.cooker.handleFoodSelect,
        "quest" : self.game.handleQuest,
        "travel" : self.game.exploration_handler.explore,
        "farm": self.farm.handleFarm,
        "skills": self.game.handleSkillTree,
        "next": self.nextPage,
        "back": self.prevPage,
      }, 
      self.showHouseMenu,
    );
    
  def enter(self):
    self.handleHome();