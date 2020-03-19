import yaml
import logging.config
import json
import os
import time
import requests
import connexion
from connexion import NoContent
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin


try:
    with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('../deployment/app_conf.yml') as f:
        app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_request_stats():
    """ Get selling requests from the data store """
    logger.info('GET request has started')

    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            json_str = f.read()
            json_data = json.loads(json_str)
            logger.debug(json_data)  # Log contents
            logger.info('GET request has completed')
            return json_data, 201
    else:
        logger.error('Log JSON File Not Found')
        logger.info('GET request has completed')
        return NoContent, 404


def populate_stats():
    """ Periodically update stats """

    # Log an INFO message indicating periodic processing has started
    logger.info("Start Periodic Processing")

    json_data = {}
    # Read in the current statistics from the JSON file
    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            json_str = f.read()
            json_data = json.loads(json_str)

    current_time = time.strftime("%Y-%m-%dT%H:%M:%S")

    if json_data.get('timestamp'):
        params = {"startDate": json_data['timestamp'], "endDate": current_time}
        response_br = requests.get(app_config['eventstore']['url']+'/buy_request', params=params)
        response_sr = requests.get(app_config['eventstore']['url']+'/sell_request', params=params)
    else:   # when json_data is empty
        params = {"startDate": '2013-01-23T09:42:47', "endDate": current_time}
        response_br = requests.get(app_config['eventstore']['url']+'/buy_request', params=params)
        response_sr = requests.get(app_config['eventstore']['url']+'/sell_request', params=params)

    br_data = response_br.json()
    sr_data = response_sr.json()

    # Log an INFO message with the number of events received
    logger.info('%s new events for buying requests are received!' % len(br_data))
    logger.info('%s new events for selling requests are received!' % len(sr_data))

    # Log an ERROR message if you did not get a 200 response code
    if response_br.status_code != 201 or response_sr.status_code != 201:
        logger.error('You received %i for GET buying requests, %i for GET selling requests' %(response_br.status_code, response_sr.status_code))

    if json_data.get('num_buy_request'):
        json_data['num_buy_request'] = json_data['num_buy_request'] + len(br_data)
    else:
        json_data['num_buy_request'] = len(sr_data)

    if json_data.get('num_sell_request'):
        json_data['num_sell_request'] = json_data['num_sell_request'] + len(sr_data)
    else:
        json_data['num_sell_request'] = len(sr_data)

    json_data['timestamp'] = current_time

    with open(app_config['datastore']['filename'],'w') as f:
        # Log a DEBUG message with your updated statistics values
        logger.debug(json_data)
        f.write(json.dumps(json_data))

    logger.info('Scheduler End')


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        populate_stats,
        'interval',
        seconds=app_config['scheduler']['period_sec']
    )
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    # run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)