class Quest:
  def __init__(self, name, desc):
    self.name = name;
    self.desc = desc;
    

def progressQuest(quest, character, combat_handler):
  if quest.name == "goblin slayer":
    quest_data = character.quests[quest.name];
    quest_data["kills"] += 1;
    if quest_data["kills"] >= 10: completeQuest(quest, character);
    
def completeQuest(quest, character):
  if quest.name == "goblin slayer":
    character.removeQuest(quest.name);
    pass; # do award here
    
QUESTS = {
  "goblin slayer" : Quest("goblin slayer", "show the goblins the hate you feel.\nkill 10 goblins"),
};