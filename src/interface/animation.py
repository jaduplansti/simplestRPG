from curtsies import Input;
from rich.live import Live;
from time import sleep;

from rich.panel import Panel;
from rich.text import Text;
from random import randint, uniform;

from rich.align import Align;

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
  
  def animateDash(self):
    with Live(refresh_per_second = 60) as dash_panel:
      for n in range(self.ui.getSize()[0] - 1):
        dash_panel.update(Panel(">" * n));
        sleep(0.01);
    self.ui.clearLine(4);
  
  def __render_sequence_bar(self, key, pressed_keys):
    return Panel(f"[italic]{' '.join(pressed_keys)}[red]", title = f"[bold yellow](press {key})[reset]", border_style="red");

  def sequenceBar(self, keys, bar_length = 20, delay = 1):
    pressed_keys = [];
    key_index = 0;
    key_count = 0;
    
    with Input(keynames = "curses") as input_generator:
      with Live(self.__render_sequence_bar(keys[key_index], pressed_keys), refresh_per_second = 60) as live:
        while key_index < len(keys):
          live.update(self.__render_sequence_bar(keys[key_index],pressed_keys));
          if input_generator.send(delay) == keys[key_index]:
            pressed_keys.append(keys[key_index]);
            key_count += 1;
          key_index += 1;
    self.ui.clearLine(3);
    return key_count;
  
  def __render_charge_bar(self, bar_length, pos, target_zone, pointer, title="Punch", released=False):
    bar = ["-"] * bar_length;
    start, end = target_zone;
    for i in range(start, end):
      bar[i] = "|";
    if pos < bar_length: bar[pos] = pointer if not released else "X";
    complete_bar = Text().from_markup("".join(bar), justify="center");
    return Panel(Align.center(f"{complete_bar}"), title=title, border_style="red");
  
  def punchAttackBar(self, speed=0.05, bar_length=30, target_size=4, pointer="•", title="Attack"):
    pos = 0;
    released = False;
    target_start = (bar_length // 2) - (target_size // 2);
    target_end = target_start + target_size;
    direction = 1;
    
    with Input(keynames="curses") as input_generator:
      with Live(self.__render_charge_bar(bar_length, pos, (target_start, target_end), pointer, title), refresh_per_second=60, console=self.ui.console) as live:
        while True:
          live.update(self.__render_charge_bar(bar_length, pos, (target_start, target_end), pointer, title, released));
          key = input_generator.send(0.01);
          if key == "\n":
            if target_start <= pos <= target_end: result = released = True;
            live.update(self.__render_charge_bar(bar_length, pos, (target_start, target_end), pointer, title, released));
            sleep(0.8);
            return [released, pos, bar_length, (target_start, target_end)];
          pos += direction;
          if pos >= bar_length - 1 or pos <= 0: direction *= -1;
          sleep(speed);
    return None;
    
  def __render_sword_bar(self, bar_length, targets, pos, pointer, title, hit_targets):
    bar = ["-"] * bar_length;
    for i, t in enumerate(targets):
      for idx in t:
        if 0 <= idx < bar_length:
          bar[idx] = "X" if hit_targets[i] else "|";
    if pos < bar_length:
      bar[pos] = pointer;
    text = "".join(bar);
    return Panel(Text(text, justify="center"), title=title, border_style="yellow");
  
  def swordAttackBar(self, speed=0.1, bar_length=30, target_size=3, pointer="†", title="Attack"):
    pos = 0;
    targets = [];
    num_targets = 3;
    gap = bar_length // (num_targets + 1);
    for i in range(num_targets):
      start = (i + 1) * gap - target_size // 2;
      targets.append(list(range(start, start + target_size)));
    
    hit_targets = [False] * num_targets;
    
    with Input(keynames="curses") as input_generator:
      with Live(self.__render_sword_bar(bar_length, targets, pos, pointer, title, hit_targets), refresh_per_second=30, console=self.ui.console) as live:
        while pos < bar_length:
          live.update(self.__render_sword_bar(bar_length, targets, pos, pointer, title, hit_targets));
          key = input_generator.send(0.01);
          if key == "\n":
            for i, t in enumerate(targets):
              if pos in t:
                hit_targets[i] = True;
          if all(hit_targets):
            live.update(self.__render_sword_bar(bar_length, targets, pos, pointer, title, hit_targets));
            return [True, pos, bar_length, targets, hit_targets];
          pos += 1;
          sleep(speed);
    return [False, pos, bar_length, targets, hit_targets];