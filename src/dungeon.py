from submenu import SubMenu;

#todo: make commands more simple. refactor all classes
# make dungeon, add more skills, refactor quest system

class Dungeon():
  def __init__(self, game):
    self.game = game;
    
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
      self.game.exploration_handler.explore
    else:
      self.game.ui.animatedPrint("[bold red]a mysterious entity pushes you towards the gates..[reset]");
      self.game.ui.printDialogue(self.game.player.name, "augh...");
      self.game.ui.awaitKey();
      self.dungeonEnter();
      
  def dungeonLoop(self):
    pass;
  
  def dungeonEnter(self):
    self.game.ui.clear();
    self.game.ui.barPrint("[blue]Packing Up[reset]", 0, 100, speed = 0.2);
    self.game.ui.barPrint("[blue]Warming Up[reset]", 0, 100, speed = 0.5);
    self.game.ui.printDialogue(self.game.player.name, "lets get started..");
    self.game.ui.awaitKey();
    self.dungeonLoop();
    
  def enter(self):
    self.handleInitiateMenu();
    