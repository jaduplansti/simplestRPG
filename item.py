class Item:
  def __init__(self, 
  name, 
  durability = 1, 
  rank = "E", 
  rarity = "common", 
  weight = 0.1, 
  stat_bonus = None, 
  category = None):
    
    self.name = name;
    self.durability = durability;
    self.rarity = rarity;
    self.weight = weight;
    self.stat_bonus = stat_bonus;
    self.category = category;
    
def createItem(name, durability = 1, rank = "E", rarity = "common", weight = 0.1, stat_bonus = None, category = None):
    return Item(
      name,
      durability = durability,
      rank = rank,
      rarity = rarity,
      weight = weight,
      stat_bonus = stat_bonus,
      category = category,
    );