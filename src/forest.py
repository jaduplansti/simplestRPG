from item import Item;
from random import randint;

class Forest:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
  
  def cutTree(self):
    if self.game.player.equipment["right arm"].name != "chopping axe":
      self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] cant cut tree's without equipping a [green italic]chopping axe[reset]!");
      return;
    
    tree_durability = 100;
    
    while tree_durability > 0:
      self.ui.clear();
      self.ui.normalPrint("press ([bold green]c[reset]) to chop tree!\n");
      self.ui.normalPrint(f"(tree: {tree_durability}/100)\n");
      if self.ui.getKey() == "c": tree_durability -= 10;
      
    wood = [Item("wood"), randint(1, 4)];
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] has cut a tree!");
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] acquired wood ([green]{wood[1]}x[reset])");
    self.game.player.addItemToInventory(wood[0])
      
  def showForestMenu(self):
    self.ui.clear();
    self.ui.normalPrint("•••••••••••••");
    self.ui.normalPrint("• [italic yellow]Your Home[reset] •");
    self.ui.normalPrint("•••••••••••••\n");
    
    #self.ui.normalPrint(art.HOUSE + "\n");
    self.ui.normalPrint("≈ [green]cut tree[reset]");
    self.ui.normalPrint("≈ [green]items[reset]");
    self.ui.normalPrint("≈ [green]leave[reset]\n");

  def handleForest(self):
    self.game.audio_handler.play("forest.mp3");
    self.game.handleMenu(
    {
      "cut tree" : self.cutTree,
      "leave" : self.game.exploration_handler.explore,
      "items" : self.game.handleUseItem, 
    }, 
    self.showForestMenu);  
    
  def enter(self):
    self.ui.clear();
    self.ui.animatedPrint(f"[green]{self.game.player.name} steps into the forest.");
    self.handleForest();
    