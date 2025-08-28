from random import randint, choices;
from copy import deepcopy;

class Skill:
  def __init__(self, name, desc, energy, rank, range = 0, level = 0, passive = False, passive_type = None, _style = None):
    self.name = name;
    self.energy = energy;
    self.rank = rank
    self.level = level;
    self.desc = desc;
    self.range = range;
    self.passive = passive;
    self.passive_type = passive_type;
    self._style = _style;
    
  def deductEnergy(self, character, n):
    character.energy = max(0, character.energy - n);
    
  def use(self, combat_handler = None, attacker = None, defender = None):
    if (self._style != None) and (self._style != attacker.attack_style): 
      combat_handler.ui.animatedPrint(f"you dont have the valid style for this skill, required '[yellow]{self._style}[reset]'");
      return;
      
    SKILLS[self.name]["action"](self, combat_handler, attacker, defender);
    self.deductEnergy(attacker, self.energy);
    attacker.prev_skill = self.name;
    
  def to_dict(self):
    return {
      "name": self.name,
      "energy": self.energy,
      "level": self.level,
      "desc" : self.desc,
      "rank" : self.rank,
      "range": self.range,
      "passive" : self.passive,
      "passive_type" : self.passive_type,
      "_style" : self._style,
      };

  @classmethod
  def from_dict(cls, data):
    return cls(**data);
    
def action_normal_damage(skill, combat_handler, attacker, defender): # generic skill attack
  if skill.name == "soul fracture":
    combat_handler.ui.printDialogue(attacker.name, "futile..");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] reaches out their hand, grasping [yellow]{defender.name}'s[reset] soul", "soul fracture");
    for stat in defender.stats: defender.stats[stat] *= 0.01;
    
  elif skill.name == "arrow rain" and attacker.itemExists("wooden arrow"):
    if combat_handler.attack_handler.validateAttack(attacker, defender, None, skill.range) is False: return;
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, (attacker.stats["strength"] + attacker.getAmountOfItem("wooden arrow")) * 1.5);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] unleashed a volley of arrows at [yellow]{defender.name}[reset], hitting for [red]{dmg}[reset] damage!", "arrow rain");
    attacker.attackEnemy(dmg, combat_handler);
    combat_handler.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], dmg * 0.4);
    defender.giveStatus("bleeding", 5);
  
  elif skill.name == "bow bash":
    if combat_handler.attack_handler.validateAttack(attacker, defender, None, skill.range) is False: return;
    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, attacker.stats["strength"]);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] bashed their bow at [yellow]{defender.name}[reset] with great force for [red]{dmg}[reset] damage!", "bow bash");
    attacker.attackEnemy(dmg, combat_handler);
    combat_handler.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], dmg);

  elif skill.name == "trislash":
    if combat_handler.attack_handler.validateAttack(attacker, defender, None, skill.range) is False: return;
    combat_handler.ui.printDialogue(attacker.name, ["my blade, your death..", "taste my blade!", "thrice, thats your end."]);
    combat_handler.ui.animatedPrint(f"[yellow]{attacker.name}[reset] drew their sword and slashed [yellow]{defender.name}[reset] 1x");
    combat_handler.game.audio_handler.play("slash1.wav");
   
    combat_handler.ui.animatedPrint(f"[yellow]{attacker.name}[reset]'s sword rotated and thrusted [yellow]{defender.name}[reset] 2x");
    combat_handler.game.audio_handler.play("thrust2.wav");
    combat_handler.ui.animatedPrint(f"[yellow]{attacker.name}[reset] put every ounce of strength and cut [yellow]{defender.name}[reset] 3x");
    combat_handler.game.audio_handler.play("slash2.wav");

    dmg = combat_handler.attack_handler.damage_handler.calculateDamage(None, attacker, defender, (attacker.stats["strength"] + randint(50, 60)) * 2.5);
    combat_handler.ui.panelAnimatedPrint(f"{attacker.name} drew their blade and sliced [yellow]{defender.name}[reset] 3x, dealing [red]{dmg}[reset] damage!", skill.name);
    attacker.attackEnemy(dmg, combat_handler);
    combat_handler.attack_handler.consumeEquipment(attacker, ["left arm", "right arm"], dmg * 0.4);
  
def action_normal_defense(skill, combat_handler, attacker, defender):
  if skill.name == "parry":
    combat_handler.ui.panelAnimatedPrintFile("parry", "parrying", [attacker.name, defender.name], "parry");
    attacker.giveStatus("parrying", 5);

