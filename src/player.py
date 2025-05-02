from character import Character;
from quest import progressQuest, QUESTS;

class Player(Character):
  def __init__(self, name):
    super().__init__(name);
    self.quests = {};
  
  def giveQuest(self, name):
    if self.questExists(name):
      return;
    
    try: 
      self.quests.update({name : {
        "obj" : QUESTS[name],
        "kills" : 0,
      }});
    except KeyError:
      return;
    
  def removeQuest(self, name):
    self.quests[name] = None;
    
  def questExists(self, name):
    try:
      self.quests[name];
      return True;
    except KeyError:
      return False;
      
  def trackQuest(self):
    for quest in self.quests:
      progressQuest(self.quests[quest]["obj"], self);
   