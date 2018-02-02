from cs50 import SQL
from flask import  request
from flask_session import Session
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

class User_Data:
    def __init__ (self):
        # Configure CS50 Library to use SQLite database
        self.db = SQL("sqlite:///sport.db")

    def create_user(self, username, hash, email):
        return self.db.execute("INSERT INTO users (username, hash, email) VALUES(:username,:hash, :email)",
                                    username=username,hash= hash, email=email)

    def get_user_info(self, username):
        return self.db.execute("SELECT * FROM users WHERE username = :username", username=username)

    def check_user(self, email):
        return self.db.execute("SELECT * FROM users WHERE email = :email", email = email)

    def create_new_event(self, id, eventDate, eventPlace, eventType, eventName):
        return self.db.execute("INSERT INTO events (id ,date, place, type, eventname, created, joined) VALUES (:id, :date, :place, :type, :eventname, :true, :false)",
                                        id=id, date = eventDate, place = eventPlace ,type = eventType, eventname = eventName, true=1, false=0)

    def get_available_events(self):
        return self.db.execute("SELECT * FROM events WHERE participant = 1 group by eventname")

    def join_event(self, id, event_id):
        return self.db.execute("INSERT INTO user_events (user_id, event_id) VALUES (:id, :event_id)", id=id, event_id=event_id)

    def already_participant(self, id, event):
        participants = self.db.execute("SELECT * FROM user_events")
        for participant in participants:
            existed_participant = participant["user_id"]
            existed_event = participant["event_id"]
            if int(existed_participant) == int(id) and int(existed_event) == int(event):
                return True
        return False

    def get_my_events(self, id):
        event_id = self.db.execute("SELECT * FROM user_events WHERE user_id = :id", id=id)
        events = []
        for event in event_id:
            event_name = event["event_id"]
            compare = self.db.execute("SELECT * FROM events WHERE index_id = :event_name", event_name = event_name)
            for line in compare:
                events.append(line)
        return events
