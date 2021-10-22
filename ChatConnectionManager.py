import json

from fastapi import WebSocket, FastAPI
from typing import List
from CustomDictionary import CustomDictionary


class ChatConnectionManager:
    roomNumber = 0
    users = []

    async def onClientTrigger(self, clientWebSocket: WebSocket):
        await clientWebSocket.accept()

    async def broadcastManager(self, client: WebSocket, data: str):
        data2 = json.loads(s=data)
        action = data2["action"]

        #CREATE ROOM
        if action == 'createRoom':

            # deny connection if already connected
            for user in self.users:
                if user['userWebSocket'] == client:
                    await client.send_text("Already connected")
                    return
            userName = data2['userName']
            # adding user to list
            dic = {'userWebSocket': client, 'roomNumber': self.roomNumber,
                   'userName': userName}

            sendDic = {
                'roomNumber': self.roomNumber,
                'userName': userName,
                'status code': 200
            }
            jsonString = str(json.dumps(sendDic))
            self.roomNumber = self.roomNumber + 1
            self.users.append(dic)
            # sending it back to client
            await client.send_text(jsonString), 200