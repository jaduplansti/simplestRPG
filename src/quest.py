from copy import deepcopy;

class Quest:
  def __init__(self, name, desc):
    self.name = name;
    self.desc = desc;

  def to_dict(self):
    return {
      "name": self.name,
      "desc" : self.desc,
    };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);

def getQuest(name):
  try:
    return deepcopy(QUESTS[name]);
  except KeyError:
    return False;
    
def progressQuest(quest, character, game, combat_handler = None):
  if quest.name == "goblin slayer" and combat_handler != None:
    quest_data = character.quests[quest.name];
    
    if combat_handler.defender.name == "goblin" and combat_handler.defender.stats["health"] <= 0: quest_data["kills"] += 1;
    if quest_data["kills"] >= 2: completeQuest(quest, character, game);
    
def completeQuest(quest, character, game):
  game.ui.panelPrint(f"[bold yellow]You have compeleted {quest.name}![reset]");
  character.removeQuest(quest.name);

  if quest.name == "goblin slayer": 
    game.ui.animatedPrint("your hatred for goblins has caused you to gain [yellow]5000[reset] exp!");
    game.givePlayerExp(5000);
  
  game.handlePlayerLevelUp();

QUESTS = {
  "goblin slayer" : Quest("goblin slayer", "show the goblins the hate you feel by killing 10 goblins"),
};