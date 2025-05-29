from flask import Flask, redirect, url_for,  render_template_string
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import db, User, Rapport , Modele
from routes.auth import auth_bp
from routes.admin_routes import admin_bp
from routes.test_routes import test_bp
from routes.fichierIni_routes import fichierIni_bp
from routes.launch_routes import launch_bp
from routes.reports_routes import reports_bp
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (.env)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')

# Configuration base de données Supabase PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db.init_app(app)

# Bcrypt pour hasher les mots de passe
bcrypt = Bcrypt(app)

# Gestion des utilisateurs (connexion)
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Enregistrement des Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(test_bp)
app.register_blueprint(fichierIni_bp)
app.register_blueprint(launch_bp)
app.register_blueprint(reports_bp)


@app.route('/')
def home():
    return redirect(url_for('auth.login'))


# Affichage des rapports
@app.route('/rapport/<int:rapport_id>')
def afficher_rapport(rapport_id):
    rapport = Rapport.query.get_or_404(rapport_id)
    contenu = rapport.contenu_html.decode('utf-8')
    return render_template_string(contenu)

# Démarrage de l'application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            password_hash = bcrypt.generate_password_hash("admin123").decode("utf-8")
            admin = User(
                username="admin",
                matricule=999999,   # ➜ Valeur fictive mais obligatoire
                password=password_hash,
                role="admin",
                email="admin@sagemcom.com"  # ➜ Email valide obligatoire
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Utilisateur admin créé : admin / admin123")
        else:
            print("ℹ️ Utilisateur admin déjà existant.")
            # Ajout des modèles
            noms = ["Ederson", "Livebox"]
            for nom in noms:
                if not Modele.query.filter_by(nom=nom).first():
                    db.session.add(Modele(nom=nom))
                    print(f"✅ Modèle ajouté : {nom}")
                else:
                    print(f"ℹ️ Modèle déjà présent : {nom}")

            db.session.commit()


    app.run(host='0.0.0.0', port=5000, debug=True)
