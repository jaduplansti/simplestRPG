from random import randint, choices;

class Item:
  """
  an Item class.
  
  Parameters:
  name, a string holding the name for the item, very important
  durability, a integer which can go beyond 100, i should fix that
  rank, a string that could be E to SSS+
  weight, a floating point, not really used.
  bodypart, a string that could be a bodypart in Character.equipment, see character.py.
  """
  
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
      game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] cant use [green]{self.name}[reset], since it does not have any uses!");
  
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
    plr.stats["strength"] -= plr.stats["strength"] * 0.1;
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
  event = choices(["expired", None], [0.1, 0.9])[0];
  
  if event == "expired":
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a {item.name} but it was expired?");
    return;
    
  if item.name == "health potion":
    health_restored = game.player.stats.get("max health") / 2;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a health potion and recovered [green]{health_restored} health[reset]!")
    game.player.healPlayer(health_restored);
     
  elif item.name == "energy potion":
    energy_restored = round(game.player.energy / 2);
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a energy potion and recovered [green]{energy_restored} energy[reset]!")
    game.player.energy = min(game.player.energy + energy_restored, 100);
  
  elif item.name == "strength potion":
    strength_increased = round(2 + game.player.stats["luck"]);
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a strength potion and gained [green]{strength_increased} strength[reset]!");
    game.player.stats["strength"] += strength_increased;
    
  
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
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] already has a [yellow]{game.player.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return;
        
  if item.name == "wooden sword":
    strength_increased = game.player.level * 3;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] equipped a [bold cyan]wooden sword[reset]!");
    game.ui.animatedPrint("Learned [bold green]swordsman[reset] style!");
    game.ui.animatedPrint(f"Strength [green]+{strength_increased}[reset]!");
    game.player.attack_style = "swordsman";
    game.player.stats["strength"] += strength_increased;

def use_chest(item, game, combat_handler):
  if item.name == "starter chest":
    possible_loot = [Item("wooden sword"), Item("scroll of repair"), Item("energy potion"), Item("health potion"), Item("strength potion")];
    
    amount_loot = randint(0, len(possible_loot));
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] opened up a [bold green]starter chest[reset]!");
    
    if amount_loot == 0:
      game.ui.animatedPrint(f"[red bold]the starter chest was empty[reset]!");
      return;
      
    recieved = choices(possible_loot[0:amount_loot], k = amount_loot);
    recieved_str = "";
    
    for item in recieved:
      amount_item = randint(1, 1 + round(game.player.stats["luck"]));
      recieved_str += (f"- [yellow]{item.name}[reset] ({item.rarity}) {amount_item} x\n");
      game.player.addItemToInventory(item, amount_item);
    game.ui.panelPrint(recieved_str.rstrip("\n"), title = "starter chest");
  
ITEMS = {
  "wooden sword": use_sword,
  "health potion" : use_potion,
  "energy potion" : use_potion,
  "scroll of instant death" : use_scroll,
  "scroll of repair" : use_scroll,
  "starter chest" : use_chest,
  "strength potion" : use_potion,
};