import subprocess
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
import time  # Pour ajouter un délai si nécessaire

launch_bp = Blueprint('launch', __name__, url_prefix="/launch")

@launch_bp.route('/livebox7', methods=["POST"])
@login_required
def run_livebox7():
    return _run_behave_test("Livebox7")

@launch_bp.route('/ederson', methods=["POST"])
@login_required
def run_ederson():
    return _run_behave_test("Ederson")

def _run_behave_test(modem_folder):
    try:
        print(f"Lancement du test {modem_folder}...")

        # Lancement de Behave via subprocess
        process = subprocess.Popen(
            ['behave', '--no-capture'],  # Commande Behave avec l'option --no-capture
            cwd=f"tests/{modem_folder}",  # Le répertoire de test spécifique
            stdout=subprocess.PIPE,  # Capture la sortie standard
            stderr=subprocess.PIPE,  # Capture les erreurs
            text=True  # Utilisation de texte pour la sortie
        )

        # Capture la sortie et les erreurs
        stdout, stderr = process.communicate()

        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")

        # Vérification du retour du processus
        if process.returncode == 0:
            flash(f"Test {modem_folder} lancé avec succès", "success")
        else:
            flash(f"Erreur lors du test {modem_folder}", "danger")

        return redirect(url_for('test.tester_dashboard'))

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Behave : {e}")
        flash(f"Erreur lors du test {modem_folder}: {e}", "danger")
        return redirect(url_for('test.tester_dashboard'))

    except OSError as e:
        print(f"Erreur système : {e}")
        flash(f"Erreur système lors du test {modem_folder}: {e}", "danger")
        return redirect(url_for('test.tester_dashboard'))

    except Exception as e:
        print(f"Erreur inattendue : {e}")
        flash(f"Erreur inattendue lors du test {modem_folder}: {e}", "danger")
        return redirect(url_for('test.tester_dashboard'))