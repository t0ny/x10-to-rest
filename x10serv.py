#!/usr/bin/python
# Copyright Tony Speer 2017 under MIT License

from x10.controllers import cm11
from bottle import route, run, request, post
import redis

pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
r = redis.Redis(connection_pool=pool)

dev = cm11.CM11("/dev/netTTY")
dev.open()

lightStatus = dict()

@route("/light/<name>")
def GetLight(name):
    global r
    
    status = r.get("light-%s" % name)

    if status == None:
        r.set("light-%s" % name, "OFF")
        status = "OFF"

    print "Light %s status %s." % (name, status)
    return status

@post("/light/<name>")
def PostLight(name):
    global r, dev
    status = request.body.getvalue()

    lamp = dev.actuator(name)

    if(status == "ON"):
        lamp.on()
    else:
        lamp.off()

    print "Turning %s %s" % (name, status)

    r.set("light-%s" % name, status)

@route("/temp/<room>")
def Temp(room):
    global r

    temp = r.get("temp-room")
    humidity = r.get("humidity-room")

    if temp == None or humidity == None:
        pass

    print "Temp: %s, hum: %s" % (temp, humidity)
    
    return "{\"room\": \"%s\", \"temperature\": %s, \"humidity\": %s}" % (room, temp, humidity)

run(host="0.0.0.0", port=7080, reloader=True)
