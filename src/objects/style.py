import string;
from objects.player import Player;
from random import randint, choice, choices, uniform;
from enum import Enum;

class SfxMode(Enum):
  SEQUENCE = 1;
  RANDOM = 2;
  RANDOM_SEQUENCE = 3;
  
class Style:
  def __init__(self, name, moves, sfx = {}, checks = [], equipmentUsed = [], mechanics = [], move_mechanics = {}):
    self.name = name;
    self.moves = moves;
    self.sfx = sfx;
    self.equipmentUsed = equipmentUsed;
    self.mechanics = mechanics;
    self.move_mechanics = move_mechanics;
   
  def playSfx(self, move, audio_handler):
    if move not in self.sfx:
      return;
    
    sfx = self.sfx[move];
    
    if sfx["mode"] == SfxMode.SEQUENCE:
      if not isinstance(sfx, list): 
        audio_handler.play(sfx["sounds"]);
        return;
     
      for sound in sfx["sounds"]:
        audio_handler.play(sound);
      return;
    
    elif sfx["mode"] == SfxMode.RANDOM:
      sound = choice(sfx["sounds"]);
      audio_handler.play(sound);
    
    elif sfx["mode"] == SfxMode.RANDOM_SEQUENCE:
      for sounds in sfx["sounds"]:
        sound = choice(sounds);
        audio_handler.play(sound);

  def damageEquipment(self, attacker, attack_handler, dmg):
    if len(self.equipmentUsed) == 0: return;
    attack_handler.consumeEquipment(attacker, self.equipmentUsed[0], dmg * self.equipmentUsed[1]);
  
  def handleMechanic(self, n, attacker, defender, game, combat_handler):
    if n < len(self.mechanics):
      return self.mechanics[n](attacker, defender, game, combat_handler);
  
  def handleMoveMechanic(self, move, attacker, defender, game, combat_handler):
    if move in self.move_mechanics:
      self.move_mechanics[move](attacker, defender, game, combat_handler);
      
  def attack(self, attacker, defender, game, combat_handler):
    attack_handler = combat_handler.attack_handler;
    ui = game.ui;
    move = choice(self.moves);
    
    if attack_handler.validateAttack(attacker, defender, move) != True: return;
    self.playSfx(move, game.audio_handler);
    self.handleMoveMechanic(move, attacker, defender, game, combat_handler);
    
    self.handleMechanic(0, attacker, defender, game, combat_handler);
    dmg = attack_handler.damage_handler.calculateDamage(move, attacker, defender);
    ui.panelAnimatedPrintFile(f"{self.name} style", move, [attacker.name, defender.name, dmg], move);
    
    attacker.attackEnemy(dmg, combat_handler);
    self.damageEquipment(attacker, attack_handler, dmg);
    self.handleMechanic(1, attacker, defender, game, combat_handler);

class StyleGiver:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    
  def giveStyle(self, char, style, announce = True):
    if self.removeStyle(char) == -1: return;
    char.attack_style = style;
    if announce is True: self.ui.animatedPrint(f"[yellow]{char.name}[reset] switched to [bold magenta]{char.attack_style}[reset] style!");
    # for skill in SKILLS:
#       if SKILLS[skill]["skill"]._class == char.attack_style: self.giveSkill(char, skill);
#     if char.attack_style == "swordsman": self.game.giveSkill(char, "parry")
#     elif char.attack_style == "cleric": self.giveSkill(char, "blunt recovery");
# 
  def removeStyle(self, char):
    if char.attack_style == "corrupted swordsman":
      self.ui.animatedPrint("cannot change style!, ([bold red]RESTRICTED[reset])");
      return -1;
      
    #for skill in SKILLS:
      #if SKILLS[skill]["skill"]._class == char.attack_style: char.removeSkill(skill);
    #char.attack_style = "basic";
  
def getStyle(name):
  return STYLES[name];
  
STYLES = {
  "basic": Style(
    name = "basic",
    moves = ["punch", "strong punch", "double punch"],
    sfx = {
      "punch" : {"mode" : SfxMode.RANDOM, "sounds" : ["punch1.wav", "punch2.wav"]},
      "strong punch" : {"mode" : SfxMode.SEQUENCE, "sounds" : "strong_punch.wav"},
      "double punch" : {"mode" : SfxMode.RANDOM_SEQUENCE, "sounds" : [["punch1.wav", "punch2.wav"], ["punch1.wav", "punch2.wav"]]},
    },
  ),
  
 "basic2": Style(
    name = "basic2",
    moves = ["kick", "tackle", "leg kick"],
    #sfx = {
      #"punch" : {"mode" : SfxMode.RANDOM, "sounds" : ["punch1.wav", "punch2.wav"]},
      #"strong punch" : {"mode" : SfxMode.SEQUENCE, "sounds" : "strong_punch.wav"},
      #"double punch" : {"mode" : SfxMode.RANDOM_SEQUENCE, "sounds" : [["punch1.wav", "punch2.wav"], ["punch1.wav", "punch2.wav"]]},
    #},
  ),
  
  "sword1": Style(
    name = "sword1",
    moves = ["slash", "thrust", "iron reversal", "blade dance"],
    sfx = {
      "slash" : {"mode" : SfxMode.RANDOM, "sounds" : ["slash1.wav", "slash2.wav"]},
      "thrust" : {"mode" : SfxMode.RANDOM, "sounds" : ["thrust1.wav", "thrust2.wav"]},
      "iron reversal" : {"mode" : SfxMode.SEQUENCE, "sounds" : "iron_reversal.wav"},
      "blade dance" : {"mode" : SfxMode.RANDOM_SEQUENCE, "sounds" : [["slash1.wav", "slash2.wav"], ["slash1.wav", "slash2.wav"], ["thrust1.wav", "thrust2.wav"]]},
    },
    equipmentUsed = [["right arm"], 0.12]
  ),
}