def action_normal_recover(skill, combat_handler, attacker, defender):
  if skill.name == "blunt recovery":
    recovered = round(attacker.stats["max health"] * 0.4);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] imbues divine energy, healing for [yellow]{recovered}[reset] health", "blunt recovery");
    attacker.stats["health"] = min(attacker.stats["health"] + recovered, attacker.stats["max health"]);
    attacker.clearStatus();
  
  elif skill.name == "divine restriction":
    if combat_handler.attack_handler.validateAttack(attacker, defender, None, skill.range) is False: return;
    combat_handler.ui.printDialogue(attacker.name, "heed my prayers oh lord..");
    combat_handler.ui.printDialogue(attacker.name, "restrict thou sinner.");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] channels divine energy at [yellow]{defender.name}[reset], binding them in place!", "divine restriction");
    defender.giveStatus("stunned", 5);
    
  elif skill.name == "status wipe":
    if combat_handler.attack_handler.validateAttack(attacker, defender, None, skill.range, ignore_block = True) is False: return;
    combat_handler.ui.printDialogue(attacker.name, "purification, for the sinners.");
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] channels divine energy at [yellow]{defender.name}[reset], clearing their status!", "status wipe");
    defender.clearStatus();
    
def action_normal_misc(skill, combat_handler, attacker, defender):
  if skill.name == "analyze":
    combat_handler.ui.printDialogue(attacker.name, "analysis!");
    combat_handler.menu.showStatsMenu(defender);
    combat_handler.ui.awaitKey();
  
  elif skill.name == "coin flip":
    combat_handler.ui.animatedPrint(f"[yellow]{attacker.name}[reset] flips a coin");
    chosen_side = choices(["heads", "tails"])[0];
    combat_handler.ui.printDialogue(attacker.name, f"[cyan]{chosen_side}![reset]");
    random_stat = choices(list(attacker.stats))[0];
    
    if chosen_side == choices(["heads", "tails"])[0]: 
      combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}'s[reset] luck is overflowing, [cyan]{random_stat}[reset] [green]2.1x[reset]", "coin flip");
      attacker.stats[random_stat] = round(attacker.stats[random_stat] * 2.1);
    else:
      combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}'s[reset] lost the gamble, [cyan]{random_stat}[reset] [green]5%[reset]", "coin flip");
      attacker.stats[random_stat] = round(attacker.stats[random_stat] * 0.95);
      if randint(1, 2) == 1:
        combat_handler.ui.printDialogue(attacker.name, f"[red]again![reset]");
        return action_normal_misc(skill, combat_handler, attacker, defender);
      combat_handler.ui.printDialogue(attacker.name, f"[red]damn it![reset]");

  elif skill.name == "shadow burst":
    if not hasattr(attacker, "shadow"):
      combat_handler.ui.animatedPrint(f"[purple]the shadows reject {attacker.name}...[reset]");
      return; 
    
    attacker.shadow = round(attacker.shadow * 1.3);  
    combat_handler.ui.printDialogue(attacker.name, f"[red]shadow burst![reset]");
    combat_handler.ui.animatedPrint(f"[purple]{attacker.name}'s shadow overflows..[reset]");
    combat_handler.ui.panelPrint(f"[purple]SHADOW ({attacker.shadow})[reset]", "center");
    
  elif skill.name == "shadow step":
    if attacker.direction is None or defender.zone in [0, 9]:
      combat_handler.ui.animatedPrint(f"[purple]the shadows try to engulf {attacker.name}, however it fails...[reset]");
      return;
      
    combat_handler.ui.animatedPrint(f"[purple]the shadows engulf {attacker.name}...[reset]");
    combat_handler.ui.printDialogue(defender.name, f"?!");
    combat_handler.ui.animatedPrint(f"[purple]{attacker.name}[reset] suddenly appears behind [yellow]{defender.name}[reset]");
    
    if attacker.direction == "forward": attacker.zone = defender.zone + 1;
    elif attacker.direction == "backward": attacker.zone = defender.zone - 1;
    combat_handler.lockTarget(attacker, defender);
    combat_handler.attack_handler.handleAttack(attacker, defender);
    
