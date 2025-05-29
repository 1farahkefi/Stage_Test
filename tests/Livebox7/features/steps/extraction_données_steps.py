import configparser
import os
from behave import when, then
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

@when('l\'utilisateur clique sur l\'icône "Paramètres avancés"')
def step_click_icon_parametres(context):
    bouton = context.driver.find_element(By.XPATH, '//div[@class="sah_page_selector"]/div[contains(@class, "iconbar-button") and contains(@class, "icon-advanced")]')
    ActionChains(context.driver).click(bouton).perform()
    time.sleep(1)

@when('l\'utilisateur clique sur l\'onglet "Informations système"')
def step_click_info_system_tab(context):
    infoSys = context.driver.find_element(By.XPATH, "//div[@id='systemInformation']//div[@class='widget']")
    ActionChains(context.driver).move_to_element(infoSys).click().perform()
    time.sleep(3)

@when("sélectionne l'iframe contenant les données")
def step_switch_to_iframe(context):
    context.driver.switch_to.frame("iframeapp")

@when('l\'utilisateur clique sur l\'onglet "{section}"')
def step_click_tab(context, section):
    mapping = {
        "Internet": "tab_information_internet",
        "WIFI": "tab_information_wifi",
        "LAN": "tab_information_lan",
        "VoIP": "tab_information_voip",
        "USB": "tab_information_usb",
        "TV": "tab_information_tv",
        "ONT": "tab_information_ont"
    }
    element_id = mapping.get(section)
    if element_id:
        context.driver.find_element(By.ID, element_id).click()
        time.sleep(7)
    else:
        raise ValueError(f"Section inconnue : {section}")

@then('les données sont extraites du tableau et enregistrées dans la section "{section}" du fichier INI')
def step_extract_generic_table(context, section):
    table = context.driver.find_element(By.XPATH, "//table")
    rows = table.find_elements(By.XPATH, ".//tr")
    table_data = {}

    for row in rows:
        divs = row.find_elements(By.TAG_NAME, "div")
        if len(divs) >= 3:
            key = divs[1].text.strip()
            value = divs[2].text.strip()
            table_data[key] = value

    path = "TABLE_DATA.ini"
    config = configparser.ConfigParser()
    if os.path.exists(path):
        config.read(path, encoding="utf-8")
    if not config.has_section(section):
        config.add_section(section)

    for k, v in table_data.items():
        config.set(section, k, v)

    with open(path, "w", encoding="utf-8") as f:
        config.write(f)
    print(f" Données '{section}' extraites et enregistrées.")

@then('les données générales sont extraites et stockées dans la section "LAN" du fichier INI')
def step_extract_lan_general(context):
    step_extract_generic_table(context, "LAN")

@then('les informations spécifiques aux ports LAN (1 à 4, 10G) sont enregistrées sous les sections correspondantes')
def step_extract_lan_ports(context):
    config = configparser.ConfigParser()
    path = "TABLE_DATA.ini"
    if os.path.exists(path):
        config.read(path, encoding="utf-8")

    subtitles = [
        ('//span[@data-translation="systemInformation.lan.firstSubtitle.title"]', 'Port ethernet 1', 'lan1_table'),
        ('//span[@data-translation="systemInformation.lan.secondSubtitle.title"]', 'Port ethernet 2', 'lan2_table'),
        ('//span[@data-translation="systemInformation.lan.thirSubtitle.title"]', 'Port ethernet 3', 'lan3_table'),
        ('//span[@data-translation="systemInformation.lan.fourthSubtitle.title"]', 'Port ethernet 4', 'lan4_table'),
        ('//span[@data-translation="systemInformation.lan.sixthSubtitle.title10Gigabit"]', 'Port ethernet 10G', 'lan6_table')
    ]

    for xpath, title, table_id in subtitles:
        try:
            subtitle_element = context.driver.find_element(By.XPATH, xpath)
            subtitle_element.text.strip()

            if not config.has_section(title):
                config.add_section(title)

            table = context.driver.find_element(By.ID, table_id)
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                divs = row.find_elements(By.TAG_NAME, "div")
                if len(divs) >= 3:
                    key = divs[1].text.strip()
                    value = divs[2].text.strip()
                    config.set(title, key, value)
        except Exception as e:
            print(f" Erreur lors de l'extraction de {title}: {e}")

    with open(path, "w", encoding="utf-8") as f:
        config.write(f)
    print(" Données des ports LAN enregistrées.")

@then("les données de service, chaîne 1, vidéo à la demande et zapping sont extraites et enregistrées dans les sections respectives")
def step_extract_tv_sections(context):
    def extract_table(section_name, xpath_table):
        table = context.driver.find_element(By.XPATH, xpath_table)
        rows = table.find_elements(By.XPATH, ".//tr")
        table_data = {}

        for row in rows:
            divs = row.find_elements(By.TAG_NAME, "div")
            if len(divs) >= 3:
                key = divs[1].text.strip()
                value = divs[2].text.strip()
                table_data[key] = value

        return table_data

    path = "TABLE_DATA.ini"
    config = configparser.ConfigParser()
    if os.path.exists(path):
        config.read(path, encoding="utf-8")

    try:
        service_state = context.driver.find_element(By.ID, "serviceState").text.strip()
        config.add_section("TV")
        config.set("TV", "État du service", service_state)
    except:
        pass

    tv_sections = [
        ("Channel 1", "//table"),
        ("Vidéo à la demande", "//table"),
        ("Zapping", "//table")
    ]

    for name, xpath in tv_sections:
        if not config.has_section(name):
            config.add_section(name)
        try:
            data = extract_table(name, xpath)
            for k, v in data.items():
                config.set(name, k, v)
        except Exception as e:
            print(f"Erreur section {name} : {e}")

    with open(path, "w", encoding="utf-8") as f:
        config.write(f)
    print("Données TV enregistrées.")


@then('l\'utilisateur clique sur "Retour"')
def step_click_retour(context):
        retour = context.driver.find_element(By.XPATH, "//span[normalize-space()='Retour']")
        ActionChains(context.driver).click(retour).perform()
        context.driver.switch_to.default_content()
        time.sleep(2)