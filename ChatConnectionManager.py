import json

from fastapi import WebSocket


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
                'status code': 200,
                "event": "createRoomEvent"
            }
            jsonString = str(json.dumps(sendDic))
            # sending it back to client
            await client.send_text(jsonString)

        elif action == 'join':
            # deny connection if already connected
            for user in self.users:
                if user['userWebSocket'] == client:
                    await client.send_text("Already connected")
                    return

            roomNumber = data2['roomNumber']
            userName = data2['userName']
            # adding user to list
            dic = {'userWebSocket': client, 'roomNumber': roomNumber,
                   'userName': userName}
            self.users.append(dic)

            sendDic = {
                'roomNumber': roomNumber,
                'userName': userName,
                'status code': 200,
                "event": "joinedRoomEvent"
            }
            jsonString = str(json.dumps(sendDic))
            # sending it back to client
            await client.send_text(jsonString)

        elif action == 'message':
            # invalid data start
            roomNumberTemp = -1
            senderName = ""

            # get room number of the sender
            for user in self.users:
                if user['userWebSocket'] == client:
                    roomNumberTemp = user['roomNumber']
                    senderName = user['userName']
                    break
            # continue this loop if roomNumberTemp is valid
            if roomNumberTemp != -1 and senderName != "":
                message = data2['message']
                # for users who have same room number as the sender we are going to send the text
                for user in self.users:
                    if user['roomNumber'] == roomNumberTemp:
                        sendDic = {
                            "message": message,
                            "senderName": senderName,
                            "event": "messageEvent"
                        }

                        jsonString = str(json.dumps(sendDic))
                        await user['userWebSocket'].send_text(jsonString)
            else:
                await client.send_text("room doesnt exist yet")

        elif action == 'getConnectedUsers':
            roomNumberTemp = -1

            # get room number of the sender
            for user in self.users:
                if user['userWebSocket'] == client:
                    roomNumberTemp = user['roomNumber']
                    break

            if roomNumberTemp == -1:
                await client.send_text("You are not in any room")
            else:
                connectedUsers = []
                for user in self.users:
                    if user['roomNumber'] == roomNumberTemp:
                        userDic = {
                            "userName": user['userName'],
                        }
                        connectedUsers.append(userDic)

                sendDic = {
                    "event": "getConnectedUsersEvent",
                    "users": connectedUsers
                }

                jsonString = str(json.dumps(sendDic))

                await client.send_text(jsonString)
