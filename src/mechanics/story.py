from random import choices, randint;

class StoryHandler:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    self.player = game.player;
  