class Codex:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    
  def open(self):
    while True:
      self.ui.clear();
      self.ui.showSeperator("?");
      self.ui.showHeader("codex", "×");
      self.ui.printTreeMenu("", INFORMATION);
      self.ui.showSeperator("?");
      
      info = self.ui.getInput();
      for text in INFORMATION[info]: self.ui.animatedPrint(text);
      
INFORMATION = {
  "sleeping" : ""
}