def action_passive(skill, combat_handler, attacker, defender):
  if skill.name == "hyper precision" and combat_handler.previous_action in ["attack", "atk"] and defender.status["blocking"][0] is True:
    if randint(1, 2) == randint(1, 2):
      defender.status["blocking"] = [False, 0];
      combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset] focused into a hyper focus state, breaking {defender.name}'s block", title = skill.name);
  
  elif skill.name == "flowing blade" and attacker.status["blocking"][0] is True and attacker.status["parrying"][0] is True:
    attacker.status["blocking"] = [False, 0];
    defender.giveStatus("stunned", 2);
    combat_handler.ui.panelAnimatedPrint(f"[yellow]{attacker.name}[reset]'s perfected defense, stunned [yellow]{defender.name}[reset]!", title = skill.name);

  elif skill.name == "arrow return" and combat_handler.previous_action in ["attack", "atk"]:
    if randint(1, 3) == randint(1, 3) and attacker.itemExists("wooden arrow"): combat_handler.game.givePlayerItem("wooden arrow", 1);
  
  elif skill.name == "divine protection" and attacker.stats["health"] <= attacker.stats["max health"] * 0.3 and randint(1, 4) == randint(1, 4):
    attacker.status["bleeding"] = [False, 0];
    attacker.status["stunned"] = [False, 0];
    attacker.stats["health"] = attacker.stats["max health"] * 0.4;
    combat_handler.ui.panelAnimatedPrint(f"a divine light engulfed [yellow]{attacker.name}[reset]'s, healing them for (40%) and clearing all debuffs.", title = skill.name);
    combat_handler.ui.panelPrint("[yellow]RECOVERY![reset]");
  
  elif skill.name == "limitless":
    if hasattr(defender, "dmg"):
      combat_handler.ui.panelAnimatedPrint(f"[yellow]{defender.name}[reset]'s, attack never reached [yellow]{attacker.name}[reset]", title = skill.name);
      combat_handler.ui.panelPrint("[blue]NO DAMAGE[reset]");
      defender.dmg = 0;
      
def getSkill(name):  
  try:
    return deepcopy(SKILLS[name]["skill"]);
  except KeyError:
    return None;
    
SKILLS = {
 "coin flip" : {
    "skill" : Skill("coin flip", "heads or tails? 50% chance to increase or decrease a stat", 20, "C", range = 0, _style = "dagger1"), 
    "action" : action_normal_misc
  },
  "shadow burst" : {
    "skill" : Skill("shadow burst", "increases shadow by 1.3x", 15, "C+", range = 0, _style = ""), 
    "action" : action_normal_misc
  },
  "shadow step" : {
    "skill" : Skill("shadow step", "the shadows creeping, appear behind an enemy for a guranteed backstab", 20, "C+", range = 0, _style = "dagger1"), 
    "action" : action_normal_misc
  },
  "arrow rain" : {
    "skill" : Skill("arrow rain", "shoots a volley of arrows at the enemy, inflicting 5 stacks of bleeding.", 25, "C+", range = 6, _style = "bow1"), 
    "action" : action_normal_damage
  },
  "bow bash" : {
    "skill" : Skill("bow bash", "smash the bow into a enemy, dealing mediocre damage", 15, "D", range = 2, _style = "bow1"), 
    "action" : action_normal_damage
  },
  "trislash" : {
     "skill" : Skill("trislash", "triple the slash, triple the fun.", 30, "C+", range = 2, _style = "sword1"), 
     "action" : action_normal_damage
  },
  "soul fracture" : {
     "skill" : Skill("soul fracture", "a divine technique capable of reducing soul capabilities, cannot be blocked or nullified", 50, "B-", range = 0), 
     "action" : action_normal_damage
  },
  "parry" : {
    "skill" : Skill("parry", "inflicts a parrying status", 12, "C", range = 0), 
    "action" : action_normal_defense
  },
  "blunt recovery" : {
    "skill" : Skill("blunt recovery", "a divine light, capable of healing any injuries.", 20, "C-", range = 0), 
    "action" : action_normal_recover
  },
  "analyze" : {
    "skill" : Skill("analyze", "eyes of appraisal, lists down the status of the target.", 0, "D", range = 0), 
    "action" : action_normal_misc,
  },
  "divine restriction" : {
    "skill" : Skill("divine restriction", "chains of a sinner, restricting for 5 stacks..", 30, "C+", range = 3, _style = "bible1"), 
    "action" : action_normal_recover
  },
  "status wipe" : {
    "skill" : Skill("status wipe", "fear, clears status of the enemy including karma.", 10, "C+", range = 3, _style = "bible1"), 
    "action" : action_normal_recover
  },
  "hyper precision" : {
    "skill" : Skill("hyper precision", "you see flaws in every stance, your attacks have a 50% to block break!", 0, "C+", range = 0, passive = True, passive_type = "attack", _style = "sword1"), 
    "action" : action_passive
  },
  "flowing blade" : {
    "skill" : Skill("flowing blade", "the ultimate defense, when you are both blocking and parrying, you apply 2 stacks of stun and reset your stance.", 0, "C+", range = 0, passive = True, passive_type = "attack", _style = "sword1"), 
    "action" : action_passive
  },
  "arrow return" : {
    "skill" : Skill("arrow return", "arrows shot have a 33% chance to return a arrow.", 0, "C-", range = 0, passive = True, passive_type = "attack", _style = "bow1"), 
    "action" : action_passive
  },
  "divine protection" : {
    "skill" : Skill("divine protection", "as a follower of god, you are blessed by thy protecion.", 0, "B-", range = 0, passive = True, passive_type = "death", _style = "bible1"), 
    "action" : action_passive
  },
}