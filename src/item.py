from random import randint, choices;
from copy import deepcopy;

# CREATE EQUIPMENT CLASS, REFACTOR THIS SHIT 

class Equipment:
  """
  an Equipment class.
  
  Parameters:
  name, a string holding the name for the equipment, very important
  durability, a integer containing the current health potion
  max_durability, a integer containing the max health point of an item
  bodypart, a string containing either left arm, right arm, head, torso and boots.
  bonus, a integer storing bonuses
  """
  
  def __init__(self, name, bodypart, durability, max_durability, bonus):
    self.name = name;
    self.bodypart = bodypart;
    self.durability = durability;
    self.max_durability = max_durability;
    self.bonus = bonus;
  
  def getDurability(self):
    return (self.durability / self.max_durability) * 100
    
  def consumeDurability(self, n):
    self.durability = max(self.durability - n, 0);
    
  def handleDurability(self, n):
    self.consumeDurability(n);
    if self.durability <= 0:
      return True;
    
  def removeEquipment(self, plr, game):
    if "sword" in self.name:
      game.removeStyle(plr);
      plr.stats["strength"] -= self.bonus;
    elif "bow" in self.name:
      plr.stats["strength"] -= self.bonus;
    plr.equipment[self.bodypart] = None;
  
  @classmethod
  def from_dict(cls, data):
    return cls(**data);
    
  def to_dict(self):
    return {
      "name": self.name,
      "max_durability" : self.max_durability,
      "durability": self.durability,
      "bodypart": self.bodypart,
      "bonus": self.bonus,
    };

def equipmentToItem(equipment):
  item = getItem(equipment.name);
  item.durability = equipment.durability;
  item.max_durability = equipment.max_durability;
  return item;
  
def itemToEquipment(item, bonus):
  return Equipment(item.name, item.bodypart, item.durability, item.max_durability, bonus);
  
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
    
  def use(self, game, user, combat_handler = None):
    try:
      fn = ITEMS[self.name]["action"]
      if fn is None: 
        game.ui.animatedPrint("this item has no uses.");
        return;
      if fn(self, game, combat_handler, user) != -1: user.usedItem(self.name);
    except KeyError:
      game.ui.animatedPrint(f"[yellow]{user.name}[reset] cant use [green]{self.name}[reset], since it does not have any uses!");
  
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
  
def getItem(name):  
  try:
    return deepcopy(ITEMS[name]["item"]);
  except KeyError:
    return None;
    
def use_potion(item, game, combat_handler, user):
  event = choices(["poison", None], [0.1, 0.9])[0]
  
  if event == "poison":
    game.giveStatus("poisoned", 1);
    game.ui.animatedPrint(f"[cyan]{user.name}[reset] used a {item.name} but it was poisoned!");
    game.ui.printDialogue(user.name, "yuck..");
    return;
    
  if item.name == "health potion":
    health_restored = user.stats.get("max health") / 2;
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] used a health potion and recovered [green]{health_restored} health[reset]!")
    user.healPlayer(health_restored);
     
  elif item.name == "energy potion":
    energy_restored = round(user.energy / 2);
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] used a energy potion and recovered [green]{energy_restored} energy[reset]!")
    user.energy = min(user.energy + energy_restored, 100);
  
  elif item.name == "strength potion":
    strength_increased = round(2 + user.stats["luck"]);
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] used a strength potion and gained [green]{strength_increased} strength[reset]!");
    user.stats["strength"] += strength_increased;
  
  elif item.name == "cleanse potion":
    for status in user.status:
      user.status[status][0] = False;
      user.status[status][1] = 0;
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] used a cleanse potion, removing [green]status effects[reset]!");
  
def use_scroll(item, game, combat_handler, user):
  if item.name == "scroll of instant death" and combat_handler != None:
    combat_handler.defender.stats["health"] = 0;
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] used a [bold cyan]scroll of instant death[reset]!");
    game.ui.animatedPrint(f"[bold red]{combat_handler.defender.name} feels their life force drain away!");
  
  elif item.name == "scroll of repair":
    game.menu.showEquipmentMenu(user);
    game.ui.animatedPrint("which equipment to repair? e.g bodypart");
    part = game.ui.getInput();
    try:
      if user.equipment[part] != None:
        user.equipment[part].durability = user.equipment[part].max_durability;
        game.ui.animatedPrint(f"[purple]{user.equipment[part].name}[reset] has been repaired (OK).");
      else: game.ui.animatedPrint(f"cannot repair item on [red]{part}[reset]")
    except KeyError:
      game.ui.animatedPrint("not a valid bodypart");
  
  elif item.name == "scroll of teleport":
    location = game.ui.getInput();
    user.usedItem(item.name);
    game.ui.clear();
    game.exploration_handler.move(location);
    
