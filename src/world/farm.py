from time import time;
from copy import deepcopy;
from random import randint, choice;

# move the showCrops to animator and make it live.

class Crop:
  def __init__(self, name, duration, time_planted = 0, description = "a seed.", gives = []):
    self.name = name;
    self.description = description;
    
    self.duration = duration;
    self.time_planted = time_planted;
    self.gives = gives;
    
  def isFinished(self):
    if self.getTime() >= self.duration: return True;
    else: return False;
  
  def getTime(self):
    return round(time() - self.time_planted);
    
class Farm:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    
    self.key_index = 0;
    self.crops = [None, None, None];
    self.crop_limit = 3;
  
    if self.loadData() == -1: self.createData();

  def plant(self, name):
    if name not in CROPS: # this is impossible btw
      self.ui.animatedPrint("erm this cant be planted.");
      return;
    self.plantCrop(name, self.key_index, time());
    self.game.player.usedItem(name);
    
  def harvest(self):
    crop = self.crops[self.key_index];
    player_luck = round(self.game.player.stats["luck"] * 100)
    amount = randint(1, round(player_luck / 2));
    if len(crop.gives) != 0: reward = choice(crop.gives);
    else: reward = crop.name;
    self.game.givePlayerItem(reward, amount);
    self.crops[self.key_index] = None;
    
  def handleKey(self):
    key = self.ui.getKey();
    if (key == "w") and (self.key_index > 0): self.key_index -= 1;
    elif (key == "s") and (self.key_index < len(self.crops) - 1): self.key_index += 1;
    else: return key;
  
  def cropDetail(self, crop):
    if crop != None: 
      self.ui.panelPrint(f"{crop.name}\n\n{crop.description}", "center");
      if crop.isFinished() is True: self.ui.normalPrint("> harvest");
      self.ui.normalPrint("> back\n");
    else: 
      self.ui.panelPrint("A empty slot.", "center");
      self.ui.normalPrint("> plant\n> back\n");
  
  def availableCrop(self):
    for item_name in self.game.player.inventory:
      if item_name in CROPS: self.ui.normalPrint(f"• {item_name}\n");
   
  def plantCrop(self, name, slot, time_planted, announce = True):
    self.crops[slot] = getCrop(name);
    self.crops[slot].time_planted = time_planted;
    if announce is True: self.ui.animatedPrint(f"{name} planted!");
    
  def showCrops(self):
    for index, crop in enumerate(self.crops):
      if self.key_index == index: color = "green";
      else: color = "white";
      if crop is None: self.ui.panelPrint("[dim]EMPTY[reset]", "center", "None", color);
      elif not crop.isFinished(): self.ui.panelPrint(f"{crop.name}", "center", f"{crop.getTime()}/{crop.duration}", color)
      else: self.ui.panelPrint("[bold yellow]READY[reset]", "center", f"{crop.name}", color);
  
  def handleSeedSelect(self):
    self.availableCrop();
    option = self.ui.getInput();
    self.plant(option);
      
  def handleFarm(self):
    while True:
      self.ui.clear();
      self.showCrops();
      self.ui.normalPrint("hint: press w/s to pick, press (enter) to select, press (q) to quit");
      key = self.handleKey();
      if key == "\n": self.handleSelect();
      elif key == "q":
        self.saveFarm();
        return;
   
  def __handleSelectCrop(self):
    while True:
      self.ui.clear();
      crop = self.crops[self.key_index];
      self.cropDetail(crop);
      key = self.ui.getInput();
      if crop.isFinished() and key == "harvest": 
        self.harvest();
        return True;
      if key == "back": return True;
      self.ui.awaitKey();
  
  def __handleSelectNone(self):
    while True:
      self.ui.clear();
      self.cropDetail(self.crops[self.key_index]);
      key = self.ui.getInput();
      if key == "plant": 
        self.handleSeedSelect();
        return True;
      elif key == "back": return True;
      self.ui.awaitKey();
      
  def handleSelect(self):
    while True:
      self.ui.clear();
      if self.crops[self.key_index] != None: 
        if self.__handleSelectCrop() is True: return;
      else: 
        if self.__handleSelectNone() is True: return;
  
  def createData(self):
    if "farm" not in self.game.player.area_data:
      self.game.player.area_data.update({"farm" : {
        "crops": [],
      }});
    
  def loadData(self):
    try:
      data = self.game.player.area_data["farm"];
      for index, crop_data in enumerate(data["crops"]):
        if crop_data != None: self.plantCrop(crop_data[0], index, crop_data[1], announce = False);
    except KeyError as err:
      return -1;
 
  def saveFarm(self):
    self.game.player.area_data["farm"]["crops"] = [];
    for crop in self.crops:
      crop_save = [crop.name, crop.time_planted] if crop != None else None;
      self.game.player.area_data["farm"]["crops"].append(crop_save);
    
def getCrop(name):
  return deepcopy(CROPS[name]);
  
CROPS = {
  "wheat" : Crop("wheat", 50, 0),
};