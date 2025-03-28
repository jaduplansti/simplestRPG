from random import randint;

class Item:
  def __init__(self, 
  name, 
  durability = 1, 
  rank = "E", 
  rarity = "common", 
  weight = 0.1,
  bodypart = None):
    
    self.name = name;
    self.durability = durability;
    self.rarity = rarity;
    self.weight = weight;
    self.bodypart = bodypart;
  
  def getRarityMultiplier(self):
    if self.rarity == "common":
      return 1;
    
  def use(self, game):
    if self.name == "health potion":
      health_restored = round((game.player.stats["health"] / randint(3, 4)) * self.getRarityMultiplier());
      game.ui.animatedPrint(f"{game.ui.coloredString(game.player.name, "yellow")} used a health potion and recovered ({game.ui.coloredString(health_restored, "blue")} hp)");
      game.player.healPlayer(health_restored);
    
    elif self.name == "bread":
      health_restored = round((game.player.stats["health"] / randint(3, 4)) * self.getRarityMultiplier());
      game.ui.animatedPrint(f"{game.ui.coloredString(game.player.name, "yellow")} ate bread and recovered ({game.ui.coloredString(health_restored, "blue")} hp)");
      game.ui.animatedPrint("yummy!");
      game.player.healPlayer(health_restored);
    
    elif self.name == "wooden sword":
      game.ui.animatedPrint(f"{game.ui.coloredString(game.player.name, "yellow")} equipped a wooden sword.");
      game.ui.animatedPrint(f"{game.ui.coloredString(game.player.name, "yellow")} gained +10 strength");
      game.ui.animatedPrint(f"{game.ui.coloredString(game.player.name, "yellow")} had learned the way of the sword.");
      game.player.equipItem(self);
      game.player.stats["strength"] += 10;
      game.player.attack_style = "swordsman";
      
    game.player.usedItem(self.name);
  
  def consumeDurability(self, n):
    self.durability = min(self.durability, n);
    
def createItem(name, durability = 1, rank = "E", rarity = "common", weight = 0.1, stat_bonus = None, bodypart = None):
    return Item(
      name,
      durability = durability,
      rarity = rarity,
      weight = weight,
      stat_bonus = stat_bonus,
      bodypart = bodypart,
    );

