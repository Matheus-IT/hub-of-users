from channels.generic.websocket import AsyncWebsocketConsumer
import json

class UsersHubConsumer(AsyncWebsocketConsumer):
	GROUP_NAME = 'users_hub'
		
	async def connect(self):
		await self.channel_layer.group_add(
			self.GROUP_NAME,
			self.channel_name
		)

		await self.accept()

		user_info = json.dumps({
			'id': self.scope['user'].id,
			'email': self.scope['user'].email,
		})

		await self.send(text_data=user_info)
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.GROUP_NAME,
			self.channel_name
		)
