import configparser
import os
import time
import psycopg2
import webbrowser
from behave import given, when, then
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


# Fonction pour enregistrer le rapport dans la base de données
def enregistrer_nom_rapport(nom_fichier_html, contenu_html, date_rapport):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            host="aws-0-eu-central-1.pooler.supabase.com",
            port=6543,
            database="postgres",
            user="postgres.ckbimfasdfzgiduhonty",
            password="SagemCom01%"
        )
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rapports (
                id SERIAL PRIMARY KEY,
                nom_fichier_html VARCHAR(255),
                contenu_html BYTEA,
                date_rapport TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modele VARCHAR(100) DEFAULT 'inconnu'
            )
        """)

        # Extraction du modèle depuis le nom du fichier HTML
        modele = "inconnu"
        try:
            base_name = os.path.basename(nom_fichier_html)
            parts = base_name.replace(".html", "").split("_")
            if len(parts) >= 2:
                modele = parts[1]
        except Exception as e:
            print(f"Erreur lors de l'extraction du modèle : {e}")

        # Insertion dans la table rapports
        cursor.execute(
            """
            INSERT INTO rapports (nom_fichier_html, contenu_html, date_rapport, modele)
            VALUES (%s, %s, %s, %s)
            """,
            (nom_fichier_html, psycopg2.Binary(contenu_html), date_rapport, modele)
        )

        # Commit pour enregistrer les changements
        conn.commit()
        print(f" Rapport '{nom_fichier_html}' enregistré dans Supabase avec modèle = '{modele}'")

    except psycopg2.Error as err:
        print(f"Erreur PostgreSQL : {err}")
    finally:
        # Fermeture de la connexion et du curseur
        if conn:
            cursor.close()
            conn.close()

# Étape pour charger les fichiers INI et récupérer les données depuis la base de données
@given('les fichiers INI "TABLE_DATA.ini" est chargé et le fichier correspondant est récupéré depuis la base de données')
def step_load_ini_files(context):
    context.file1_path = "TABLE_DATA.ini"
    context.config1 = configparser.ConfigParser()
    context.config1.read(context.file1_path, encoding="utf-8")

    modele = context.config1.get("General", "modèle", fallback="modele_inconnu").replace(" ", "_")
    nom_fichier_bdd = f"Data_{modele}.ini"

    try:
        conn = psycopg2.connect(
            host="aws-0-eu-central-1.pooler.supabase.com",
            port=6543,
            database="postgres",
            user="postgres.ckbimfasdfzgiduhonty",
            password="SagemCom01%"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT contenu FROM fichier__ini WHERE nom_fichier = %s", (nom_fichier_bdd,))
        result = cursor.fetchone()
        if result:
            ini_content = bytes(result[0]).decode("utf-8")
            context.config2 = configparser.ConfigParser()
            context.config2.read_string(ini_content)
            context.file2_path = nom_fichier_bdd
        else:
            raise FileNotFoundError(f"Le fichier '{nom_fichier_bdd}' n'a pas été trouvé dans la base de données.")
    except psycopg2.Error as err:
        print(f" Erreur MySQL : {err}")
        raise
    finally:
        cursor.close()
        conn.close()


@when('les sections et clés sont comparées entre les deux fichiers')
def step_compare_ini_files(context):
    html_rows = ""

    # Boucler sur les sections communes aux deux fichiers
    for section in context.config1.sections():
        if context.config2.has_section(section):
            keys1 = set(context.config1.options(section))
            keys2 = set(context.config2.options(section))
            common_keys = keys1 & keys2

            for key in sorted(common_keys):
                value1 = context.config1.get(section, key, fallback="Non trouvé")
                value2 = context.config2.get(section, key, fallback="Non trouvé")

                if value1 != value2:
                    status = "Échec"
                    row_class = "error"
                else:
                    status = "Succès"
                    row_class = "success"

                html_rows += f"""
                    <tr class='{row_class}'>
                        <td>{section}</td>
                        <td>{key}</td>
                        <td>{value1}</td>
                        <td>{value2}</td>
                        <td>{status}</td>
                    </tr>
                    """

    context.html_rows = html_rows

@then('le rapport HTML est généré')
def step_generate_html_only(context):
    config = context.config1
    fabricant = config.get("General", "fabricant", fallback="Inconnu")
    modele = config.get("General", "modèle", fallback="Inconnu")
    numero_serie = config.get("General", "numéro de série", fallback="Inconnu")
    mac = config.get("General", "adresse mac", fallback="Inconnu")

    # Créer dossier dernier_rapport si pas existe
    dossier_rapport = "dernier_rapport"
    if not os.path.exists(dossier_rapport):
        os.makedirs(dossier_rapport)

    nom_fichier = f"rapport_{modele}_{numero_serie}.html".replace(" ", "_")
    chemin_fichier = os.path.join(nom_fichier)
    context.nom_fichier_html = chemin_fichier

    # Comparaison douchette
    sn_douchette, mac_douchette = "Non détecté", "Non détecté"
    if os.path.exists("scan_douchette.txt"):
        with open("scan_douchette.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("Veuillez")]
            if len(lines) >= 2:
                sn_douchette, mac_douchette = lines[0], lines[1]

    comparaison_html = f"""
    <h3>Comparaison avec données scannées</h3>
    <table>
        <tr><th>Champ</th><th>Donnée scannée</th><th>Donnée extraite</th><th>Statut</th></tr>
        <tr class="{'success' if sn_douchette == numero_serie else 'error'}">
            <td>Numéro de série</td><td>{sn_douchette}</td><td>{numero_serie}</td><td>{'Succès' if sn_douchette == numero_serie else 'Échec'}</td>
        </tr>
        <tr class="{'success' if mac_douchette == mac else 'error'}">
            <td>Adresse MAC</td><td>{mac_douchette}</td><td>{mac}</td><td>{'Succès' if mac_douchette == mac else 'Échec'}</td>
        </tr> 
    </table>
    """

    info_html = f"""
    <div style="display: flex; justify-content: space-between; margin-top: 18px;">
        <div style="margin-top: 58px;">
            <p><strong>Fabricant :</strong> {fabricant}</p>
            <p><strong>Modèle :</strong> {modele}</p>
            <p><strong>Numéro de série :</strong> {numero_serie}</p>
            <p><strong>Adresse MAC :</strong> {mac}</p>
        </div>
        <div><img id="modemImage" src="LIVEBOX7.png" alt="Image du modem" style="max-width: 180px;"></div>
    </div>
    <hr style="margin: 30px 0;">
    """

    html_content = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><title>Rapport</title>
    <style>body{{font-family:Arial;padding:40px;}}table{{width:100%;border-collapse:collapse;margin-top:20px;}}
    th,td{{border:1px solid #ccc;padding:12px;text-align:left;}}th{{background-color:#2c3e50;color:white;}}
    .success{{background-color:#e6f9ec;color:#2e7d32;}}.error{{background-color:#fdecea;color:#c62828;}}</style></head>
    <body><h2 style="text-align:center;">Rapport - {modele}</h2>{info_html}{comparaison_html}
    <h3>Comparaison complète INI</h3><table><thead>
    <tr><th>Section</th><th>Clé</th><th>Valeur dans {context.file1_path}</th><th>Valeur dans {context.file2_path}</th><th>Statut</th></tr>
    </thead><tbody>{context.html_rows}
    <script>
  const img = document.getElementById('modemImage');
  img.onerror = function() {{
    this.onerror = null;
    this.src = "/static/images/LIVEBOX7.png";
  }};
</script>
</body></html>

</tbody></table></body></html>"""

    with open(chemin_fichier, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Sauvegarde en base
    date_creation = datetime.utcnow()
    enregistrer_nom_rapport(chemin_fichier, html_content.encode("utf-8"), date_creation)

    # Sauvegarde du chemin temporaire
    with open("dernier_rapport.txt", "w", encoding="utf-8") as f:
        f.write(chemin_fichier)

    print(f"Rapport HTML généré : {chemin_fichier}")

    # Suppression du fichier TABLE_DATA.ini après génération du rapport
    try:
        if os.path.exists(context.file1_path):
            os.remove(context.file1_path)
            print(f" Fichier '{context.file1_path}' supprimé après génération du rapport.")
        else:
            print(f" Le fichier '{context.file1_path}' n'existe pas ou a déjà été supprimé.")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier '{context.file1_path}': {e}")

@when('l\'utilisateur clique sur l\'icône "Assistance et dépannage"')
def step_click_icon_assistance(context):
    bouton = context.driver.find_element(By.XPATH, '//div[contains(@class, "iconbar-button") and contains(@class, "icon-support")]')
    ActionChains(context.driver).click(bouton).perform()
    time.sleep(2)

@when('l\'utilisateur clique sur "Réinitialiser"')
def step_click_reset(context):
    reset = context.driver.find_element(By.XPATH, "//div[@id='systemReset']//div[@class='widget']")
    ActionChains(context.driver).move_to_element(reset).click().perform()
    time.sleep(2)

@when("sélectionner l'iframe contenant le bouton de réinitialisation")
def step_switch_to_iframe(context):
    context.driver.switch_to.frame("iframeapp")

@when('l\'utilisateur clique sur le bouton "Réinitialiser"')
def step_click_reset_button(context):
    reset = context.driver.find_element(By.ID, "reset")
    ActionChains(context.driver).move_to_element(reset).click().perform()
    time.sleep(2)

@then('l\'utilisateur clique sur le bouton "Confirmer"')
def step_click_confirm_button(context):
    confirm = context.driver.find_element(By.ID, "popup_confirm_reinit_submit")
    ActionChains(context.driver).move_to_element(confirm).click().perform()
    time.sleep(10)

# --- Affichage puis suppression automatique du fichier ---
@then('le rapport HTML est affiché dans le navigateur')
def step_open_html_report(context):
    if not os.path.exists("dernier_rapport.txt"):
        raise Exception("Le rapport HTML n'a pas été généré.")

    with open("dernier_rapport.txt", "r", encoding="utf-8") as f:
        chemin_fichier = f.read().strip()

    if not os.path.exists(chemin_fichier):
        raise Exception(f"Le fichier '{chemin_fichier}' n'existe pas.")

    # Ouvre dans navigateur
    webbrowser.open(f"file://{os.path.abspath(chemin_fichier)}")
    time.sleep(3)  # Attendre que l'affichage soit fait

    # Supprimer le fichier rapport + dernier_rapport.txt
    os.remove(chemin_fichier)
    print(f"Fichier {chemin_fichier} supprimé.")
    os.remove("dernier_rapport.txt")
    print("Fichier 'dernier_rapport.txt' supprimé.")