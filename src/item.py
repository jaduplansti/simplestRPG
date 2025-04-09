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
  
  def use(self, game, combat_handler = None):
    try:
      ITEMS[self.name](self, game, combat_handler);
      game.player.usedItem(self.name);
    except KeyError:
      pass;
  
  def consumeDurability(self, n):
    self.durability = max(self.durability - n, 0);
    
  def handleDurability(self, n):
    self.consumeDurability(n);
    if self.durability <= 0:
      return True;
      
  def to_dict(self):
    return {
      "name": self.name,
      "rarity": self.rarity,
      "durability": self.durability,
      "bodypart": self.bodypart,
      };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);

def removeEquipment(plr, part):
  item = plr.equipment[part];
  if "sword" in item.name:
    plr.attack_style = "basic";
    plr.stats["strength"] = plr.stats["strength"] - (3 * plr.level);
  plr.equipment[part] = None;
  
# def createItem(name, durability = 1, rank = "E", rarity = "common", weight = 0.1, stat_bonus = None, bodypart = None):
#     return Item(
#       name,
#       durability = durability,
#       rarity = rarity,
#       weight = weight,
#       stat_bonus = stat_bonus,
#       bodypart = bodypart,
#     );
# 

def use_potion(item, game, combat_handler):
  if item.name == "health potion":
    health_restored = game.player.stats.get("max health") / 2;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a health potion and recovered [green]{health_restored} health[reset]!")
    game.player.healPlayer(health_restored);
     
  elif item.name == "energy potion":
    energy_restored = round(game.player.energy / 2);
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a energy potion and recovered [green]{energy_restored} energy[reset]!")
    game.player.energy = min(game.player.energy + energy_restored, 100);
    
def use_scroll(item, game, combat_handler):
  if item.name == "scroll of instant death" and combat_handler != None:
    combat_handler.defender.stats["health"] = 0;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a [bold cyan]scroll of instant death[reset]!");
    game.ui.animatedPrint(f"[bold red]{combat_handler.defender.name} feels their life force drain away!");
  
  elif item.name == "scroll of repair":
    game.menu.showEquipmentMenu(game.player);
    game.ui.animatedPrint("which equipment to repair? e.g bodypart");
    part = game.ui.getInput();
    try:
      if game.player.equipment[part] != None:
        game.player.equipment[part].durability += 1000; # temporary
        game.ui.animatedPrint(f"[purple]{game.player.equipment[part].name}[reset] has been repaired.");
      else: game.ui.animatedPrint(f"cannot repair item on [red]{part}[reset]")
    except KeyError:
      game.ui.animatedPrint("not a valid bodypart");
      
def use_sword(item, game, combat_handler):
  if game.player.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] has already equipped a [bold cyan]wooden sword[reset]!");
    return;
        
  if item.name == "wooden sword":
    strength_increased = game.player.level * 3;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] equipped a [bold cyan]wooden sword[reset]!");
    game.ui.animatedPrint("Learned [bold green]swordsman[reset] style!");
    game.ui.animatedPrint(f"Strength [green]+{strength_increased}[reset]!");
    game.player.attack_style = "swordsman";
    game.player.stats["strength"] += strength_increased;

ITEMS = {
  "wooden sword": use_sword,
  "health potion" : use_potion,
  "energy potion" : use_potion,
  "scroll of instant death" : use_scroll,
  "scroll of repair" : use_scroll,
};