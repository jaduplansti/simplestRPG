from character import Character;
from quest import Quest,progressQuest, getQuest;

class Player(Character):
  def __init__(self, name):
    super().__init__(name);
    self.quests = {};
  
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
    self.quests[name] = None;
    
  def questExists(self, name):
    try:
      self.quests[name];
      return True;
    except KeyError:
      return False;
      
  def trackQuest(self, game, combat_handler = None):
    for quest in self.quests:
      progressQuest(self.quests[quest]["obj"], self, game, combat_handler);
   