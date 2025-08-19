from curtsies import Input;
from rich.live import Live;
from time import sleep;
from rich.panel import Panel;
from rich.text import Text;

class Animator:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
  
  def __render_attack_bar(self, bar_length, target_pos, pos, hit=False):
    bar = ["-"] * bar_length
    bar[target_pos] = "|"
    bar[pos] = "^" if not hit else "X"
    complete_bar = Text().from_markup("".join(bar), justify = "center");
    return Panel(complete_bar, title="Attack", border_style="cyan")
  
  def attackBar(self, speed = 0.1, bar_length = 20, random = False):
    hit = False;
    pos = 0;
    target_pos = bar_length // 2;
    if random is True: target_pos = randint(0, bar_length);
    
    with Input(keynames = "curses") as input_generator:
      with Live(self.__render_attack_bar(bar_length, target_pos, pos), refresh_per_second = 30, console = self.ui.console) as live:
        while pos < bar_length:
            live.update(self.__render_attack_bar(bar_length, target_pos, pos, hit));
            if input_generator.send(0.01) == "\n":
              hit = True;
              live.update(self.__render_attack_bar(bar_length, target_pos, pos, hit));
              return [hit, pos, bar_length, target_pos];
            pos += 1;
            sleep(speed);
    return None;
    
  def transition(self, block = "•"):
    self.ui.clear();
    width, height = self.ui.getSize();

    for i in range(height):
      line = block * width
      for _ in range(i):
        self.ui.normalPrint(f"[{self.ui.randomColor()}]{line}[reset]");
      sleep(0.03);

    for i in range(height):
      self.ui.clearLine();
      sleep(0.03);

    self.ui.clear();
  
  def panelFlickerPrint(self, s):
    pass;
    
    