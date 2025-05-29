import os
import subprocess
import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from behave import given, when, then


@given("un fichier texte est généré pour le scan douchette")
def step_generate_txt_for_scan(context):
    fichier_txt = "scan_douchette.txt"

    # Créer le fichier avec l'instruction
    with open(fichier_txt, "w", encoding="utf-8") as f:
        f.write("Veuillez scanner le numéro de série et l'adresse MAC :\n")

    try:
        subprocess.Popen(["notepad.exe", fichier_txt])
        print("Fichier texte ouvert dans Notepad. En attente du scan...")
    except Exception as e:
        print(f"[ERREUR] Impossible d'ouvrir Notepad : {e}")
        return

    lignes = []
    start_time = time.time()
    timeout = 20

    while True:
        if os.path.exists(fichier_txt):
            with open(fichier_txt, "r", encoding="utf-8") as f:
                lignes = [l.strip() for l in f.readlines() if l.strip() and not l.lower().startswith("veuillez")]

        if len(lignes) == 2:
            print("→ Données scannées détectées dans le fichier.")
            break

        if time.time() - start_time > timeout:
            print("Temps d'attente écoulé sans détection suffisante.")
            break

        time.sleep(1)

    # Enregistrer et fermer Notepad
    pyautogui.hotkey("ctrl", "s")
    print("Données enregistrées avec Ctrl+S.")
    subprocess.run(["taskkill", "/f", "/im", "notepad.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Notepad fermé automatiquement.")

    # Sauvegarder dans le contexte
    context.numero_serie = lignes[0] if len(lignes) > 0 else ""
    context.adresse_mac = lignes[1] if len(lignes) > 1 else ""
    print(f"Numéro de série : {context.numero_serie}")
    print(f"Adresse MAC : {context.adresse_mac}")

    # Une fois le fichier traité, ouvrir la page du modem
    context.driver.get("http://192.168.1.254/")
    print("Page du modem ouverte à l'URL http://192.168.1.254/")


@given('le fichier "credentials.txt" contient le mot de passe')
def step_read_credentials(context):
    with open("credentials.txt", "r", encoding="utf-8") as f:
        context.password = f.readline().strip()


@given("l'utilisateur est sur la page d'installation")
def step_open_homepage(context):
# context.driver.get("http://192.168.1.254/")
 pass

@when("l'utilisateur procède à l'installation ou à la connexion")
def step_process_by_url(context):
    current_url = context.driver.current_url.lower()
    if "installation" in current_url:
        try:
            bouton = WebDriverWait(context.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[@class="btn-container btn-install"]/button[@class="cta-1"]'))
            )
            # Scrolling to the element before clicking
            context.driver.execute_script("arguments[0].scrollIntoView();", bouton)
            ActionChains(context.driver).move_to_element(bouton).click().perform()
            time.sleep(5)
        except Exception as e:
            print(f"Erreur lors du clic sur le bouton : {e}")

        try:
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='step-02 private step-02-bis']//div[2]//input[1]"))
            )
            print("Création du mot de passe...")
            champ_pwd = context.driver.find_element(By.XPATH,
                                                    "//div[@class='step-02 private step-02-bis']//div[2]//input[1]")
            champ_confirm = context.driver.find_element(By.XPATH,
                                                        "//div[@class='step-02 private step-02-bis']//div[3]//input[1]")
            bouton_valider = context.driver.find_element(By.XPATH,
                                                         "//div[@class='step-02 private step-02-bis']//button[@class='cta-1'][normalize-space(text())='Valider']")

            champ_pwd.send_keys(context.password)
            champ_confirm.send_keys(context.password)
            bouton_valider.click()

            # Passer les étapes
            skip1 = context.driver.find_element(By.XPATH, "//div[contains(text(),'Passer cette étape')]")
            ActionChains(context.driver).move_to_element(skip1).click().perform()
            skip2 = context.driver.find_element(By.XPATH, "//button[normalize-space()='Passer cette étape']")
            ActionChains(context.driver).move_to_element(skip2).click().perform()
        except Exception as e:
            print("Erreur pendant la création de mot de passe :", e)
    elif "login" in current_url:
        try:
            print("Connexion en cours...")
            champ_password = WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            champ_password.send_keys(context.password)
            bouton_connexion = context.driver.find_element(By.XPATH, "//button[normalize-space()='Connexion']")
            bouton_connexion.click()
        except Exception as second_error:
            print(f"→ Erreur pendant la connexion : {second_error}")
            assert False, f"Connexion échouée : {second_error}"
    else:
        print(f"Aucune action pour cette URL : {current_url}")
        assert False, "URL inattendue – ni installation ni login"


@then("l'installation démarre ou la page suivante s'affiche")
def step_verify_navigation(context):
    current_url = context.driver.current_url.lower()
    assert "installation" in current_url or "login" in current_url or "index" in current_url, \
        f"Redirection inattendue : {current_url}"


