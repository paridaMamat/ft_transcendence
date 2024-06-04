import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):

    # Initial game state
    # Ce state sera mis à jour au fur et à mesure que le jeu progresse en fonction des actions des joueurs et des événements du jeu.
    state = {
        'ball_position': {'x': 0, 'y': 0},
        'paddles': {
            'left': {'y': 0},
            'right': {'y': 0},
        },
        'score': {'left': 0, 'right': 0},
    }

    # Méthode connect: Cette méthode est appelée lorsque qu'un client WebSocket se connecte.
    # Elle ajoute le canal du client à un groupe de canaux correspondant à la salle de jeu
    # (room_group_name) et envoie l'état initial du jeu au client nouvellement connecté.
    async def connect(self):
        self.room_group_name = 'pong_room'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send the initial game state to the newly connected client
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'state': PongConsumer.state,
        }))
        print("Client connected and initial game state sent:", PongConsumer.state)

    # Méthode disconnect: Cette méthode est appelée lorsque le client se déconnecte du serveur.
    # Elle retire le canal du client du groupe de canaux correspondant à la salle de jeu.
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Client disconnected")

    # Méthode receive: Cette méthode est appelée lorsqu'un message est reçu du client.
    # Elle analyse le message JSON pour déterminer l'action à entreprendre, puis met à jour l'état du jeu en conséquence. Ensuite, elle envoie l'état mis à jour à tous les clients dans le groupe de canaux.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        print("Received action:", action)

        # Update the game state based on the received action
        if action == 'move_paddle':
            side = text_data_json['side']
            position = text_data_json['position']
            PongConsumer.state['paddles'][side]['y'] = position
            print(f"Updated paddle position: {side} to {position}")

        elif action == 'ball_update':
            PongConsumer.state['ball_position'] = text_data_json['position']
            print("Updated ball position:", PongConsumer.state['ball_position'])

        elif action == 'score_update':
            PongConsumer.state['score'] = text_data_json['score']
            print("Updated score:", PongConsumer.state['score'])

        # Send the updated game state to all clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state',
                'state': PongConsumer.state,
            }
        )
        print("Sent updated game state to all clients")

    # Méthode game_state: Cette méthode est appelée lorsqu'un événement de type game_state est reçu du groupe de canaux.
    # Elle envoie l'état du jeu au client WebSocket.
    async def game_state(self, event):
        # Send the game state to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'state': event['state']
        }))
        print("Game state sent to client:", event['state'])





# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class PongConsumer(AsyncWebsocketConsumer):

#     # Initial game state
#     #  Ce state sera mis à jour au fur et à mesure que le jeu progresse en fonction des actions des joueurs et des événements du jeu.
#     state = {
#     'ball_position': {'x': 0, 'y': 0},
#     'paddles': {
#         'left': {'y': 0},
#         'right': {'y': 0},
#     },
#     'score': {'left': 0, 'right': 0},
#     }

#     # Méthode connect: Cette méthode est appelée lorsque qu'un client WebSocket se connecte.
#     # Elle ajoute le canal du client à un groupe de canaux correspondant à la salle de jeu
#     # (room_group_name) et envoie l'état initial du jeu au client nouvellement connecté.
#     async def connect(self):
#         self.room_group_name = 'pong_room'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#         # Send the initial game state to the newly connected client
#         await self.send(text_data=json.dumps({
#             'type': 'game_state',
#             'state': PongConsumer.state,
#         }))

#     # Méthode disconnect: Cette méthode est appelée lorsque le client se déconnecte du serveur.
#     # Elle retire le canal du client du groupe de canaux correspondant à la salle de jeu.
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

# # Méthode receive: Cette méthode est appelée lorsqu'un message est reçu du client.
# # Elle analyse le message JSON pour déterminer l'action à entreprendre, puis met à jour l'état du jeu en conséquence. Ensuite, elle envoie l'état mis à jour à tous les clients dans le groupe de canaux.
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         action = text_data_json['action']

#         # Update the game state based on the received action
#         if action == 'move_paddle':
#             side = text_data_json['side']
#             position = text_data_json['position']
#             PongConsumer.state['paddles'][side]['y'] = position

#         elif action == 'ball_update':
#             PongConsumer.state['ball_position'] = text_data_json['position']

#         elif action == 'score_update':
#             PongConsumer.state['score'] = text_data_json['score']

#         # Send the updated game state to all clients
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'game_state',
#                 'state': PongConsumer.state,
#             }
#         )

# # Méthode game_state: Cette méthode est appelée lorsqu'un événement de type game_state est reçu du groupe de canaux.
# #Elle envoie l'état du jeu au client WebSocket.
#     async def game_state(self, event):
#         # Send the game state to WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'game_state',
#             'state': event['state']
#         }))


# NEW CODE

# import json
# import asyncio
# import random
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async

# WIN_SCORE = 5

# class Player():
#     def __init__(self, username, side, websocket):
#         self.username = username
#         self.position = 0
#         self.score = 0
#         self.side = side
#         self.websocket = websocket
#         self.disconnected = False

# class Ball():
#     def __init__(self):
#         self.position = {'x': 0, 'y': 0}
#         self.direction = {'x': random.choice([-1, 1]), 'y': random.choice([-1, 1])}
#         self.size = 0.4

#     def move(self, players):
#         # Logique de mouvement de la balle
#         pass


#     def reset(self):
#         self.position = {'x': 0, 'y': 0}
#         self.direction = {'x': random.choice([-1, 1]), 'y': random.choice([-1, 1])}

# class PongConsumer(AsyncWebsocketConsumer):
#     state = {
#         'ball_position': {'x': 0, 'y': 0},
#         'paddles': {
#             'left': {'y': 0},
#             'right': {'y': 0},
#         },
#         'score': {'left': 0, 'right': 0},
#     }

#     async def connect(self):
#         self.room_group_name = 'pong_room'
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#         await self.send(text_data=json.dumps({
#             'type': 'game_state',
#             'state': PongConsumer.state,
#         }))
#         self.players = {}
#         self.ball = Ball()
#         asyncio.create_task(self.game_loop())

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#         for player in self.players.values():
#             player.disconnected = True

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         action = text_data_json.get('action')

#         if action == 'move_paddle':
#             side = text_data_json['side']
#             position = text_data_json['position']
#             PongConsumer.state['paddles'][side]['y'] = position

#         elif action == 'ball_update':
#             PongConsumer.state['ball_position'] = text_data_json['position']

#         elif action == 'score_update':
#             PongConsumer.state['score'] = text_data_json['score']

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'game_state',
#                 'state': PongConsumer.state,
#             }
#         )

#     async def game_state(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'game_state',
#             'state': event['state']
#         }))

#     async def game_loop(self):
#         while True:
#             # Logique de la boucle de jeu, par exemple, mouvement de la balle
#             self.ball.move(self.players)
#             PongConsumer.state['ball_position'] = self.ball.position
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'game_state',
#                     'state': PongConsumer.state,
#                 }
#             )
#             await asyncio.sleep(0.01)
