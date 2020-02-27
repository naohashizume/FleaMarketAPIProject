import connexion
from connexion import NoContent
from pykafka import KafkaClient
import yaml
import json
from flask_cors import CORS, cross_origin

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

client = KafkaClient(hosts='%s:%i' % (app_config['kafka']['server'], app_config['kafka']['port']))
topic = client.topics['%s' % (app_config['kafka']['topic'])]


def get_sell_request(number):
    """ Receives a request for selling an item based on offset number """
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)

    i = 1
    for msg in consumer:
        # print(" % s[key = % s, id = % s, offset = % s]" % (msg.value, msg.partition_key, msg.partition_id, msg.offset))
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'sr':
            if i == number:
                return msg['payload'], 200
            else:
                i = i + 1


def get_oldest_buy_request():
    """ Receives an oldest request for buying an item """
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    i = 1
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'br':
            if i == 1:
                return msg['payload'], 200
            else:
                i = i + 1

def get_oldest_sell_request():
    """ Receives an oldest request for selling an item """
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    i = 1
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'sr':
            if i == 1:
                return msg['payload'], 200
            else:
                i = i + 1


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    app.run(port=8110)