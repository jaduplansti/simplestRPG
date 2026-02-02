MAP1 = [
  ["wall"] * 20,
  ["wall", None, None, None, "bush", None, None, None, None, None, None, None, "rock", None, None, None, None, None, None, "wall"],
  ["wall", None, "tree", None, None, None, "rock", None, None, None, None, "bush", None, None, None, "tree", None, None, None, "wall"],
  ["wall", None, None, None, None, None, None, "bush", None, "rock", None, None, None, None, None, None, None, "tree", None, "wall"],
  ["wall", None, "bush", None, None, "tree", None, None, None, None, None, None, "rock", None, None, None, "bush", None, None, "path_2"],
  ["wall", None, None, None, "rock", None, None, None, "tree", None, None, None, None, None, "bush", None, None, None, None, "path_2"],
  ["wall", None, None, "tree", None, None, None, None, None, None, "rock", None, None, None, None, "bush", None, None, None, "path_2"],
  ["wall", None, None, None, None, "bush", None, None, None, None, None, None, "tree", None, None, None, None, None, None, "wall"],
  ["wall", None, None, None, None, None, None, "rock", None, None, None, None, None, None, "tree", None, None, None, None, "wall"],
  ["wall"] * 20
]

MAP2 = [
  ["wall"] * 20,
  ["wall", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "wall"],
  ["wall", None, "tree", None, None, None, "water", "water", "water", "water", "water", None, None, None, None, None, "tree", None, None, "wall"],
  ["wall", None, None, None, None, "water", "water", "water", "water", "water", "water", "water", None, None, None, None, None, None, None, "wall"],
  ["path_1", None, None, None, "water", "water", "water", "water", None, None, "water", "water", "water", None, None, None, None, None, None, "wall"],
  ["path_1", None, None, None, "water", "water", "water", None, None, None, None, "water", "water", "water", None, None, None, "tree", None, "path_3"],
  ["wall", None, None, None, None, "water", "water", "water", "water", "water", "water", "water", None, None, None, None, None, None, None, "wall"],
  ["wall", None, "tree", None, None, None, "water", "water", "water", "water", "water", None, None, None, None, None, None, None, "tree", "wall"],
  ["wall", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "wall"],
  ["wall"] * 20
]

MAP3 = [
  ["wall"] * 20,
  ["wall", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "wall"],
  ["wall", None, None, None, "wall", None, None, None, None, None, None, None, "wall", None, None, None, None, None, None, "wall"],
  ["wall", None, None, None, "wall", None, None, None, None, "dungeon", None, None, "wall", None, None, None, None, None, None, "wall"],
  ["path_2", None, None, None, "wall", None, None, None, None, None, None, None, "wall", None, None, None, None, None, None, "wall"],
  ["wall", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "wall"],
  ["wall", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "wall"],
  ["wall", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "wall"],
  ["wall", "shop", None, None, None, None, None, None, None, None, None, None, "home", None, None, None, None, None, None, "wall"],
  ["wall"] * 20
]



MAPS = {
  "map1" : MAP1,
  "map2": MAP2,
  "map3": MAP3
}