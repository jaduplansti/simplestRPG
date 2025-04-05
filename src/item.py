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
  
  def use(self, game):
    if self.name == "health potion":
      health_restored = game.player.stats.get("max health") / 2;
      game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a health potion and recovered [green]{health_restored} health[reset]!")
      game.player.healPlayer(health_restored);
    
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

