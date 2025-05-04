from submenu import SubMenu;
from item import Item, getItem;
from copy import deepcopy;

class Shop(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    self.items = {
      "health potion" : [getItem("health potion"), 20, 1],
    };
  
  def showShopInfo(self):
    self.ui.normalPrint(f"× [green]{self.game.player.name}[reset] has [yellow]{self.game.player.money} gold[reset]\n")
    if len(self.game.player.inventory) > 0: self.ui.normalPrint(f"× top item is the [bold yellow]{list(self.game.player.inventory.keys())[-1]}[reset]\n");
    else: self.ui.normalPrint("× [underline red]no items to sell![reset]\n");
    self.ui.normalPrint(f"× {len(self.items)} items in stock!\n");
    
  def showShopMenu(self):
    self.ui.clear();
    self.showShopInfo();
    self.ui.showSeperator("=");
    
    self.ui.normalPrint("≈ [yellow]buy[reset]");
    self.ui.normalPrint("≈ [cyan]sell[reset]");
    self.ui.normalPrint("≈ [red]exit[reset]\n");
  
  def evaluateItem(self, name): # todo: evaluate item price
    item = self.game.player.getItem(name);
    return 1;
    
  def handleBuy(self):
    self.ui.clear();
    for item in self.items:
      self.ui.normalPrint(f"- [yellow]{item}[reset] ({self.items[item][2]} gold)");
    self.ui.newLine();
    
    option = self.ui.getInput().lower();
    
    try:
      item_obj = self.items[option][0];
      if self.game.player.money >= self.items[option][2]:
        self.game.givePlayerItem(option);
        self.game.player.money -= self.items[option][2];
      else: self.ui.normalPrint(f"{self.game.player.name} does not have enough money\n");
    except KeyError:
      self.ui.normalPrint(f"[red]item {option} does not exist[reset]!\n");
  
  def handleSell(self):
    self.ui.normalPrint("NOT ADDED!");
    
  def handleShop(self):
    self.game.handleMenu(
      {
        "buy" : self.handleBuy, 
        "sell" : self.handleSell,
        "exit" : self.game.exploration_handler.explore,
      }, 
      self.showShopMenu,
    );
    
  def enter(self):
    self.handleShop();