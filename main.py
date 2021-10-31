from fastapi import FastAPI, WebSocket
from ChatConnectionManager import ChatConnectionManager

app = FastAPI()
ccm = ChatConnectionManager()


@app.websocket("/")
async def websocketRoot(ws: WebSocket):
    await ccm.onClientTrigger(clientWebSocket=ws)
    try:
        while True:
            data = await ws.receive_text()
            await ccm.broadcastManager(ws, data)
    except:
        await ccm.disconnect(ws);

# When client is triggered we need to do these
# 1. if status is connected we need to add in list
# 2. if status is disconnected we need to remove from list
# when broadcast is triggered we need to take action parameter and
# 1. create room if needed
# 2. let them join room if needed
# 3. send message to the room
