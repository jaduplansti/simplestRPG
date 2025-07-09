from random import randint, choices;
from copy import deepcopy;

# CREATE EQUIPMENT CLASS, REFACTOR THIS SHIT 

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
  max_durability = 1,
  durability = 1, 
  rank = "E", 
  rarity = "common", 
  weight = 0.1,
  bodypart = None,
  ):
    
    self.name = name;
    self.max_durability = max_durability
    self.durability = durability;
    self.rank = rank;
    self.rarity = rarity;
    self.weight = weight;
    self.bodypart = bodypart;
    
  def use(self, game, combat_handler = None):
    try:
      fn = ITEMS[self.name]["action"]
      if fn is None: 
        game.ui.animatedPrint("this item has no uses.");
        return;
      if fn(self, game, combat_handler) != -1: game.player.usedItem(self.name);
    except KeyError:
      game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] cant use [green]{self.name}[reset], since it does not have any uses!");
  
  def getDurability(self):
    return (self.durability / self.max_durability) * 100
    
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
      "max_durability" : self.max_durability,
      "durability": self.durability,
      "bodypart": self.bodypart,
      };
  
  def rarityToVal(self):
    for n, val in enumerate(["common", "uncommon"]):
      if self.rarity == val: return (n + 1) * 10;
  
  @classmethod
  def from_dict(cls, data):
    return cls(**data);
  
def removeEquipment(plr, part):
  item = plr.equipment[part];
  if "sword" in item.name:
    plr.attack_style = "basic";
    plr.stats["strength"] -= 0;
  elif "bow" in item.name:
    plr.attack_style = "basic";
    plr.stats["strength"] -= 0;
   
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

def getItem(name):  
  try:
    return deepcopy(ITEMS[name]["item"]);
  except KeyError:
    return None;
    
def use_potion(item, game, combat_handler):
  event = choices(["poison", None], [0.1, 0.9])[0];
  
  if event == "poison":
    game.giveStatus("poisoned", 1);
    game.ui.animatedPrint(f"[cyan]{game.player.name}[reset] used a {item.name} but it was poisoned!");
    game.ui.printDialogue(game.player.name, "yuck..");
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
  
  elif item.name == "cleanse potion":
    for status in game.player.status:
      game.player.status[status][0] = False;
      game.player.status[status][1] = 0;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] used a cleanse potion, removing [green]status effects[reset]!");
  
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
        game.player.equipment[part].durability = game.player.equipment[part].max_durability;
        game.ui.animatedPrint(f"[purple]{game.player.equipment[part].name}[reset] has been repaired (OK).");
      else: game.ui.animatedPrint(f"cannot repair item on [red]{part}[reset]")
    except KeyError:
      game.ui.animatedPrint("not a valid bodypart");
  
  elif item.name == "scroll of teleport":
    location = game.ui.getInput();
    game.player.usedItem(item.name);
    game.ui.clear();
    game.exploration_handler.move(location);
    
def use_sword(item, game, combat_handler):
  if game.player.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] already has a [yellow]{game.player.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return -1;
        
  if item.name == "wooden sword":
    strength_increased = round(game.player.stats["strength"] * 0.1);
    game.player.equipment[item.bodypart].bonus = strength_increased;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] equipped a [bold cyan]wooden sword[reset]!");
    game.ui.animatedPrint("learned [bold green]swordsman[reset] style!");
    game.ui.animatedPrint(f"strength increased by [green]10%[reset]!");
    game.player.attack_style = "swordsman";
    game.player.stats["strength"] += strength_increased;
    game.givePlayerSkill("parry");
  
  if item.name == "steel sword":
    strength_increased = round(game.player.stats["strength"] * 0.1);
    game.player.equipment[item.bodypart].bonus = strength_increased;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] equipped a [bold blue]steel sword[reset]!");
    game.ui.animatedPrint("learned [bold green]swordsman[reset] style!");
    game.ui.animatedPrint(f"strength increased by [green]10%[reset]!");
    game.player.attack_style = "swordsman";
    game.player.stats["strength"] += strength_increased;
    game.givePlayerSkill("parry");
  
  if item.name == "kevins sword":
    strength_increased = round(game.player.stats["strength"] * 0.13);
    game.player.equipment[item.bodypart].bonus = strength_increased;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] equipped a [bold blue]kevin's sword[reset]!");
    game.ui.animatedPrint("learned [bold green]swordsman[reset] style!");
    game.ui.animatedPrint(f"strength increased by [green]13%[reset]!");
    game.player.attack_style = "swordsman";
    game.player.stats["strength"] += strength_increased;
    game.givePlayerSkill("parry");
    
