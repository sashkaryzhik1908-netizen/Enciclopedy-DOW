from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Race(db.Model):
    __tablename__ = "races"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    units = db.relationship("Units", back_populates="race")
    buildings = db.relationship("Building", back_populates="race")
    vehicles = db.relationship("Vehicle", back_populates="race")
    icon = db.Column(db.String)
    content = db.Column(db.Text)
    build_icon = db.Column(db.String)
    vechicle_icon = db.Column(db.String)

    def __repr__(self):
        return self.name


class Units(db.Model):
    __tablename__ = "units"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"))
    race = db.relationship("Race", back_populates="units")
    icon = db.Column(db.String)

    def __repr__(self):
        return self.name


class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"))
    race = db.relationship("Race", back_populates="buildings")

    def __repr__(self):
        return self.name


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"))
    race = db.relationship("Race", back_populates="vehicles")

    def __repr__(self):
        return self.name


@app.route("/")
def index():
    races = Race.query.all()
    units = Units.query.all()
    buildings = Building.query.all()
    vehicles = Vehicle.query.all()
    return render_template(
        "index.html",
        title="Главная",
        current=None,
        races=races,
        units=units,
        buildings=buildings,
        vehicles=vehicles,
    )


@app.route("/races/<int:race_id>")
def race(race_id):
    current = Race.query.get_or_404(race_id)
    races = Race.query.all()
    units = Units.query.filter_by(race_id=race_id).all()
    return render_template(
        "races_list.html",
        title=current.name,
        current=current,
        races=races,
        units=units,
    )


@app.route("/races/<int:race_id>/category")
def category(race_id):
    races = Race.query.all()
    race = Race.query.get_or_404(race_id)
    return render_template("category.html", race=race, races=races)


@app.route("/races/<int:race_id>/units/<int:unit_id>")
def units_detail(race_id, unit_id):
    races = Race.query.all()
    race = Race.query.get_or_404(race_id)
    unit = Units.query.filter_by(id=unit_id, race_id=race_id).first_or_404()
    return render_template("unit.html", unit=unit, race=race, current=race, races=races)


if __name__ == "__main__":
    app.run(debug=True)
