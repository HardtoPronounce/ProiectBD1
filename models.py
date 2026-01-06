from database import db

class Pacient(db.Model):
    __tablename__ = 'pacienti'
    id_pacient = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)
    data_nasterii = db.Column(db.Date, nullable=False)

class Medicament(db.Model):
    __tablename__ = 'medicamente'
    id_medicament = db.Column(db.Integer, primary_key=True)
    denumire = db.Column(db.String(100), nullable=False)
    producator = db.Column(db.String(100), nullable=False)

class Reteta(db.Model):
    __tablename__ = 'retete'
    id_pacient = db.Column(db.Integer, db.ForeignKey('pacienti.id_pacient'), primary_key=True)
    id_medicament = db.Column(db.Integer, db.ForeignKey('medicamente.id_medicament'), primary_key=True)
    data_start = db.Column(db.Date, nullable=False)
    doza = db.Column(db.String(50), nullable=False)

    pacient = db.relationship('Pacient')
    medicament = db.relationship('Medicament')