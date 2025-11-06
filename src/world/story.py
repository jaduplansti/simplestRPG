from mechanics.combat import CombatHandler;
from objects.character import Character;

class Story:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    self.old_speed = [0, 0];
    self.progress = 1;
    
  def overrideSpeed(self, newSpeed : list):
    self.old_speed = list(self.game.settings.values());
    self.game.settings["type speed"] = newSpeed[0];
    self.game.settings["delay speed"] = newSpeed[1];
  
  def restoreSpeed(self):
    self.game.settings["type speed"] = self.old_speed[0];
    self.game.settings["delay speed"] = self.old_speed[1];
   
  def scene1(self):
    self.ui.clear();
    self.ui.animatedPrint("would you like to skip the [yellow]story/tutorial[reset]?");
    self.ui.printTreeMenu("", ["yes", "no"]);
    if self.ui.getInput() == "yes":
      self.progress = 5;
      return;
    self.ui.clear();
    
    self.overrideSpeed([0.03, 2]);
    self.ui.animatedPrint("...");
    self.ui.animatedPrint("[yellow]The throne room hums with power.[reset]");
    self.ui.animatedPrint("A glowing circle burns into the marble floor.");
    
    self.ui.animatedPrint("Dozens of mages stand around it, their hands trembling.");
    self.ui.animatedPrint("Their chants grow louder, the air twisting from heat.");
    self.ui.animatedPrint("[red]*A blinding light fills the room.*[reset]");
    self.ui.animatedPrint("Then, silence.")
    
    self.ui.animatedPrint("You stand in the center of the circle.");
    self.ui.animatedPrint("Smoke rises. The smell of ash clings to the air.");
    self.ui.printDialogue("King", "So... this is the one?");
    self.ui.printDialogue("Head Mage", "Your Majesty... the summoning is complete.");
    
    self.ui.showStatus("analyzing..", 2);
    self.ui.panelPrint(f"[yellow]{self.game.player.name}[reset] (HERO)\n- no skills\n- no talents\n- Overall: F", "center", "appraise");
    self.ui.printDialogue("King", "No aura. No weapon. No skill?");
    self.ui.printDialogue("Mage", "Perhaps... there was a mistake.");
    
    self.ui.animatedPrint("[dim]The room grows tense. The mages look away.[reset]");
    self.ui.printDialogue("King", "You wasted our strength on this?");
    self.ui.animatedPrint("He turns his back to you, voice cold and final.");
    self.ui.printDialogue("King", "Send them away.")
    
    self.ui.animatedPrint("[magenta]The circle beneath you ignites once more.[reset]");
    self.ui.animatedPrint("The mages chant weakly, drained but obedient.");
    self.ui.animatedPrint("Light swallows your vision. The castle fades away.");
    self.ui.animatedPrint("...");
    
    self.ui.animatedPrint("[green]When you wake, you’re lying on dirt and grass.[reset]");
    self.ui.animatedPrint("The night sky glows faintly through the trees.");
    self.ui.animatedPrint("The summoning circle flickers once... then fades.");
    self.ui.awaitKey();
    
    self.restoreSpeed();
    self.progress += 1;
    self.scene2();
    
  def scene2(self):
    self.ui.clear();
    self.overrideSpeed([0.03, 1.5]);
    self.ui.animatedPrint("The forest is still. Only the wind moves.");
    self.ui.animatedPrint("You sit up slowly, dirt clinging to your clothes.");
    self.ui.animatedPrint("No castle. No voices. Just the whisper of leaves.");
    
    self.ui.animatedPrint("...");
    self.ui.animatedPrint("[dim]Something wet slides against the grass nearby.[reset]");
    self.ui.animatedPrint("You glance over.");
    self.ui.animatedPrint("[yellow]A small, translucent mass quivers in the dark.[reset]");
    
    self.ui.animatedPrint("It jiggles forward—curious, harmless-looking.");
    self.ui.printDialogue(self.game.player.name, "...a slime?");
    self.ui.animatedPrint("It trembles once, then leaps straight at you.");
    self.ui.printDialogue(self.game.player.name, "Guess that answers that.");
    
    self.ui.animatedPrint("[red]The slime attacks![reset]");
    self.ui.awaitKey();
    
    self.restoreSpeed();
    combat = CombatHandler(self.game);
    combat.initiateFightNpc(self.game.player, "slime");
    self.ui.awaitKey();
    
    self.ui.clear();
    self.overrideSpeed([0.03, 1.5]);
    
    if combat.won == self.game.player.name:
      self.ui.animatedPrint("[green]*The slime bursts apart, dissolving into the soil.*[reset]");
      self.ui.animatedPrint("You catch your breath, wiping the goo from your arms.");
      self.ui.printDialogue(self.game.player.name, "Tougher than it looked...");
    else:
      self.ui.animatedPrint("[red]*The slime slams into you, knocking you to the ground.*[reset]");
      self.ui.animatedPrint("Your vision blurs. The air feels heavy.");
      self.ui.animatedPrint("The last thing you see is the slime pulsing faintly in the dark.");
      self.ui.printDialogue(self.game.player.name, "Damn... not like this...");
      self.ui.animatedPrint("[dim]Everything fades to black.[reset]");
      self.ui.animatedPrint("...");
      self.ui.animatedPrint("When you open your eyes, the forest is silent again.");
    
    self.game.player.stats["health"] = self.game.player.stats["max health"];
    self.ui.animatedPrint("[dim]Something faint glows where the slime fell.[reset]");
    self.ui.animatedPrint("You pick up a small crystal—warm to the touch.");
    self.ui.printDialogue(self.game.player.name, "No aura... but maybe this could be useful.");
    self.game.givePlayerItem("seal of origin");
    
    self.restoreSpeed();
    self.ui.awaitKey();
    self.progress += 1;
    self.scene3();
    
  def scene3(self):
    self.ui.clear();
    self.overrideSpeed([0.03, 1.5]);
    self.ui.printDialogue(self.game.player.name, "Gotta get moving... I don't know this continent at all.");
    self.ui.printDialogue(self.game.player.name, "I mean, what kind of idiot summons someone from another world and just leaves them to fend for themselves?");
    
    self.ui.printDialogue(self.game.player.name, "So much for a classic 'isekai' plot...");
    self.ui.showStatus("walking...", 10);
    self.ui.animatedPrint("After a while, you notice a small village in the distance.");
    self.ui.animatedPrint("The sunlight glints off the rooftops, but you can also make out guards stationed at the gate, alert and tense.");
    
    self.ui.printDialogue(self.game.player.name, "Hmm… gates on a village? That’s… unusual.");
    self.ui.animatedPrint("Cautiously, you approach the villager standing watch at the gate. The air feels tense, like even a small mistake could draw their ire.");
    self.ui.printDialogue("villager", "Identify yourself, foreigner.");
    name = self.ui.input("What’s your name?");
    
    if name != "":
      self.ui.printDialogue("villager", f"{name}? I see...");
    else:
      self.ui.printDialogue("villager", "Hmph… can't even say your own name.");
    
    self.ui.printDialogue("villager", "Very well, you may pass.");
    self.ui.printDialogue("villager", "Just… try not to cause any trouble while you’re here.");
    self.ui.animatedPrint("You step through the gate, the village stretching out before you, alive with the murmur of daily life—but something feels off...");
    
    self.restoreSpeed();
    self.ui.awaitKey();
    self.progress += 1;
    self.scene4();
    
  def scene4(self):
    self.ui.clear();
    self.overrideSpeed([0.03, 1.5]);
    
    self.ui.animatedPrint("You step fully into the village, leaving the gates behind.");
    self.ui.animatedPrint("The cobblestone streets hum with life—children dart between market stalls, merchants shout over each other, and the smell of fresh bread drifts from a bakery.");
    self.ui.animatedPrint("For the first time since arriving in this world, things… feel ordinary.");
    
    self.ui.printDialogue(self.game.player.name, "Huh… a village that isn’t trying to kill me yet. Small miracles, I guess.");
    self.ui.animatedPrint("A cheerful voice calls out from the side of the street. An older woman, hands on her hips, squints at you.");
    self.ui.printDialogue("villager", "Hey there, stranger! You look like you could use a rest. Just arrived, huh?");
    self.ui.printDialogue(self.game.player.name, "Yeah… kinda. Don’t really know anyone yet.");
    
    self.ui.printDialogue("villager", "Well, you’re in luck! My home has an empty room, and tonight it’s yours. No charge. Consider it a proper welcome to our little corner of the world.");
    self.game.giveSkill(self.game.player, "analyze", announce = True);
    self.ui.input("open skill panel (y/n)"); # opens it regardless lmao
    self.game.handleUseSkill("analyze", self.game, self.game.player, Character("Elara"));
    
    self.ui.clear();
    self.ui.animatedPrint("You raise an eyebrow, half-expecting a trap, but there’s nothing but warmth in her smile.");
    self.ui.printDialogue(self.game.player.name, "…Wow. Thanks. Really. I haven’t had a proper bed in ages.");
    self.ui.animatedPrint("The villager gestures for you to follow, weaving through narrow lanes lined with lanterns and flower boxes.");
   
    self.ui.animatedPrint("Inside her cozy house, a fire crackles, casting dancing shadows. A simple bed waits, blankets neatly folded.");
    self.ui.printDialogue("villager", "Rest up. Tomorrow’s another day, and who knows what kind of trouble—or adventure—you’ll find.");
    self.restoreSpeed();
    self.ui.awaitKey();
    
    self.progress += 1;
    return;
  
  def scene5(self):
    self.ui.clear();
    self.overrideSpeed([0.03, 1.5]);

    self.ui.animatedPrint("Someone knocks on your door.");
    self.ui.printDialogue("???", f"is this {self.game.player.name}?");
    name_confirm = self.ui.input("(yes/no)");
    if name_confirm == "no":
      self.ui.printDialogue("???", f"oh—sorry, must’ve mixed up the houses.");
      self.ui.printDialogue(self.game.player.name, f"haha, just kidding. yeah, i’m {self.game.player.name}.");
    self.ui.printDialogue("isaac", f"thank the stars. we’ve got a problem, and we need you.");
    self.ui.printDialogue("isaac", f"a swarm of slimes just oozed into the village outskirts.");
    self.ui.printDialogue("isaac", f"they’ve been clogging the wells, eating crops—total chaos.");
    self.ui.printDialogue("isaac", f"the guards are stretched thin after last night’s patrol.");
    self.ui.printDialogue("isaac", f"i figured someone like you could handle a few blobs of goo.");
    self.ui.printDialogue(self.game.player.name, f"slimes, huh? guess it’s better than bandits.");
    self.ui.printDialogue("isaac", f"you say that now, but these things multiply fast. one turns to ten before you know it.");
    self.ui.printDialogue(self.game.player.name, f"got it. any idea where they’re coming from?");
    self.ui.printDialogue("isaac", f"the forest near the old mill. nobody’s sure why, but the ground there’s... sticky. corrupted, maybe.");
    self.ui.printDialogue("isaac", f"take this job, and the villagers will owe you one. maybe even the baker’ll toss in some free bread.");
    self.ui.printDialogue(self.game.player.name, f"free bread and slime guts. my favorite combination.");
    self.ui.printDialogue("isaac", f"haha, good attitude. when you’re ready, head to the east gate. i’ll have someone waiting to guide you.");
    self.game.giveQuest("pest control");
    
    self.restoreSpeed();
    self.progress += 0.5;
    self.ui.awaitKey();
  
  def scene6(self):
    self.ui.clear();
    self.overrideSpeed([0.03, 1.5]);
  
    self.ui.animatedPrint("A knock sounds at your door. You open it to see Isaac grinning like he’s got good news.");
    self.ui.printDialogue("Isaac", "Hey! It’s me, Isaac. First off… thanks again for dealing with those slimes. The village owes you big time.");
    self.ui.printDialogue(self.game.player.name, "Yeah… those little blobs were trickier than I thought. Sneaky little things.");
    self.ui.printDialogue("Isaac", "Ha! Sneaky is one word for it. I heard some villagers tried to fight them off and… well… let’s just say it didn’t end well.");
  
    choice = self.ui.input("Say something to Isaac:");
    self.ui.printDialogue(self.game.player.name, choice);
    self.ui.printDialogue("Isaac", "Haha, glad to hear that. Anyway, I’ve got your reward right here.");
  
    self.ui.animatedPrint("Isaac pulls out a small pouch and some bread.");
    self.game.givePlayerMoney(100);
    self.game.givePlayerItem("bread", 3);
  
    self.ui.printDialogue(self.game.player.name, "Fresh bread?! You didn’t have to…");
    self.ui.printDialogue("Isaac", "Yep! Straight from the bakery this morning. Extra butter, too. Consider it a ‘thanks for saving our village’ bonus.");
  
    bread_response = self.ui.input("How do you react to the bread?");
    self.ui.printDialogue(self.game.player.name, bread_response);
    self.ui.printDialogue("Isaac", "Haha, thought you’d like that.");
  
    self.ui.printDialogue("Isaac", "And don’t forget, you got some gold too, 100 coins. Not a fortune, but enough to get started.");
    self.ui.printDialogue(self.game.player.name, "Alright, gold and bread. Today’s shaping up nicely.");
  
    self.ui.printDialogue("Isaac", "I better get going more villagers to calm down and… other duties. But don’t forget to check out the shop. They’ve got useful stuff, and if you’re clever, you can haggle a bit.");
    self.ui.printDialogue(self.game.player.name, "Got it. I’ll try not to spend all my bread in one place.");
  
    self.ui.animatedPrint("[yellow]Hint:[reset] The [bold]shop[reset] is a great way to get general items. Negotiating can get you better deals!");
  
    self.restoreSpeed();
    self.progress += 1;
    self.ui.awaitKey();
  
  def scene7(self, dave):
    self.ui.clear();
    self.overrideSpeed([0.03, 1.5]);
    self.ui.printDialogue(dave.name, "Oi mate, word is the village owes you a lot.");
    self.ui.printDialogue(dave.name, "So, on their behalf… I’ve got a little something for you.");
    self.ui.printDialogue(dave.name, "A starter chest—hope it’s worth the effort.");
    self.game.givePlayerItem("starter chest", 3);
    self.ui.printDialogue(self.game.player.name, "Whoa… that’s heavier than I expected, but cheers.");
    self.ui.printDialogue(dave.name, "Ha! Don’t just stand there groaning, lad. That chest ain’t gonna carry itself.");
    self.ui.printDialogue(self.game.player.name, "Alright, alright… I’ll manage. Looks like it’s packed pretty well too.");
    self.ui.printDialogue(dave.name, "Good stuff inside, nothing fancy, but should help get you started.");
    self.ui.printDialogue(dave.name, "Now, enough chatter. Let’s get to business, eh?");
    self.restoreSpeed();
    self.progress += 1;
    self.ui.awaitKey();
  
  def scene8(self, dave):
    self.ui.clear()
    self.overrideSpeed([0.03, 1.5])
    
    self.ui.printDialogue("Isaac", f"{self.game.player.name}! Hey, got a minute?")
    self.ui.printDialogue(self.game.player.name, "Hmm? Sure, what’s up?")
    self.ui.printDialogue("Isaac", "Okay… this is a bit awkward.")
    self.ui.printDialogue("Isaac", "I need… money.")
    self.ui.printDialogue(self.game.player.name, "Ohhh boy… this should be interesting.")
    
    self.ui.printDialogue(dave.name, "*sigh* here we go again. Lending money to this guy is a full-time job.")
    self.ui.printDialogue("Isaac", "Look, it’s my anniversary. My wife wants a ring… and I’m 100g short.")
    self.ui.printDialogue(dave.name, "Anniversary, huh? Sounds expensive.")
    self.ui.printDialogue("Isaac", "Yeah, and of course Dave here is stingy as ever, won’t lend me a single coin!")
    self.ui.printDialogue(dave.name, "For heaven’s sake, Isaac… get a second job already.")
    self.ui.printDialogue("Isaac", "My job barely pays enough to keep food on the table, okay?")
    
    self.ui.animatedPrint("[dim]You glance at Isaac. He’s genuinely stressed… but also somehow charmingly desperate.[reset]")
    
    lend_money = self.ui.input("Do you lend him money? (yes/no)")
    money = 100
    
    if lend_money.lower() == "no":
      self.ui.printDialogue(self.game.player.name, "Ah… can’t help this time, sorry.")
      self.ui.printDialogue("Isaac", "Aw… really? Come on! I promise I’ll make it up to you!")
      self.ui.printDialogue(self.game.player.name, "…Fine. Don’t make a habit of this.")
      self.ui.printDialogue(dave.name, "*grumble* humans, so unreliable…")
    
    if self.game.player.money < 100:
      money = self.game.player.money // 2
      self.ui.printDialogue(self.game.player.name, f"Okay… I don’t have 100g, but here’s {money}g. Make it last.")
      self.ui.printDialogue("Isaac", "Half? Better than nothing! You’re a lifesaver!")
    else:
      self.ui.printDialogue(self.game.player.name, f"Sure, Isaac. Here’s 100g. Happy anniversary.")
      self.ui.printDialogue("Isaac", "YES! You’re a legend! I owe you one, big time.")
    
    self.ui.animatedPrint(f"[yellow]{self.game.player.name}[reset] lent [green]{money}[reset]g to Isaac.")
    
    self.ui.printDialogue("Isaac", "Seriously, thank you! I’ll… uh… bake you a cake or something!")
    self.ui.printDialogue(dave.name, "Cake, huh? Don’t forget last time it exploded all over the shop.")
    self.ui.printDialogue("Isaac", "That was one time! Okay… maybe two.")
    self.ui.printDialogue(self.game.player.name, "…I’ll hold you to that cake promise.")
    
    self.ui.printDialogue("Isaac", "Anyway! Gotta run. Duty calls, chaos awaits, yada yada. Thanks again!")
    self.ui.printDialogue(dave.name, "Finally… back to business.")
    
    self.game.player.money -= money;
    self.restoreSpeed()
    self.progress += 1
    self.ui.awaitKey()
  
  def scene9(self):
    pass;
    
  def handleStory(self, combat_handler = None): # this function runs the scene, for the current progress.
    if self.progress == 6: self.scene6();
    elif self.game.player.level >= 4 and self.progress == 5: self.scene5();
      
   
