@app.route("/add/building", methods=["GET", "POST"])
def add_building():
    form = BuildingForm()

    form.race_id.choices = [(race.id, race.name) for race in Race.query.all()]

    form.name.choices = [(building.id, building.name) for building in Building.query.all()]

    if form.validate_on_submit():
        race = db.session.get(Race, form.race_id.data)
        building = db.session.get(Building, form.name.data)

        icon = form.icon.data

        if icon and icon.filename:
            icon_name = secure_filename(icon.filename)
            icon_name = f"{uuid.uuid4()}_{icon_name}"

            upload_folder = os.path.join(
                app.config["UPLOAD_FOLDER"], str(race.name), "buildings"
            )

            os.makedirs(upload_folder, exist_ok=True)
            icon.save(os.path.join(upload_folder, icon_name))

            building.icon = f"images/{race.name}/vehicles/{icon_name}"

        building.race_id = race.id

        db.session.commit()

        return redirect(url_for("add"))

    return render_template("add_building.html", form=form)

@app.route("/add/vehicle", methods=["GET", "POST"])
def add_vehicle():
    form = VehicleForm()

    form.race_id.choices = [
        (race.id, race.name) for race in Race.query.all()
    ]

    form.name.choices = [
        (vehicle.id, vehicle.name) for vehicle in Vehicle.query.all()
    ]

    if form.validate_on_submit():
        race = db.session.get(Race, form.race_id.data)
        vehicle = db.session.get(Vehicle, form.name.data)

        icon = form.icon.data

        if icon and icon.filename:
            icon_name = secure_filename(icon.filename)
            icon_name = f"{uuid.uuid4()}_{icon_name}"

            upload_folder = os.path.join(
                app.config["UPLOAD_FOLDER"],
                str(race.name),
                "vehicles"
            )

            os.makedirs(upload_folder, exist_ok=True)
            icon.save(os.path.join(upload_folder, icon_name))

            vehicle.icon = f"images/{race.name}/vehicles/{icon_name}"

        vehicle.race_id = race.id

        db.session.commit()

        return redirect(url_for("add"))

    return render_template("add_building.html", form=form)