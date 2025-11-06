from random import randint, choices, choice, random;

class GoreHandler:
  def __init__(self, combat_handler):
    self.game = combat_handler.game;
    self.ui = combat_handler.ui;
    self.combat_handler = combat_handler;
    
    self.limb_resistance = {
      "head": 90,
      "arms": 60,
      "legs": 70,
    };
    
  def pickRandomPart(self, defender):
    if choices([True, False], [0.1, 0.9])[0] == False: return None;
    bodypart = choice(list(defender.bodyparts));
    if defender.bodyparts[bodypart] is False: return None;
    return bodypart;
  
  def canBreak(self, part, dmg, defender):
    damage_ratio = dmg / defender.stats["max health"]
    scaled_resistance = self.limb_resistance[part] * (1 + defender.level * 0.05)
    break_chance = damage_ratio * (100 / scaled_resistance);
    break_chance = min(break_chance, 0.80)  # cap at 80%
    return random() < break_chance;
    
  def injure(self, dmg, defender):
    bodypart = getattr(defender.enemy, "target_part", None);
    if bodypart is None: return;
    if defender.bodyparts[bodypart] is False: return;
    if self.canBreak(bodypart, dmg, defender) != True: return;
    self.ui.panelAnimatedPrintFile("gore", bodypart, [defender.name], bodypart);
    defender.bodyparts[bodypart] = False;
    defender.enemy.target_part = None;
    
  def getMultiplier(self, defender):
    bodypart = getattr(defender.enemy, "target_part", None);
    if bodypart is None: return 1;
    
    if bodypart == "head": return 1.6;
    elif bodypart == "arms": return 0.5;
    elif bodypart == "legs": return 0.8;
   