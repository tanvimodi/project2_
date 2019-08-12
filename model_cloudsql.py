# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    instrument = db.Column(db.String(255))
    
    

    def __repr__(self):
        return "<User(name='%s', email= '%s', instrument = '%s')" % (self.name, self.email , self.instrument )
# [END model]

# [START model]
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(255))
    address = db.Column(db.String(255))

    def __repr__(self):
        return "<User(venue_name='%s', address= '%s')" % (self.venue_name, self.address )
# [END model]
    

# [START model]
class Timeslot(db.Model):
    __tablename__ = 'timeslots'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    def __repr__(self):
        return "<User(time='%s')" % (self.time)
    
# [END model]   
    

# [START model]
    
class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(255))
    admin_email = db.Column(db.String(255))
    
    
    def __repr__(self):
        return "<User(admin_name='%s', admin_email = '%s')" % (self.time)
 # [END model]   
    
    
# [START model]
class Event(db.Model):
    __tablename__ = 'events_two'

    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(255))
    started = db.Column(db.Boolean())
    date = db.Column(db.Date())
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))
    
    def __repr__(self):
        return "<User(eventname='%s', date = '%s')" % (self.eventname, self.date)
    
 # [END model]  
    
    
  # [START model]  
class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255))
    event_id = db.Column(db.Integer, db.ForeignKey('events_two.id'))
    
    def __repr__(self):
        return "<User(user_email='%s', event_id = '%s')" % (self.user_email, self.event_id)
# [END model]


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Event.query)
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]

# [START list]
def list_e(date, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Event.query)
    books = builtin_list(map(from_sql, query.filter_by(date =date )))
    return (books)
# [END list]




# [START list]
def list_venues(cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Venue.query)
    books = builtin_list(map(from_sql, query.all()))
    return (books)
# [END list]


# [START list]
def list_v(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Venue.query)
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]


# [START list]
def list_reservations(user_email, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Reservation.query)
    books = builtin_list(map(from_sql, query.filter_by(user_email =user_email )))
    #next_page = cursor + limit if len(books) == limit else None
    return (books)
# [END list]



# [START list]
def list_events(venueid, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Event.query)
    books = builtin_list(map(from_sql, query.filter_by(venue_id =venueid )))
    #next_page = cursor + limit if len(books) == limit else None
    return (books)
# [END list]

# [START list]
def list_events_time(date, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Event.query)
    books = builtin_list(map(from_sql, query.filter_by(date = date)))
    #next_page = cursor + limit if len(books) == limit else None
    return (books)
# [END list]


# [START read]
def read(id):
    result = User.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def create(data):
    book = User(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create]

# [START create]
def create_reservation(data):
    book = Reservation(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create]



# [START create]
def create_venue(data):
    book = Venue(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create]



# [START update]
def update(data, id):
    book = User.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)
# [END update]


def delete(id):
    Event.query.filter_by(id=id).delete()
    
    db.session.commit()
    
def delete_reservations(id):
    Reservation.query.filter_by(event_id=id).delete()
    
    db.session.commit()
    
    
def delete_user(id):
    User.query.filter_by(id=id).delete()
    
    db.session.commit()
    
def delete_reserve(id):
   
    Reservation.query.filter_by(venue_id=id).delete()
    
    db.session.commit()
    
def delete_event(id):
    
    Event.query.filter_by(venue_id=id).delete()

    db.session.commit()
       
def delete_venue(id):
     #get the first event with that venue
    theevent = Event.query.filter_by(venue_id=id).first()

    #the the first events id
    theeventid = theevent.id

    #delete the reservation using the first events id
    Reservation.query.filter_by(event_id=theeventid).delete()

    #delete the events at this venue
    Event.query.filter_by(venue_id=id).delete()

    #delete the venue
    Venue.query.filter_by(id=id).delete()

    db.session.commit()
       
      
    
    

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
