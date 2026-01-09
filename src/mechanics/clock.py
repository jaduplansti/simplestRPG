from threading import Thread, Lock
from time import time, sleep

class Clock:
  def __init__(self, game):
    self.game = game
    self.lock = Lock()
    self.time_started = 0
    self.is_day = None
    self.running = False
    self.startClock()
    
  def startClock(self):
    self.running = True
    saved_time = getattr(self.game.player, "saved_time", None)
    if saved_time is not None:
      self.time_started = time() - saved_time
    else:
      self.time_started = time()
    elapsed = self.currentTime() % 5
    self.is_day = elapsed < 2.5
    thread = Thread(target=self.watchTime, daemon=True)
    thread.start()
    
  def currentTime(self):
    return time() - self.time_started
  
  def saveClock(self):
    with self.lock:
      self.game.player.saved_time = self.currentTime()
  
  def stopClock(self):
    with self.lock:
      self.running = False
    
  def isDay(self):
    with self.lock:
      return self.is_day
  
  def watchTime(self):
    while True:
      sleep(1)
      with self.lock:
        if not self.running: break;
        elapsed = self.currentTime() % 300
        new_day = elapsed < 150
        if new_day != self.is_day:
          self.is_day = new_day