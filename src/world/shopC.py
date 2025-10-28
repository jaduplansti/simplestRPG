from objects.item import getItem, ITEMS;
from copy import deepcopy;

class Shop:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    self.shopkeeper = self.createShopKeeper();

    self.stock = {};
  
  def createShopKeeper(self):
    return None;
    
  def stockExists(self, name):
    return name in self.stock;
  
  def removeStock(self, name, n = 1):
    n = max(self.stock[name][1] - n, 0);
    self.stock[name][1] = n;
      
  def addStock(self, name, n = 1):
    item = getItem(name);
    if not self.stockExists(name): self.stock.update({name : [item, n]});
    else: self.stock[name][1] += n;
    
  def cycleStock(self, categories):
    for name in ITEMS:
      if ITEMS[name]["item"]._type in categories:
        self.addStock(name);
  
  def calculatePrice(self, name, interest = 0.1, time = 1):
    item = deepcopy(self.stock[name][0]);
    interest = round(item.getValue() * interest * time); # I = prt;
    return round(item.getValue() + interest);
    
  def buy(self, character, name, price):
    item = deepcopy(self.stock[name][0]);
    character.addItemToInventory(item);
    character.money -= price;
    self.shopkeeper.money += price;
    self.removeStock(name);
    
  def sell(self, character, name, price):
    item = character.getItem(name);
    self.addStock(name);
    character.usedItem(name);
    self.shopkeeper.money -= price;
    character.money += price;
    
  def enter(self):
    self.cycleStock(["potion", "book", "sword"]);
    self.handleMenu();