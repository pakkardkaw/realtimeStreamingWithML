import time
import paho.mqtt.client as paho
from paho import mqtt
import mysql.connector



def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    insertMySql(float(msg.payload))

def insertMySql(payloaddata):
    

    cnx = mysql.connector.connect(user='xxxxx', password='xxxx',
                              host='sql6.freemysqlhosting.net',
                              database='xxxxx')

    cursor = cnx.cursor()

    ts = time.time()
    add_record = ("INSERT INTO realtimedata "
                "( datatype, value, source) "
                "VALUES ( 'co2', "+str(payloaddata)+", 'MQTT')")
    

    # Insert new employee
    cursor.execute(add_record)
    
    cnx.commit()

    cursor.close()
    cnx.close()   
    print("Saved to Database") 


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set("kxxxxxak", "kaxxxxak")

client.connect("xxxxxx.s2.eu.hivemq.cloud", 8883)


client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


client.subscribe("realtime/co2", qos=1)


client.loop_forever()