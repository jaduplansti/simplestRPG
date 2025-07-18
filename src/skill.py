from random import randint, choices;
from copy import deepcopy;

class Skill:
  def __init__(self, name, desc, energy, rank, level = 0, passive = False, passive_type = None):
    self.name = name;
    self.energy = energy;
    self.rank = rank
    self.level = level;
    self.desc = desc;
    self.passive = passive;
    self.passive_type = passive_type;
    
  def deductEnergy(self, character, n):
    character.energy = max(0, character.energy - n);
    
  def use(self, combat_handler = None, attacker = None, defender = None):
    SKILLS[self.name]["action"](self, combat_handler, attacker, defender);
    self.deductEnergy(attacker, self.energy);
    
  def to_dict(self):
    return {
      "name": self.name,
      "energy": self.energy,
      "level": self.level,
      "desc" : self.desc,
      "rank" : self.rank,
      "passive" : self.passive,
      "passive_type" : self.passive_type,
      };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);
    
def action_normal_damage(skill, combat_handler, attacker, defender): # generic skill attack
  if skill.name == "soul shatter":
    if (attacker.stats["health"] < defender.stats["health"]) and combat_handler.game.isPlayer(attacker):
      combat_handler.ui.panelPrint(f"user's health is lower than the enemy, this will sacrifice 20% max health in return, proceed (yes/no)", "center", "Warning", "red");
      if combat_handler.ui.getInput() == "n": return;
      attacker.stats["max health"] = round(attacker.stats["max health"] * 0.8);
    combat_handler.ui.printDialogue(attacker.name, "thy soul is stained..");
    combat_handler.ui.printDialogue(attacker.name, "this stained soul shall be cleansed.");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] reaches out their hand, grasping [yellow]{defender.name}'s[reset] soul and crushing it.", "soul shatter");
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, 9999);
    attacker.attackEnemy(dmg);
    
  elif combat_handler.attack_handler.handleBlock(attacker, defender) is True:
      return;  
      
  elif skill.name == "crimson edge": # this is just a placeholder
    combat_handler.ui.panelPrint(f"{attacker.name} unleashed a crimson edge!");
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, 500);
    for n in range(1, 100):
      combat_handler.ui.panelPrint(f"[bold red]DEALT 5 DAMAGE! {n}x[reset]");
      attacker.attackEnemy(5);
  
  elif skill.name == "arrow rain" and attacker.itemExists("wooden arrow"):
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, attacker.stats["strength"] * 1.5);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] unleashed a volley of arrows at [yellow]{defender.name}[reset], hitting for [red]{dmg}[reset] damage!", "arrow rain");
    attacker.attackEnemy(dmg);
    combat_handler.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], dmg * 0.4);
    defender.giveStatus("bleeding", 5);
  
  elif skill.name == "bow bash":
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, attacker.stats["strength"]);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] bashed their bow at [yellow]{defender.name}[reset] with great force for [red]{dmg}[reset] damage!", "bow bash");
    attacker.attackEnemy(dmg);
    combat_handler.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], dmg);

  elif skill.name == "trislash":
    combat_handler.ui.printDialogue(attacker.name, "my blade, your death..");
    combat_handler.ui.animatedPrint(f"[yellow]{attacker.name}[reset] drew their sword and slashed [yellow]{defender.name}[reset] 1x");
    combat_handler.ui.animatedPrint(f"[yellow]{attacker.name}[reset]'s sword rotated and thrusted [yellow]{defender.name}[reset] 2x");
    combat_handler.ui.printDialogue(attacker.name, "the finale!");

    combat_handler.ui.animatedPrint(f"[yellow]{attacker.name}[reset] put every ounce of strength and cut [yellow]{defender.name}[reset] 3x");
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, attacker.stats["strength"] * 1.8);
    combat_handler.ui.panelAnimatedPrint(f"{attacker.name} drew his blade and sliced [yellow]{defender.name}[reset] 3x, dealing [red]{dmg}[reset] damage!", skill.name);
    attacker.attackEnemy(dmg);
  
  
def action_normal_defense(skill, combat_handler, attacker, defender):
  if skill.name == "parry":
    attacker.giveStatus("parrying", 5);

