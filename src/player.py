from character import Character;
from quest import Quest, progressQuest, getQuest;

from item import getItem;
from skill import getSkill;
from copy import deepcopy;

class Player(Character):
  def __init__(self, name):
    super().__init__(name);
    self.quests = {};   # { quest_name: Quest }
    
  def to_dict(self):
    data = super().to_dict();
    data.update({
      "quests": {
        name: quest.to_dict()
        for name, quest in self.quests.items()
      }
    });
    return data;
  
  @classmethod
  def from_dict(cls, data):
    char = super().from_dict(data);
    char.quests = {
      name: Quest.from_dict(quest_data)
      for name, quest_data in data.get("quests", {}).items()
    };
    return char;
    
  def giveQuest(self, name):
    if self.questExists(name):
      return -1;
    quest = getQuest(name);
    if quest == False: return -1;
    self.quests[name] = quest;
    
  def removeQuest(self, name):
    if name in self.quests:
      del self.quests[name];
    
  def questExists(self, name):
    return name in self.quests;
      
  def trackQuest(self, game, combat_handler = None):
    quests_backup = deepcopy(self.quests);
    for quest in quests_backup:
      progressQuest(self.quests[quest], self, game, combat_handler);