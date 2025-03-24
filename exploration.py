from item import Item;

class Bakery: 
  def __init__(self, game): 
    self.game = game;
    self.player = self.game.player;
    self.ui = self.game.ui;
    self.stock = {};
  
  def addStock(self, stock, amount, price, item):
    if self.stockExists(stock) is True:
      self.getStock(stock)["amount"] += amount;
    else:
      self.stock.update({stock : {"amount" : amount, "price" : price, "item" : item}});
      
  def stockExists(self, stock):
    try:
      self.stock[stock];
      return True;
    except KeyError:
      return False;
      
  def listStock(self):
    for food in self.stock:
      self.ui.normalPrint(f"{food} {self.stock[food]["amount"]}x ({self.stock[food]["price"]})");
    self.ui.newLine();
  
  def getStock(self, item):
    return self.stock[item];
    
  def buyStock(self, item):
    if self.stockExists(item) is False:
      self.ui.animatedPrint(f"i dont sell anythin called {self.ui.coloredString(item, "red")}");
      return;
    
    if self.player.money < self.getStock(item)["price"]:
      self.ui.animatedPrint(f"you dont have enough money");
      return;
      
    self.player.money -= self.getStock(item)["price"];
    self.getStock(item)["amount"] -= 1;
    self.player.inventory.update({item : self.getStock(item)["item"]})
    self.ui.animatedPrint(f"you bought {self.ui.coloredString(item, "red")} for {self.ui.coloredString(self.getStock(item)["price"], "green")} gold.");

    if self.getStock(item)["amount"] <= 0:
      del self.stock[item];
    
  def bakeryMenu(self):
    while True:
      self.ui.showDynamicMenu(self.player);
      option = self.ui.getInput();
      
      if option == "list foods":
        self.listStock();
      elif option == "buy food":
        self.buyStock(self.ui.getInput());
      elif option == "go back":
        self.player.setLocation("market")
        return;
      
      self.ui.awaitKey();
      
class MoveMenuHandler:
  def __init__(self, game):
    self.game = game;
    self.player = self.game.player;
    self.ui = self.game.ui;
    
    self.bakery = Bakery(self.game);
    self.bakery.addStock("bread", 1, 1, Item("bread"));
    self.bakery.addStock("apple pie", 10, 1, Item("bread"));

  def homeTravelMenu(self):
    while True:
      self.ui.showDynamicMenu(self.player);
      option = self.ui.getInput();
      
      if option == "market":
        self.player.setLocation("market");
        self.marketMenu();
      elif option == "go back":
        return;
        
  def marketMenu(self):
    while True:
      self.ui.showDynamicMenu(self.player);
      option = self.ui.getInput();
      
      if option == "bakery":
        self.player.setLocation("bakery");
        self.bakery.bakeryMenu();
      elif option == "go back":
        self.player.setLocation("home");
        return;
        