import connexion
from connexion import NoContent
import requests
from pykafka import KafkaClient
import yaml
import datetime
import json

try:
     with open('/config/app_conf.yml') as f:
        app_config = yaml.safe_load(f.read())
except:
    with open('app_conf.yaml', 'r') as f:
            app_config = yaml.safe_load(f.read())

def add_sell_request(sell_request):
    """ Receives a request for selling an item """
    # response = requests.post(STORE_SERVICE_SELL_REQUEST_URL, json=sell_request, headers=HEADERS)
    client = KafkaClient(hosts='%s:%i' % (app_config['kafka']['server'], app_config['kafka']['port']))
    topic = client.topics['%s' % (app_config['kafka']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "sr",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": sell_request}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 200


def add_buy_request(buy_request):
    """ Receives a request for buying an item """
    # response = requests.post(STORE_SERVICE_BUY_REQUEST_URL, json=buy_request, headers=HEADERS)
    client = KafkaClient(hosts='%s:%i' % (app_config['kafka']['server'], app_config['kafka']['port']))
    topic = client.topics['%s' % (app_config['kafka']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "br",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": buy_request}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)