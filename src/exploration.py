from rich.status import Status;
from time import sleep;
from random import randint, choices;
from combat import CombatHandler;

from home import Home;
from forest import Forest;
from shop import Shop;

from dungeon import Dungeon;
from guild_hall import GuildHall;
from character import Character;

def createArea(name, handler, _next = [], prev = [], enemies = None, position = 0):
  return {name : {
    "handler" : handler,
    "prev" : prev,
    "next" : _next,
    "enemies" : enemies,
    "position" : position
  }};

AREAS = {
  **createArea("home", Home, _next = ["shop", "guild hall", "dungeon"], position = 0),
  #**createArea("forest", Forest, prev = ["home"], _next = ["dungeon"], position = 10),
  **createArea("guild hall", GuildHall, prev = ["home"], position = 50),
  **createArea("shop", Shop, prev = ["home"], position = 30),
  **createArea("dungeon", Dungeon, prev = ["home"], position = 70),
};


NARRATION_AND_EVENT = {
  "shop": [
    ("The [yellow]cobbled road[reset] hums with light traffic.", "none"),
    ("A [cyan]handcart[reset] rattles by, iron rims clicking.", "none"),
    ("The air holds a trace of [green]fresh herbs[reset] and [bold magenta]dyes[reset].", "none"),
    ("Snatches of [dim]street haggling[reset] drift on the breeze.", "none"),
    ("Bright [blue]fabric pennants[reset] flutter over side lanes.", "none"),
    ("Your boots tap steady on worn [bold]stone[reset].", "none"),
    ("Somewhere, a [yellow]door bell[reset] jingles once.", "none"),
    ("Chalk-smeared [cyan]price boards[reset] lean against a wall.", "none"),
    ("A [magenta]tailor’s thread[reset] glints as it rides the wind.", "none"),
    ("The scent of [bold green]baked grain[reset] and [italic]warm yeast[reset] hangs in the air.", "none"),
    ("You pass stacked [dim]crates[reset] stamped with unfamiliar marks.", "none"),
    ("Coins clink in a nearby [blue]purse[reset], then fall silent.", "none"),
    ("A [red]wagon wheel[reset] creaks as it turns down a side street.", "none"),
    ("The shadow of a swinging [bold cyan]signboard[reset] slides over the ground.", "none"),
    ("Bundles of [green]dried plants[reset] sway from a lintel somewhere.", "none"),
    ("Scuffed [yellow]cobblestones[reset] show grooves from countless carts.", "none"),
    ("A [magenta]painted emblem[reset] flakes from an old storefront.", "none"),
    ("Faint [cyan]music[reset] threads through the clatter of the road.", "none")
  ],
  "guild hall": [
    ("Stonework broadens into [bold cyan]carved courses[reset] along the avenue.", "none"),
    ("Banners of [red]faded cloth[reset] hang from iron hooks overhead.", "none"),
    ("The rhythm of [yellow]practice strikes[reset] rings from a hidden yard.", "none"),
    ("You pass [dim]notice boards[reset] layered with curled postings.", "none"),
    ("A waft of [green]oiled leather[reset] rides the air.", "none"),
    ("Bootsteps drum on [bold]flagstones[reset] in steady cadence.", "none"),
    ("A [magenta]heraldic shield[reset] leans against a doorway.", "none"),
    ("The scent of [cyan]ink[reset] and [blue]parchment[reset] lingers near an office front.", "none"),
    ("Laughter breaks into brief [bold yellow]cheers[reset] before fading.", "none"),
    ("An [italic]old campaign map[reset] is pinned to a kiosk by the road.", "none"),
    ("Two silhouettes spar behind a [dim]palisade[reset], blades flashing.", "none"),
    ("A crisp [red]trumpet call[reset] echoes from a distant tower.", "none"),
    ("You step over chalked [magenta]training circles[reset] on the stone.", "none"),
    ("Sunlight pools across broad [cyan]steps[reset] of public buildings.", "none"),
    ("The scrape of [bold]armor plates[reset] carries on the wind.", "none"),
    ("A [green]standard[reset] snaps once, then settles.", "none"),
    ("Muted [blue]voices[reset] trade news of contracts and routes.", "none"),
    ("A row of [yellow]practice dummies[reset] leans against a wall.", "none")
  ],
  "dungeon": [
    ("The path narrows under [green]twisted boughs[reset] and snagging briars.", "none"),
    ("Cold [cyan]air[reset] trickles from somewhere ahead.", "none"),
    ("Your steps crush [dim]lichen[reset] and brittle twigs.", "none"),
    ("An [italic]old waystone[reset] lists at the trail’s edge, glyphs eroded.", "none"),
    ("A [red]crow’s call[reset] breaks the hush, then nothing.", "none"),
    ("Dark [blue]rock outcrops[reset] crowd the track.", "none"),
    ("The smell of [bold green]wet earth[reset] clings to your boots.", "none"),
    ("A [magenta]hollow log[reset] lies half-buried beside the trail.", "none"),
    ("Pale [cyan]fungus[reset] freckles a shaded stump.", "none"),
    ("Water ticks from a [yellow]overhang[reset] in a steady beat.", "none"),
    ("Your breath fogs in the [dim]cool shade[reset].", "none"),
    ("Scratch marks score a [bold]stone[reset] where something squeezed past.", "none"),
    ("Loose gravel skitters down a [blue]scree patch[reset].", "none"),
    ("A [red]distant rumble[reset] fades beneath the roots.", "none"),
    ("The canopy knits tight, dimming the [green]light[reset].", "none"),
    ("A faint [magenta]iron tang[reset] rides the air.", "none"),
    ("You skirt a [cyan]sinkhole[reset] rim crusted with moss.", "none"),
    ("Old [yellow]rope fibers[reset] hang from a bent post.", "none")
  ],
  "home": [
    ("The lane grows familiar with [green]hedges[reset] trimmed low along the sides.", "none"),
    ("A thread of [cyan]woodsmoke[reset] threads the air.", "none"),
    ("Fence rails creak with [dim]weathered age[reset] as the wind shifts.", "none"),
    ("You pass a rack of [yellow]wild herbs[reset] drying in the light.", "none"),
    ("Fresh [blue]wash lines[reset] flutter between posts.", "none"),
    ("Your steps thud softly on packed [bold]earth[reset].", "none"),
    ("A [magenta]child’s chalk drawing[reset] scrawls across a flat stone.", "none"),
    ("The scent of [green]stew greens[reset] and [italic]root vegetables[reset] drifts by.", "none"),
    ("A [cyan]bucket[reset] sits by a well, beaded with moisture.", "none"),
    ("A neat [dim]woodpile[reset] rests beneath a lean-to.", "none"),
    ("Low [yellow]sparrows[reset] hop in the dust then flit away.", "none"),
    ("The [blue]eaves[reset] of small roofs peek over the hedgerow.", "none"),
    ("Wheel ruts groove the [bold]lane[reset] in parallel lines.", "none"),
    ("A [magenta]pinwheel[reset] turns idly in the breeze.", "none"),
    ("Sunlight lays long [cyan]bars[reset] across the path.", "none"),
    ("The clack of a [green]garden gate[reset] carries from somewhere nearby.", "none"),
    ("Warm [yellow]baking scents[reset] tease the senses.", "none"),
    ("The murmur of [dim]quiet households[reset] settles over the road.", "none")
  ]
};

