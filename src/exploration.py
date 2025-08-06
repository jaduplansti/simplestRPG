from rich.status import Status;
from time import sleep;
from random import randint, choices;
from combat import CombatHandler;

from home import Home;
from forest import Forest;
from shop import Shop;

from dungeon import Dungeon;
from guild_hall import GuildHall;
from character import Character;

def createArea(name, handler, _next = [], prev = [], enemies = None, position = 0):
  return {name : {
    "handler" : handler,
    "prev" : prev,
    "next" : _next,
    "enemies" : enemies,
    "position" : position
  }};

AREAS = {
  **createArea("home", Home, _next = ["forest", "shop", "guild hall"], position = 0),
  **createArea("forest", Forest, prev = ["home"], _next = ["dungeon"], position = 10),
  **createArea("guild hall", GuildHall, prev = ["home"], position = 8),
  **createArea("shop", Shop, prev = ["home"], position = 5),
  **createArea("dungeon", Dungeon, prev = ["forest"], position = 25),
};

class ExplorationEventHandler:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    
    self.merchant = Character("jacob");
    
  def getRandomEvent(self):
    return choices(["fight", None], [0.05, 0.99])[0];

  def __merchant_buy(self):
    if len(self.merchant.inventory) <= 0:
      self.ui.printDialogue(self.merchant.name, "sorry adventurer...");
      self.ui.printDialogue(self.merchant.name, "i dont have any items sell!");
      self.ui.printDialogue(self.merchant.name, "but i would be willing to buy your stuff.");
      return;
    
    while True:
      pass;
      
  def handleMerchant(self):
    self.ui.clear();
    self.ui.animatedPrint(f"a wandering merchant, approaches you..");
    self.ui.printDialogue(self.merchant.name, "hello adventurer!");
    
    while True:
      self.ui.printTreeMenu("", ["buy", "sell", "talk"]);
      option = self.ui.getInput();
      if option == "buy": self.__merchant_buy();
      elif option == "sell": pass;
      elif option == "talk": pass;
      self.ui.clear();
    
class Exploration:
  def __init__(self, game):
    self.game = game;
    self.ui = self.game.ui;
    self.event_handler = ExplorationEventHandler(game);
    
  def handleGetNext(self, area):
    while True:
      self.ui.clear();
      try:
        for loc in area["next"]: self.ui.normalPrint(f"- [yellow underline]{loc}[reset] ({AREAS[loc]['position']} fyres) ⬆\n");
        for loc in area["prev"]: self.ui.normalPrint(f"- [yellow underline]{loc}[reset] ({AREAS[loc]['position']} fyres) ⬇\n");

        destination_name = self.ui.getInput();
        return [AREAS[destination_name], destination_name];
      except KeyError:
        self.ui.normalPrint("not a valid destination");
        self.ui.awaitKey();
        
  def handleExplore(self, player, destination):
    event = None;
    while player.position != destination["position"]:
      self.ui.clear();
      self.ui.animatedPrint(f"[yellow]{player.name}[reset] started walking");
      with Status("walking", spinner="runner") as status:
        while True:
          if player.position < destination["position"]: player.position += 1;
          elif player.position > destination["position"]: player.position -= 1;
          #event = self.getRandomEvent();
          sleep(0.2);
          status.update(f"[green]walking ({player.position} / {destination['position']})[reset]");
          # event is None
          if player.position == destination["position"]: break;
      #self.handleEvent(event);
  
  def move(self, loc):
    if loc in AREAS:
      self.game.player.location = loc;
      self.game.player.position = AREAS[loc]["position"];
      AREAS[loc]["handler"](self.game).enter();
    else:
      self.ui.animatedPrint("failed to teleport!");

  def explore(self):
    area = AREAS[self.game.player.location];
    destination, destination_name = self.handleGetNext(area);
    self.handleExplore(self.game.player, destination);
    
    self.ui.normalPrint(f"[bold cyan]you have arrived at {destination_name}[reset]\n");
    self.game.player.location = destination_name;
    self.ui.awaitKey();
    
    destination["handler"](self.game).enter();