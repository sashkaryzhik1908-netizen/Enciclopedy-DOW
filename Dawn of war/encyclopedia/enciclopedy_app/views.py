import os
import uuid
from werkzeug.utils import secure_filename
from flask import render_template, redirect,  url_for
from . import app, db
from .models import Race, Units, Building, Vehicle
from .forms import RaceForm, UnitForm, BuildingForm, VehicleForm


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

@app.route("/races/<int:race_id>/category")
def category(race_id):
    races = Race.query.all()
    current = Race.query.get_or_404(race_id)
    return render_template("category.html",current=current, races=races)


@app.route("/races/<int:race_id>/units")
def race(race_id):
    current = Race.query.get_or_404(race_id)
    races = Race.query.all()
    units = Units.query.filter_by(race_id=race_id).all()
    return render_template(
        "units_list.html",
        title=current.name,
        current=current,
        races=races,
        units=units,
    )

@app.route("/races/<int:race_id>/buildings")
def buildings(race_id):
    current = Race.query.get_or_404(race_id)
    races = Race.query.all()
    units = Building.query.filter_by(race_id=race_id).all()
    return render_template(
        "buildings_list.html",
        title=current.name,
        current=current,
        races=races,
        units=units,
    )


@app.route("/races/<int:race_id>/vehicle")
def vehicle(race_id):
    current = Race.query.get_or_404(race_id)
    races = Race.query.all()
    units = Vehicle.query.filter_by(race_id=race_id).all()
    return render_template(
        "vehicle_list.html",
        title=current.name,
        current=current,
        races=races,
        units=units,
    )


@app.route("/races/<int:race_id>/units/<int:object_id>")
def units_detail(race_id, object_id):
    races = Race.query.all()
    race = Race.query.get_or_404(race_id)
    unit = Units.query.filter_by(id=object_id, race_id=race_id).first_or_404()
    return render_template("unit.html", unit=unit, race=race, current=race, races=races)

@app.route("/races/<int:race_id>/buildings/<int:object_id>")
def buildings_detail(race_id, object_id):
    races = Race.query.all()
    race = Race.query.get_or_404(race_id)
    building = Building.query.filter_by(id=object_id, race_id=race_id).first_or_404()
    return render_template("buildings.html", building=building, race=race, current=race, races=races)


@app.route("/races/<int:race_id>/vehicle/<int:object_id>")
def vehicle_detail(race_id, object_id):
    races = Race.query.all()
    race = Race.query.get_or_404(race_id)
    vehicle = Vehicle.query.filter_by(id=object_id, race_id=race_id).first_or_404()
    return render_template("vehicle.html", vehicle=vehicle, race=race, current=race, races=races)


@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/add/img", methods=["GET", "POST"])
def edit():
    form = RaceForm()
    form.name.choices = [(race.id, race.name) for race in Race.query.all()]
    if form.validate_on_submit():
        race = db.session.get(Race, form.name.data)

        build_icon = form.build_icon.data
        build_name = secure_filename(build_icon.filename)
        build_name = str(uuid.uuid4())+ '_' + build_name

        vehicle_icon = form.vehicle_icon.data
        vehicle_name = secure_filename(vehicle_icon.filename)
        vehicle_name = str(uuid.uuid4())+ '_' + vehicle_name

        build_icon.save(os.path.join(
            app.config['UPLOAD_FOLDER'], 'races', 'build', build_name
        ))

        vehicle_icon.save(
            os.path.join(app.config["UPLOAD_FOLDER"], "races", "vehicle", vehicle_name)
        )

        race.build_icon = f'images/races/build/{build_name}'
        race.vechicle_icon = f'images/races/vehicle/{vehicle_name}'

        db.session.commit()

        return redirect(url_for("add"))

    return render_template("edit.html", form=form)

@app.route("/add/unit", methods=["GET", "POST"])
def add_unit():
    form = UnitForm()

    form.race_id.choices = [(race.id, race.name) for race in Race.query.all()]
    if form.validate_on_submit():
        race = db.session.get(Race, form.race_id.data)

        icon = form.icon.data
        icon_name = secure_filename(icon.filename)
        icon_name = f"{uuid.uuid4()}_{icon_name}"

        upload_folder = os.path.join(
            app.config["UPLOAD_FOLDER"],
            str(race.name),
            "units"
        )
        os.makedirs(upload_folder, exist_ok=True)
        icon.save(os.path.join(upload_folder, icon_name))
        unit = Units(
            name=form.name.data,
            race_id=race.id,
            icon=f"images/{race.name}/units/{icon_name}"
        )

        db.session.add(unit)
        db.session.commit()

        return redirect(url_for("add"))

    return render_template("add_unit.html", form=form)


@app.route("/add/building", methods=["GET", "POST"])
def add_building():
    form = BuildingForm()

    form.race_id.choices = [(race.id, race.name) for race in Race.query.all()]
    if form.validate_on_submit():
        race = db.session.get(Race, form.race_id.data)
        name = form.name.data
        icon = form.icon.data
        icon_name = secure_filename(icon.filename)
        icon_name = f"{uuid.uuid4()}_{icon_name}"

        upload_folder = os.path.join(
            app.config["UPLOAD_FOLDER"], str(race.name), "buildings"
        )
        os.makedirs(upload_folder, exist_ok=True)
        icon.save(os.path.join(upload_folder, icon_name))
        building = Building(
            name=name,
            race_id=race.id,
            icon=f"images/{race.name}/buildings/{icon_name}",
        )

        db.session.add(building)
        db.session.commit()

        return redirect(url_for("add"))

    return render_template("add_building.html", form=form)


@app.route("/add/vehicle", methods=["GET", "POST"])
def add_vehicle():
    form = VehicleForm()

    form.race_id.choices = [(race.id, race.name) for race in Race.query.all()]
    if form.validate_on_submit():
        race = db.session.get(Race, form.race_id.data)
        name = form.name.data
        icon = form.icon.data
        icon_name = secure_filename(icon.filename)
        icon_name = f"{uuid.uuid4()}_{icon_name}"

        upload_folder = os.path.join(
            app.config["UPLOAD_FOLDER"], str(race.name), "vehicle"
        )
        os.makedirs(upload_folder, exist_ok=True)
        icon.save(os.path.join(upload_folder, icon_name))
        vehicle = Vehicle(
            name=name,
            race_id=race.id,
            icon=f"images/{race.name}/vehicle/{icon_name}",
        )

        db.session.add(vehicle)
        db.session.commit()

        return redirect(url_for("add"))

    return render_template("add_vehicle.html", form=form)