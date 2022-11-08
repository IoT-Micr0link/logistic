from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timezone

COORS = [
    (4.7530568, -74.1390735),
    (4.746894, -74.1396052),
    (4.745446, -74.141162),
    (4.747892, -74.143531),
    (4.748272, -74.144035),
    (4.747041, -74.143045),
    (4.743448, -74.139891),
    (4.741557, -74.138304),
    (4.737326, -74.134805),
    (4.732314, -74.130390),
    (4.724573, -74.123882),
    (4.710933, -74.113430),
    (4.703684, -74.102762),
    (4.697669, -74.093780),
    (4.688423, -74.082797),
    (4.682757, -74.079253),
    (4.684051, -74.078202),
    (4.684639, -74.079532),
    (4.685997, -74.079285),
    (4.685238, -74.077944),
    (4.683527, -74.079671),
    (4.679515, -74.084708),
    (4.672586, -74.088967),
    (4.666850, -74.093000),
    (4.662027, -74.096884),
    (4.656799, -74.100937),
    (4.652778, -74.104199),
    (4.650736, -74.105787),
]

def _connect_database():
    db = create_engine('postgres://iot_app_user:tkGcbOC2w8x3tos1@localhost/iot-demo')
    Session = sessionmaker(db, autoflush=False)
    session = Session()
    Base = automap_base()
    Base.prepare(db, reflect=True)

    return session, Base

def add_cors():

    Session, Base = _connect_database()

    transfer_coors = Base.classes.rfid_transferordertracking
    transfer_order = Base.classes.rfid_transferorder

    order = Session.query(transfer_order)

    for coor in COORS:
        c = transfer_coors(
            timestamp_reading=datetime.today().replace(tzinfo=timezone.utc).timestamp(),
            latitude=coor[0],
            longitude=coor[1],
            order_id=order[0],
        )
        Session.add(c)

    Session.commit()


if __name__ == '__main__':
    add_cors()
