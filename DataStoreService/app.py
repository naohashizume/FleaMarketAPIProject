import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from sell_request import SellRequest
from buy_request import BuyRequest
from sqlalchemy.sql.elements import and_
import datetime
import pymysql
import yaml
from pykafka import KafkaClient
import json
import logging.config
from threading import Thread

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')



# DB_ENGINE = create_engine('sqlite:///requests.sqlite')
DB_ENGINE = create_engine('mysql+pymysql://%s:%s@%s:%i/%s' %(app_config['datastore']['user'],
                                                             app_config['datastore']['password'],
                                                             app_config['datastore']['hostname'],
                                                             app_config['datastore']['port'],
                                                             app_config['datastore']['db']))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_sell_request(startDate, endDate):
    """ Get selling requests from the data store """

    results_list = []

    session = DB_SESSION()

    results = session.query(SellRequest).filter(and_(SellRequest.date_created >= datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S"), SellRequest.date_created <= datetime.datetime.strptime(endDate,"%Y-%m-%dT%H:%M:%S")))
    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 201


def get_buy_request(startDate, endDate):
    """ Get buying requests from the data store """

    results_list = []

    session = DB_SESSION()


    results = session.query(BuyRequest).filter(and_(BuyRequest.date_created >= datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S"), BuyRequest.date_created <= datetime.datetime.strptime(endDate,"%Y-%m-%dT%H:%M:%S")))

    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 201


def add_request_to_db(type, payload):
    if type == "br":
        logger.info('Adding new buy request...')
        session = DB_SESSION()
        br = BuyRequest(payload['customer_id'],
                        payload['seller_id'],
                        payload['item_id'],
                        payload['item_name'],
                        payload['time_stamp']
                        )
        session.add(br)
        session.commit()
        session.close()
        logger.info("Added new buy request to database")
    elif type == "sr":
        logger.info('Adding new sell request...')
        session = DB_SESSION()
        sr = SellRequest(payload['customer_id'],
                         payload['seller_id'],
                         payload['item_id'],
                         payload['item_name'],
                         payload['time_stamp']
                         )
        session.add(sr)
        session.commit()
        session.close()
        logger.info("Added new sell request to database")
    return


def process_messages():
    client = KafkaClient(hosts='%s:%i' % (app_config['kafka']['server'], app_config['kafka']['port']))
    topic = client.topics['%s' % (app_config['kafka']['topic'])]
    consumer = topic.get_simple_consumer(auto_commit_enable=True, auto_commit_interval_ms=1000, consumer_group="storageApi")
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        # Check the type and add to the DB
        logger.info(json.dumps(msg['payload']))
        print('-' * 100)
        add_request_to_db(msg['type'], msg['payload'])


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    # run our standalone event server
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)