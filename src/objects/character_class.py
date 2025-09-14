from copy import deepcopy;

class Class:
  def __init__(self, name, stat_bonus = {}, skills = [], desc = ""):
    self.name = name;
    self.stat_bonus = stat_bonus;
    self.skills = skills;
    self.desc = desc;
  
  def to_dict(self):
    return {
      "name": self.name,
      "stat_bonus": self.stat_bonus,
      "skills" : self.skills,
      "desc" : self.desc,
      };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);
    
def getClass(name):
  return deepcopy(CLASSES[name]);
  
CLASSES = {
  "peasant": Class(
    "peasant", 
    {
      "increase" : [],
      "decrease" : [],
    },
    [],
  ),
  "swordsman": Class(
    "swordsman", 
    {
      "increase" : [["strength", 25]],
      "decrease" : [],
    },
    ["trislash", "blade blink", "hyper precision", "parry"],
    "insert desc here",
  ),
  "cleric": Class(
    "cleric", 
    {
      "increase" : [["defense", 30]],
      "decrease" : [],
    },
    ["divine protection", "divine restriction", "blunt recovery"],
    "insert desc here",
  ),
  "thief": Class(
    "thief", 
    {
      "increase" : [["dexterity", 20]],
      "decrease" : [["defense", 10]],
    },
    ["shadow step", "coin flip"],
    "insert desc here",
  )
};
 