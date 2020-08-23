import yaml
from kafka import KafkaConsumer
import json
import psycopg2

from kafka.admin import KafkaAdminClient, NewTopic

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

print(topic)

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092"
)
try:
    topic_list = []
    topic_list.append(NewTopic(name="icl-producer", num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
except Exception as e:
    print("Cannot create topic. It may already exist.")
    print(e)

consumer = {}
try:
    consumer = KafkaConsumer(topic, bootstrap_servers=config["kafka"]["url"])
except Exception as e:
    print("'kafka.url' key not found in config ")
    print(e)
    exit(2)

conn = {}
try:
    host = config["postgres"]["host"]
    port = config["postgres"]["port"]
    user = config["postgres"]["user"]
    password = config["postgres"]["password"]
    database = config["postgres"]["database"]
    # from https://www.postgresqltutorial.com/postgresql-python/connect/
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
except Exception as e:
    print("error when trying to read postgres config or connect to db:")
    print(e)
    exit(4)


consumer.subscribe([topic])

tables = {
    "htmlrequests":["xRequestId","time","version","product","application","applicationVersion","buildVersion","environment","backendRegion","origin","channel","path","method","userAgent"],
    "service":["serviceId", "serviceProviderName", "serviceMainType","startTime","endTime","predictedStartTime","predictedEndTime"],
    "sub":["subId", "vin", "serviceStatus","startLocationLongitude","startLocationLatitude",
    "endLocationLongitude","endLocationLatitude","serviceId"],
    "requests":["requestId", "serviceId"],
    "event":["id", "time", "privacyClass","flowId","xRequestId","contentCategory"]
    }

def runQuery (data,cur,table):
    names = ','.join(tables[table]).lower()
    values = ""
    for item in tables[table]:
        if table == "htmlrequests" or table=="event":
            values += "'{}'".format(data[item])+","
        elif table=="service" or table=="requests":
            values += "'{}'".format(data["content"][item])+","
        elif table=="sub":
            if "Location" in item:
                itemarr = item.split("L")
                value = data["content"][itemarr[0]+"L"+itemarr[1]]["l"+itemarr[2]] if itemarr[0]+"L"+itemarr[1] in data["content"] else ""
                values += "'{}'".format(value)+","
            else:
                values += "'{}'".format(data["content"][item])+","
    values = values[:-1]
    query = "INSERT INTO " + config["postgres"]["table"] + "."+ table + "("+names+")"+ "VALUES("+values+")"
    print(query)
    cur.execute(query)
    
try:
    cur = conn.cursor()
    for msg in consumer:
        data = json.loads(msg.value.decode('utf-8'))
        runQuery(data,cur,"htmlrequests")
        conn.commit()

        query = "select * from icl.service where serviceid = "+"'"+data["content"]["serviceId"]+"'"
        cur.execute(query)
        if len(cur.fetchall()) == 0:
            runQuery(data,cur,"service")
            conn.commit()
        
        runQuery(data,cur,"sub")
        conn.commit()

        query = "select * from icl.requests where requestid = "+"'"+data["content"]["requestId"]+"'"
        cur.execute(query)
        if len(cur.fetchall()) == 0:
                runQuery(data,cur,"requests")
                conn.commit()

        runQuery(data,cur,"event")
        conn.commit()
finally:
    cur.close()
    conn.close()