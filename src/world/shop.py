from interface.submenu import SubMenu;
from objects.item import Item, getItem, ITEMS;
from copy import deepcopy;
from random import uniform, choices, randint;
from objects.npc import NPC;
from mechanics.combat import CombatHandler;
import os;

# add bulk buying

class Shop(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    
    self.dave = NPC("dave");
    self.dave.money = 5000;
    
    self.sell_failed_items = [];
    self.items = {};
    self.player_debt = 0;
    
    self.negotiate_value = None;
  
  def setMoney(self, n):
    self.dave.money = n;
    self.game.player.area_data["shop"]["money"] = self.dave.money;
 
  def cycleItems(self):
    number_of_items = randint(5, 8);
    for n in range(number_of_items):
      item_name = choices(list(ITEMS))[0];
      amount = randint(1, 20);
      for n in range(amount): self.__add_stock(item_name);
    
    if self.game.player.area_data["shop"]["reserved item"] != None and self.game.player.area_data["shop"]["reserved item"] not in self.items:
      self.__add_stock(self.game.player.area_data["shop"]["reserved item"]);
      
  def showShopMenu(self):
    self.ui.clear();
    self.ui.printArtPanel("dave shop");
    dialogue = f"{self.ui.getDialogue("dave", "welcome", None, True)}"
    self.ui.panelPrint(f"{dialogue}\n\n[yellow]{self.game.player.money}g[reset] 💰\n\n([yellow]stock[reset] 💳) ↗ ([green]sell[reset] 💸) ↘ ([bold]exit[reset] 🚪)", "center", "Dave's Shop");
  
  def showItemDetail(self, name):
    item = self.items[name][0];
    if self.negotiate_value is None: price = self.calculatePrice(name);
    else: price = self.negotiate_value;
    self.ui.panelPrint(f"[yellow]{item.name}[reset] ({item.rarity})\n\n[underline]{item.desc}[reset]\n\nBase Price: [green]{item.getValue()}[reset]\nSelling Price: [cyan]{price}[reset]\nStock: [blue]{self.items[name][1]}[reset]", "center", name);
    self.ui.normalPrint("≈ [green]buy[reset]");
    self.ui.normalPrint("≈ [bold]negotiate[reset]");
    self.ui.normalPrint("≈ [cyan]reserve[reset]");
    self.ui.normalPrint("≈ [red]back[reset]\n");
  
  def showCloseItems(self, price):
    close_items = self.findCloseItems(price);
    formatted_items = "";
    
    for item in close_items:
      formatted_items += f"[green]{item.name}[reset] > [yellow]{item.getValue()}[reset]g\n";
    formatted_items = formatted_items.rstrip("\n");
    self.ui.panelPrint(formatted_items, title = "exchange");
    
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
      if name == self.game.player.area_data["shop"]["reserved item"]: items += f"(^) {name} - [bold magenta]reserved[reset]\n";
      elif self.items[name][1] <= 0: items += f"(×) {name} (❌) - [yellow]{self.calculatePrice(name)}g[reset]\n";
      else: items += f"(×) {name} - [yellow]{self.calculatePrice(name)}g[reset]\n";
      
    items = items.rstrip("\n");
    self.ui.panelPrint(f"(💼) [green]{self.game.player.getTotalItems()}[reset]\n(🪙) [yellow]{self.game.player.money}[reset]\n\n{items}", title = "stock");
  
  def findCloseItems(self, price, tolerance=0.2):
    close_items = []
    for item_info in self.items.values():
      item = item_info[0];
      item_value = item.getValue()
      if price * (1 - tolerance) <= item_value <= price * (1 + tolerance):
        close_items.append(item)
    return close_items;
  
  def calculatePrice(self, name):
    item = self.items[name][0];
    interest = 0.1 * (self.game.player.area_data["shop"]["stole count"] + 1) 
    if self.game.player.area_data["shop"]["reserved item"] == name: interest += 0.15;
    return round(item.getValue() + (item.getValue() * interest));
  
  def __consume_stock(self, name, n = 1):
    if self.items[name][1] <= 0:
      return;
    
    self.items[name][1] -= n;
  
  def __add_stock(self, name):
    if name in list(self.items):
      self.items[name][1] += 1;
      return
    
    self.items.update({name : [getItem(name), 1]});
  
  def attemptBargain(self, item, price, tries, old_bargain):
    bargain_price = uniform(0.75, 1.35);
    
    if tries == 0:
      self.ui.printDialogue(self.dave.name, f"mate id buy that for [green]{round(price * bargain_price)}g[reset]");
      self.ui.normalPrint("([yellow]yes[reset]) to agree, ([red]no[reset]) to decline\n");
      option = self.ui.getInput();
      if option == "yes": return round(price * bargain_price)
      else: return self.attemptBargain(item, price, 1, bargain_price);
    
    else:
      if bargain_price > old_bargain:
        increased_price = round(price * bargain_price);
        self.ui.printDialogue(self.dave.name, f"alright lad, ill raise it to [blue]{increased_price}g[reset]?");
        self.ui.printDialogue(self.dave.name, f"im being really generous today, take it or leave it..");
        self.ui.normalPrint("([yellow]yes[reset]) to agree, ([red]no[reset]) to decline\n");
        option = self.ui.getInput();
        if option == "yes": return increased_price;
        return False;
        
      elif bargain_price < old_bargain:
        reduced_price = round(price * bargain_price);
        decreased_rate = round(abs(1 - bargain_price), 2) * 100;
        self.ui.printDialogue(self.dave.name, f"alright lad, while we were talking, prices went down by [yellow]{decreased_rate}[reset]%");
        self.ui.printDialogue(self.dave.name, f"that would be around [red]{reduced_price}[reset]g!");
        self.ui.printDialogue(self.dave.name, f"so, what is it gonna be?");
        self.ui.normalPrint("([yellow]yes[reset]) to agree, ([red]no[reset]) to decline\n");
        option = self.ui.getInput();
        if option == "yes": return reduced_price;
        return False;

      else:
        return False;
  
  def bulkSell(self, name):
    if self.game.player.getAmountOfItem(name) <= 3: return 1;

    self.ui.printDialogue(self.dave.name, f"i see that you have a couple of [bold]{name}'s[reset] to sell.");
    self.ui.printDialogue(self.dave.name, f"would you like to sell in a bulk?");
    self.ui.normalPrint("([yellow]yes[reset]) to agree, ([red]no[reset]) to decline\n");
    option = self.ui.getInput();
    
    if option == "no": return 1;
    self.ui.normalPrint(f"type the amount to sell, e.g ([green]{self.game.player.getAmountOfItem(name)}[reset])\n");
    amount = self.ui.getInput(num = True);
    
    if int(amount) <= 1:
      self.ui.printDialogue(self.dave.name, f"huh...");
      return 0;
    
    return amount;
    
  def __sell_for_gold(self, item, name):
    amount = self.bulkSell(name);
    sold_price = self.attemptBargain(item, item.getValue() * amount, 0, None);
    if self.dave.money < sold_price:
      self.ui.printDialogue(self.dave.name, "[red]i cant afford that..[reset]");
      return;
      
    if sold_price is False:
      self.ui.printDialogue(self.dave.name, f"[red]fine then..[reset]!");
      self.sell_failed_items.append(name);
      return;
    
    self.game.player.money += sold_price;
    self.setMoney(self.dave.money - sold_price);
    self.__add_stock(name);
    for n in range(amount):
      self.game.player.usedItem(name);
    self.ui.printDialogue(self.dave.name, f"[bold]pleasure doing business lad[reset]!");
    if item.durability < item.max_durability: self.ui.printDialogue(self.dave.name, f"[bold]this is gonna take a while to patch up.[reset]!");
  
  def __sell_for_item(self, item, name):
    item_price = item.getValue();
    close_items = [item.name for item in self.findCloseItems(item_price)];
    self.showCloseItems(item_price);
    picked_item = self.ui.getInput();
    
    if picked_item in close_items:
      self.ui.printDialogue(self.dave.name, f"alright lad, your [yellow]{item.name}[reset] for my [yellow]{picked_item}[reset].");
      
      self.game.player.addItemToInventory(getItem(picked_item), 1);
      self.game.player.usedItem(item.name);
      self.__add_stock(item.name);
      self.__consume_stock(picked_item);
     
      self.ui.printDialogue(self.dave.name, ["thanks mate.", "pleasure.", "great.."]);
    else:
      self.ui.printDialogue(self.dave.name, f"changed your mind eh?");
     

  def __sell(self, name):
    item = self.game.player.getItem(name);
  
    if name in self.sell_failed_items:
      self.ui.printDialogue(self.dave.name, "lad we werent able to strike a deal, lets try next time eh?");
      return;

    self.ui.printDialogue(self.dave.name, "what do you want for that mate?");
    self.ui.printTreeMenu("", ["([yellow]gold[reset]) - receive money", f"([cyan]trade[reset]) - item exchange", "([red]back[reset]) - close the menu"]);
    action = self.ui.getInput();
    if action == "gold": self.__sell_for_gold(item, name);
    elif action == "trade": self.__sell_for_item(item, name);
    else: return;
  
  def __negotiate(self, name):
    if self.negotiate_value != None:
      self.ui.printDialogue(self.dave.name, f"i cant negotiate any further than that lad.");
      return;
      
    self.ui.printDialogue(self.dave.name, f"alright lad, name the price!");
    self.ui.normalPrint(f"type a price, e.g ([green]{self.calculatePrice(name)}[reset]g)\n");
    price = self.ui.getInput(num = True);
    negotiate_ratio = price / self.calculatePrice(name);
    if (negotiate_ratio >= round(uniform(0.8, 0.99), 2)): 
      self.ui.printDialogue(self.dave.name, f"great, ill take [yellow]{price}[reset]g.");
      self.negotiate_value = price;
    else: self.ui.printDialogue(self.dave.name, f"mate i think ill pass on [red]{price}[reset]g, too low..");
   
  def __buy(self, name):
    if self.game.player.area_data["shop"]["killed"] is True: # if dave recently was killed, free items
      self.game.player.addItemToInventory(self.items[name][0], 1);
      self.__consume_stock(name);
      self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] took [yellow]{name}[reset]");
      return; 
      
    if self.items[name][1] <= 0:
      self.ui.printDialogue(self.dave.name, f"sorry lad.... no more [yellow]{name}[reset] on stock!");
      return;
    
    if self.game.player.money < self.calculatePrice(name):
      self.ui.printDialogue(self.dave.name, f"ya dont have enough money lad, you need [green]{round(abs(self.game.player.money - self.calculatePrice(name)))}[reset] more!");
      return;
    
    if self.negotiate_value is None: price = self.handlePromo(name);  
    else: price = self.negotiate_value;
    
    self.game.player.addItemToInventory(self.items[name][0], 1);
    self.game.player.money -= price;
    self.setMoney(self.dave.money + price);
    
    self.__consume_stock(name);
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] bought [yellow]{name}[reset] for [green]{price}[reset]g");
    self.game.player.area_data["shop"]["buy count"] += 1;
    if self.game.player.area_data["shop"]["reserved item"] == name: self.game.player.area_data["shop"]["reserved item"] = None;
    
  def __reserve(self, name):
    self.ui.printDialogue(self.dave.name, [f"ok mate, come back for your [yellow]{name}[reset] later!", f"lad, i reserved [yellow]{name}[reset] for you to buy soon.."]);
    self.ui.animatedPrint("[cyan]you reserved an item![reset] ([bold green]+15% interest[reset])");
    self.game.player.area_data["shop"]["reserved item"] = name;
    
  def handlePromo(self, name):
    if (self.game.player.area_data["shop"]["buy count"] % 3 == 0):
      discount = uniform(0.6, 0.85);
      actual_discount = round((1 - discount) * 100);
      self.ui.printDialogue(self.dave.name, [f"lad, ill give you this for [green]{actual_discount}%[reset] off.", f"lad, here ill give a discount of [green]{actual_discount}[reset]%."]);
      return round(self.calculatePrice(name) * discount);
    else: return self.calculatePrice(name);
  
  def buyDetails(self, name):
    self.negotiate_value = None;
    while True:
      self.ui.clear();
      self.showItemDetail(name);
      option = self.ui.getInput();
      if option == "buy": self.__buy(name);
      elif option == "reserve": self.__reserve(name);
      elif option == "negotiate": self.__negotiate(name);
      elif option == "back": return;
     
      self.ui.awaitKey();
  
  def handleBuy(self):
    while True:
      self.ui.clear();
      self.listItems();
      option = self.ui.getInput(list(self.items));
      if option == "close": return;
      elif option in list(self.items): self.buyDetails(option);
      else: 
        if self.game.player.area_data["shop"]["killed"] is False: self.ui.printDialogue(self.dave.name, [f"mate, i dont sell no {option} here", f"whatchu mean by {option} mate?"]);
      self.ui.awaitKey();
      
  def handleSell(self):
    if self.game.player.area_data["shop"]["killed"] is True:
      return;
      
    while True:
      self.ui.clear();
      self.listSellItems();
      option = self.ui.getInput(list(self.game.player.inventory));
      if option == "close": return;
      elif self.game.player.itemExists(option): self.__sell(option);
      else: pass;
      self.ui.awaitKey();
  
  def handleShop(self):
    self.game.handleMenu(
      {
        "stock" : self.handleBuy, 
        "sell" : self.handleSell,
        "exit" : self.game.exploration_handler.explore,
      }, 
      self.showShopMenu,
    );
  
  def createData(self):
    if "shop" not in self.game.player.area_data:
      self.game.player.area_data.update({"shop" : {}});
      self.game.player.area_data["shop"] = {
        "killed" : False,
        "stole count": 0,
        "money": 100,
        "buy count": 0,
        "reserved item": None,
        "player_debt": 0,
      }
  
  def loadData(self):
    try:
      data = self.game.player.area_data["shop"];
      self.dave.money = data["money"];
      self.player_debt = data["player_debt"];
    except KeyError:
      return -1;
      
  def enter(self):
    self.ui.clear();
    if self.loadData() == -1: self.createData();
    self.cycleItems();
    self.handleShop();