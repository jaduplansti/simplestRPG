from rich.status import Status;
from time import sleep;
from random import randint, choices;
from combat import CombatHandler;

from home import Home;
from forest import Forest;
from shop import Shop;

from dungeon import Dungeon;
from guild_hall import GuildHall;

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

class Exploration:
  def __init__(self, game):
    self.game = game;
    self.ui = self.game.ui;

  def getRandomEvent(self):
    return choices(["fight", None], [0.05, 0.99])[0];

  def handleEvent(self, event):
    if event == "fight":
      CombatHandler(self.game).initiateFightNpc(self.game.player, "slime");
      self.ui.awaitKey();
    elif event == "loot":
      #self.game.player.addInventory();
      pass;
      
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
          event = self.getRandomEvent();
          sleep(0.2);
          status.update(f"[green]walking ({player.position} / {destination['position']})[reset]");
          if event is not None or player.position == destination["position"]: break;
      self.handleEvent(event);
  
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