from fastapi import WebSocket


class CustomDictionary:
    def __init__(self):
        self.websocket = None
        self.roomNumber = None

    def setWebsocket(self, websocket: WebSocket):
        self.websocket = websocket

    def getWebSocket(self):
        return self.websocket

    def setRoomNumber(self, roomNumber: int):
        self.roomNumber = roomNumber

    def getRoomNumber(self):
        return self.roomNumber
