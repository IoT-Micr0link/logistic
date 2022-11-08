from sqlalchemy import create_engine, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
import time
from datetime import datetime, timezone
import random


def _connect_database():
    db = create_engine('postgres://iot_app_user:tkGcbOC2w8x3tos1@localhost/iot-demo')
    Session = sessionmaker(db)
    session = Session()
    Base = automap_base()
    Base.prepare(db, reflect=True)

    return session, Base


def insertPostgresData(event):
    Session, Base = _connect_database()

    Readings = Base.classes.rfid_reading
    Items = Base.classes.rfid_item
    gsp_track = Base.classes.rfid_transferordertracking

    timestamp = None
    readings = None

    if 'data' in event:
        data = event['data']
        timestamp = datetime.fromtimestamp(data['timestamp'])
    else:
        return print('Without data')

    items = Session.query(Items)

    readings = data['readings']
    location = data['location_id']
    item = items.filter_by(epc=readings['epc'])

    if readings['Action'] == 'READ' or readings['Action'] == 'IN':
        item.update({
            'last_seen_timestamp': timestamp,
            'last_seen_action': readings['Action'],
            'last_seen_location_id': 2,
        })

    elif readings['Action'] == 'OUT':
        item.update({
            'last_seen_timestamp': timestamp,
            'last_seen_location_id': None,
            'in_transit': True,
        })

    r = Readings(
        epc=readings['epc'],
        antenna_id=readings['antennaID'],
        node_id=readings['node_id'],
        reader_id=readings['reader_id'],
        timestamp_reading=timestamp,
        action=readings['Action']
    )

    Session.add(r)
    print('Readings Added: ' + str(len(readings)))

    try:
        pedido = data['pedido']
        lat = data['latitude']
        lon = data['longitude']
        g = gsp_track(
            order_id=pedido,
            latitude=lat,
            longitude=lon,
            timestamp_reading=timestamp
        )
        Session.add(g)
        print('Last GPS track: ' + 'lat: ' + str(lat), 'lon: ' + str(lon))
    except KeyError:
        print("No es GPS")

    Session.commit()


def insertFirebaseData(event):

    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db

    import base64
    import json
    from datetime import datetime

    # Firebase Config

    if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
        cred = credentials.Certificate('firebaseprivatekey.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://healthy-zone-266815.firebaseio.com/'
        })

        print('firebase instance already exists')

        timestamp = None
        readings = None
        location = None

        if 'data' in event:
            data = event['data']
            timestamp = data['timestamp']
            readings = data['readings']
            location = data['location_id']
        else:
            data = 'Its empty!'

        date = datetime.fromtimestamp(timestamp)
        root = db.reference()
        child = root.child('reads')
        child.set({
            'count_reads': len(readings),
            'location': location,
            'time': str(date.ctime())
        })

        print('payload', readings, 'timestamp', date.ctime())


        # [END functions_insertFirebaseData]


def generate_data():
    Session, Base = _connect_database()
    Items = Base.classes.rfid_item
    items = Session.query(Items)
    items_list = []

    for i in items:
        items_list.append(i.epc)

    ACTION = ['IN', 'OUT', 'READ']

    event = {
        'data': {
            'readings': {
                'epc': random.choice(items_list),
                'antennaID': random.randint(1, 2),
                'node_id': 1,
                'reader_id': 1,
                'Action': random.choice(ACTION)
            },
            'location_id': random.randint(1, 2),
            'timestamp': datetime.today().replace(tzinfo=timezone.utc).timestamp(),
        }
    }

    print(event)
    return event


if __name__ == '__main__':
    while True:
        event = generate_data()
        insertPostgresData(event)
        time.sleep(10)