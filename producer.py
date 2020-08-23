import yaml
from kafka import KafkaProducer
import json

config = []

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("error parsing config")
        print(exc)
        exit(1)

# print(config)

topic = ""
try:
    topic = config["kafka"]["topic"]
except Exception as e:
    print("'kafka.topic' key not found in config")
    print(e)
    exit(3)

# print(topic)

producer = {}
try:
    producer = KafkaProducer(bootstrap_servers=config["kafka"]["url"])
except Exception as e:
    print("'kafka.url' key not found in config ")
    print(e)
    exit(2)

try:
    with open('service_subset.json', 'r') as data_file:
        json_data = data_file.read()
    data = json.loads(json_data)
    for item in data:
        #print(item)
        jsonbytes=json.dumps(item).encode('utf-8')
        producer.send(topic, jsonbytes)
except Exception as e:
    print(e,"HEREE")
finally:
    producer.flush()
