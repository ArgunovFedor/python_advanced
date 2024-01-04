import os

from sqlalchemy import Column, Integer, String, Float, \
    create_engine, Sequence, Identity, ForeignKey, delete, Boolean, JSON, ARRAY, union, cast
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from flask import Flask, jsonify
from typing import Dict, Any
from sqlalchemy.dialects.postgresql import insert

app = Flask(__name__)
host = 'localhost'
port = 5432
user = 'admin'
password = 'admin'
mydb = 'skillbox_db'
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{mydb}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Coffee (Base):
    __tablename__ = 'coffees'
    id = Column(Integer, Sequence('coffee_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(200))
    notes = Column(ARRAY(Integer))
    def __repr__(self):
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id  = Column(Integer, ForeignKey('coffees.id', ondelete='CASCADE', onupdate='CASCADE'))
    coffee = relationship("Coffee", backref="coffees")

    def __repr__(self):
        return f"Пользователь {self.username}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


@app.before_request
def before_request_func():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    objects = [
        Coffee(title="Dark Cake", origin='Western Region, Kigoma, Tanzania', intensifier='astringent'),
        Coffee(title="Holiday Been", origin='Nayarit, Mexico', intensifier='muted'),
        Coffee(title="Pumpkin-spice Cup", origin='Boquete, Panama', intensifier='balanced'),
        Coffee(title="Chocolate Level", origin='Mount Elgon', intensifier='tart'),
        Coffee(title="Express Bean", origin='San Luis Potosi, Mexico', intensifier='astringent'),
        Coffee(title="Cascara Mug", origin='Lintong, Sumatra","variety', intensifier='clean'),
        Coffee(title="Seattle Treat", origin='Western Region, Bukova, Tanzania', intensifier='muted'),
        Coffee(title="Wake-up Light", origin='West Valley, Costa Rica', intensifier='faint'),
        Coffee(title="Strong Equinox", origin='Cundinamarca, Colombia', intensifier='bright'),
        Coffee(title="Pumpkin-spice Equinox", origin='Rulindo, Rwanda', intensifier='delicate'),
        User(name='u1', coffee_id=1, address={"id":6216,"uid":"f75d1435-e018-46f3-9bc1-90a33d798a4c","city":"North Tequila","street_name":"Green Parks","street_address":"834 Bergstrom Tunnel","secondary_address":"Apt. 802","building_number":"769","mail_box":"PO Box 604","community":"Eagle Court","zip_code":"20337-1332","zip":"73543-3433","postcode":"26976-6381","time_zone":"Asia/Tokyo","street_suffix":"Keys","city_suffix":"chester","city_prefix":"New","state":"Kansas","state_abbr":"WA","country":"Singapore","country_code":"CL","latitude":-50.62470953356819,"longitude":144.65295945440283,"full_address":"Suite 994 3206 Elanor Village, New Mark, TX 00309"}),
        User(name='u2', coffee_id=1, address={"id":767,"uid":"2665f539-6dd9-4638-aa4a-e5bc70c3ca6a","city":"North Cecile","street_name":"McLaughlin Stravenue","street_address":"877 Daugherty Meadows","secondary_address":"Suite 139","building_number":"6808","mail_box":"PO Box 33","community":"Eagle Crossing","zip_code":"26960-2142","zip":"20625","postcode":"64909","time_zone":"Europe/Bucharest","street_suffix":"Meadow","city_suffix":"berg","city_prefix":"Port","state":"Delaware","state_abbr":"ID","country":"Guadeloupe","country_code":"SG","latitude":56.44094203918226,"longitude":-11.274122922738457,"full_address":"Apt. 616 649 Edmundo Corners, McGlynnview, TN 56115"}),
        User(name='u3', coffee_id=1, address={"id":5907,"uid":"afe11e38-2616-47e2-ba48-2e9b9dba7bc9","city":"South Richardhaven","street_name":"Loren Islands","street_address":"46503 Fawn Inlet","secondary_address":"Apt. 475","building_number":"651","mail_box":"PO Box 4425","community":"Autumn Acres","zip_code":"77883","zip":"97753-0221","postcode":"45214","time_zone":"Asia/Seoul","street_suffix":"Causeway","city_suffix":"mouth","city_prefix":"New","state":"North Dakota","state_abbr":"NV","country":"Brunei Darussalam","country_code":"AW","latitude":34.57631568241075,"longitude":38.948772019228414,"full_address":"1227 Alonzo Lake, South Jeniferstad, WY 43172-7396"}),
        User(name='u4', coffee_id=1, address={"id":3159,"uid":"c932a503-9f4f-48be-926b-700190e3bd98","city":"Mullermouth","street_name":"Oren Viaduct","street_address":"1423 Considine Course","secondary_address":"Suite 311","building_number":"2972","mail_box":"PO Box 2859","community":"Royal Oaks","zip_code":"18894","zip":"31063-7344","postcode":"62055","time_zone":"Europe/Stockholm","street_suffix":"Meadow","city_suffix":"chester","city_prefix":"New","state":"Nebraska","state_abbr":"CA","country":"Bahrain","country_code":"BA","latitude":75.06627999001901,"longitude":-145.30144865307648,"full_address":"52691 Elwood Tunnel, Theronview, CO 43432-3600"}),
        User(name='u5', coffee_id=1, address={"id":2218,"uid":"3eab066e-cf9d-4893-ad06-3e8100355ea8","city":"Lake Kylestad","street_name":"Toney Landing","street_address":"5239 Sherwood Overpass","secondary_address":"Apt. 761","building_number":"197","mail_box":"PO Box 151","community":"Pine Estates","zip_code":"63684-6625","zip":"86344","postcode":"53623","time_zone":"Asia/Kolkata","street_suffix":"Centers","city_suffix":"ton","city_prefix":"West","state":"Connecticut","state_abbr":"GA","country":"Liechtenstein","country_code":"GU","latitude":6.851882565314227,"longitude":-74.29383265587451,"full_address":"94622 Ericka Mountain, Lake Earle, AL 13779-7370"}),
        User(name='u6', coffee_id=1, address={"id":8752,"uid":"6ab036cf-d2f7-4cf7-b202-26a46e4943e8","city":"Lake Hsiu","street_name":"Skiles Row","street_address":"774 Reichel Mountains","secondary_address":"Suite 813","building_number":"989","mail_box":"PO Box 29","community":"Eagle Square","zip_code":"09472","zip":"02543","postcode":"42474-7365","time_zone":"Europe/Athens","street_suffix":"Crest","city_suffix":"borough","city_prefix":"North","state":"Missouri","state_abbr":"MN","country":"Saint Lucia","country_code":"IE","latitude":-47.377132241259645,"longitude":-107.6552747704894,"full_address":"Suite 328 584 Saul Wells, Lake Branditown, PA 62401-2782"}),
        User(name='u7', coffee_id=1, address={"id":9924,"uid":"392e7f53-c845-46f7-b68e-9be936af4121","city":"Emoryview","street_name":"Min Stravenue","street_address":"5485 Ching Glens","secondary_address":"Apt. 673","building_number":"7456","mail_box":"PO Box 29","community":"Summer Estates","zip_code":"38665","zip":"09852","postcode":"82051-3904","time_zone":"Asia/Yerevan","street_suffix":"Wall","city_suffix":"chester","city_prefix":"East","state":"Ohio","state_abbr":"ID","country":"Uganda","country_code":"PH","latitude":5.616590950885808,"longitude":102.9788831597196,"full_address":"954 Tammi Club, Stehrmouth, ID 85464-5969"}),
        User(name='u8', coffee_id=1, address={"id":9877,"uid":"378b6aad-2495-43a7-ab99-089cf2ece710","city":"Port Krismouth","street_name":"Shizue Cliffs","street_address":"1357 Buster Orchard","secondary_address":"Suite 276","building_number":"41099","mail_box":"PO Box 6191","community":"Autumn Oaks","zip_code":"06053-9817","zip":"22363","postcode":"90275-6457","time_zone":"America/Indiana/Indianapolis","street_suffix":"Harbor","city_suffix":"shire","city_prefix":"North","state":"Louisiana","state_abbr":"NE","country":"Bahrain","country_code":"CG","latitude":24.431305624874568,"longitude":129.73476759762013,"full_address":"8682 Bong Walks, Port Markburgh, CA 40927-7601"}),
        User(name='u9', coffee_id=1, address={"id":9493,"uid":"a67bf969-1e03-4a5d-8a0e-c982e8363ef1","city":"Port Fritz","street_name":"Geoffrey Throughway","street_address":"142 Huong Island","secondary_address":"Suite 546","building_number":"642","mail_box":"PO Box 3280","community":"Royal Creek","zip_code":"86919-2729","zip":"63190","postcode":"07885","time_zone":"Asia/Kabul","street_suffix":"Ville","city_suffix":"view","city_prefix":"West","state":"Kansas","state_abbr":"IN","country":"Denmark","country_code":"FM","latitude":17.66841321280897,"longitude":-23.896275686376953,"full_address":"Apt. 728 773 Vikki Cape, Ikeland, ME 12579"}),
        User(name='u10', coffee_id=1, address={"id":3474,"uid":"95e02a6f-d60c-4720-9dd5-69d5bd4ca412","city":"Nienowhaven","street_name":"Mandi Valley","street_address":"40358 Clementine Vista","secondary_address":"Suite 383","building_number":"72744","mail_box":"PO Box 6286","community":"Willow Square","zip_code":"48871-7868","zip":"20809-9099","postcode":"23336","time_zone":"Asia/Karachi","street_suffix":"Mews","city_suffix":"fort","city_prefix":"Port","state":"New Mexico","state_abbr":"MT","country":"Dominican Republic","country_code":"GQ","latitude":-16.61752216336555,"longitude":11.64513694987022,"full_address":"5205 Wuckert Cape, North Giuseppe, OR 09922"}),
    ]
    session.bulk_save_objects(objects)
    session.commit()

@app.route('/users', methods=['POST'])
def create_new_user():
    # TOBE: по хорошему, чтобы из аргументов принимало параметры, но для примера так захардкодил
    insert_query = insert(User).values(name='Новый пользователь', has_sale=False, address='Новый адрес', coffee_id=1)
    session.execute(insert_query)
    session.commit()
    result = session.query(User).order_by(User.id.desc()).first()
    return result.to_json(), 200

@app.route('/coffees/<string:text>', methods=['GET'])
def find_coffee(text: str):
    coffees = session.query(Coffee).where(
        Coffee.title.match(text, postgresql_regconfig='english')
    )
    products_list = []
    for coffee in coffees:
        coffee_obj = coffee.to_json()
        products_list.append(coffee_obj)
    return jsonify(products_list)

@app.route('/coffees/<int:id>/unotes')
def get_unique_notes():
    pass

@app.route('/users/country/<string:address_text>')
def get_unique_users_from_country(address_text: str):
    users = session.query(User).filter(
        User.address["city"] == "Doe").all()
    users_list = []
    for user2 in users:
        user_obj = user2.to_json()
        users_list.append(user_obj)
    return jsonify(users_list)


if __name__ == '__main__':
    app.run()
