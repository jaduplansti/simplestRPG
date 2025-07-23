from copy import deepcopy;

class Quest:
  def __init__(self, name, desc, rank = "F"):
    self.name = name;
    self.desc = desc;
    self.rank = rank;
    
  def to_dict(self):
    return {
      "name": self.name,
      "desc" : self.desc,
      "rank" : self.rank,
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
  if quest.name == "goblin cleanup" and combat_handler != None:
    quest_data = character.quests[quest.name];
    
    if combat_handler.defender.name == "goblin" and combat_handler.defender.stats["health"] <= 0: quest_data["kills"] += 1;
    if quest_data["kills"] >= 4: completeQuest(quest, character, game);
  
  if quest.name == "pest control" and combat_handler != None:
    quest_data = character.quests[quest.name];
    
    if combat_handler.defender.name == "slime" and combat_handler.defender.stats["health"] <= 0: quest_data["kills"] += 1;
    if quest_data["kills"] >= 4: completeQuest(quest, character, game);
  
  if quest.name == "fallen heart": completeQuest(quest, character, game);
  
def completeQuest(quest, character, game):
  game.ui.panelPrint(f"[bold yellow]You have compeleted {quest.name}![reset]");
  character.removeQuest(quest.name);

  if quest.name == "goblin cleanup": 
    game.ui.animatedPrint("your hatred for goblins has caused you to gain [yellow]5000[reset] exp!");
    game.givePlayerExp(5000);
  
  elif quest.name == "pest control": 
    game.ui.animatedPrint("your hatred for slimes has caused you to gain [yellow]3000[reset] exp!");
    game.givePlayerExp(3000);
  
  elif quest.name == "fallen heart": game.givePlayerExp(10000);
  
  game.handlePlayerLevelUp();

QUESTS = {
  "goblin cleanup" : Quest("goblin cleanup", "show the goblins the hate you feel by killing 4 goblins", rank = "E"),
  "pest control" : Quest("pest control", "crush 4 slimes to death..", rank = "E"),
  "fallen heart" : Quest("fallen heart", "kill a fallen knight", rank = "D"),
};