def action_normal_recover(skill, combat_handler, attacker, defender): # generic skill attack
  if skill.name == "blunt recovery":
    recovered = round(attacker.stats["max health"] * 0.4);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] imbues divine energy, healing for [yellow]{recovered}[reset] health", "blunt recovery");
    attacker.stats["health"] = min(attacker.stats["health"] + recovered, attacker.stats["max health"]);
    attacker.clearStatus();
  
  elif skill.name == "divine restriction":
    combat_handler.ui.printDialogue(attacker.name, "heed my prayers oh lord..");
    combat_handler.ui.printDialogue(attacker.name, "restrict thou sinner.");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] channels divine energy at [yellow]{defender.name}[reset], binding them in place!", "divine restriction");
    defender.giveStatus("stunned", 5);
    
  elif skill.name == "status wipe":
    combat_handler.ui.printDialogue(attacker.name, "purification, for the sinners.");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] channels divine energy at [yellow]{defender.name}[reset], clearing their status!", "status wipe");
    defender.clearStatus();
    
def action_passive(skill, combat_handler, attacker, defender):
  if skill.name == "hyper precision" and combat_handler.previous_action in ["attack", "atk"]:
    if randint(1, 2) == randint(1, 2):
      defender.status["blocking"] = [False, 0];
      combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] focused into a hyper focus state, breaking {defender.name}'s block", title = skill.name);
  
  elif skill.name == "flowing blade" and attacker.status["blocking"][0] is True and attacker.status["parrying"][0] is True:
    attacker.status["blocking"] = [False, 0];
    defender.giveStatus("stunned", 2);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset]'s perfected defense, stunned [yellow]{defender.name}[reset]!", title = skill.name);

  elif skill.name == "arrow return" and combat_handler.previous_action in ["attack", "atk"]:
    if randint(1, 3) == randint(1, 3) and attacker.itemExists("wooden arrow"): combat_handler.game.givePlayerItem("wooden arrow", 1);
  
  elif skill.name == "divine protection" and attacker.stats["health"] <= attacker.stats["max health"] * 0.3 and randint(1, 3) == randint(1, 3):
    attacker.status["bleeding"] = [False, 0];
    attacker.status["stunned"] = [False, 0];
    attacker.stats["health"] = attacker.stats["max health"] * 0.7;
    combat_handler.ui.panelAnimatedPrint(f"a divine light engulfed [yellow]{attacker.name}[reset]'s, healing them for (50%) and clearing all debuffs.", title = skill.name);
    combat_handler.ui.panelPrint("[yellow]RECOVERY![reset]");
    
def getSkill(name):  
  try:
    return deepcopy(SKILLS[name]["skill"]);
  except KeyError:
    return None;
    
SKILLS = {
  "arrow rain" : {
    "skill" : Skill("arrow rain", "shoots a volley of arrows at the enemy, inflicting 5 stacks of bleeding.", 25, "C+"), 
    "action" : action_normal_damage
  },
  "bow bash" : {
    "skill" : Skill("bow bash", "smash the bow into a enemy, dealing mediocre damage", 15, "D"), 
    "action" : action_normal_damage
  },
  "trislash" : {
     "skill" : Skill("trislash", "triple the slash, triple the fun.", 30, "C+"), 
     "action" : action_normal_damage
  },
  "soul shatter" : {
     "skill" : Skill("soul shatter", "a divine technique capable of crushing the soul of the enemy, cannot be blocked or nullified", 80, "S+"), 
     "action" : action_normal_damage
  },
  "parry" : {
    "skill" : Skill("parry", "inflicts a parrying status", 12, "C"), 
    "action" : action_normal_defense
  },
  "blunt recovery" : {
    "skill" : Skill("blunt recovery", "a divine light, capable of healing any injuries.", 20, "C-"), 
    "action" : action_normal_recover
  },
  "divine restriction" : {
    "skill" : Skill("divine restriction", "chains of a sinner, restricting for 5 stacks..", 30, "C+"), 
    "action" : action_normal_recover
  },
  "status wipe" : {
    "skill" : Skill("status wipe", "fear, clears status of the enemy including karma.", 10, "B--"), 
    "action" : action_normal_recover
  },
  "hyper precision" : {
    "skill" : Skill("hyper precision", "you see flaws in every stance, your attacks have a 50% to block break!", 0, "C+", passive = True, passive_type = "attack"), 
    "action" : action_passive
  },
  "flowing blade" : {
    "skill" : Skill("flowing blade", "the ultimate defense, when you are both blocking and parrying, you apply 2 stacks of stun and reset your stance.", 0, "C+", passive = True, passive_type = "attack"), 
    "action" : action_passive
  },
  "arrow return" : {
    "skill" : Skill("arrow return", "arrows shot have a 33% chance to return a arrow.", 0, "C-", passive = True, passive_type = "attack"), 
    "action" : action_passive
  },
  "divine protection" : {
    "skill" : Skill("divine protection", "as a follower of god, you are blessed by thy protecion.", 0, "B-", passive = True, passive_type = "death"), 
    "action" : action_passive
  },
};

