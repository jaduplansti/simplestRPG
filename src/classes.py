class Classes():
  warrior_class = {
    "skills" : {},
    "level" : 5,
    "next" : ["swordsman"],
  }
  
  mage_class = {
    "skills" : {},
    "level" : 5,
    "next" : ["archmage"],
  }
  
  archer_class = {
    "skills" : {},
    "level" : 5,
    "next" : ["ranger"],
  }
  
  thief_class = {
    "skills" : {},
    "level" : 5,
    "next" : ["assassin"],
  }
  
  def getAvailableClass(level):
    classes = Classes.__dict__;
    available_classes = [];
    for key in classes:
      if isinstance(classes[key], dict) and classes[key]["level"] <= level:
        available_classes.append(key.replace("_class", ""));
    return available_classes;
  
  def getClassInfo(class_name):
    try:
      return Classes.__dict__[f"{class_name}_class"];
    except KeyError:
      return None;
  
  def isBaseClass(class_name):
    try:
      Classes.getClassInfo(class_name)["prev"];
      return False;
    except KeyError:
      return True;
      
  def tryGiveClass(plr, class_name):
    if plr.level <= Classes.getClassInfo(class_name)["level"]:
      return False;
      
    if Classes.isBaseClass(class_name) is True or Classes.getClassInfo(class_name)["prev"] == plr._class:
      Classes.__giveClass(plr, class_name)
    else:
      return False;
  
  def __giveClass(plr, class_name):
    if class_name == "warrior":
      pass;
    
