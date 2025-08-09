from submenu import SubMenu;
from random import choices, randint, uniform;
from combat import CombatHandler;
from item import getItem, ITEMS;

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
      #"ambush", "rest", "npc", "hidden_passage", 
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
    elif event == "puzzle": self.__puzzleEvent();
    
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
    
    xp_gain = round(self.game.player.exp * uniform(2.1, 4.1) + 100);
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
    combat_handler = CombatHandler(self.game);
    combat_handler.initiateFightNpc(self.game.player, choices(["goblin", "slime", "orc", "skeleton", "bandit"])[0]);
  
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
      self.game.ui.animatedPrint("[bold red]you plummeted towards darkness[reset]");
      self.game.player.stats["health"] *= 0.95;
    elif trap == "poison":
      self.game.ui.animatedPrint("you step forward, only to be suddenly hit by a poison dart.");
      CombatHandler(self.game).attack_handler.status_handler.afflict(self.game.player, "poisoned", 3);
      self.game.ui.printDialogue(self.game.player.name, "ouch.. this venom stings.");
    else:
      self.game.ui.animatedPrint("you step forward..");
      self.game.ui.animatedPrint("thankfully the trap was off..");
      self.game.ui.printDialogue(self.game.player.name, "*sigh*");
  
  def __puzzleEvent(self):
    puzzle = choices(["passcode"])[0];
   
    if puzzle == "passcode":
      valid_code = f"{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}";
      hint = valid_code[randint(0, 2)];
      
      self.game.ui.animatedPrint(f"A massive door stands before [yellow]{self.game.player.name}[reset], right beside it holds a keypad.");
      self.game.ui.printDialogue(self.game.player.name, "keypad? how the hell..");
      self.game.ui.printDialogue(self.game.player.name, "better get this opened!");
      self.game.ui.printDialogue(self.game.player.name, "what are the odds of this being a trap? perhaps a exit!");
      
      while True:
        self.game.ui.printTreeMenu("door", ["unlock", "examine", "attack"]);
        option = self.game.ui.getInput();
        
        if option == "unlock":
          self.game.ui.printDialogue(self.game.player.name, "beep boop bop, 3 digits.");
          passw = self.game.ui.getInput();
          if passw == valid_code: 
            self.game.ui.animatedPrint("The massive door screeches, slowly opening..");
            self.game.ui.panelPrint("[bold cyan]DOOR UNLOCKED[reset]");
            return;
          else:
            self.game.ui.animatedPrint("The massive door does not budge.");
            self.game.ui.printDialogue(self.game.player.name, "must be the wrong passcode.");
            self.game.ui.printDialogue(self.game.player.name, f"i think {hint} is one of the digits in the code!");
        
        elif option == "examine":
          self.game.ui.animatedPrint("its a iron door, keypad on the right, 3 digits");
          self.game.ui.animatedPrint("this door has [red]1000 hp[reset], [underline]dealing 1000 damage will break it[reset].");
          self.game.ui.printDialogue(self.game.player.name, f"there's the digit {hint} written below!");
          self.game.ui.printDialogue(self.game.player.name, f"a message? thou shall not pass");
          self.game.ui.panelPrint(f"[cyan]CODE ({valid_code})[reset]");
        
        elif option == "attack":
          self.game.ui.panelAnimatedPrint(f"[yellow]{self.game.player.name}[reset] tried to break the [yellow]door[reset], dealing [red]{self.game.player.stats["strength"]}[reset] damage!", "punch");
          if self.game.player.stats["strength"] < 1000:
            self.game.ui.animatedPrint("the door barely shook..");
            self.game.ui.printDialogue(self.game.player.name, f"ouch!");
            self.game.ui.panelPrint("[red]HEALTH (-2%)[reset]");
            self.game.player.stats["strength"] *= 0.02;
          elif self.game.player.stats["strength"] >= 1000:
            self.game.ui.animatedPrint("[red]the door breaks down![reset]");
            self.game.ui.panelPrint("[bold cyan]DOOR UNLOCKED[reset]");
            return;
            
        self.game.ui.awaitKey();
        self.game.ui.clear();
        
    elif puzzle == "pattern flash":
      pass;
      
  def ambushEvent(self):
    self.game.ui.animatedPrint();
     

