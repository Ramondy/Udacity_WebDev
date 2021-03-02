# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from sqlalchemy.exc import SQLAlchemyError
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *

# ----------------------------------------------------------------------------#
# Helpers.
# ----------------------------------------------------------------------------#

def count_shows_by(resource, upcoming=True):

    areas = Area.query.all()
    shows_by_count = {}

    if resource == 'Venue':

        for area in areas:
            for venue in area.venues:
                shows_by_count[venue.id] = 0

        if upcoming:
            shows_listTuples = db.session.query(Showtime, Show, Venue).filter(Showtime.show_id == Show.id,
                                                                                       Show.venue_id == Venue.id,
                                                                                       Showtime.show_time >= datetime.now()).all()
        if not upcoming:
            shows_listTuples = db.session.query(Showtime, Show, Venue).filter(Showtime.show_id == Show.id,
                                                                                       Show.venue_id == Venue.id,
                                                                                       Showtime.show_time < datetime.now()).all()

        for show_time, show, venue in shows_listTuples:
            shows_by_count[venue.id] += 1

    if resource == 'Artist':

        for area in areas:
            for artist in area.artists:
                shows_by_count[artist.id] = 0

        if upcoming:
            shows_listTuples = db.session.query(Showtime, Show, Artist).filter(Showtime.show_id == Show.id,
                                                                                       Show.artist_id == Artist.id,
                                                                                       Showtime.show_time >= datetime.now()).all()
        if not upcoming:
            shows_listTuples = db.session.query(Showtime, Show, Artist).filter(Showtime.show_id == Show.id,
                                                                                       Show.artist_id == Artist.id,
                                                                                       Showtime.show_time < datetime.now()).all()

        for show_time, show, artist in shows_listTuples:
            shows_by_count[artist.id] += 1

    return shows_by_count


def list_shows_by(resource, upcoming=True):

    areas = Area.query.all()
    shows_by_lists = {}

    if resource == 'Venue':

        for area in areas:
            for venue in area.venues:
                shows_by_lists[venue.id] = []

        if upcoming:
            shows_listTuples = db.session\
                .query(Showtime, Show, Artist, Venue)\
                .filter(Showtime.show_id == Show.id, Show.venue_id == Venue.id,
                        Show.artist_id == Artist.id, Showtime.show_time >= datetime.now()).all()

        if not upcoming:
            shows_listTuples = db.session\
                .query(Showtime, Show, Artist, Venue)\
                .filter(Showtime.show_id == Show.id, Show.venue_id == Venue.id,
                        Show.artist_id == Artist.id, Showtime.show_time < datetime.now()).all()

        for showtime, show, artist, venue in shows_listTuples:
            shows_by_lists[venue.id].append((showtime, show, artist, venue))

    if resource == 'Artist':

        for area in areas:
            for artist in area.artists:
                shows_by_lists[artist.id] = []

        if upcoming:
            shows_listTuples = db.session\
                .query(Showtime, Show, Artist, Venue)\
                .filter(Showtime.show_id == Show.id, Show.venue_id == Venue.id,
                        Show.artist_id == Artist.id, Showtime.show_time >= datetime.now()).all()

        if not upcoming:
            shows_listTuples = db.session\
                .query(Showtime, Show, Artist, Venue)\
                .filter(Showtime.show_id == Show.id, Show.venue_id == Venue.id,
                        Show.artist_id == Artist.id, Showtime.show_time < datetime.now()).all()

        for showtime, show, artist, venue in shows_listTuples:
            shows_by_lists[artist.id].append((showtime, show, artist, venue))

    return shows_by_lists


def build_areas_dict():
    areas_dict = {}
    areas = Area.query.all()
    for area in areas:
        key = area.city + ", " + area.state
        value = area.id
        areas_dict[key] = value
    return areas_dict


def build_venues_dict():
    venues_dict = {}
    venues = Venue.query.all()
    for venue in venues:
        key = venue.name + ", " + str(venue.area_id)
        value = venue.id
        venues_dict[key] = value
    return venues_dict


def build_genres_dict():
    genres_dict = {}
    genres = Genre.query.all()
    for genre in genres:
        key = genre.name
        value = genre.id
        genres_dict[key] = value
    return genres_dict


def build_artists_dict():
    artists_dict = {}
    artists = Artist.query.all()
    for artist in artists:
        key = artist.name + ", " + str(artist.area_id)
        value = artist.id
        artists_dict[key] = value
    return artists_dict


def build_shows_dict():
    shows_dict = {}
    shows = Show.query.all()
    for show in shows:
        key = str(show.venue_id) + ", " + str(show.artist_id)
        value = show.id
        shows_dict[key] = value
    return shows_dict


