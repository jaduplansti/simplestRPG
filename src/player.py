from character import Character;
from quest import Quest,progressQuest, getQuest;

from item import getItem;
from skill import getSkill;

class Player(Character):
  def __init__(self, name):
    super().__init__(name);
    self.quests = {};
  
    self.addItemToInventory(getItem("bible"), 1);
    self.addItemToInventory(getItem("skill book"), 20);
    self.addItemToInventory(getItem("health potion"), 10);
    self.addItemToInventory(getItem("wooden sword"), 1);
    self.addItemToInventory(getItem("wooden dagger"), 1);
    self.addSkill(getSkill("soul fracture"));
    self.addSkill(getSkill("analyze"));

  def to_dict(self):
    data = super().to_dict();
    data.update({"quests": {
        name: {
          "obj": quest_data["obj"].to_dict(),
          "kills": quest_data["kills"]
        } for name, quest_data in self.quests.items()
    }});
    return data;
  
  @classmethod
  def from_dict(cls, data):
    char = super().from_dict(data);
    char.quests = {
      name: {
          "obj": Quest.from_dict(quest_data["obj"]),
          "kills": quest_data["kills"]
        } for name, quest_data in data["quests"].items()
    }
    return char;
    
  def giveQuest(self, name):
    if self.questExists(name):
      return -1;
    
    try: 
      self.quests.update({name : {
        "obj" : getQuest(name),
        "kills" : 0,
      }});
    except KeyError:
      return -1;
    
  def removeQuest(self, name):
    del self.quests[name];
    
  def questExists(self, name):
    try:
      self.quests[name];
      return True;
    except KeyError:
      return False;
      
  def trackQuest(self, game, combat_handler = None):
    for quest in list(self.quests):
      progressQuest(self.quests[quest]["obj"], self, game, combat_handler);
   