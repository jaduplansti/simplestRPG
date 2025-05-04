from game import Game;

def main():
  try:
    game = Game();
    #game.doUpdate();
    game.handleConfiguration();
    game.handleMainMenu();
  except KeyboardInterrupt:
    game.handleQuit();
    
if __name__ == "__main__":
  main();
  