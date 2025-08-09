from random import randint, choices;
from copy import deepcopy;

class Equipment:
  """
  an Equipment class.
  
  Parameters:
  name, a string holding the name for the equipment, very important
  durability, a integer containing the current health potion
  max_durability, a integer containing the max health point of an item
  bodypart, a string containing either left arm, right arm, head, chest and boots.
  bonus, a integer storing bonuses
  """
  
  def __init__(self, name, bodypart, durability, max_durability, desc, bonus = None):
    self.name = name;
    self.bodypart = bodypart;
    self.durability = durability;
    self.max_durability = max_durability;
    self.desc = desc;
    if bonus != None: self.bonus = bonus;
    else: self.bonus = {"increase" : {}, "decrease" : {}};
   
  def getDurability(self):
    return (self.durability / self.max_durability) * 100
    
  def consumeDurability(self, n):
    self.durability = round(max(self.durability - n, 0));
    
  def handleDurability(self, n):
    self.consumeDurability(n);
    if self.durability <= 0:
      return True;
  
  def setBonus(self, key, stat, n):
    self.bonus[key].update({stat : n});
  
  def formatBonus(self):
    formatted_bonus = "";
    for stat in self.bonus["increase"]:
      formatted_bonus += f"[yellow]{stat}[reset] ([cyan]{self.bonus["increase"][stat]}[reset] ↑)\n"
    for stat in self.bonus["decrease"]:
      formatted_bonus += f"[yellow]{stat}[reset] ([red]{self.bonus["decrease"][stat]}[reset] ↓)\n"
    formatted_bonus = formatted_bonus.rstrip("\n");
    return formatted_bonus;
    
  def removeEquipment(self, plr, game):
    if any(name in self.name.lower() for name in ["sword", "dagger", "bow"]) : game.removeStyle(plr);
    for stat in self.bonus["increase"]: plr.stats[stat] = max(0, plr.stats[stat] - self.bonus["increase"][stat]);
    for stat in self.bonus["decrease"]: plr.stats[stat] += self.bonus["decrease"][stat]
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
      "desc": self.desc,
    };

def equipmentToItem(equipment):
  item = getItem(equipment.name);
  item.durability = equipment.durability;
  item.max_durability = equipment.max_durability;
  return item;
  
def itemToEquipment(item):
  return Equipment(item.name, item.bodypart, item.durability, item.max_durability, item.desc);
  
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
  _type = None,
  desc = None,
  ):
    
    self.name = name;
    self.max_durability = max_durability
    self.durability = durability;
    self.rank = rank;
    self.rarity = rarity;
    self.weight = weight;
    self.bodypart = bodypart;
    self.desc = desc;
    self._type = _type;
    
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
      "rank": self.rank,
      "desc" : self.desc,
      "bodypart": self.bodypart,
      };
  
  def rarityToVal(self, weight = 3):
    for n, val in enumerate(["common", "uncommon", "rare", "epic", "legendary"]):
      if self.rarity == val: return (n + 1) * weight;
    return weight;
    
  def durabilityToVal(self):
    if self.durability <= self.max_durability * 0.2:
      return 0.2;
    elif self.durability <= self.max_durability * 0.5:
      return 0.5;
    elif self.durability < self.max_durability * 0.8:
      return 0.8;
    return 1;
  
  def typeToVal(self):
    if self._type == "sword": return 50;
    elif self._type == "dagger": return 30;
    elif self._type == "bow": return 20;
    elif self._type == "arrow": return 8;
    elif self._type == "book": return 35;
    elif self._type == "scroll": return 32;
    elif self._type == "chest armor": return 60;
    elif self._type == "potion": return 25;
    elif self._type == "food": return 10;
    else: return 1;
    
  def getValue(self):
    return (self.typeToVal() * self.rarityToVal()) * self.durabilityToVal();
    
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
  
  elif item.name == "exp potion":
    if user.exp <= 0:
      game.ui.animatedPrint(f"[yellow]{user.name}[reset] used a exp potion, but it failed..");
      return;
      
    exp_increased = round(user.exp * 5);
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] used a exp potion!");
    game.ui.printDialogue(user.name, "argh!");
    
    game.ui.printDialogue(user.name, "it hurts...");
    game.ui.showStatus("evolving!", 3, "boxBounce");
    game.ui.printDialogue(user.name, "ARGH........");
    game.ui.showStatus("evolving!", 3, "boxBounce");
    
    user.giveDamage(round(user.stats["max health"] * 0.6))
    if user.stats["health"] <= 0:
      game.ui.animatedPrint(f"[red]{user.name} couldn't handle the exp potion..[reset]");
      game.ui.animatedPrint(f"[yellow]{user.name}[reset] vision flicker, slowly collapsing...");
    else:
      game.givePlayerExp(exp_increased);
      game.ui.animatedPrint(f"[yellow]{user.name}[reset] gained [cyan]{exp_increased}[reset] exp!");
      game.handlePlayerLevelUp();
      game.ui.printDialogue(user.name, "im never doing that again.");
      user.giveDamage(round(user.stats["max health"] * 0.6))

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
  elif item.name == "ashrend sword": strength_increased = 30 * user.level;

  game.ui.animatedPrint(f"strength increased by [green]{strength_increased}[reset]!");
    
  game.giveStyle(user, "swordsman");
  user.stats["strength"] += strength_increased;
    
  user.equipment[item.bodypart].setBonus("increase", "strength", strength_increased);
  
