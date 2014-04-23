from flask import Flask, render_template, url_for, request, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# key for wtf forms
app.config['SECRET_KEY'] = 'hard to guess string'
#db config
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql://paul:oracle@localhost/winecellar'
#db options
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#db var
db = SQLAlchemy(app)

##########
# Models #
##########


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Wine(db.Model):
    __tablename__ = 'wines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    year = db.Column(db.String(32))
    country = db.Column(db.String(64))
    vineyard = db.Column(db.String(128))
    genre = db.Column(db.String(128))

    def __repr__(self):
        return '<Wine %r>' % self.name


#########
# Forms #
#########
class wine_form(Form):
    name = StringField('Name of the wine?')
    year = StringField('Year the wine was bottled?')
    country = StringField('Country of origin?')
    vineyard = StringField('Name of the vineyard')
    genre = StringField('Type of wine?')
    submit = SubmitField('Add Wine to Cellar')


##########
# Routes #
##########
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wines', methods=['GET'])
def wine_listing():
    wines = Wine.query.all()
    return render_template('wine_listing.html', wines=wines)


@app.route('/wine/<int:id>')
def wine_id(id):
    wine = Wine.query.filter_by(id=id)
    return render_template('wine.html', wine=wine)


@app.route('/wine/add', methods=['GET', 'POST'])
def wine_add():
    if request.method == 'GET':
        form = wine_form()
        wines = Wine.query.all()
        return render_template('wine_add.html', form=form)

    if request.method == 'POST':
        w_name = request.form['name']
        w_year = request.form['year']
        w_country = request.form['country']
        w_vineyard = request.form['vineyard']
        w_genre = request.form['genre']
        new_wine = Wine(name=w_name, year=w_year, country=w_country, vineyard=w_vineyard, genre=w_genre)
        db.session.add(new_wine)
        db.session.commit()
        flash('Nice, a new bottle!')
        wines = Wine.query.all()
        return render_template('wine_listing.html', wines=wines)


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/<username>')
def user(username):
    return render_template('user.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
