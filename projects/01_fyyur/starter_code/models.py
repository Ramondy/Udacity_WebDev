# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

genre_venues = db.Table('genre_venues',
                 db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
                 db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
                 )

genre_artists = db.Table('genre_artists',
                 db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
                 db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
                 )


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String())
    state = db.Column(db.String(2))
    venues = db.relationship('Venue', backref='area')
    artists = db.relationship('Artist', backref='area')


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # ADD MISSING FIELDS
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))

    # RELATIONSHIPS
    shows = db.relationship('Show', backref='artist')
    genres = db.relationship('Genre', secondary=genre_artists, backref=db.backref('artists', lazy=True))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone
        }


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # ADD MISSING FIELDS
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))

    # RELATIONSHIPS
    shows = db.relationship('Show', backref='venue')
    genres = db.relationship('Genre', secondary=genre_venues, backref=db.backref('venues', lazy=True))


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    # RELATIONSHIPS
    showtimes = db.relationship('Showtime', backref='show')


class Showtime(db.Model):
    __tablename__ = 'showtimes'

    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), primary_key=True)
    show_time = db.Column(db.DateTime(), primary_key=True)