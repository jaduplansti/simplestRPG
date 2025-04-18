import subprocess;
import os;

class AudioPlayer:
  def __init__(self, game):
    self.enabled = False;
    self.game = game;
    
    if self.isTermux() is True:
      self.enabled = True;
    else:
      print("sorry audioplayer for other platforms arent available right now.\n");
   
  def isTermux(self):
    return "PREFIX" in os.environ and "/data/data/com.termux/files/usr" in os.environ["PREFIX"];
  
  def __play_termux(self, sound):
    # check if media player is installed
    subprocess.run(["termux-media-player", "play", f"../soundtracks/{sound}"], stdout = subprocess.DEVNULL);
   
  def __stop_termux(self):
    subprocess.run(["termux-media-player", "stop"], stdout = subprocess.DEVNULL);

  def play(self, sound):
    if self.enabled != True:
      return;
    self.__play_termux(sound);
    self.game.ui.showStatus(f"[bold yellow] playing: {sound}[reset]", 1);
    
  def stop(self):
    if self.enabled != True:
      return;
    self.__stop_termux();

