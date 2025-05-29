import os
import platform
import subprocess
from flask import Blueprint, request, jsonify, Response, redirect, url_for, render_template
from flask import current_app
from flask import flash
from flask_login import login_required, current_user
from io import BytesIO

from models import db, Fichier_Ini

fichierIni_bp = Blueprint('fichierIni', __name__)

# PAGE PRINCIPALE
@fichierIni_bp.route('/fichierIni', methods=['GET'])
@login_required
def afficher_fichiers():
    if current_user.role != "admin":
        return render_template("403.html"), 403

    fichiers = Fichier_Ini.query.all()
    return render_template("fichierIni.html", fichiers=fichiers)


# CREATE (Upload)
@fichierIni_bp.route('/fichiers', methods=['POST'])
@login_required
def ajouter_fichier():
    if current_user.role != "admin":
        return render_template("403.html"), 403

    fichier = request.files.get('fichier_ini')
    if not fichier:
        return "Aucun fichier fourni", 400

    nouveau = Fichier_Ini(
        nom_fichier=fichier.filename,
        contenu=fichier.read()
    )
    db.session.add(nouveau)
    db.session.commit()

    return redirect(url_for('fichierIni.afficher_fichiers'))


# DOWNLOAD
@fichierIni_bp.route('/fichiers/download/<int:id>', methods=['GET'])
@login_required
def telecharger_fichier(id):
    if current_user.role != "admin":
        return render_template("403.html"), 403

    fichier = Fichier_Ini.query.get_or_404(id)
    return Response(
        fichier.contenu,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename={fichier.nom_fichier}"}
    )


# DELETE
@fichierIni_bp.route('/fichiers/delete/<int:id>', methods=['POST'])
@login_required
def supprimer_fichier(id):
    if current_user.role != "admin":
        return render_template("403.html"), 403

    fichier = Fichier_Ini.query.get_or_404(id)
    db.session.delete(fichier)
    db.session.commit()

    return redirect(url_for('fichierIni.afficher_fichiers'))


@fichierIni_bp.route('/voir/<int:id>')
def voir_fichier(id):
    fichier = Fichier_Ini.query.get_or_404(id)

    # Si contenu est stocké en bytes, on le décode en UTF-8
    if isinstance(fichier.contenu, bytes):
        contenu = fichier.contenu.decode('utf-8')
    else:
        contenu = fichier.contenu

    return render_template('voir_fichier.html', fichier=fichier, contenu=contenu)



@fichierIni_bp.route('/voir/<int:id>', methods=['POST'])
def update_fichier(id):
    fichier = Fichier_Ini.query.get_or_404(id)
    nouveau_contenu = request.form.get('contenu_fichier')  # Assure-toi que le name du <textarea> est correct

    if nouveau_contenu:
        fichier.contenu = nouveau_contenu.encode('utf-8')  # encode en bytes
        db.session.commit()
        flash("Fichier mis à jour avec succès !", "success")
    else:
        flash("Le contenu du fichier ne peut pas être vide.", "warning")

    return redirect(url_for('fichierIni.afficher_fichiers'))