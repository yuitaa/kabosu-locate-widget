import http.server
import socketserver
import urllib.request
import os
import time
import json
import math

PORT = 8800
PLAYERNAME = '_yuita_'

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path.startswith("/api/") or self.path.startswith("/api"):

            url = f"http://mc-kabosu.mydns.jp:8123/up/world/world/{int(time.time())}"

            with urllib.request.urlopen(url) as response:
                world_data = json.loads(response.read())

                account_data = {
                    "world": "world",
                    "armor": 0,
                    "name": "",
                    "x": 0,
                    "y": 0,
                    "health": 0,
                    "z": 0,
                    "sort": 1,
                    "type": "player",
                    "account": "",
                }

                for i in world_data["players"]:
                    if i["account"] == PLAYERNAME:
                        account_data = i

                if account_data["world"] != "world":
                    url = f"http://mc-kabosu.mydns.jp:8123/up/world/{account_data['world']}/{int(time.time())}"

                    with urllib.request.urlopen(url) as response:
                        world_data = json.loads(response.read())
                        for i in world_data["players"]:
                            if i["account"] == PLAYERNAME:
                                account_data = i

                hour = math.floor(world_data["servertime"] / 1000 + 6)
                hour = hour % 24
                minute = int(((world_data["servertime"] / 1000) * 60) % 60)
                minute = math.floor(minute / 15) * 15

                output = {}
                output["player"] = account_data
                output["world"] = account_data["world"]
                output["time"] = [hour, minute]

                contents = json.dumps(output).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(contents)
        else:

            root = os.getcwd() + "/docs"
            path = self.translate_path(self.path)
            if os.path.isdir(path):
                for index in "index.html", "index.htm":
                    index = os.path.join(path, index)
                    if os.path.exists(index):
                        path = index
                        break
                else:
                    return self.list_directory(path)
            return http.server.SimpleHTTPRequestHandler.do_GET(self)


Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