def build_showtimes_dict():
    showtimes_dict = {}
    showtimes = Showtime.query.all()
    for showtime in showtimes:
        key = str(showtime.show_id) + ", " + datetime.strftime(showtime.show_time, format="%Y-%m-%d %H:%M:%S")
        value = showtime.show_id
        showtimes_dict[key] = value
    return showtimes_dict

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    areas = Area.query.all()
    return render_template('pages/venues.html', areas=areas,
                           upcoming_counter=count_shows_by(resource='Venue', upcoming=True))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venue = Venue.query.get(venue_id)
    area = Area.query.get(venue.area_id)

    upcoming_shows = list_shows_by('Venue', upcoming=True)[venue_id]
    past_shows = list_shows_by('Venue', upcoming=False)[venue_id]

    upcoming_counter = count_shows_by(resource='Venue', upcoming=True)[venue_id]
    past_counter = count_shows_by(resource='Venue', upcoming=False)[venue_id]

    return render_template('pages/show_venue.html', venue=venue, area=area,
                           upcoming_counter=upcoming_counter, upcoming_shows=upcoming_shows,
                           past_counter=past_counter, past_shows=past_shows)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    form = VenueForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            name = form.name.data
            city = form.city.data
            state = form.state.data
            address = form.address.data
            phone = form.phone.data
            genres = form.genres.data
            image_link = form.image_link.data
            website_link = form.website_link.data
            facebook_link = form.faceboook_link.data
            seeking_talent = form.seeking_talent.data
            seeking_description = form.seeking_description.data

            # if (city, state) is a new area, insert in areas - then get area.id
            area_string = city + ", " + state
            areas_dict = build_areas_dict()

            if area_string not in areas_dict:
                new_area = Area(city=city, state=state)
                db.session.add(new_area)

            areas_dict = build_areas_dict()
            area_id = areas_dict[area_string]

            # if (name, area_id) is a new venue, insert in venues - then get venue.id
            venue_string = name + ", " + str(area_id)
            venues_dict = build_venues_dict()

            if venue_string not in venues_dict:
                new_venue = Venue(name=name, address=address, phone=phone, area_id=area_id, image_link=image_link,
                                  website=website_link, facebook_link=facebook_link, seeking_talent=seeking_talent,
                                  seeking_description=seeking_description)
                db.session.add(new_venue)

            venues_dict = build_venues_dict()
            venue_id = venues_dict[venue_string]

            # if (genres) are new genres, insert in genres - then insert in genre_venues
            for genre in genres:
                if genre not in build_genres_dict():
                    new_genre = Genre(name=genre)
                    db.session.add(new_genre)

                genres_dict = build_genres_dict()
                genre_id = genres_dict[genre]
                statement = genre_venues.insert().values(venue_id=venue_id, genre_id=genre_id)
                db.session.execute(statement)

            # commit changes to db
            db.session.commit()
            flash('Venue ' + form.name.data + ' was successfully listed!')

        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
            flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

        finally:
            db.session.close()

    else:
        message = []
        for field, errors in form.errors.items():
            message.append(field + ': (' + '|'.join(errors) + ')')
        flash('The Venue data is not valid. Please try again!')

    return render_template('pages/home.html')


#  Search Venue
#  ----------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.all()
    response = {'count': 0, 'data': []}
    for venue in venues:
        if search_term.lower() in venue.name.lower():
            response['count'] += 1
            upcoming_shows_count = count_shows_by(resource='Venue', upcoming=True)[venue.id]
            response['data'].append({'id': venue.id, 'name': venue.name,
                                     'num_upcoming_shows': upcoming_shows_count})

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


#  Update Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        # "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Delete Venue
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Read Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data,
                           upcoming_counter=count_shows_by(resource='Artist', upcoming=True))


