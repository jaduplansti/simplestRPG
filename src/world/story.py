from mechanics.combat import CombatHandler;
from objects.character import Character;
from copy import deepcopy;

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
  
  def __startScene(self):
    self.ui.clear();
    self.overrideSpeed([0.02, 2]);
  
  def __endScene(self):
    self.ui.awaitKey();
    self.restoreSpeed();
    self.progress += 1;
  
  def intro(self):
    self.ui.clear();
    self.ui.normalPrint("-- [green]would you like to skip chapter 1[reset] --\n");
    self.ui.normalPrint("(yes) or (no)\n");
    option = self.ui.getInput();
    if option == "yes": return;
    self.scene1();
    
  def scene1(self):
    self.__startScene();
    self.game.player.stats["health"] = 20;
    
    self.game.animator.matrixIntro();
    self.ui.printDialogue(self.game.player.name, "Augh, my head hurts..");
    self.ui.printDialogue(self.game.player.name, "Where am i..");
    self.ui.animatedPrint("[bold](warning)[reset]: [red]Health Under 25%[reset]");
    self.ui.animatedPrint("Your vision clears slightly, Strange shapes and faint light surrounds you.");
    self.ui.printDialogue("???", "Finally, you have awoken.");
    option = self.ui.getChoice(["Who the hell are you?!", "Who are you.."]);
    
    if option == 1: self.ui.printDialogue("???", "Now now, no need for such vulgar language.");
    self.ui.printDialogue("???", "My identity should not be your concern.");
    self.ui.printDialogue("???", "What matters is what [red]'you'[reset] are.");
    self.ui.printDialogue("???", "A [magenta]fallen hero[reset]..");
    option = self.ui.getChoice(["What?"]);
    
    self.ui.printDialogue("???", f"Think [yellow]{self.game.player.name}[reset], think.");
    self.ui.printDialogue("???", f"[bold red]Remember what they did to you![reset]");
    self.ui.printDialogue(self.game.player.name, "............");
    self.__endScene();
    self.scene2();
    
  def scene2(self):
    self.__startScene();
    self.ui.showHeader("Memories", "+");
    
    self.ui.printDialogue("elira", "Guys focus! the demon lord is just up ahead.");
    self.ui.printDialogue("asta", "Hell yeah, cant wait to be famous, id be king!");
    self.ui.printDialogue(self.game.player.name, "Not sure man, i dont think a loner like you can.");
    self.ui.printDialogue("asta", "What? no way, for your information i go outside my room every week.");
    
    self.ui.printDialogue("elira", "Hehe, not with your lazy attitude.");
    self.ui.printDialogue("asta", "Tch. you have a point..");
    self.ui.printDialogue("roman", f"Hey {self.game.player.name}?");
    option = self.ui.getChoice(["What is it?", "Huh?"]);
    
    self.ui.printDialogue("roman", f"We'll stay and handle the small fries.");
    self.ui.printDialogue("roman", f"Go and finish this [italic yellow]once and for all[reset].");
    self.__endScene();
    self.scene3();
  
  def scene3(self):
    self.__startScene();
    self.ui.showHeader("Memories", "+");
    self.ui.printDialogue(self.game.player.name, "[magenta]Demon King Azaroth[reset].");
    self.ui.printDialogue(self.game.player.name, "Its about time this 100th year war ends.");
    self.ui.printDialogue(self.game.player.name, "No more war, No more bloodshed.");
    
    self.ui.printDialogue("[magenta]azaroth[reset]", "[red]HAHAHAHAHAHAHAHAHHAHAHAHAHAHHAAHHA[reset].");
    self.ui.printDialogue("[magenta]azaroth[reset]", "How foolish of you, to think that bloodshed will end?");
    option = self.ui.getChoice(["Burn in hell azaroth", "Fuck you."]);
    if option == 1: self.ui.printDialogue("[magenta]azaroth[reset]", "Quite ironic, for a demon to burn in hell.");
    
    self.ui.printDialogue("[magenta]azaroth[reset]", "Ill crush your [red]resolve[reset] hero.");
    self.__endScene();

    # combat setup
    backup = deepcopy(self.game.player);
    self.game.givePlayerExp(100000);
    self.game.player.tryLevelUp();
    
    combat = CombatHandler(self.game);
    combat.initiateFightNpc(self.game.player, "azaroth");
    self.game.player = backup;
    self.ui.awaitKey();
    
    if combat.won == self.game.player.name: self.scene3a();
    else: self.scene3b();
    
  def scene3a(self):
    self.__startScene();
    self.ui.printDialogue(self.game.player.name, "[red]Augh![reset] Damn it...");
    self.ui.panelPrint("Forgotten Hero\n\n+25 all stats", "center", "title acquired");
    for stat in self.game.player.stats:
      if stat != "luck": self.game.player.stats[stat] += 25;
    self.ui.printDialogue("[magenta]azaroth[reset]", "Impressive, hero...");
    self.ui.printDialogue("[magenta]azaroth[reset]", "Humans. So fragile, so pure at a glance, yet they harbor the deepest corruption.");
    self.ui.printDialogue("[magenta]azaroth[reset]", "This world you cling to. Is it worth saving? They hasten their own extinction.");
    option = self.ui.getChoice(["What do you mean?"]);
    self.ui.printDialogue("[magenta]azaroth[reset]", "I almost feel sorry for you...");
    self.ui.animatedPrint("[magenta]azaroths[bold] corpse slowly crumbles into ash. The Hundred Year War finally ends, each generation failing where the last once stood, never truly slaying the next demon lord.");
    self.ui.animatedPrint("Without warning, a cold blade pierces your back. The shock burns, sharp, deep, and [red]agonizing[reset].");
    self.ui.printDialogue(self.game.player.name, "[bold red]Elira?![reset] Why?!");
    self.ui.printDialogue("elira", "[cyan]Aww~ you were getting too close, you know that?[reset]");
    self.ui.printDialogue("elira", "We cant have a hero tearing apart our little future.");
    self.ui.printDialogue("elira", "Roman and the others already agreed. You outlived your usefulness.");
    self.ui.printDialogue("elira", "So this is goodbye, hero~");
    self.ui.printDialogue(self.game.player.name, "[red]ELIRA![reset]");
    self.ui.animatedPrint("You Have Died.");
    self.__endScene();
  
  def scene3b(self):
    self.__startScene();
    self.ui.animatedPrint("[red]You struggle to breathe, barely clinging to your dear life.[reset]");
    self.ui.animatedPrint("[magenta]Azaroth grabs you by the neck and strangles you.[reset]");
    self.ui.printDialogue("[magenta]azaroth[reset]", "[red]Trash[reset], is that all human?");
    self.ui.printDialogue("[magenta]azaroth[reset]", "I expected more, you dream of ending this war.");
    self.ui.printDialogue("[magenta]azaroth[reset]", "But is this all you can do? disappointing..");
    option = self.ui.getChoice(["My comrades are coming, they'll wipe the grin off your face.", "My teammates are going kill you bastard!"]);
    self.ui.printDialogue("[magenta]azaroth[reset]", "Really? you mean those dogshit corpses?");
    self.ui.animatedPrint("Suddenly you hear a faint scream, resembling elira's voice.");
    self.ui.printDialogue(self.game.player.name, "Elira?!");
    self.ui.printDialogue("[magenta]azaroth[reset]", "Ah that woman? she'll make a good breeding slave for our orcs, well if she survives.");
    self.ui.printDialogue(self.game.player.name, "You mother fucke-");
    self.__endScene();
    
  def scene4(self):
    self.__startScene();
    self.ui.printDialogue("???", f"So do you remember now, {self.game.player.name}?");
    option = self.ui.getChoice(["Yeah..", "A bit, buts its a bit hazy.."]);
    self.__endScene();
    
  def handleStory(self, combat_handler = None): # this function runs the scene, for the current progress.
    pass;