from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email =  db.Column(db.String(150), unique=True, nullable=False)
    matricule =  db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Rapport(db.Model):
    __tablename__ = 'rapports'
    id = db.Column(db.Integer, primary_key=True)
    nom_fichier_html = db.Column(db.String(255), nullable=False)
    date_rapport = db.Column(db.DateTime, default=datetime.utcnow)
    contenu_html = db.Column(db.LargeBinary, nullable=False)
    modele = db.Column(db.String(100), nullable=False)


class Fichier_Ini(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(255), nullable=False)
    contenu = db.Column(db.LargeBinary, nullable=False)

class Modele(db.Model):
    _tablename_ = 'modele'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Modele {self.nom}>"

