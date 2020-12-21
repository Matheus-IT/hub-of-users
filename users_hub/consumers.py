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
			'status_online': True
		})

		await self.channel_layer.group_send(
			self.GROUP_NAME,
			{
				'type': 'send_user_info_to_client',
				'user_info': user_info
			}
		)
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.GROUP_NAME,
			self.channel_name
		)

		user_info = json.dumps({
			'id': self.scope['user'].id,
			'email': self.scope['user'].email,
			'status_online': False
		})

		await self.channel_layer.group_send(
			self.GROUP_NAME,
			{
				'type': 'send_user_info_to_client',
				'user_info': user_info
			}
		)

	async def send_user_info_to_client(self, event):
		await self.send(text_data=json.dumps({
			'userInfo': event['user_info']
		}))