def use_chest(item, game, combat_handler):
  if item.name == "starter chest":
    possible_loot = [getItem("wooden sword"), getItem("energy potion"), getItem("health potion"), getItem("scroll of repair"), getItem("strength potion")];
    
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
  
def use_glove(item, game, combat_handler):
  if game.player.attack_style != "basic":
    game.ui.animatedPrint("you must have a basic attack style!");
    return -1;
  
  if game.player.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] already has a [yellow]{game.player.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return;
    
  if item.name == "leather gloves":
    game.ui.animatedPrint("you put on the leather gloves");
    game.ui.animatedPrint("its feel comfy.. gained +3 strength");
    game.player.stats["strength"] += 3;

def use_bow(item, game, combat_handler):
  if game.player.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] already has a [yellow]{game.player.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return -1;
        
  if item.name == "wooden bow":
    strength_increased = 25;
    game.player.equipment[item.bodypart].bonus = strength_increased;
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] equipped a [bold blue]wooden bow[reset]!");
    game.ui.animatedPrint("learned [bold green]archer[reset] style!");
    game.ui.animatedPrint(f"strength [green]+{strength_increased}[reset]!");
    game.player.attack_style = "archer";
    game.player.stats["strength"] += strength_increased;
    #game.givePlayerSkill("parry");
  
def use_food(item, game, combat_handler):
  if item.name == "bread":
    game.ui.animatedPrint(f"[yellow]{game.player.name}[reset] ate a loaf of [bold green]bread[reset]!");
    game.ui.animatedPrint(f"hunger: {game.player.hunger} + 10");
    game.player.hunger = min(100, game.player.hunger + 10);
  
ITEMS = {
  "wooden sword": {
    "item": Item(name="wooden sword", max_durability = 2000, durability = 2000, rank="E", weight=2.0, bodypart="right arm"),
    "action": use_sword
  },
  "wooden bow": {
    "item": Item(name="wooden bow", max_durability = 2000, durability = 2000, rank = "E", weight = 2.0, bodypart = "right arm"),
    "action": use_bow
  },
  "steel sword": {
    "item": Item(name="steel sword", max_durability = 5000, durability = 5000, rank="D+", weight = 5.0, bodypart= "right arm"),
    "action": use_sword
  },
  "kevins sword": {
    "item": Item(name="kevins sword", max_durability = 15000, durability = 15000, rank="C", weight = 2.0, bodypart = "right arm"),
    "action": use_sword
  },
  "health potion": {
    "item": Item(name="health potion", rank="E", weight=0.5),
    "action": use_potion
  },
  "energy potion": {
    "item": Item(name="energy potion", rank="E", weight=0.5),
    "action": use_potion
  },
  "scroll of instant death": {
    "item": Item(name="scroll of instant death", rank="B", rarity="rare", weight=0.2),
    "action": use_scroll
  },
  "scroll of repair": {
    "item": Item(name="scroll of repair", rank="D", rarity="uncommon", weight=0.2),
    "action": use_scroll
  },
  "starter chest": {
    "item": Item(name="starter chest", durability=1, rank="D", rarity="common", weight=5.0),
    "action": use_chest
  },
  "strength potion": {
    "item": Item(name="strength potion", rank="D", rarity="uncommon", weight=0.6),
    "action": use_potion
  },
  "cleanse potion": {
    "item": Item(name="cleanse potion", rank="C", rarity="uncommon", weight=0.6),
    "action": use_potion
  },
  "leather gloves": {
    "item": Item(name = "leather gloves", bodypart = "left arm", rank = "D", rarity = "uncommon", weight = 0.5),
    "action": use_glove,
  },
  "scroll of teleport": {
    "item": Item(name = "scroll of teleport", rank = "C", rarity = "rare", weight = 0.1),
    "action": use_scroll,
  },
  "wooden arrow": {
    "item": Item(name = "wooden arrow", rank = "D", rarity = "common", weight = 0.3),
    "action": None,  
  },
  "bread": {
    "item": Item(name = "bread", rank = "D", rarity = "common", weight = 0.01),
    "action": use_food,  
  }
}

class Equipment:
  def __init__(self, name, bodypart, durability, max_durability, bonus):
    self.name = name;
    self.bodypart = bodypart;
    self.durability = durability;
    self.max_durability = max_durability;
    self.bonus = bonus;
   
  def removeEquipment(self, plr):
    if "sword" in self.name:
      plr.attack_style = "basic";
      plr.stats["strength"] -= 0;
    elif "bow" in self.name:
      plr.attack_style = "basic";
      plr.stats["strength"] -= 0;
    plr.equipment[self.bodypart] = None;
   
def itemToEquipment(item, bonus):
  return Equipment(item.name, item.bodypart, item.durability, item.max_durability);