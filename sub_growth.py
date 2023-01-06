import time
import paho.mqtt.client as paho
from paho import mqtt
import mysql.connector
import requests



def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    insertMySql("popgrowth",float(msg.payload))

    api_url = "https://xxxxxxxx.herokuapp.com/"
    response = requests.post(api_url,json={'inputdata':float(msg.payload),})
    x=response.json()
    print(x['message'])
    insertMySql("pred_co2",float(x['message']))

def insertMySql(datatype,payloaddata):
    

    cnx = mysql.connector.connect(user='sqlxxxxxx', password='xxxxx',
                              host='sql6.freemysqlhosting.net',
                              database='xxxxxxx')

    cursor = cnx.cursor()

    ts = time.time()
    add_record = ("INSERT INTO realtimedata "
                "( datatype, value, source) "
                "VALUES ( '"+datatype+"', "+str(payloaddata)+", 'MQTT')")
    

    # Insert new employee
    cursor.execute(add_record)
    
    cnx.commit()

    cursor.close()
    cnx.close()   
    print("Saved to Database") 


    
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set("katxxxxxak", "kaxxxxxak")

client.connect("xxxxxxxxx.s2.eu.hivemq.cloud", 8883)


client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


client.subscribe("realtime/popgrowth", qos=1)

client.loop_forever()