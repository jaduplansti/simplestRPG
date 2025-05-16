from game import Game;

def main():
  try:
    game = Game();
    #game.doUpdate();
    game.handleMainMenu();
  except KeyboardInterrupt:
    game.handleQuit();
    
if __name__ == "__main__":
  main();
  