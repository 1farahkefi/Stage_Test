import os
import subprocess
import time
import pyautogui
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

@given('la commande get_lb_info.py est exécutée')
def step_run_command(context):
    try:
        subprocess.run(["python", "Stage/get_lb_info.py"])

        print("Commande exécutée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {e}")


@given("un fichier texte est généré pour le scan douchette")
def step_generate_txt_for_scan(context):
    fichier_txt = "scan_douchette.txt"

    # Créer le fichier texte avec l'instruction
    with open(fichier_txt, "w", encoding="utf-8") as f:
        f.write("Veuillez scanner le numéro de série et l'adresse MAC :\n")

    print("Fichier texte créé : scan_douchette.txt")
    print("En attente que l'utilisateur ajoute les données dans le fichier...")

    # Essayer d'ouvrir Notepad (si environnement Windows)
    try:
        subprocess.Popen(["notepad.exe", fichier_txt])
        print("Fichier texte ouvert dans Notepad. En attente du scan...")
    except Exception as e:
        print(f"[ERREUR] Impossible d'ouvrir Notepad : {e}")
        return

    lignes = []
    start_time = time.time()
    timeout = 20  # Temps d'attente maximum pour scanner les données

    # Boucle d'attente pour récupérer les données du fichier
    while True:
        if os.path.exists(fichier_txt):
            with open(fichier_txt, "r", encoding="utf-8") as f:
                lignes = [l.strip() for l in f.readlines() if l.strip() and not l.lower().startswith("veuillez")]

        if len(lignes) >= 2:  # Vérification de l'existence des deux lignes de données (numéro de série et adresse MAC)
            print("Données scannées détectées dans le fichier.")
            break

        if time.time() - start_time > timeout:
            print("Temps d'attente écoulé sans détection des données.")
            break

        time.sleep(1)

    # Sauvegarder les données dans le contexte
    context.numero_serie = lignes[0] if len(lignes) > 0 else ""
    context.adresse_mac = lignes[1] if len(lignes) > 1 else ""

    print(f"Numéro de série : {context.numero_serie}")
    print(f"Adresse MAC : {context.adresse_mac}")

    # Si nécessaire, fermer Notepad après l'ajout des données
    pyautogui.hotkey("ctrl", "s")
    print("Données enregistrées avec Ctrl+S.")
    subprocess.run(["taskkill", "/f", "/im", "notepad.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Notepad fermé automatiquement.")

    # Après traitement du fichier, vous pouvez ouvrir la page du modem
    context.driver.get("http://192.168.1.1/")  # Ou l'URL appropriée
    print("Page du modem ouverte à l'URL http://192.168.1.1/")

@given('le fichier "credentials.txt" contient le mot de passe administrateur')
def step_read_credentials(context):
    with open("credentials.txt", "r", encoding="utf-8") as f:
        context.password = f.readline().strip()

@given("la page d'accueil du modem est ouverte à l'adresse \"http://192.168.1.1/\"")
def step_open_homepage(context):
    context.driver.get("http://192.168.1.1/")
    time.sleep(3)

@when('l\'utilisateur entre le mot de passe dans le champ "password" si la première page est disponible')
def step_enter_password_if_available(context):
    try:
        WebDriverWait(context.driver, 3).until(EC.presence_of_element_located((By.ID, 'changepwd_password')))
        print("Première page détectée, remplissage du formulaire...")
        context.driver.find_element(By.ID, 'changepwd_password').send_keys(context.password)
        context.driver.find_element(By.ID, 'changepwd_confirmpassword').send_keys(context.password)
        context.driver.find_element(By.ID, 'changepwd_save').send_keys(Keys.RETURN)
        time.sleep(10)
        context.driver.find_element(By.ID, 'confirm_change').send_keys(Keys.RETURN)
        time.sleep(1)
    except Exception:
        print("Première page non détectée, tentative sur la deuxième page...")

    context.driver.find_element(By.XPATH, '//div[@class="sah_dialog_body_password"]/input[@name="password"]').send_keys(context.password)
    context.driver.find_element(By.XPATH, '//div[@class="sah_dialog_body_password"]/input[@name="password"]').send_keys(Keys.RETURN)
    time.sleep(2)

@when("valide la connexion")
def step_submit_password(context):
    try:
        WebDriverWait(context.driver, 5).until(EC.presence_of_element_located((By.ID, 'confirm_change')))
        context.driver.find_element(By.ID, 'confirm_change').send_keys(Keys.RETURN)
        time.sleep(5)
    except Exception:
        print("Le bouton de confirmation n'a pas été trouvé.")

@then("la page d'accueil s'affiche après authentification")
def step_check_connected(context):
    assert "192.168.1.1" in context.driver.current_url
