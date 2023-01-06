import time
from time import sleep
import paho.mqtt.client as paho
from paho import mqtt
from worldometer import Worldometer


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set("kaXXXXXXXk", "kaXXXXXXXk")

client.connect("XXXXXXXXXXXXX.s2.eu.hivemq.cloud", 8883)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish




client.loop_start()

x=1
oldvalue = 0
newvalue=0


while x!=0:
    try:
        w = Worldometer()
        x=w.metrics_with_labels()
        #sleep(5)
        print(x)

        newvalue=x['net_population_growth_today']
        if oldvalue >0:

            client.publish("realtime/popgrowth", payload=newvalue-oldvalue, qos=1)
        oldvalue=newvalue


    except:
        pass
   
client.loop_stop()