def use_dagger(item, game, combat_handler, user):
  if user.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] already has a [yellow]{user.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return -1;
  
  game.ui.animatedPrint(f"[yellow]{user.name}[reset] equipped a [bold yellow]{item.name}[reset]!");
  dexterity_increased = round(user.stats["dexterity"] * 2);
  defense_decreased = round(user.stats["defense"] * 0.5);
 
  game.ui.animatedPrint(f"dexterity increased by [green]{dexterity_increased}[reset]!");
  game.ui.animatedPrint(f"defense decreased by [red]{defense_decreased}[reset]!");

  game.giveStyle(user, "thief");
  user.stats["dexterity"] += dexterity_increased;
  user.stats["defense"] = max(0, user.stats["defense"] - defense_decreased);

  user.equipment[item.bodypart].setBonus("increase", "dexterity", dexterity_increased);
  user.equipment[item.bodypart].setBonus("decrease", "defense", defense_decreased);
    
def use_chest(item, game, combat_handler, user):
  if item.name == "starter chest":
    possible_loot = [];
    for item in ITEMS: 
      if ITEMS[item]["item"].rarity in ["common", "uncommon"]: possible_loot.append(ITEMS[item]["item"]);
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
  
def use_bow(item, game, combat_handler, user):
  if user.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] already has a [yellow]{user.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return -1;
        
  if item.name == "wooden bow":
    strength_increased = 25;
    user.equipment[item.bodypart].setBonus("increase", "strength", strength_increased);
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] equipped a [bold blue]wooden bow[reset]!");
    game.ui.animatedPrint(f"strength [green]+{strength_increased}[reset]!");
    game.giveStyle(user, "archer");
    user.stats["strength"] += strength_increased;

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
  
  elif item.name == "skill book":
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] opened a [bold cyan]skill book[reset]!");
    skills = [];
    all_skills = game.getSkills();
    for skill in all_skills: 
      if all_skills[skill]["skill"]._class == None: skills.append(skill);
    skill = choices(list(skills))[0];
 
    game.ui.showStatus("reading", 3);
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] learnt [underline green]{skill}[reset]!");
    game.giveSkill(user, skill);
    
def use_armor(item, game, combat_handler, user):
  if user.equipItem(item) != True:
    game.ui.animatedPrint(f"[yellow]{user.name}[reset] already has a [yellow]{user.equipment[item.bodypart].name}[reset] on their [italic green]{item.bodypart}[reset]");
    return -1;
    
  game.ui.animatedPrint(f"[yellow]{user.name}[reset] equipped a [bold cyan]{item.name}[reset]!");

  if item.name == "peasant tunic":
    defense_increased = 30;
    user.equipment[item.bodypart].setBonus("increase", "defense", defense_increased);
    game.ui.animatedPrint(f"defense [green]+{defense_increased}[reset]!");
    user.stats["defense"] += defense_increased;

  if item.name == "worn leather vest":
    defense_increased = 50;
    user.equipment[item.bodypart].setBonus("increase", "defense", defense_increased);
    game.ui.animatedPrint(f"defense [green]+{defense_increased}[reset]!");
    user.stats["defense"] += defense_increased;

