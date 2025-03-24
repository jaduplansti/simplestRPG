from item import Item;

class Bakery: 
  def __init__(self, game): 
    self.game = game;
    self.player = self.game.player;
    self.ui = self.game.ui;
    
    self.stock = {};
    self.sold_stock = [];
    
  def addStock(self, stock, amount, price, item):
    if self.stockExists(stock) is True:
      self.getStock(stock)["amount"] += amount;
    else:
      self.stock.update({stock : {"amount" : amount, "price" : price, "item" : item}});
  
  def soldStock(self, stock):
    self.sold_stock.append(self.getStock(stock));
    del self.stock[stock];
    
  def stockExists(self, stock):
    try:
      self.stock[stock];
      return True;
    except KeyError:
      return False;
  
  def isSoldOut(self, stock):
    for stock2 in self.sold_stock:
      if stock2["item"].name == stock:
        return True;
    return False;
      
  def listStock(self):
    self.ui.showDialogue("baker", "here's a list of what i baked.");
    for food in self.stock:
      self.ui.normalPrint(f"{self.ui.coloredString(food, "magenta")} {self.stock[food]["amount"]}x ({self.ui.coloredString(self.stock[food]["price"], "yellow")} gold)");
    self.ui.newLine();
  
  def getStock(self, item):
    return self.stock[item];
    
  def buyStock(self, item):
    if item == "":
      self.ui.showDialogue("baker", f"you didnt specify what to {self.ui.coloredString("buy", "red")}.");
      return;
    elif self.isSoldOut(item) is True:
      self.ui.showDialogue("baker", f"sorry, we ran out of {self.ui.coloredString(item, "red")}.");
      return;
    elif self.stockExists(item) is False:
      self.ui.showDialogue("baker", f"i dont sell anythin called {self.ui.coloredString(item, "red")}");
      return;
    
    if self.player.money < self.getStock(item)["price"]:
      self.ui.showDialogue("baker", f"you dont have enough money.");
      return;
      
    self.player.money -= self.getStock(item)["price"];
    self.getStock(item)["amount"] -= 1;
    self.player.inventory.update({item : self.getStock(item)["item"]})
    self.ui.showDialogue("baker", f"here is your {self.ui.coloredString(item, "red")} for {self.ui.coloredString(self.getStock(item)["price"], "green")} gold.");

    if self.getStock(item)["amount"] <= 0:
      self.soldStock(item);
    
  def bakeryMenu(self):
    while True:
      self.ui.showDynamicMenu(self.player);
      option = self.ui.getInput();
      
      if option == "list foods":
        self.listStock();
      elif option == "buy food":
        self.ui.showDialogue("baker", "what are you going to buy?");
        self.buyStock(self.ui.getInput());
      elif option == "attack":
        self.game.initiateCombat("baker");
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
        