import json
import requests

from websocket import create_connection

def subscribe(ws, event, data):
    if(isinstance(event, str) is not True):
        print("Event must be a string")
        return
    elif(isinstance(data, str) is not True):
        print("Data must be a string")
        return
    else:
        ws.send(json.dumps({
            "event": "wsRelay:register",
            "data": f"{event}:{data}"
        }))

ip = input("Enter IP (127.0.0.1): ")
port = input("Enter Port (49322): ")

if ip == "":
    ip = "127.0.0.1"

if port == "":
    port = "49322"

ws = create_connection(f"ws://{ip}:{port}")
subscribe(ws, "game", "goal_scored")
subscribe(ws, "game", "round_started_go")
subscribe(ws, "game", "statfeed_event")

if(ws is not None):
    print("Connected to WS Relay!")


while True:
    result = ws.recv()
    result = json.loads(result)
    if(result["event"] == "game:goal_scored"):
        # Make vmix request on goal scored
        requests.post(url = "http://127.0.0.1:8088/api/?Function=Cut&Input=2")
        print("A goal was scored!")
    elif(result["event"] == "game:round_started_go"):
        # Make vmix request on goal scored
        requests.post("http://127.0.0.1:8088/api/?Function=Cut&Input=1")
        print("Kickoff started!")
    elif (result["event"] == "game:statfeed_event"):
        print (result)