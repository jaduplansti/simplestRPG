from submenu import SubMenu;
from random import choices;
from quest import QUESTS, getQuest;

class GuildHall(SubMenu):
  def __init__(self, game):
    super().__init__(game);
    self.max_page = 1;
    self.board = [];
    
  def showGuildMenu(self):
    self.ui.clear();
    
    self.ui.showSeperator("-");
    self.showGuildHeader();
    self.ui.showSeperator("-");
    
    self.ui.normalPrint("••••••••••••••");
    self.ui.normalPrint("• [italic yellow]Guild Hall[reset] •");
    self.ui.normalPrint("••••••••••••••\n");
    
    self.ui.normalPrint("≈ [yellow]board[reset]");
    self.ui.normalPrint("≈ [red]bounty[reset]");
    self.ui.normalPrint("≈ [green]request[reset]");
    self.ui.normalPrint("≈ [purple]learn[reset]");
    self.ui.normalPrint("≈ [blue]leave[reset]\n");

  def showGuildHeader(self):
    self.ui.console.print(f"[yellow]{self.game.player.name}[reset] ([cyan]rank {self.game.player.guild_info["rank"]}[reset])\n", justify = "center");

  def createGuildInfo(self):
    plr = self.game.player;
    plr.guild_info = {
      "rank" : "E",
      "completed" : 0,
    };
  
  def generateBoard(self):
    self.board = [];
    for quest in QUESTS:
      if QUESTS[quest].rank == self.game.player.guild_info["rank"]:
        self.board.append(getQuest(quest));
   
  def handleApply(self):
    self.ui.clear();
    self.ui.printDialogue("clara", "hey.. i haven't see you around before!");
    self.ui.printDialogue(self.game.player.name, "yeah, how do i get started?");
    self.ui.awaitKey();
    
    self.ui.printDialogue("clara", "you need to register for a guild card!");
    self.ui.printDialogue("clara", "here give me your hand, this will only take a second.");
    self.ui.showStatus("registering", 10);
    self.ui.printDialogue("clara", "all good!");
    
    self.ui.printDialogue("clara", f"welcome to the guild hall [yellow]{self.game.player.name}[reset]!");
    self.createGuildInfo();
    self.ui.normalPrint(f"[yellow]{self.game.player.name}[reset]({self.game.player.guild_info["rank"]})\n");
    self.ui.awaitKey();
  
  def handleBoard(self):
    self.generateBoard();
    while True:
      self.ui.clear();
      for quest in self.board: self.ui.panelPrint(f"{quest.desc}", "center", f"{quest.name} ({quest.rank})");
      self.ui.printDialogue("clara", choices(["pick your poison!", "choose a quest..", "pick wisely!"])[0]);
      option = self.ui.getInput();
      
      for quest in self.board: 
        if option == quest.name:
          self.game.giveQuest(option);
          self.ui.printDialogue("clara", "goodluck!");
          return;
      self.ui.printDialogue("clara", f"{option} is not on the board silly.");
      self.ui.awaitKey();
      
  def handleGuild(self):
    if not self.game.player.guild_info: self.handleApply();
    self.game.handleMenu(
      {
        "board" : self.handleBoard, 
        "leave" : self.game.exploration_handler.explore,
      }, 
      self.showGuildMenu,
    );
    
  def enter(self):
    self.handleGuild();