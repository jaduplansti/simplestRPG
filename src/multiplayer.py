import socket
from time import sleep;
from player import Player

import json;
MAX_PAYLOAD_SIZE = 5000;

class MultiplayerHandler:
  def __init__(self, game):
    self.game = game;
    self.ip = socket.gethostbyname(socket.gethostname())
    self.port = 5001;
    self.server_socket = None;
    self.player_connected = None;
  
  def addPlayer(self, plr):
    self.player_connected = plr;
    
  def endInput(self):
    if self.server_socket:
      self.server_socket.close();
      self.server_socket = None;
  
  def getInput(self, n):
    try:
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
      self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
      self.server_socket.bind((self.ip, self.port));
      self.server_socket.listen(1);
      client, address = self.server_socket.accept();
      data = client.recv(n);
      client.close();
      return data;
    except Exception as e:
      pass;
    finally:
      self.endInput();
      sleep(0.1); # Allow the OS to release the port
  
  def sendInput(self, s):
    try:
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
      self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
      self.server_socket.connect((self.ip, self.port));
      self.server_socket.send(s.encode());
      return True;
    except ConnectionRefusedError:
      return False;
    except Exception as e:
      return False;
    finally:
      self.endInput();
    
  def forceGetInput(self, n):
    data = "";
    while True:
      data = self.getInput(n);
      if data != None:
        break;
    return data;
   
  def showMultiplayerMenu(self):
    self.game.ui.clear();
    self.game.ui.normalPrint("{=}{=}{=}{=}{=}{=}");
    self.game.ui.normalPrint("    Multiplayer   " );
    self.game.ui.normalPrint("{=}{=}{=}{=}{=}{=}\n");
  
    self.game.ui.normalPrint("× [yellow]create lobby[reset]");
    self.game.ui.normalPrint("× [green]join lobby[reset]");
    self.game.ui.normalPrint("× [red]back[reset]\n");
  
  def showLobbyMenu(self):
    self.game.ui.clear();
    self.game.ui.normalPrint("{=}{=}{=}{=}");
    self.game.ui.normalPrint("    Lobby   " );
    self.game.ui.normalPrint("{=}{=}{=}{=}\n");
  
    self.game.ui.normalPrint(f"{self.player_connected.keys()}\n");
    self.game.ui.normalPrint("× [red]fight[reset]");
    self.game.ui.normalPrint("× [yellow]trade[reset]");
    self.game.ui.normalPrint("× [yellow]quit[reset]");

  def handleMultiplayerMenu(self):
    while True:
      self.showMultiplayerMenu();
      option = self.game.ui.getInput();
    
      if option == "create lobby":
        self.createLobby();
      elif option == "join lobby":
        self.joinLobby();
      elif option == "back":
        return;
      
      self.game.ui.awaitKey();
  
  def handleLobbyMenu(self):
    while True:
      self.showLobbyMenu();
      option = self.game.ui.getInput();
    
      if option == "fight":
        pass;
      elif option == "trade":
        pass;
      elif option == "back":
        return
      
  def createLobby(self):
    self.game.ui.animatedPrint("name of the lobby:");
    name = self.game.ui.getInput();
    
    payload = {
      "player": self.game.player.getData(),
    }

    self.game.ui.animatedPrint("waiting for players..");
    name = self.forceGetInput(MAX_PAYLOAD_SIZE);
    data = self.forceGetInput(MAX_PAYLOAD_SIZE);
    self.sendInput(json.dumps(payload));
    
    parsed_data = json.loads(data.decode());
    self.addPlayer(Player("").loadDataFromJson(parsed_data["player"]));
    self.handleLobbyMenu();
    
  def joinLobby(self):
    while True:
      response = self.sendInput(f"{self.game.player.name}");
      if response is False:
        pass;
      else:
        payload = {
          "player": self.game.player.getData(),
        }
        while self.sendInput(json.dumps(payload)) is False:
          pass;
        data = self.forceGetInput(MAX_PAYLOAD_SIZE);
        parsed_data = json.loads(data.decode());
        self.addPlayer(Player("").loadDataFromJson(parsed_data["player"]));
        self.handleLobbyMenu();
        break;
        
    