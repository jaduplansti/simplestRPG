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
  
  def changeMap(self, path):
    map_number = path.split("_")[1];
    current_number = self.game.player.current_map.split("map")[1];
  
    for y, objs in enumerate(MAPS[f"map{map_number}"]):
      for x, obj in enumerate(objs):
        if obj == f"path_{current_number}":
  
          spawn_y = y;
          spawn_x = x + 1;
  
          if spawn_x >= len(objs):
            spawn_x = x - 1;
          
          self.current_map[self.game.player.position[0]][self.game.player.position[1]] = None;
          self.game.player.current_map = f"map{map_number}";
          self.game.player.position = [spawn_y, spawn_x];
  
          self.current_map = MAPS[self.game.player.current_map];
          return;
          
  def explore(self):
    self.ui.clear();
    self.game.audio_handler.popTracks();
    self.current_map = MAPS[self.game.player.current_map];
    
    if self.map_explorer.findObject("plr", self.current_map) != True: self.map_explorer.placePlayer(self.game.player.position, self.current_map);
    
    interacted = None;
    
    with Input(keynames = "curses") as input_generator:
      with Live(Panel(self.map_explorer.render(self.current_map)), auto_refresh = False) as live:  
        while True:
          key = input_generator.send(0.01);
          if key != None: 
            interacted = self.map_explorer.movePlayer(key, self.current_map);
            live.update(Panel(self.map_explorer.render(self.current_map)), refresh = True);
            if interacted != None: break;
          
    if interacted[0] == "home": Home(self.game).enter()     
    elif interacted[0] == "shop": Shop(self.game).enter()
    elif interacted[0] == "dungeon": Dungeon(self.game, self.map_explorer).enter();
    else: self.explore();