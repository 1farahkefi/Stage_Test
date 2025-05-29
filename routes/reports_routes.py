from flask import Blueprint, render_template, redirect, url_for, Response, send_file, request, jsonify
from flask_login import login_required, current_user
from models import db, Rapport
import os
from io import BytesIO
from collections import defaultdict


reports_bp = Blueprint('reports', __name__, url_prefix='/admin/reports')


@reports_bp.route('/')
@login_required
def afficher_rapports():


    rapports = Rapport.query.order_by(Rapport.date_rapport.desc()).all()
    rapports_par_modele = defaultdict(list)

    for r in rapports:
        rapports_par_modele[r.modele].append(r)

    nombre_par_modele = {modele: len(liste) for modele, liste in rapports_par_modele.items()}
    return render_template('report_list.html',
                           rapports_par_modele=rapports_par_modele,
                           nombre_par_modele=nombre_par_modele)

@reports_bp.route('/supprimer/<int:id>')
@login_required
def supprimer_rapport(id):
    if current_user.role != "admin":
        return render_template("403.html"), 403
    rapport = Rapport.query.get_or_404(id)
    db.session.delete(rapport)
    db.session.commit()
    return redirect(url_for('reports.afficher_rapports'))

@reports_bp.route('/show/<filename>')
@login_required
def show_report_html(filename):
    filepath = os.path.join("static", "rapports_html", filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    return "Fichier non trouvé", 404


@reports_bp.route('/view/<int:rapport_id>')
@login_required
def afficher_rapport(rapport_id):
    if current_user.role != "admin":
        return "Accès refusé", 403

    rapport = Rapport.query.get_or_404(rapport_id)
    html_template = rapport.contenu_html.decode('utf-8')

    # Par exemple, ici tu veux afficher l'image "F@st5696b"
    photo = Photo.query.filter_by(nom='F@st5696b').first()

    if photo and photo.image_data:
        # Encoder en base64 le binaire stocké en base
        image_base64 = base64.b64encode(photo.image_data).decode('utf-8')
        # Créer la data URI (avec le bon type MIME, ici png)
        image_url = f"data:image/png;base64,{image_base64}"
    else:
        image_url = ""  # Ou url d'une image par défaut

    # Rendre le template HTML avec l'image inline
    rendered_html = render_template_string(html_template, image_url=image_url)

    return rendered_html

@reports_bp.route('/html/<int:rapport_id>')
@login_required
def download_html(rapport_id):
    if current_user.role != "admin":
        return render_template("403.html"), 403
    rapport = Rapport.query.get_or_404(rapport_id)
    filename = rapport.nom_fichier_html
    file_stream = BytesIO(rapport.contenu_html)
    return send_file(file_stream, mimetype="text/html", download_name=filename, as_attachment=False)









