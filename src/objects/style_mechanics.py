from random import randint, choice;

def flowFinisher(attacker, defender, dmg, style, combat_handler):
  if defender.stats["health"] <= defender.stats["max health"] * 0.3:
    combat_handler.ui.printDialogue(attacker.name, "the next hit will end this.");
    attacker.true_crit = True;
    attacker.next_crit_multiplier = 20;
    style.attack(attacker, defender, combat_handler.game, combat_handler);

def handleBasicMechanic(attacker, defender, style, move, combat_handler, dmg = 0):
  if combat_handler.game.isPlayer(attacker) is False: 
    return;
  
  if hasattr(attacker, "flow_meter") is False:
    attacker.flow_meter = 0;
  
  attacker.flow_meter += 1;

  if move == "double punch" and randint(1, 3) == 1:
    attacker.flow_meter += 2;
    style.attack(attacker, defender, combat_handler.game, combat_handler);
  
  if move == "strong punch" and dmg >= defender.stats["defense"] * 1.2:
    defender.giveStatus("stunned", 1);
    
  if attacker.flow_meter >= 10: 
    attacker.flow_meter = 0;
    combat_handler.ui.panelPrint("[bold blue]Flow Overflow[reset]");
    flowFinisher(attacker, defender, dmg, style, combat_handler);
    
  elif (attacker.flow_meter % 4) == 0 and (getattr(attacker, "true_crit", False) is False):
    combat_handler.ui.animatedPrint("[blue]Flow bonus triggered, critical guaranteed[reset].");
    attacker.true_crit = True;
    attacker.next_crit_multiplier = attacker.flow_meter;
    
def handleSword1Mechanic(attacker, defender, style, move, combat_handler, dmg = 0):
  if getattr(defender, "sword_weakness", None) is None and randint(1, 3) == 1:
    attacker.weakness_noticed = False;
    defender.sword_weakness = choice(list(defender.bodyparts));
  
  if getattr(attacker, "weakness_noticed", False) is False and getattr(defender, "sword_weakness", None) != None and combat_handler.game.isPlayer(attacker) and defender.stats["health"] > 0:
    combat_handler.ui.printDialogue(attacker.name, f"Their {defender.sword_weakness}, that’s the weak point.");
    attacker.weakness_noticed = True;
  
  if getattr(attacker, "target_part", None) != None and attacker.target_part == getattr(defender, "sword_weakness", ""):
    combat_handler.ui.panelAnimatedPrint(f"{attacker.name} read {defender.name}'s stance and drove their blade cleanly through!", "Precise!")
    defender.sword_weakness = choice([bp for bp in defender.bodyparts if bp != defender.sword_weakness]);
    attacker.true_crit = True;
    attacker.giveStatus("parrying", 1);

 