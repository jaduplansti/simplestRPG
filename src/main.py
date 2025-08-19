from game import Game;
import traceback;

def main():
  try:
    game = Game();
    #game.doUpdate();
    game.handleMainMenu();
  except KeyboardInterrupt:
    game.handleQuit();
  except Exception as e:
    game.ui.clear();
    game.ui.panelPrint(f"[bold underline]{traceback.format_exc()}[reset]\n\n[bold red]A EXCEPTION HAS OCCURED[reset] (see details above) ⬆", title = "FATAL");
    game.handleQuit();
    
if __name__ == "__main__":
  main();
  