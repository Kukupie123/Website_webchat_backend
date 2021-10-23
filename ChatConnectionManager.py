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

        # CREATE ROOM
        if action == 'createRoom':

            # deny connection if already connected
            for user in self.users:
                if user['userWebSocket'] == client:
                    await client.send_text("Already connected")
                    return

            userName = data2['userName']
            # adding user to list
            oldRN = self.roomNumber
            dic = {'userWebSocket': client, 'roomNumber': self.roomNumber,
                   'userName': userName}
            self.users.append(dic)

            self.roomNumber = self.roomNumber + 1
            sendDic = {
                'roomNumber': oldRN,
                'userName': userName,
                'status code': 200
            }
            jsonString = str(json.dumps(sendDic))
            # sending it back to client
            await client.send_text(jsonString)

        elif action == 'message':
            # invalid data start
            roomNumberTemp = -1

            # get room number of the sender
            for user in self.users:
                if user['userWebSocket'] == client:
                    roomNumberTemp = user['roomNumber']
                    break
            # continue this loop if roomNumberTemp is valid
            if roomNumberTemp != -1:
                message = data2['message']
                # for users who have same room number as the sender we are going to send the text
                for user in self.users:
                    if user['roomNumber'] == roomNumberTemp:
                        await user['userWebSocket'].send_text(message)
            else:
                await client.send_text("room doesnt exist yet")
        elif action == 'join':
            roomNumber = data2['roomNumber']
            for user in self.users:
                if user['roomNumber'] == roomNumber:
                    await user