class ExplorationEventHandler:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    self.event_every = 10; # event every n step
  
  def handleEvent(self, event):
    if event == "":
      pass;
    
  def getNarration(self, steps, destination_name, destination):
    if steps % self.event_every != 0:
      return;
    try:
      narration, event = choices(NARRATION_AND_EVENT[destination_name])[0];
      self.ui.normalPrint(f"> {narration}" + "\n");
      self.handleEvent(event);
    except KeyError:
      pass;
        
class Exploration:
  def __init__(self, game):
    self.game = game;
    self.ui = self.game.ui;
    self.event_handler = ExplorationEventHandler(game);
    
  def handleGetNext(self, area):
    while True:
      self.ui.clear();
      try:
        for loc in area["next"]: self.ui.normalPrint(f"- [yellow underline]{loc}[reset] ({AREAS[loc]['position']} fyres) ⬆\n");
        for loc in area["prev"]: self.ui.normalPrint(f"- [yellow underline]{loc}[reset] ({AREAS[loc]['position']} fyres) ⬇\n");

        destination_name = self.ui.getInput();
        return [AREAS[destination_name], destination_name];
      except KeyError:
        self.ui.normalPrint("not a valid destination");
        self.ui.awaitKey();
        
  def getWalkingBar(self, destination):
    return f"energy ({self.ui.showBar(self.game.player.energy, 100, 4, "cyan")}) [{self.ui.randomColor()}]{choices(["<-", "->"])[0]}[reset] ({self.game.player.position}/{destination["position"]})";
    
  def handleExplore(self, destination, destination_name):
    self.ui.clear();
    self.steps = 0;
    with Status(self.getWalkingBar(destination), spinner = "runner") as status:
      while self.game.player.position != destination["position"]:
        if self.game.player.position < destination["position"]: self.game.player.position += 1;
        elif self.game.player.position > destination["position"]: self.game.player.position -= 1;
        sleep(0.6);
        status.update(self.getWalkingBar(destination));
        self.steps += 1;
        self.event_handler.getNarration(self.steps, destination_name, destination);
        
  def move(self, loc):
    if loc in AREAS:
      self.game.player.location = loc;
      self.game.player.position = AREAS[loc]["position"];
      AREAS[loc]["handler"](self.game).enter();
    else:
      self.ui.animatedPrint("failed to teleport!");

  def explore(self):
    area = AREAS[self.game.player.location];
    destination, destination_name = self.handleGetNext(area);
    self.handleExplore(destination, destination_name);
    
    self.ui.normalPrint(f"[bold cyan]you have arrived at {destination_name}[reset]\n");
    self.game.player.location = destination_name;
    self.ui.awaitKey();
    
    destination["handler"](self.game).enter();