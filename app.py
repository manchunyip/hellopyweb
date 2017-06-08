from flask import Flask
from flask import request
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/pyapi")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    #provided_ips = web.ctx.env.get("HTTP_X_FORWARDED_FOR")
    provided_ips = request.remote_addr

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>X-Forwarded-For:</b> {xff}<br/>" \
           "<b>Visits:</b> {visits}" 
    return html.format(name=os.getenv("NAME", "me"), hostname=socket.gethostname(), visits=visits, xff=provided_ips)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=4000)
