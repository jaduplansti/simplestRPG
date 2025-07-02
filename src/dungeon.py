from submenu import SubMenu;
from random import choices, randint, uniform;
from combat import CombatHandler;
from item import getItem, ITEMS;

#todo: make commands more simple. refactor all classes
# make dungeon, add more skills, refactor quest system

class Dungeon():
  def __init__(self, game):
    self.game = game;
    self.progress = 0;
    self.max_progress = randint(3, 11);
    
  def dungeonInitiateEvent(self):
    if self.game.player.level == 1:
      self.game.ui.printDialogue(self.game.player.name, "this is terrifying..");
      self.game.ui.panelPrint("[red]strength (-1)[reset]");
      self.game.player.stats["strength"] -= 1;
      
  def dungeonInitiateMenu(self):
    self.game.ui.clear();
    self.game.ui.animatedPrint("You arrive at the [yellow]dungeon[reset], a tall stone yet metallic door surrounds you..");
    self.game.ui.printDialogue(self.game.player.name, "damn..");
    self.game.ui.animatedPrint("You are drawn in by the dungeon gates..");
    
    self.dungeonInitiateEvent();
    self.game.ui.panelAnimatedPrint("[bold red]YOU ARE NOW IN THE DUNGEON[reset]", "DuNgeoN");
    self.game.ui.printDialogue(self.game.player.name, "[yellow]here we go[reset]..");
    
    self.game.ui.showCombatBar(self.game.player);
    self.game.ui.printTreeMenu("dungeon", ["enter", "exit"]);
  
  def handleInitiateMenu(self): # use submenu later
    self.dungeonInitiateMenu();
    option = self.game.ui.getInput();
    
    if option == "enter":
      self.dungeonEnter();
    elif option == "exit":
      self.game.exploration_handler.explore()
    else:
      self.game.ui.animatedPrint("[bold red]a mysterious entity pushes you towards the gates..[reset]");
      self.game.ui.printDialogue(self.game.player.name, "augh...");
      self.game.ui.awaitKey();
      self.dungeonEnter();
  
  def dungeonEvent(self):
    event = choices([
      "encounter", "item", "trap", "puzzle", 
      #"lore", "rest", "npc", "hidden_passage", 
      #"scenic_view", "old_bones", "strange_flora", 
      #"echoing_chasm", "flickering_light", "rune_pedestal", 
      #"cracked_wall", "glowing_pool", "pressure_plate", 
      #"lever_puzzle", "illusion", "rockfall", "quick_sand", 
      #"toxic_fumes", "unstable_ground", "darkness_zone", "eerie_sound", 
      #"cold_spot", "whispering_wind", "strange_odor", "spectral_glimpse", 
      #"sleeping_monster", "chase_sequence", "empty_chest", "cursed_item"
    ])[0];
    
    self.game.ui.clear();
    if event == "encounter": self.__encounterEvent();
    elif event == "item": self.__itemEvent();
    elif event == "trap" : self.__trapEvent();
    elif event == "puzzle": pass;
    
    self.progress += 1;
    
  def dungeonDeath(self):
    self.game.ui.animatedPrint("[yellow]the shadows of death grow closer[reset]..");
    self.game.ui.animatedPrint("[bold red]death engulfs you![reset]");
    self.game.ui.printDialogue(self.game.player.name, "no..");
    
    self.game.ui.panelPrint("[bold red]DUNGEON FAILED[reset]");
    self.game.ui.awaitKey();
    self.game.exploration_handler.move("home");
    
  def dungeonComplete(self):
    self.game.ui.animatedPrint("The doors shine [yellow]brightly[reset]");
    self.game.ui.panelPrint("[bold green]DUNGEON COMPLETE[reset]");
    
    rewards = [];
    
    xp_gain = self.game.player.exp * uniform(2.1, 4.1) + 100;
    money_gain = randint(1, 100);
    for _ in range(0, randint(1, 5)): rewards.append(choices(list(ITEMS))[0]);
    self.game.ui.panelPrint(f"exp : {xp_gain}\nmoney: {money_gain}\n items: {rewards}", "center", "rewards");
    
    self.game.givePlayerExp(xp_gain);
    self.game.handlePlayerLevelUp();
    for item in rewards: self.game.player.addItemToInventory(getItem(item), 1);
    
    self.game.player.money += money_gain;
    self.game.ui.awaitKey();
    self.game.exploration_handler.move("home");
    
  def dungeonLoop(self):
    while True:
      self.dungeonEvent();
      if self.game.player.stats["health"] <= 0: self.dungeonDeath();
      elif self.progress >= self.max_progress: self.dungeonComplete();
      self.game.ui.awaitKey();
        
  def dungeonEnter(self):
    self.dungeonLoop();
    
  def enter(self):
    self.handleInitiateMenu();
  
  def __encounterEvent(self):
    self.game.ui.printDialogue(self.game.player.name, choices(["an enemy!", "is that a monster?", "is this hostile?", "shit..", "oh great an enemy."])[0]);
    self.game.ui.awaitKey();
    combat_handler = CombatHandler(self.game);
    combat_handler.initiateFightNpc(self.game.player, "slime");
  
  def __itemEvent(self):
    self.game.ui.animatedPrint("you see a object ahead, laying on the ground..");
    self.game.ui.printDialogue(self.game.player.name, "is that a item?");
    
    item = getItem(choices(list(ITEMS))[0]);
    while True:
      self.game.ui.printTreeMenu(item.name, ["pick up", "examine", "ignore"]);
      option = self.game.ui.getInput();
      if option in ["pick up", "pickup"]:
        self.game.player.addItemToInventory(item, 1);
        self.game.ui.animatedPrint(f"you picked up a {item.name}");
        break;
      elif option == "examine":
        self.game.ui.panelPrint(f"{item.name}({item.rank})({item.rarity})");
      elif option == "ignore":
        return;
      self.game.ui.awaitKey();
      self.game.ui.clear();
      
  def __trapEvent(self):
    trap = choices(["fall", "poison", None])[0];
    if trap == "fall": 
      self.game.ui.animatedPrint("you step forward, and the ground beneath your feet suddenly vanishes");
      self.game.ui.printDialogue(self.game.player.name, "[red]shit![reset]");
      self.game.ui.animatedPrint("[bold red]you plummted towards darkness[reset]");
      self.game.player.stats["health"] *= 0.95;
    elif trap == "poison":
      self.game.ui.animatedPrint("you step forward, only to be suddenly hit by a poison dart.");
      CombatHandler(self.game).attack_handler.status_handler.afflict(self.game.player, "poisoned", 3);
      self.game.ui.printDialogue(self.game.player.name, "ouch.. this venom stings.");
    else:
      self.game.ui.animatedPrint("you step forward..");
      self.game.ui.animatedPrint("thankfully the trap was off..");
      self.game.ui.printDialogue(self.game.player.name, "*sigh*");
    