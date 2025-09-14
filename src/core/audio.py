import os;
import subprocess;
from time import sleep;

class AudioHandler:
  def __init__(self, game):
    self.tracks = [];
    self.track_limit = 6;
    self.game = game;
    
  def play(self, track, loop = False):
    self.cleanTracks();
    self.trackFull();
    
    proc = subprocess.Popen(
      ["play", f"tracks/{track}"],
      stdin = subprocess.DEVNULL,
      stdout = subprocess.DEVNULL,
      stderr = subprocess.DEVNULL,
    );
    
    self.tracks.append(proc);
    self.game.ui.showStatus(f"playing {track}", 0.5)
    
  def cleanTracks(self):
    self.tracks = [p for p in self.tracks if p.poll() is None];

  def popTracks(self):
    for proc in self.tracks:
      proc.terminate();
    self.tracks = [];   
    
  def trackFull(self):
    if len(self.tracks) < self.track_limit:
      return;
     
    self.tracks[0].terminate();
    self.tracks.pop(0);
    print("track full")