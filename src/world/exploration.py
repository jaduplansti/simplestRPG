from rich.status import Status;
from time import sleep;
from random import randint, choices;
from mechanics.combat import CombatHandler;
from world.map import MAPS;
from world.home import Home;
from world.shop import Shop;
from world.dungeon import Dungeon;
from mechanics.map_explorer import MapExplorer;
from rich.panel import Panel;
from rich.live import Live;
from curtsies import Input;

class Exploration:
  def __init__(self, game):
    self.game = game;
    self.map_explorer = MapExplorer(game);
    self.ui = self.game.ui;
    
  def explore(self):
    self.ui.clear();
    MAP = MAPS[self.game.player.current_map];
    self.map_explorer.placePlayer(self.game.player.position, MAP);
    interacted = None;
    
    with Input(keynames = "curses") as input_generator:
      with Live(Panel(self.map_explorer.render(MAP)), auto_refresh = False) as live:  
        while True:
          key = input_generator.send(0.01);
          if key != None: 
            interacted = self.map_explorer.movePlayer(key, MAP);
            live.update(Panel(self.map_explorer.render(MAP)), refresh = True);
            if interacted != None: break;
          
    if interacted[0] == "home": Home(self.game).enter()     
    elif interacted[0] == "shop": Shop(self.game).enter()
    elif interacted[0] == "dungeon": Dungeon(self.game, self.map_explorer).enter();