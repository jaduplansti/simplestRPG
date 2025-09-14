class SubMenu:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    self.page = 1;
    self.max_page = 1;
    
  def nextPage(self):
    if self.page < self.max_page:
      self.page += 1;
  
  def prevPage(self):
    if self.page > 1:
      self.page -= 1;
  
    