from . import db

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