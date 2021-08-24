import json
import requests

from websocket import create_connection

def subscribe(ws, event, data):
    ws.send(json.dumps({
        "event": "wsRelay:register",
        "data": f"{event}:{data}"
    }))


ws = create_connection("ws://127.0.0.1:49322")
subscribe(ws, "game", "goal_scored")
subscribe(ws, "game", "round_started_go")
subscribe(ws, "game", "statfeed_event")



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