@app.route('/api/artists')
def api_artists():

    artists = Artist.query.all()
    data = [artist.format() for artist in artists]

    return jsonify({
        'success': True,
        'artists': data,
        'total_artists': len(data)
    })


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    artist = Artist.query.get(artist_id)
    area = Area.query.get(artist.area_id)

    # shows = db.session.query(Showtime, Show, Artist, Venue)\
    #     .filter(Showtime.show_id == Show.id, Show.artist_id == Artist.id, Show.venue_id == Venue.id).all()

    upcoming_counter = count_shows_by(resource='Artist', upcoming=True)[artist_id]
    upcoming_shows = list_shows_by('Artist', upcoming=True)[artist_id]

    past_counter = count_shows_by(resource='Artist', upcoming=False)[artist_id]
    past_shows = list_shows_by('Artist', upcoming=False)[artist_id]

    return render_template('pages/show_artist.html', artist=artist, area=area,
                           upcoming_counter=upcoming_counter, upcoming_shows=upcoming_shows,
                           past_counter=past_counter, past_shows=past_shows)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            name = form.name.data
            city = form.city.data
            state = form.state.data
            phone = form.phone.data
            genres = form.genres.data
            image_link = form.image_link.data
            website_link = form.website_link.data
            facebook_link = form.faceboook_link.data
            seeking_venue = form.seeking_venue.data
            seeking_description = form.seeking_description.data

            # if (city, state) is a new area, insert in areas - then get area.id
            area_string = city + ", " + state
            areas_dict = build_areas_dict()

            if area_string not in areas_dict:
                new_area = Area(city=city, state=state)
                db.session.add(new_area)

            areas_dict = build_areas_dict()
            area_id = areas_dict[area_string]

            # if (name, area_id) is a new artist, insert in artists - then get artist.id
            artist_string = name + ", " + str(area_id)
            artist_dict = build_artists_dict()

            if artist_string not in artist_dict:
                new_artist = Artist(name=name, phone=phone, area_id=area_id, image_link=image_link,
                                  website=website_link, facebook_link=facebook_link, seeking_venue=seeking_venue,
                                  seeking_description=seeking_description)
                db.session.add(new_artist)

            artist_dict = build_artists_dict()
            artist_id = artist_dict[artist_string]

            # if genres are new genres, insert in genres - then insert in genre_artists
            for genre in genres:
                if genre not in build_genres_dict():
                    new_genre = Genre(name=genre)
                    db.session.add(new_genre)

                genres_dict = build_genres_dict()
                genre_id = genres_dict[genre]
                statement = genre_artists.insert().values(artist_id=artist_id, genre_id=genre_id)
                db.session.execute(statement)

            # commit changes to db
            db.session.commit()
            flash('Artist ' + request.form['name'] + ' was successfully listed!')

        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
            flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')

        finally:
            db.session.close()

    else:
        message = []
        for field, errors in form.errors.items():
            message.append(field + ': (' + '|'.join(errors) + ')')
        flash('The Venue data is not valid. Please try again!')

    return render_template('pages/home.html')


#  Search Artist
#  ----------------------------------------------------------------

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist.query.all()
    response = {'count': 0, 'data': []}
    for artist in artists:
        if search_term.lower() in artist.name.lower():
            response['count'] += 1
            upcoming_shows_count = count_shows_by(resource='Artist', upcoming=True)[artist.id]
            response['data'].append({'id': artist.id, 'name': artist.name,
                                     'num_upcoming_shows': upcoming_shows_count})

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))

#  Update Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))

#  Delete Artist
#  ----------------------------------------------------------------



#  Read Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    shows = db.session.query(Showtime, Show, Artist, Venue)\
        .filter(Showtime.show_id == Show.id, Show.artist_id == Artist.id, Show.venue_id == Venue.id).all()
    return render_template('pages/shows.html', shows=shows)

#  Create Shows
#  ----------------------------------------------------------------

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            artist_id = form.artist_id.data
            venue_id = form.venue_id.data
            show_time = form.start_time.data

            # if (artist_id, venue_id) is a new show, insert in shows - then get show.id
            show_string = str(venue_id) + ", " + str(artist_id)
            shows_dict = build_shows_dict()

            if show_string not in shows_dict:
                new_show = Show(venue_id=venue_id, artist_id=artist_id)
                db.session.add(new_show)

            shows_dict = build_shows_dict()
            show_id = shows_dict[show_string]

            # if (show_id, show_time) is a new show_time, insert in showtimes
            showtime_string = str(show_id) + ", " + datetime.strftime(show_time, format="%Y-%m-%d %H:%M:%S")
            showtimes_dict = build_showtimes_dict()

            if showtime_string not in showtimes_dict:
                new_showtime = Showtime(show_id=show_id, show_time=show_time)
                db.session.add(new_showtime)

            # commit changes to db
            db.session.commit()
            flash('Show was successfully listed!')

        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
            flash('An error occurred. Show could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

        finally:
            db.session.close()

    else:
        message = []
        for field, errors in form.errors.items():
            message.append(field + ': (' + '|'.join(errors) + ')')
        flash('The Show data is not valid. Please try again!')

    return render_template('pages/home.html')

    # on successful db insert, flash success
    #



#  Miscellaneous
#  ----------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
