from submenu import SubMenu;
from item import Item, getItem;
from copy import deepcopy;
from random import uniform;
from character import Character;
from enemy import characterToEnemy;

class Shop(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    
    self.dave = Character("dave");
    self.dave.money = 100;
    
    self.items = {
      "health potion" : [getItem("health potion"), 50],
      "wooden arrow" : [getItem("wooden arrow"), 9999],
      "wooden sword" : [getItem("wooden sword"), 60],
      "scroll of teleport" : [getItem("scroll of teleport"), 100],
      "starter chest" : [getItem("starter chest"), 100],
      "bread" : [getItem("bread"), 100],
      "apple" : [getItem("apple"), 100],
      "biscuit" : [getItem("biscuit"), 100],
      "steel sword" : [getItem("steel sword"), 50],
      "kevins sword" : [getItem("kevins sword"), 30],
      "peasant tunic" : [getItem("peasant tunic"), 30],
      "worn leather vest" : [getItem("worn leather vest"), 30],
      "ashrend sword" : [getItem("ashrend sword"), 30],
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
  
  def showItemDetail(self, name):
    item = self.items[name][0];
    self.ui.panelPrint(f"[yellow]{item.name}[reset] ({item.rarity})\n\n[underline]{item.desc}[reset]\n\nBase Price: [green]{item.getValue()}[reset]\nSelling Price: [cyan]{self.calculatePrice(item.name)}[reset]\nStock: [blue]{self.items[name][1]}[reset]", "center", name);
    self.ui.normalPrint("≈ [green]buy[reset]");
    self.ui.normalPrint("≈ [red]back[back]\n");
  
  def listSellItems(self):
    items = "";
    for name in self.game.player.inventory:
      item = self.game.player.getItem(name);
      if self.dave.money < item.getValue(): items += f"(😐) [red]{name}[reset] - [yellow]{item.getValue()}g[reset]\n";
      else: items += f"(🤑) [green]{name}[reset] - [yellow]{item.getValue()}g[reset]\n";
    items = items.rstrip("\n");
    self.ui.panelPrint(f"(💼) [green]{self.game.player.getTotalItems()}[reset]\n(🪙) [yellow]{self.game.player.money}[reset]\n\n{items}", title = f"{self.game.player.name} items");

  def listItems(self):
    items = "";
    for name in self.items:
      if self.items[name][1] <= 0: items += f"(×) {name} (❌) - [yellow]{self.calculatePrice(name)}g[reset]\n";
      else: items += f"(×) {name} - [yellow]{self.calculatePrice(name)}g[reset]\n";
      
    items = items.rstrip("\n");
    self.ui.panelPrint(f"(💼) [green]{self.game.player.getTotalItems()}[reset]\n(🪙) [yellow]{self.game.player.money}[reset]\n\n{items}", title = "stock");
    
  def calculatePrice(self, name):
    item = self.items[name][0];
    return round(item.getValue() + (item.getValue() * 0.1));
  
  def __consume_stock(self, name):
    if self.items[name][1] <= 0:
      return;
    
    self.items[name][1] -= 1;
  
  def __add_stock(self, name):
    if name in list(self.items):
      self.items[name][1] += 1;
      return
    
    self.items.update({name : [getItem(name), 1]});
  
  def attemptBargain(self, item, price, tries, old_bargain):
    bargain_price = uniform(0.75, 1.35);
    
    if tries == 0:
      self.ui.printDialogue("dave", f"mate id buy that for [green]{round(item.getValue() * bargain_price)}g[reset]");
      self.ui.normalPrint("([yellow]yes[reset]) to agree, ([red]no[reset]) to decline\n");
      option = self.ui.getInput();
      if option == "yes": return round(price * bargain_price)
      else: return self.attemptBargain(item, price, 1, bargain_price);
    
    else:
      if bargain_price > old_bargain:
        increased_price = round(price * bargain_price);
        self.ui.printDialogue("dave", f"alright lad, ill raise it to [blue]{increased_price}g[reset]?");
        self.ui.printDialogue("dave", f"im being really generous today, take it or leave it..");
        self.ui.normalPrint("([yellow]yes[reset]) to agree, ([red]no[reset]) to decline\n");
        option = self.ui.getInput();
        if option == "yes": return increased_price;
        return False;
        
      elif bargain_price < old_bargain:
        reduced_price = round(price * bargain_price);
        decreased_rate = round(abs(1 - bargain_price), 2) * 100;
        self.ui.printDialogue("dave", f"alright lad, while we were talking, prices went down by [yellow]{decreased_rate}[reset]%");
        self.ui.printDialogue("dave", f"that would be around [red]{reduced_price}[reset]g!");
        self.ui.printDialogue("dave", f"so, what is it gonna be?");
        self.ui.normalPrint("([yellow]yes[reset]) to agree, ([red]no[reset]) to decline\n");
        option = self.ui.getInput();
        if option == "yes": return reduced_price;
        return False;

      else:
        return False;

  def __sell(self, name):
    item = self.game.player.getItem(name);
    if self.dave.money < item.getValue():
      self.ui.printDialogue("dave", "[red]i cant afford that..[reset]");
      return;
    
    sold_price = self.attemptBargain(item, item.getValue(), 0, None);
    if sold_price is False:
      self.ui.printDialogue("dave", f"[red]fine then..[reset]!");
      return;
    
    self.game.player.money += sold_price;
    self.dave.money -= sold_price;
    self.__add_stock(name);
    self.game.player.usedItem(name);
    self.ui.printDialogue("dave", f"[bold]pleasure doing business lad[reset]!");
    if item.durability < item.max_durability: self.ui.printDialogue("dave", f"[bold]this is gonna take a while to patch up.[reset]!");

  def __buy(self, name):
    if self.items[name][1] <= 0:
      self.ui.printDialogue("dave", f"sorry lad.... no more [yellow]{name}[reset] on stock!");
      return;
      
    if self.game.player.money <= self.calculatePrice(name):
      self.ui.printDialogue("dave", f"ya dont have enough money lad, you need [green]{round(abs(self.game.player.money - self.calculatePrice(name)))}[reset] more!");
      return;
    
    self.game.player.addItemToInventory(self.items[name][0], 1);
    self.game.player.money -= self.calculatePrice(name);
    self.dave.money += self.calculatePrice(name);
    
    self.__consume_stock(name);
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] bought [yellow]{name}[reset]");
    
  def buyDetails(self, name):
    while True:
      self.ui.clear();
      self.showItemDetail(name);
      option = self.ui.getInput();
      if option == "buy": self.__buy(name);
      elif option == "back": return;
      self.ui.awaitKey();
  
  def handleBuy(self):
    while True:
      self.ui.clear();
      self.listItems();
      option = self.ui.getInput();
      if option == "close": return;
      elif option in list(self.items): self.buyDetails(option);
      else: self.ui.printDialogue("dave", [f"mate, i dont sell no {option} here", f"whatchu mean by {option} mate?"]);
      self.ui.awaitKey();
      
  def handleSell(self):
    while True:
      self.ui.clear();
      self.listSellItems();
      option = self.ui.getInput();
      if option == "close": return;
      elif self.game.player.itemExists(option): self.__sell(option);
      else: pass;
      self.ui.awaitKey();
  
  def handleRob(self):
    pass;
    
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