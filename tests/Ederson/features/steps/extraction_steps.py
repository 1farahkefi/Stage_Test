import os
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import when, then
from configparser import ConfigParser
import time

# Étape : L'utilisateur clique sur l'onglet "Ma Box"
@when('l\'utilisateur clique sur l\'onglet "Ma Box"')
def step_click_ma_box(context):
    try:
        # Attente explicite de l'élément et s'assurer qu'il est cliquable
        WebDriverWait(context.driver, 40).until(
            EC.element_to_be_clickable((By.ID, "linkToBbox"))
        )
        # Cliquer directement après s'être assuré que l'élément est cliquable
        context.driver.find_element(By.ID, "linkToBbox").click()
    except TimeoutException:
        print("Erreur : Timeout lors de l'attente de l'élément 'linkToBbox'.")
    except NoSuchElementException:
        print("Erreur : L'élément 'linkToBbox' n'a pas été trouvé.")

# Étape : L'utilisateur attend le chargement des données système
@when("l'utilisateur attend le chargement des données système")
def step_wait_for_data(context):
    try:
        # Attendre explicitement la visibilité de l'élément
        WebDriverWait(context.driver, 40).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "form_infoline__PvYyq"))
        )
    except TimeoutException:
        print("Erreur : Timeout lors de l'attente du chargement des données système.")

# Étape : L'utilisateur extrait les blocs d'informations visibles
@when("il extrait les blocs d'informations visibles")
def step_extract_info_blocks(context):
    context.infos = {}
    try:
        # On s'assure que les blocs sont visibles avant d'interagir
        for index in [1, 2]:
            xpath = f"//div[@id='page_bbox']//div[@class='form_grid3__cZhDB']/div[{index}]"
            blocs = WebDriverWait(context.driver, 40).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )

            for bloc in blocs:
                titre = bloc.find_element(By.CLASS_NAME, "form_minTitleH1__yq5aG").text.strip()
                context.infos[titre] = {}

                lignes = bloc.find_elements(By.CLASS_NAME, "form_infoline__PvYyq")
                for ligne in lignes:
                    spans = ligne.find_elements(By.TAG_NAME, "span")
                    if len(spans) >= 2:
                        key = spans[0].text.strip()
                        value = spans[1].text.strip()
                        context.infos[titre][key] = value

                if index == 1:
                    bouton1 = bloc.find_elements(By.XPATH,"//div[@class='devicemap_value__tZz3s devicemap_outlines__yofPL ']")
                    bouton2 = bloc.find_elements(By.XPATH, "//div[@class='devicemap_label__xPwuI']")
                    if bouton1 and bouton2:
                        key = bouton2[0].text.strip()
                        value = bouton1[0].text.strip()
                        if key and value:
                            context.infos[titre][key] = value
    except NoSuchElementException:
        print("Erreur : L'un des éléments à extraire n'a pas été trouvé.")

    try:
        details = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='linkToWan']"))
        )
        ActionChains(context.driver).move_to_element(details).click().perform()

        iframe = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@id='iframeContainer']"))
        )
        context.driver.switch_to.frame(iframe)

        mode_elem = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='GPON-B+']"))
        )
        mode_text = mode_elem.text.strip()

        olt_elem = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='sff']//div[@id='olt_model']//div[@class='value']"))
        )
        olt_text = olt_elem.text.strip()

        for section in context.infos:
            if section.lower() == "informations réseau":
                context.infos[section]["Mode PON"] = mode_text
                context.infos[section]["Modèle OLT"] = olt_text
                break
        else:
            context.infos["Informations Réseau"] = {"Modèle OLT": olt_text}
    finally:
        context.driver.switch_to.default_content()

# Étape : Sauvegarder les informations extraites dans un fichier INI
@then("les informations produit et réseau doivent être affichées dans le fichier .ini")
def step_save_info_to_ini(context):
    config = ConfigParser()
    ini_file = "extraction_infos.ini"

    for section, data in context.infos.items():
        if isinstance(data, dict):
            if not config.has_section(section):
                config.add_section(section)
            for key, value in data.items():
                config.set(section, key, str(value))

    with open(ini_file, "w", encoding="utf-8") as f:
        config.write(f)

# Étape : L'utilisateur clique sur "info WIFI"
@when('l\'utilisateur clique sur info WIFI')
def step_click_info_wifi(context):
    try:
        # Attendre que l'élément soit visible et cliquable
        ongletwifi = WebDriverWait(context.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "linkToWireless"))
        )
        ActionChains(context.driver).move_to_element(ongletwifi).click().perform()
    except TimeoutException:
        print("Erreur : Timeout lors de l'attente de l'élément 'linkToWireless'.")