def use_sword(item, game, combat_handler, user):
  if user.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] already has a [yellow]{user.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return -1;
  
  game.ui.animatedPrint(f"[yellow]{user.name}[reset] equipped a [bold yellow]{item.name}[reset]!");
  strength_increased = round(user.stats["strength"] * 0.3);
  
  if item.name == "kevins sword": strength_increased *= 1.5;
  game.ui.animatedPrint(f"strength increased by [green]{strength_increased}[reset]!");
    
  game.giveStyle(user, "swordsman");
  user.stats["strength"] += strength_increased;
    
  user.equipment[item.bodypart].bonus = strength_increased;
    
def use_chest(item, game, combat_handler, user):
  if item.name == "starter chest":
    possible_loot = [getItem("wooden sword"), getItem("energy potion"), getItem("health potion"), getItem("scroll of repair"), getItem("strength potion")];
    
    amount_loot = randint(0, len(possible_loot));
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] opened up a [bold green]starter chest[reset]!");
    
    if amount_loot == 0:
      game.ui.animatedPrint(f"[red bold]the starter chest was empty[reset]!");
      return;
      
    recieved = choices(possible_loot[0:amount_loot], k = amount_loot);
    recieved_str = "";
    
    for item in recieved:
      amount_item = randint(1, 1 + round(user.stats["luck"]));
      recieved_str += (f"- [yellow]{item.name}[reset] ({item.rarity}) {amount_item} x\n");
      user.addItemToInventory(item, amount_item);
    game.ui.panelPrint(recieved_str.rstrip("\n"), title = "starter chest");
  
def use_glove(item, game, combat_handler, user):
  if user.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] already has a [yellow]{user.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return;
    
  if item.name == "leather gloves":
    game.ui.animatedPrint("you put on the leather gloves");
    game.ui.animatedPrint("its feel comfy.. gained +3 strength");
    user.stats["strength"] += 3;
    user.equipment[item.bodypart].bonus = strength_increased;

def use_bow(item, game, combat_handler, user):
  if user.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] already has a [yellow]{user.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return -1;
        
  if item.name == "wooden bow":
    strength_increased = 25;
    user.equipment[item.bodypart].bonus = strength_increased;
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] equipped a [bold blue]wooden bow[reset]!");
    game.ui.animatedPrint(f"strength [green]+{strength_increased}[reset]!");
    game.giveStyle(user, "archer");
    user.stats["strength"] += strength_increased;
    user.equipment[item.bodypart].bonus = strength_increased;

def use_food(item, game, combat_handler, user):
  if item.name == "bread":
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] ate a loaf of [bold green]bread[reset]!");
    game.ui.animatedPrint(f"hunger: {user.hunger + 20}");
    user.hunger = min(100, user.hunger + 20);
  
  elif item.name == "biscuit":
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] ate crunchy [bold green]biscuits[reset]!");
    game.ui.animatedPrint(f"hunger: {user.hunger + 10}");
    user.hunger = min(100, user.hunger + 10);
  
  elif item.name == "apple":
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] ate a fresh [bold cyan]apple[reset]!");
    game.ui.animatedPrint(f"hunger: {user.hunger + 15}");
    user.hunger = min(100, user.hunger + 15);
  
def use_book(item, game, combat_handler, user):
  if item.name == "bible":
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] opens up the [bold yellow]bible[reset]!");
    game.giveStyle(user, "cleric");
    
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
    "item": Item(name = "bread", rank = "D", rarity = "common", weight = 0.04),
    "action": use_food,  
  },
  "biscuit": {
    "item": Item(name = "biscuit", rank = "D", rarity = "common", weight = 0.02),
    "action": use_food,  
  },
  "apple": {
    "item": Item(name = "apple", rank = "D", rarity = "common", weight = 0.015),
    "action": use_food,  
  },
  "bible": {
    "item": Item(name = "bible", rank = "???", rarity = "???", weight = 0.05),
    "action": use_book,  
  }
};

