import mysql.connector
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

class Config(object):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secretAgent007'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///config.db'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://user:password@xxx.yyy.zzz.w/equipconfig"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Equip(db.Model):
    __tablename__ = 'equip'

    eid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100))
    line = db.Column(db.String(100))
    lineid = db.Column(db.String(50))
    etype = db.Column(db.String(100))
    simulator = db.Column(db.Boolean)
    errate = db.Column(db.Float)
    success = db.Column(db.Float)
    filename = db.Column(db.String(50))

    def __init__(self, eid, name, line, lineid, etype, simulator, errate, success, filename):
        self.eid = eid
        self.name = name
        self.line = line
        self.lineid = lineid
        self.etype = etype
        self.simulator = simulator
        self.errate = errate
        self.success = success
        self.filename = filename

    def __repr__(self):
        return '<Equip {}>'.format(self.name)


class Continuous(db.Model):
    __tablename__ = 'continuous'

    cid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100))
    eid = db.Column(db.Integer)
    cmax = db.Column(db.Float)
    cmin = db.Column(db.Float)

    distribution = db.Column(db.String(50))
    posparam1 = db.Column(db.Float)
    posparam2 = db.Column(db.Float)
    negparam1 = db.Column(db.Float)
    negparam2 = db.Column(db.Float)

    def __init__(self, cid, name, eid, cmax, cmin, distribution='norm', posparam1=0, posparam2=1, negparam1=0, negparam2=1):
        self.cid = cid
        self.name = name
        self.eid = eid
        self.cmax = cmax
        self.cmin = cmin
        self.distribution = distribution
        self.posparam1 = posparam1
        self.posparam2 = posparam2
        self.negparam1 = negparam1
        self.negparam2 = negparam2

    def __repr__(self):
        return '<Continuous {}>'.format(self.name)


class Discrete(db.Model):
    __tablename__ = 'discrete'

    dd = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100))
    eid = db.Column(db.Integer)
    numlevels = db.Column(db.Integer)
    levels = db.Column(db.String(500))
    posprobs = db.Column(db.String(500))
    negprobs = db.Column(db.String(500))

    def __init__(self, dd, name, eid, numlevels, levels, posprobs='', negprobs=''):
        self.dd = dd
        self.name = name
        self.eid = eid
        self.numlevels = numlevels
        self.levels = levels
        self.posprobs = posprobs
        self.negprobs = negprobs

    def __repr__(self):
        return '<Discrete {}>'.format(self.name)


class Alert(db.Model):
    __tablename__ = 'alert'

    aid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100))
    eid = db.Column(db.Integer)
    atype = db.Column(db.String(100))
    warnlevel = db.Column(db.Float)
    alarmlevel = db.Column(db.Float)
    increasing = db.Column(db.Boolean)

    def __init__(self, aid, name, eid, atype, warnlevel, alarmlevel, increasing):
        self.aid = aid
        self.name = name
        self.eid = eid
        self.atype = atype
        self.warnlevel = warnlevel
        self.alarmlevel = alarmlevel
        self.increasing = increasing

    def __repr__(self):
        return '<Alarm {}>'.format(self.name)


if __name__ == '__main__':
    manager.run()