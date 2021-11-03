import paho.mqtt.client as mqtt
import threading
import configparser


class MQTT_Process(threading.Thread):

    def __init__(self, layout_instance):
        super().__init__()
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.layout_instance = layout_instance

        self.config = configparser.ConfigParser()
        self.config.read('./Config/config.ini')
        
        # self.ip = self.config.get('MQTT', 'ip')
        # self.port = int(self.config.get('MQTT', 'port'))
        # self.username = self.config.get('MQTT', 'username')
        # self.password = self.config.get('MQTT', 'password')
        # self.client_id = self.config.get('MQTT', 'client_id')

        # self.client_id = self.config.get('MQTT', 'SYS') + str('_') + str(random.randint(1, 9999))
        self.client = mqtt.Client()

        # self.cs_topic = '/'.join([self.com, self.sys])
        # self.sub_topic_1 = '/'.join([self.cs_topic, '+', '+'])
        # self.sub_topic_2 = '/'.join([self.cs_topic, '+', '+', '+'])
        # self.sub_topic_3 = '/'.join([self.cs_topic, '+', '+', '+', '+'])

        # self.domain_info_ID = self.config.get('MQTT', 'info_domain')
        # self.domain_data_ID = self.config.get('MQTT', 'data_domain')
        # self.domain_control_ID = self.config.get('MQTT', 'control_domain')
        # self.req = 'REQ'
        # self.res = 'RES'


        # self.info_pub_topic = None

    def run(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.ip, self.port, 10)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def connect_func(self):
        self.ip = self.config.get('MQTT', 'ip')
        self.port = int(self.config.get('MQTT', 'port'))
        self.username = self.config.get('MQTT', 'username')
        self.password = self.config.get('MQTT', 'password')
        self.client_id = self.config.get('MQTT', 'client_id')
        self.client = mqtt.Client(self.client_id)
        print('Connected')
    
    def disconnect_func(self):
        self.client.disconnect()
        print('Disconnected')

    def publish_func(self, pub_topic, pub_payload):
        self.client.publish(pub_topic, pub_payload)

    def subscribe_func(self, sub_topic):
        self.client.subscribe(sub_topic)
        print('Subscribe : ' + sub_topic)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            # print('========== MQTT broker info ============')
            # print('[  ip  ] : ' + self.ip)
            # print('[ port ] : ' + str(self.port))
            # print('=' * 40)
            # print(' Connect Success!  Communication Ready! ')
            # print('=' * 40)
            print('MQTT_Protocol : MQTT CONNECTION OK\n')
            self.layout_instance.mqtt_connection_flag(True)
        else:
            self.layout_instance.mqtt_connection_flag(False)
            self.layout_instance.mqtt_connection_rc(rc)
            self.client.disconnect()
        

    def on_disconnect(self, client, userdata, flags, rc=0):
        if rc == 0:
            print('MQTT_Protocol : MQTT DISCONNECTION\n')
            self.layout_instance.mqtt_connection_flag(False)
        else:
            self.layout_instance.mqtt_connection_flag(False)
            self.layout_instance.mqtt_connection_rc(rc)


    def on_subscribe(self, client, userdata, mid, granted_qos):
        print('subscribed: ' + str(client) + ' ' + str(granted_qos) + 'Registration OK!')

    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        msg = str(msg.payload).replace('b', '').replace('\'', '')
        self.layout_instance.mqtt_sub_msg(topic, msg)