# Étape : Extraire les informations Wi-Fi
@when("il extrait les informations Wi-Fi")
def step_extract_wifi_info(context):
    if not hasattr(context, "infos"):
        context.infos = {}
    section = "Informations Wi-Fi"
    context.infos[section] = {}
    champs_wifi = [
        ("Nom du Wi-Fi", "ssid_wifi_principal_vue_simple"),
        ("Mot de passe", "passphrase_wifi_principal_vue_simple"),
    ]
    for label_texte, input_id in champs_wifi:
        try:
            # Recherche de l'élément juste avant d'agir dessus
            label_elem = WebDriverWait(context.driver, 40).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//form[@id='wifi_principal_vue_simple']//label[normalize-space()='Nom du Wi-Fi']"))
            )
            input_elem = WebDriverWait(context.driver, 40).until(
                EC.visibility_of_element_located((By.ID, input_id))
            )
            key = label_elem.text.strip()
            value = input_elem.get_attribute("value").strip()
            context.infos[section][key] = value
        except NoSuchElementException:
            print("Erreur : L'élément Wi-Fi n'a pas été trouvé.")

# Étape : Sauvegarder les informations Wi-Fi dans le fichier INI
@then("les informations WIFI doivent être affichées dans le fichier .ini")
def step_save_wifi_to_ini(context):
    config = ConfigParser()
    ini_file = "extraction_infos.ini"
    if os.path.exists(ini_file):
        config.read(ini_file, encoding="utf-8")

    for section, data in context.infos.items():
        if isinstance(data, dict):
            if not config.has_section(section):
                config.add_section(section)
            for key, value in data.items():
                config.set(section, key, value)
    with open(ini_file, "w", encoding="utf-8") as f:
        config.write(f)

# Étape : L'utilisateur clique sur "Appareils connectés"
@when('l\'utilisateur clique sur "Appareils connectés"')
def step_click_app_con(context):
    try:
        # Attente explicite de l'élément cliquable
        appcon = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@aria-label='Mes appareils / Tout ce qui est connecté à ma Bbox']"))
        )
        ActionChains(context.driver).move_to_element(appcon).click().perform()
    except TimeoutException:
        print("Erreur : Timeout lors de l'attente de l'élément 'Appareils connectés'.")

# Étape : Parcourir la liste des appareils connectés
@when("il parcourt la liste des appareils connectés")
def step_scan_all_devices(context):
    if not hasattr(context, "infos"):
        context.infos = {}
    section = "Appareils connectés"
    context.infos[section] = {}
    appareils = context.driver.find_elements(By.XPATH, "//div[starts-with(@id, 'device_')]")
    context.infos[section]["Nombre total"] = str(len(appareils))
    for index, appareil in enumerate(appareils, start=1):
        try:
            nom_elem = appareil.find_element(By.XPATH, ".//div[contains(@class,'cards_cardFrame__XX4ji')]")
            nom = nom_elem.text.strip()
            context.infos[section][f"Appareil {index}"] = nom if nom else "Nom vide"
        except:
            context.infos[section][f"Appareil {index}"] = "Nom non trouvé"
    step_save_wifi_to_ini(context)

# Étape : Vérifier la disponibilité du téléphone
@when("l\'utilisateur vérifie la disponibilité du téléphone")
def step_telephone(context):
    if not hasattr(context, "infos"):
        context.infos = {}
    section = "Téléphone"
    context.infos[section] = {}
    try:
        flesh = context.driver.find_element(By.ID, 'linkToIndex')
        ActionChains(context.driver).move_to_element(flesh).click().perform()
        time.sleep(2)

        dispo_elem = context.driver.find_element(
            By.XPATH,"//div[contains(@class,'cards_molecule__3VYwv cards_cardTemplate__vr3-9 cards_voip__cLxP- cards_radiusTop__RJP-3 cards_radiusBottom__sGjId')]//span[contains(@class,'cards_label__ZGNTe')]"
        )
        texte = dispo_elem.text.strip()
        context.infos[section]["Disponibilité"] = texte if texte else "Aucun texte trouvé"
    except NoSuchElementException:
        context.infos[section]["Disponibilité"] = "Élément introuvable"

    step_save_wifi_to_ini(context)

# Étape : Vérifier la disponibilité de l'USB
@when("l'utilisateur vérifie la disponibilité de l'USB")
def step_USB(context):
    if not hasattr(context, "infos"):
        context.infos = {}
    section = "USB"
    context.infos[section] = {}
    try:
        icon = WebDriverWait(context.driver, 40).until(
            EC.presence_of_element_located((By.ID, "LinkToAdvancedSettings"))
        )
        ActionChains(context.driver).move_to_element(icon).click().perform()
        button = context.driver.find_element(
            By.XPATH,
            "//a[@href='/usb']//button[@class='action_secondary__VuEnn action_white__Acg7j'][normalize-space()='Consulter']"
        )
        ActionChains(context.driver).move_to_element(button).click().perform()

        iframe = WebDriverWait(context.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@id='iframeContainer']"))
        )
        context.driver.switch_to.frame(iframe)

        usb_elem = WebDriverWait(context.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='capacity']"))
        )
        usb_text = usb_elem.text.strip()
        if usb_text:
            context.infos[section]["Etat"] = "Disponible"
        else:
            context.infos[section]["Etat"] = "Indisponible"
    finally:
        context.driver.switch_to.default_content()
    step_save_wifi_to_ini(context)
