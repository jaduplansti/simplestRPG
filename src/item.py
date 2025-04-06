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
  
    elif self.name == "energy potion":
      energy_restored = round(100 / 3);
      game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a energy potion and recovered [green]{energy_restored} energy[reset]!")
      game.player.energy += min(game.player.energy + energy_restored, 100);
    
    elif self.name == "wooden sword":
      if game.player.equipItem(self) != True:
        game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] has already equipped a [bold cyan]wooden sword[reset]!");
        return;
        
      strength_increased = game.player.level * 3;
      game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] equipped a [bold cyan]wooden sword[reset]!");
      game.ui.animatedPrint("Learned [bold green]swordsman[reset] style!");
      game.ui.animatedPrint(f"Strength [green]+{strength_increased}[reset]!");
      game.player.attack_style = "swordsman";
      game.player.stats["strength"] += strength_increased;
      
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

