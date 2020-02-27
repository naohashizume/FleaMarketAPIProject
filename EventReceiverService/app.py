import connexion
from connexion import NoContent
import requests

STORE_SERVICE_SELL_REQUEST_URL = "http://localhost:8090/sell_request"
STORE_SERVICE_BUY_REQUEST_URL = "http://localhost:8090/buy_request"
HEADERS = {"content-type":"application/json"}


def add_sell_request(sell_request):
    """ Receives a request for selling an item """
    response = requests.post(STORE_SERVICE_SELL_REQUEST_URL, json=sell_request, headers=HEADERS)

    return NoContent, response.status_code


def add_buy_request(buy_request):
    """ Receives a request for buying an item """
    response = requests.post(STORE_SERVICE_BUY_REQUEST_URL, json=buy_request, headers=HEADERS)

    return NoContent, response.status_code


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)