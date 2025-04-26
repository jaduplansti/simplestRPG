from submenu import SubMenu;
from item import Item;

class Shop(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    self.items = {
      "health potion" : [Item("health potion"), 20, 1],
    };
    
  def showShopMenu(self):
    self.ui.clear();
    
    self.ui.showHeader("SHOP", "*");
    self.ui.normalPrint("≈ [green]buy[reset]");
    self.ui.normalPrint("≈ [red]sell[reset]");
    self.ui.normalPrint("≈ [red]exit[reset]");
  
  def handleBuy(self):
    for item in self.items:
      self.ui.normalPrint(f"- [yellow]{item}[reset] ({self.items[item][2]} gold)");
    self.ui.newLine();
    
    option = self.ui.getInput().lower();
    try:
      item_obj = self.items[option][0];
      if self.game.player.money >= self.items[option][2]:
        self.game.player.addItemToInventory(item_obj, 1);
      else: self.ui.normalPrint("not enough coins\n");
    except KeyError:
      self.ui.normalPrint("item does not exist!\n");
  
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