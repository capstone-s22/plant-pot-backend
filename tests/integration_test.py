from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import json

from main import app

valid_sample_messages_dirpath = "tests/sample_messages/valid"
invalid_sample_messages_dirpath = "tests/sample_messages/invalid"

def get_data(filepath):
    with open(filepath, 'r') as f:
        datastore = json.load(f)
    return datastore

def test_register_pot_valid():
    client = TestClient(app)
    message_filepath = "{}/create_pot_valid.json".format(valid_sample_messages_dirpath)
    message = get_data(message_filepath)
    pot_id = message['potId']
    with client.websocket_connect("/ws/{}".format(pot_id)) as websocket:
        websocket.send_json(message)
        data = websocket.receive_text()
        assert data == "Pod {} created.".format(pot_id)

def test_check_in_valid():
    parameter = "checkIn"
    client = TestClient(app)
    message_filepath = "{}/daily_checkin_valid.json".format(valid_sample_messages_dirpath)
    message = get_data(message_filepath)
    pot_id = message['potId']
    with client.websocket_connect("/ws/{}".format(pot_id)) as websocket:
        websocket.send_json(message)
        data = websocket.receive_text()
        assert data == "{} for Pot {} updated.".format(parameter, pot_id)

def test_sensor_values_valid():
    parameter = "Sensor values"
    client = TestClient(app)
    message_filepath = "{}/update_sensors_valid.json".format(valid_sample_messages_dirpath)
    message = get_data(message_filepath)
    pot_id = message['potId']
    with client.websocket_connect("/ws/{}".format(pot_id)) as websocket:
        websocket.send_json(message)
        data = websocket.receive_text()
        assert data == "{} for Pot {} updated.".format(parameter, pot_id)

def test_register_pot_invalid():
    client = TestClient(app)
    message_filepath = "{}/create_pot_invalid.json".format(invalid_sample_messages_dirpath)
    message = get_data(message_filepath)
    pot_id = message['potId']
    with client.websocket_connect("/ws/{}".format(pot_id)) as websocket:
        websocket.send_json(message)
        data = websocket.receive_text()
        assert data == "Invalid data model"

def test_check_in_invalid():
    parameter = "checkIn"
    client = TestClient(app)
    message_filepath = "{}/daily_checkin_invalid.json".format(invalid_sample_messages_dirpath)
    message = get_data(message_filepath)
    pot_id = message['potId']
    with client.websocket_connect("/ws/{}".format(pot_id)) as websocket:
        websocket.send_json(message)
        data = websocket.receive_text()
        assert data == "Invalid data model"

def test_sensor_values_invalid():
    parameter = "Sensor values"
    client = TestClient(app)
    message_filepath = "{}/update_sensors_invalid.json".format(invalid_sample_messages_dirpath)
    message = get_data(message_filepath)
    pot_id = message['potId']
    with client.websocket_connect("/ws/{}".format(pot_id)) as websocket:
        websocket.send_json(message)
        data = websocket.receive_text()
        assert data == "Invalid data model"


if __name__ == '__main__':
    pass

