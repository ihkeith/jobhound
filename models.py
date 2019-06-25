import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('job_tracker.db')


class User(UserMixin, Model):
    username = CharField(max_length=255, unique=True)
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)
    date_joined = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
    
    @classmethod
    def create_user(cls, username, email, password, date_joined):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
            )
        except IntegrityError:
            raise ValueError("User already exists")
    
    def get_applications(self):
        return Application.select().where(Application.user == self)
    
    def get_events(self):
        return Event.select().where(Event.user == self)
    
    def get_contacts(self):
        return Contact.select().where(Contact.user == self)


class Application(Model):
    date_applied = DateField()
    company_name = CharField(max_length=255)
    job_title = CharField(max_length=255)
    notes = TextField()
    phone_interview = CharField(max_length=5)
    in_person_interview = CharField(max_length=5)
    application_contact = CharField(max_length=255)
    user = ForeignKeyField(User, backref="applications")

    class Meta:
        database = DATABASE
        order_by = ('-date_applied',)


class Event(Model):
    event_date = DateTimeField()
    event_name = CharField(max_length=255)
    event_type = CharField(max_length=255)
    event_location = CharField(max_length=255)
    event_time = TimeField()
    event_cost = CharField()
    event_notes = TextField()
    user = ForeignKeyField(User, backref="events")

    class Meta:
        database = DATABASE
        order_by = ('-event_date',)


class Contact(Model):
    contact_name = CharField(max_length=255, unique=True)
    contact_current_company = CharField(max_length=255)
    contact_title = CharField(max_length=255)
    contact_phone = CharField(max_length=11)
    contact_email = CharField(max_length=255)
    contact_is_reference = CharField()
    contact_notes = TextField()
    user = ForeignKeyField(User, backref="contacts")

    class Meta:
        database = DATABASE
        order_by = ('-contact_name',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Application, Event, Contact], safe=True)
    DATABASE.close()