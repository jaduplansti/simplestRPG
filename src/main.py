from game import Game;

def main():
  try:
    game = Game();
    game.handleConfiguration();
    game.audio_handler.enabled = False; # bug fix
    game.handleMainMenu();
  except KeyboardInterrupt:
    game.handleQuit();
    
if __name__ == "__main__":
  main();
  