from submenu import SubMenu;
from item import Item, getItem;
from copy import deepcopy;

class Shop(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    self.items = {
      "health potion" : [getItem("health potion"), 50, 10],
      "wooden arrow" : [getItem("wooden arrow"), 9999, 2],
      "wooden sword" : [getItem("wooden sword"), 60, 20],
      "scroll of teleport" : [getItem("scroll of teleport"), 100, 50],
      "starter chest" : [getItem("starter chest"), 100, 80],
      "bread" : [getItem("bread"), 100, 6],
      "apple" : [getItem("apple"), 100, 1],
      "biscuit" : [getItem("biscuit"), 100, 3],
      "steel sword" : [getItem("steel sword"), 50, 50],
      "kevins sword" : [getItem("kevins sword"), 30, 150],
      "peasant tunic" : [getItem("peasant tunic"), 30, 100],
      "worn leather vest" : [getItem("worn leather vest"), 30, 200],
    };
  
  def showShopInfo(self):
    self.ui.normalPrint(f"× [green]{self.game.player.name}[reset] has [yellow]{self.game.player.money} gold[reset]\n")
    #if len(self.game.player.inventory) > 0: self.ui.normalPrint(f"× items in stock ({len(self.items)})");
    #else: self.ui.normalPrint("× [underline red]no items to sell![reset]\n");
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
    
  def handleBuy(self): # refactor this soon.
    while True:
      self.ui.clear();
      for item in self.items:
        self.ui.normalPrint(f"- [yellow]{item}[reset] ({self.items[item][2]} gold)");
      self.ui.newLine();
    
      option = self.ui.getInput().lower().split(",");
      buy_count = 1;
      
      if option[0] == "close": return;
      try:
        if len(option) >= 2: buy_count = int(option[1]);
      except ValueError:
        self.ui.normalPrint("not a valid count.");
        continue;
        
      try:
        item_obj = self.items[option[0]][0];
        if self.game.player.money >= self.items[option[0]][2] * buy_count:
          self.game.givePlayerItem(option[0], buy_count);
          self.game.player.money -= self.items[option[0]][2] * buy_count;
        else: self.ui.normalPrint(f"{self.game.player.name} does not have enough money\n");
      except KeyError:
        self.ui.normalPrint(f"[red]item {option[0]} does not exist[reset]!\n");
      self.ui.awaitKey();
      
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