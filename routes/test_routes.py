from flask import Blueprint, render_template, request
from flask_login import login_required
import subprocess

test_bp = Blueprint('test', __name__)

@test_bp.route("/tester", methods=["GET", "POST"])
@login_required
def tester_dashboard():
    if request.method == "POST":
        modem = request.form.get("modem")
        feature_file = f"bdd_tests/features/{modem}.feature"
        result = subprocess.run(["behave", feature_file], capture_output=True, text=True)
        return render_template("result.html", output=result.stdout)
    return render_template("tester.html")
