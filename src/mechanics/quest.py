from copy import deepcopy;

class Quest:
  def __init__(self, name, desc, condition, _type, progress = 0, rank = "F"):
    self.name = name;
    self.desc = desc;
    self.rank = rank;
    self._type = _type;
    self.condition = condition;  # e.g. ["goblin", 4]
    self.progress = progress;
    
  def to_dict(self):
    return {
      "name": self.name,
      "desc": self.desc,
      "rank": self.rank,
      "_type": self._type,
      "condition": self.condition,
      "progress": self.progress,
    };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);

def getQuest(name):
  try:
    return deepcopy(QUESTS[name]);
  except KeyError:
    return False;

def progressKill(quest, character, game, combat_handler):
  if combat_handler is None: return;
  if combat_handler.defender.name == quest.condition[0] and combat_handler.defender.stats["health"] <= 0:
    quest.progress += 1;
  if quest.progress < quest.condition[1]: return;
  else: completeQuest(quest, character, game);
  
def progressQuest(quest, character, game, combat_handler = None):
  if quest._type == "kill":
    progressKill(quest, character, game, combat_handler);
    
def completeQuest(quest, character, game):
  game.ui.panelPrint(f"[bold yellow]You have compeleted {quest.name}![reset]");
  
  if quest.name == "pest control":
    if game.story_handler.progress == 5.5:
      game.story_handler.slime_cleaned = True;
      game.story_handler.progress += 0.5;
    game.ui.animatedPrint("you gain [yellow]3000[reset] exp!");
    game.givePlayerExp(3000);
    
  elif quest.name == "goblin cleanup":
    game.ui.animatedPrint("you gain [yellow]5000[reset] exp!");
    game.givePlayerExp(5000);

  elif quest.name == "fallen heart":
    game.ui.animatedPrint("you gain [yellow]10000[reset] exp!");
    game.givePlayerExp(10000);
  
  character.removeQuest(quest.name);

def upgradeRank(quest, character, game):
  next_rank = "";
  current_rank = character.guild_hall["rank"];
  
  rank_order = ["E", "D", "C", "B", "A", "S"];
  if current_rank in rank_order:
    idx = rank_order.index(current_rank);
    if idx + 1 < len(rank_order): next_rank = rank_order[idx + 1];

QUESTS = {
  "goblin cleanup": Quest(
    "goblin cleanup",
    "show the goblins the hate you feel by killing 4 goblins",
    condition=["goblin", 4],
    _type="kill",
    rank="E",
  ),
  "pest control": Quest(
    "pest control",
    "crush 4 slimes to death..",
    condition=["slime", 4],
    _type="kill",
    rank="E",
  ),
  "fallen heart": Quest(
    "fallen heart",
    "kill a fallen knight",
    condition=["fallen knight", 1],
    _type="kill",
    rank="D",
  ),
};