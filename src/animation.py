from curtsies import Input;
from rich.live import Live;
from time import sleep;

from rich.panel import Panel;
from rich.text import Text;
from random import randint, uniform;

class Animator:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
  
  def __render_attack_bar(self, bar_length, target_pos, pos, pointer, hit=False, title = "Attack"):
    bar = ["-"] * bar_length
    bar[target_pos] = "|"
    bar[pos] = pointer if not hit else "X"
    complete_bar = Text().from_markup("".join(bar), justify = "center");
    return Panel(complete_bar, title=title, border_style="cyan")
  
  def attackBar(self, speed = 0.1, bar_length = 20, random = False, title = "Attack", pointer = "•"):
    hit = False;
    pos = 0;
    target_pos = bar_length // 2;
    if random is True: target_pos = randint(0, bar_length - 1);
    
    with Input(keynames = "curses") as input_generator:
      with Live(self.__render_attack_bar(bar_length, target_pos, pos, pointer, title = title), refresh_per_second = 30, console = self.ui.console) as live:
        while pos < bar_length:
            live.update(self.__render_attack_bar(bar_length, target_pos, pos, pointer, hit, title));
            if input_generator.send(0.01) == "\n":
              hit = True;
              live.update(self.__render_attack_bar(bar_length, target_pos, pos, pointer, hit, title));
              return [hit, pos, bar_length, target_pos];
            pos += 1;
            sleep(speed);
    return None;
    
  def transition(self, block = "×"):
    self.ui.clear();
    width, height = self.ui.getSize();

    for i in range(height):
      line = block * width
      for _ in range(i):
        self.ui.normalPrint(f"[{self.ui.randomColor()}]{line}[reset]");
      sleep(0.01);

    for i in range(height):
      self.ui.clearLine();
      sleep(0.03);

    self.ui.clear();
 
  def transitionLine(self, block = "="):
    self.ui.clear();
    width, height = self.ui.getSize();
    
    for h in range(height):
      for w in range(width):
        self.ui.normalPrint(block * w);
        sleep(0.01);
        if w < width - 1: self.ui.clearLine();
    
    for h in range(height):
      self.ui.clearLine();
      sleep(0.03);
  
  def transitionClosing(self, block="█", random = False):
    self.ui.clear()
    width, height = self.ui.getSize()

    for step in range(width // 2 + 1):
        self.ui.clear()
        for _ in range(height):
            left = block * step
            right = block * step
            middle_space = " " * (width - step * 2)
            line = f"{left}{middle_space}{right}"
            self.ui.normalPrint(line)
        if random: sleep(uniform(0.01, 0.09))
        else: sleep(0.01);

    for step in range(width // 2 + 1):
        self.ui.clear()
        for _ in range(height):
            left = block * ((width // 2) - step)
            right = block * ((width // 2) - step)
            middle_space = " " * (step * 2)
            line = f"{left}{middle_space}{right}".ljust(width)
            self.ui.normalPrint(line)
        if random: sleep(uniform(0.01, 0.09))
        else: sleep(0.01);    
        self.ui.clear()
        
  def animateTitle(self):
    self.ui.clear();
    title = "≈ simplestRpg ≈";
    place_holder = "xxxxxxxxxxxxxxx";
    new_title = list(place_holder);
    border = "≈" * len(title);
    
    self.ui.normalPrint(f"{border}\n{place_holder}\n{border}");
    self.ui.clear();
    for n in range(len(place_holder)):
      new_title[n] = title[n];
      self.ui.normalPrint(f"{border}\n{''.join(new_title)}\n{border}");
      sleep(0.01);
      self.ui.clear();
    self.ui.clear();
  
  def animateCritical(self, multiplier, delay = 0.1):
    with Live(refresh_per_second = 60) as crit_panel:
      for n in range(4):
        if n == 1: crit_panel.update(Panel(f"[dim red]CRITICAL HIT[reset] ([green]{multiplier}x[reset])"));
        elif n == 2: crit_panel.update(Panel(f"[italic red]CRITICAL HIT[reset] ([green]{multiplier}x[reset])"));
        elif n == 3: crit_panel.update(Panel(f"[bold red]CRITICAL HIT![reset] ([green]{multiplier}x[reset])"));
        sleep(delay);
    self.ui.newLine();
  
  def animatePerfectCritical(self, multiplier, delay = 0.1):
    with Live(refresh_per_second = 60) as crit_panel:
      for n in range(4):
        if n == 1: crit_panel.update(Panel(f"[dim cyan]PERFECT CRITICAL![reset] ([magenta]{multiplier}x[reset]) 🕐"));
        elif n == 2: crit_panel.update(Panel(f"[italic cyan]PERFECT CRITICAL![reset] ([magenta]{multiplier}x[reset]) 🕐"));
        elif n == 3: crit_panel.update(Panel(f"[bold cyan]PERFECT CRITICAL![reset] ([magenta]{multiplier}x[reset]) 🕑"));
        sleep(delay);
    self.ui.newLine();