ITEMS = {
  "wooden sword": {
    "item": Item(name="wooden sword", max_durability = 150, durability = 150, rank="E", weight=3.5, bodypart="right arm", _type = "sword", desc="A basic, unrefined sword carved from wood. Good for training or fending off small creatures."),
    "action": use_sword
  },
  "wooden dagger": {
    "item": Item(name="wooden dagger", max_durability = 100, durability = 100, rank="E", weight=2.0, bodypart="right arm", _type = "dagger", desc="A small, crude dagger made from wood. Not very effective in combat, but better than nothing."),
    "action": use_dagger
  },
  "peasant tunic": {
    "item": Item(name="peasant tunic", max_durability = 100, durability = 100, rank="E", weight=4.0, bodypart="chest", _type = "chest armor", desc="A simple, cloth tunic worn by peasants. Offers very little protection."),
    "action": use_armor,
  },
  "worn leather vest": {
    "item": Item(name="worn leather vest", max_durability = 250, durability = 250, rank="E", weight=4.5, bodypart="chest", _type = "chest armor", desc="A vest made from old, worn leather. Provides more protection than a tunic, but is far from new."),
    "action": use_armor,
  },
  "wooden bow": {
    "item": Item(name="wooden bow", max_durability = 100, durability = 100, rank = "E", weight = 3.5, bodypart = "right arm", _type = "bow", desc="A simple bow crafted from a single piece of wood. Suitable for target practice or hunting small game."),
    "action": use_bow
  },
  "steel sword": {
    "item": Item(name="steel sword", max_durability = 400, durability = 400, rank="D+", weight = 14.5, bodypart= "right arm", _type = "sword", desc="A solid sword forged from steel. A reliable and sturdy weapon for the average adventurer."),
    "action": use_sword
  },
  "ashrend sword": {
    "item": Item(name="ashrend sword", max_durability = 800, durability = 800, rarity = "legendary", rank="A", weight = 18.5, bodypart= "right arm", _type = "sword",  desc="A legendary sword said to be forged in the heart of a volcano. It glows with a faint, fiery aura and feels surprisingly light."),
    "action": use_sword
  },
  "kevins sword": {
    "item": Item(name="kevins sword", max_durability = 1, durability = 1, rank="C", weight = 1.0, bodypart = "right arm", _type = "sword", desc="A seemingly ordinary sword with an incredibly low durability. Who is Kevin, and why is his sword so fragile?"),
    "action": use_sword
  },
  "health potion": {
    "item": Item(name="health potion", rank="E", weight=0.5, _type = "potion", desc="A small vial containing a crimson liquid. Consuming it restores a small amount of health."),
    "action": use_potion
  },
  "energy potion": {
    "item": Item(name="energy potion", rank="E", weight=0.5, _type = "potion", desc="A small vial containing a bright green liquid. It provides a quick burst of energy, perfect for replenishing stamina."),
    "action": use_potion
  },
  "scroll of instant death": {
    "item": Item(name="scroll of instant death", rank="B", rarity="rare", weight=0.2, _type = "scroll", desc="A rare and powerful scroll. Once activated, it unleashes a curse that can instantly defeat a single target."),
    "action": use_scroll
  },
  "scroll of repair": {
    "item": Item(name="scroll of repair", rank="D", rarity="uncommon", weight=0.2, _type = "scroll", desc="A scroll with a magical inscription. It can be used to repair the durability of a single item."),
    "action": use_scroll
  },
  "starter chest": {
    "item": Item(name="starter chest", durability=1, rank="D", rarity="common", weight=20.0, _type = "chest", desc="A simple wooden chest containing basic items to help a new adventurer on their journey."),
    "action": use_chest
  },
  "strength potion": {
    "item": Item(name="strength potion", rank="D", rarity="uncommon", weight=0.5, _type = "potion", desc="A potion that permanently boosts the drinker's physical strength."),
    "action": use_potion
  },
  "cleanse potion": {
    "item": Item(name="cleanse potion", rank="C", rarity="uncommon", weight=0.5, _type = "potion", desc="A potion that purges the body of minor ailments, curses, and poisons."),
    "action": use_potion
  },
  "scroll of teleport": {
    "item": Item(name = "scroll of teleport", rank = "C", rarity = "rare", weight = 0.2, _type = "scroll", desc="A scroll that allows the user to instantly teleport to a known location."),
    "action": use_scroll,
  },
  "wooden arrow": {
    "item": Item(name = "wooden arrow", rank = "D", rarity = "common", weight = 1.5, _type = "arrow", desc="A simple wooden arrow. The standard ammunition for most bows."),
    "action": None,  
  },
  "bread": {
    "item": Item(name = "bread", rank = "D", rarity = "common", weight = 0.8, _type = "food", desc="A loaf of fresh-baked bread. A basic food that restores a small amount of health and energy."),
    "action": use_food,  
  },
  "biscuit": {
    "item": Item(name = "biscuit", rank = "D", rarity = "common", weight = 0.5, _type = "food", desc="A small, hard biscuit. While not the most appetizing, it provides a small bit of sustenance."),
    "action": use_food,  
  },
  "apple": {
    "item": Item(name = "apple", rank = "D", rarity = "common", weight = 0.5, _type = "food", desc="A crisp, red apple. It's a healthy and refreshing snack."),
    "action": use_food,  
  },
  "bible": {
    "item": Item(name = "bible", rank = "???", rarity = "???", weight = 0.5, _type = "book", desc="An ancient book containing holy scripture. Its true power is a mystery."),
    "action": use_book,  
  },
  "skill book": {
    "item": Item(name = "skill book", rank = "A", rarity = "epic", weight = 3.5, _type = "book", desc="A rare and valuable book that, when read, can teach the reader a new skill."),
    "action": use_book,  
  },
  "exp potion": {
    "item": Item(name = "exp potion", rank = "A", rarity = "rare", weight = 0.9, _type = "potion", desc="A potion of experience, gives 5x exp."),
    "action": use_potion,  
  }
};

