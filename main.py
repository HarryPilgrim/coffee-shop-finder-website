from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    map_url = StringField('map (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Image (URL)', validators=[DataRequired(), URL()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    has_toilet = BooleanField('Has a toilet?')
    has_wifi = BooleanField('Has Wi-Fi?')
    has_sockets = BooleanField('Has sockets to use?')
    can_take_calls = BooleanField('Can you take calls')
    price = StringField('Price of a coffee', validators=[DataRequired()])

    submit = SubmitField('Submit')


class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

# with app.app_context():
#     db.create_all()

@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    #dict_cafes = [cafe.to_dict() for cafe in all_cafes]
    print(len(all_cafes))
    return render_template("index.html", cafes=all_cafes)

@app.route("/one-cafe/<int:index>")
def one_cafe(index):
    chosen_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == index)).scalar()
    return render_template("one_cafe.html", cafe=chosen_cafe)

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/add-cafe", methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # name = form.name.data
        # location = form.location.data
        # map_url = form.map_url.data
        # img_url = form.img_url.data
        # seats = form.seats.data
        # has_toilet = form.has_toilet.data
        # has_wifi = form.has_wifi.data
        # has_sockets = form.has_sockets.data
        # can_take_calls = form.can_take_calls.data
        # price = form.price.data
        # cafe_data_all = [cafe_name, location, image_url, seats, has_toilet, has_wifi, has_sockets, has_wifi, can_take_calls, price]

        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("has_sockets")),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'), code=302)
    return render_template("add_cafe.html", form=form)









if __name__ == '__main__':
    app.run(debug=True)