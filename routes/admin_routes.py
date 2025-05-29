from collections import Counter, defaultdict
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from models import db, User, Rapport, Modele
from flask_bcrypt import Bcrypt
from collections import Counter, defaultdict


admin_bp = Blueprint('admin', __name__)
bcrypt = Bcrypt()

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return render_template("403.html"), 403


    reports = Rapport.query.all()
    users = User.query.all()
    modeles = Modele.query.all()


    # Rapports par modèle
    rapports_par_modele = defaultdict(list)
    for r in reports:
        rapports_par_modele[r.modele].append(r)
    nombre_par_modele = {modele: len(rs) for modele, rs in rapports_par_modele.items()}

    # Rapports par mois
    rapports_par_mois = defaultdict(int)
    for r in reports:
        if r.date_rapport:  # Assure-toi que r.date est un objet datetime
            mois = r.date_rapport.strftime('%Y-%m')  # e.g., "2025-05"
            rapports_par_mois[mois] += 1

    # Tri par date
    rapports_par_mois = dict(sorted(rapports_par_mois.items()))

    return render_template(
        "dashboard.html",
        users=users,
        reports=reports,
        nombre_par_modele=nombre_par_modele,
        rapports_par_mois=rapports_par_mois,
        modeles=modeles
    )


@admin_bp.route('/dashboard_testeur')
@login_required
def dashboardTesteur():
    reports = Rapport.query.all()
    users = User.query.all()
    modeles = Modele.query.all()

    # Rapports par modèle
    rapports_par_modele = defaultdict(list)
    for r in reports:
        rapports_par_modele[r.modele].append(r)
    nombre_par_modele = {modele: len(rs) for modele, rs in rapports_par_modele.items()}

    # Rapports par mois
    rapports_par_mois = defaultdict(int)
    for r in reports:
        if r.date_rapport:  # Assure-toi que r.date est un objet datetime
            mois = r.date_rapport.strftime('%Y-%m')  # e.g., "2025-05"
            rapports_par_mois[mois] += 1

    # Tri par date
    rapports_par_mois = dict(sorted(rapports_par_mois.items()))

    return render_template(
        "dashboard_testeur.html",
        users=users,
        reports=reports,
        nombre_par_modele=nombre_par_modele,
        rapports_par_mois=rapports_par_mois,
        modeles=modeles
    )

@admin_bp.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return render_template("403.html"), 403
    users = User.query.all()
    return render_template("user_list.html", users=users)

@admin_bp.route("/admin/add", methods=["GET", "POST"])
@login_required
def add_user():
    if current_user.role != "admin":
        return render_template("403.html"), 403
    if request.method == "POST":
        email = request.form["email"]
        matricule = request.form["matricule"]
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        role = request.form["role"]
        db.session.add(User(email=email, matricule=matricule, username=username, password=password, role=role))
        db.session.commit()
        return redirect("/admin/list_user")

@admin_bp.route("/admin/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if current_user.role != "admin":
        return render_template("403.html"), 403
    user = User.query.get(user_id)
    if request.method == "POST":
        user.email = request.form["email"]
        user.matricule = request.form["matricule"]
        user.username = request.form["username"]
        if request.form["password"]:
            user.password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        user.role = request.form["role"]
        db.session.commit()
        return redirect("/admin/list_user")

@admin_bp.route("/admin/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    if current_user.role != "admin":
        return render_template("403.html"), 403
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/admin/list_user")
