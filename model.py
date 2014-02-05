import config
import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class Declarations ###

class User(Base, UserMixin):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	first_name = Column(String(64), nullable=False)
	last_name = Column(String(64), nullable=False)
	email = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)
	salt = Column(String(64), nullable=False)

	trips = relationship("Trip", uselist=True)
	packing_lists = relationship("PackingList", uselist=True)

	def set_password(self, password):
	self.salt = bcrypt.gensalt()
	password = password.encode("utf-8")
	self.password = bcrypt.hashpw(password, self.salt)

	def authenticate(self, password):
		password = password.encode("utf-8")
		return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

class Trip(Base):
	__tablename__ = "trips"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	title = Column(String(64), nullable=False)
	destination = Column(String(100), nullable=False)
	start_date = Column(DateTime, nullable=False, default=None)
	end_date = Column(DateTime, nullable=False, default=None)
	total_days = Column(Integer, nullable=False)

	user = relationship("User", backref=backref("trips", order_by=id))
	packing_list = relationship("PackingList")

class PackingList(Base):
	__tablename__ = "packing_lists"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	trip_id = Column(Integer, ForeignKey("trips.id"))

	user = relationship("User", backref=backref("packing_lists", order_by=id))
	trip = relationship("Trip", backref=backref("trips", order_by=id))

class PackListItems(Base):
	__tablename__ = "packlist_items"

	id =Column(Integer, primary_key=True)
	packing_list_id=Column(Integer, ForeignKey('packing_lists.id'))
	item_id=Column(Integer, ForeignKey('items.id'), nullable=True)
	item_qty=Column(Integer, nullable=True)

	packing_list = relationship("PackingList", backref=backref("packlist_items", order_by=id))
	item = relationship("Item", backref=backref("packlist_items", order_by=id))

class Item(Base):
	__tablename__="items"

	id = Column(Integer, primary_key=True)
	name = Column(String(64), nullable=False)
	max_qty = Column(Integer, nullable=True)
	always = Column(Integer, nullable=True)

class ActivityItem(Base):
	__tablename__="activity_items"

	id = Column(Integer, primary_key=True)
	item_id = Column(Integer, ForeignKey('items.id'), nullable=True)
	activity_id = Column(Integer, ForeignKey('activities.id'), nullable=True)

	item = relationship("Item", backref=backref("activity_items", order_by=id))
	activity = relationship("Activity", backref=backref("activity_items", order_by=id))

class Activity(Base):
	__tablename__="activities"
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)

class TripActivity(Base):
	__tablename__="trip_activities"

	id = Column(Integer, primary_key=True)
	trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
	activity_id = Column(Integer, ForeignKey('activities.id'), nullable=False)

	trip = relationship("Trip", backref=backref("trip_activities", order_by=id))
	activity = relationship("Activity", backref=backref("trip_activities", order_by=id))






def create_tables():
	Base.metadata.create_all(engine)

def main():
	pass

if __name__ == "__main__":
	main()










