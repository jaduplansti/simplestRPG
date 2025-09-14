from random import randint, choices;
from copy import deepcopy;
from objects.item import getItem;

class Cooker:
  def __init__(self, game):
    self.game = game;
    self.ui = game.ui;
    
  def cook(self, character = None, name = "fruit basket"):
    if character is None: self.__cook_player(name);
    else: pass;
  
  def __chop(self, food):
    keys = self.ui.getRandomKeys(food["chop_count"]);
    for key in keys:
      self.ui.panelPrint(f"[bold]{key}[reset]\n\n[underline]press the {key} to chop[reset]!", "center");
      if self.ui.getKey(end = "") == key: food["score"] += 2;
      self.ui.clearLine(7)
  
  def __heat(self, food):
    results = [];
    for n in range(food["required_heat"]):
      results.append(self.game.animator.attackBar(random = True, title = "cook"));
      self.ui.showStatus("[green]wait..[reset]", 2);
   
    for result in results:
      if (result != None) and result[1] == result[3]: 
        food["score"] += 3;
 
  def __wash(self, food):
    directions = [];
    for n in range(food["wash_count"]):
      directions.append(choices(["a", "s", "d", "w"])[0]);
    
    for direction in directions:
      if direction == "a": self.ui.panelPrint("<- <- <-\n\ntype (a) to wash", "center");
      elif direction == "d": self.ui.panelPrint("-> -> ->\n\ntype (d) to wash", "center");
      elif direction == "s": self.ui.panelPrint("↓ ↓ ↓\n\ntype (s) to wash", "center");
      elif direction == "w": self.ui.panelPrint("↑ ↑ ↑\n\ntype (w) to wash", "center");
      
      if self.ui.getInputWithTimeout("", 2) == direction: food["score"] += 1.5;
      self.ui.clearLine(9)

  def __cook_player(self, name):
    food = deepcopy(FOODS[name]);
    if self.game.player.hasItems(food["ingredients"]) is False: 
      self.ui.animatedPrint("You don’t have all the ingredients needed for this dish.")
      return;
    
    self.ui.clear();
    self.ui.showStatus("prep time!, [yellow]get ready[reset]", randint(2, 5))
    
    for step in food["steps"]:
      if step == "chop": self.__chop(food);
      elif step == "heat": self.__heat(food)
      elif step == "wash": self.__wash(food)

    if food["score"] < food["minimum_score"]:
      self.ui.panelPrint(
        f"[bold red]Oh no![reset] You couldn’t make [bold]{name}[reset].\n\nScore: [yellow]{food['score']}[reset]/[green]{food['minimum_score']}[reset]", 
        "center")
    else:
      self.ui.panelPrint(
        f"[bold green]Congrats![reset] You successfully made [bold]{name}[reset]!", 
        "center");
      self.game.givePlayerItem(name);
    
    for ingredient in food["ingredients"]:
      self.game.player.usedItem(ingredient);
      
  def handleFoodSelect(self):
    while True:
      self.ui.clear();
      self.showAvailableFoods();
      selected_food = self.ui.getInput();
      
      if selected_food in list(FOODS): self.cook(name = selected_food);
      elif selected_food == "close": return;
      self.ui.awaitKey();
      
  def showAvailableFoods(self):
    lines = ["[bold underline](🍽) Available Foods[reset]\n"];
    
    for food_name, details in FOODS.items():
      ingredient_status = [];
      for ingredient in details["ingredients"]:
        if self.game.player.itemExists(ingredient):
          ingredient_status.append(f"[italic green]{ingredient}[reset] (✓)");
        else:
          ingredient_status.append(f"[dim red]{ingredient}[reset] (✗)");
      
      ingredients_str = ", ".join(ingredient_status);
      line = (
        f"[bold]• {food_name}[reset]  [cyan]({details['minimum_score']})[reset]\n"
        f"[underline]Ingredients:[reset] {ingredients_str}\n"
      );
      lines.append(line);
    
    output = "\n".join(lines).rstrip();
    self.ui.panelPrint(output);

def createFood(name, ingredients, steps, minimum_score, wash_count = 0, chop_count = 0, required_heat = 0):
  return {name : {"ingredients" : ingredients, "steps": steps, "minimum_score": minimum_score, "wash_count" : wash_count, "chop_count": chop_count, "required_heat" : required_heat, "score" : 0}};
   
FOODS = {
  **createFood("bread", ["flour", "water"], ["heat"], minimum_score = 5, required_heat = 3),
  **createFood("fruit basket", ["apple", "banana", "orange"], ["wash"], minimum_score = 3, wash_count = 3),
  **createFood("salad", ["lettuce", "tomato", "cucumber"], ["wash", "chop"], minimum_score=6, wash_count=3, chop_count=3),
  **createFood("grilled fish", ["fish", "lemon"], ["wash", "heat"], minimum_score=7, wash_count=2, required_heat=4),
  **createFood("stir fry", ["carrot", "broccoli", "chicken"], ["wash", "chop", "heat"], minimum_score=8, wash_count=2, chop_count=3, required_heat=3),
  **createFood("smoothie", ["banana", "strawberry", "milk"], ["wash", "chop"], minimum_score=5, wash_count=2, chop_count=2),
  **createFood("omelette", ["egg", "milk", "cheese"], ["chop", "heat"], minimum_score=6, chop_count=1, required_heat=3),
}  
    
