from flask import render_template, redirect, url_for
from . import app, db
from .models import Race, Units, Building, Vehicle
from .forms import RaceForm


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
    current = Race.query.get_or_404(race_id)
    return render_template("category.html",current=current, races=races)


@app.route("/races/<int:race_id>/units/<int:unit_id>")
def units_detail(race_id, unit_id):
    races = Race.query.all()
    race = Race.query.get_or_404(race_id)
    unit = Units.query.filter_by(id=unit_id, race_id=race_id).first_or_404()
    return render_template("unit.html", unit=unit, race=race, current=race, races=races)

@app.route('/add', methods=['GET', 'POST'])
def edit():
    form = RaceForm()
    if form.validate_on_submit():
        race = Race.query.filter_by(name=form.name.data).first()

        if race:
            race.build_icon = form.build_icon.data
            race.vechicle_icon = form.vehicle_icon.data

            db.session.commit()

        return redirect(url_for("index"))

    return render_template("edit.html", form=form)

