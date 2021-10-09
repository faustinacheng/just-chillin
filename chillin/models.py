from chillin import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    # username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # budget = db.Column(db.Integer, nullable=False, default=1000)
    hosted_events = db.relationship("Event", backref="event_host", lazy=True)
    joined_events = db.relationship("UserEvent", backref="event_member", lazy=True)

    def get_id(self):
        return (self.user_id)

    # @property
    # def prettier_budget(self):
    #     if len(str(self.budget)) >= 4:
    #         formatted_budget = str(self.budget)
    #         for n in range(3, len(str(self.budget)), 4):
    #             formatted_budget = f"{formatted_budget[:-n]},{formatted_budget[-n:]}"
    #         return f"${formatted_budget}"
    #     else:
    #         return f"${self.budget}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    # def can_purchase(self, item_obj):
    #     return self.budget >= item_obj.price
    #
    # def can_sell(self, item_obj):
    #     return item_obj in self.items


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=60), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    location = db.Column(db.String(length=100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    group_size = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(length=20), nullable=False)
    joined = db.Column(db.Integer, nullable=False, default=0)
    host = db.Column(db.Integer(), db.ForeignKey('user.user_id'))

    # def __repr__(self):
    #     return f"Item {self.name}"
    #
    # @property
    # def prettier_price(self):
    #     if len(str(self.price)) >= 4:
    #         formatted_price = str(self.price)
    #         for n in range(3, len(str(self.price)), 4):
    #             formatted_price = f"{formatted_price[:-n]},{formatted_price[-n:]}"
    #         return f"${formatted_price}"
    #     else:
    #         return f"${self.price}"
    #
    # def buy(self, user_obj):
    #     self.owner = user_obj.id
    #     user_obj.budget -= self.price
    #
    # def sell(self, user_obj):
    #     self.owner = None
    #     user_obj.budget += self.price

class UserEvent(db.Model):
    userevent_id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    event = db.Column(db.Integer(), db.ForeignKey('event.event_id'))