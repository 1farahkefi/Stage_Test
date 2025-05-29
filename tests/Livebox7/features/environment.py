import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
    # Première partie : Vérification de la connexion au modem
    try:
        print("Tentative de connexion au modem...")
        response = requests.get("http://192.168.1.1", timeout=5)
        response.raise_for_status()  # Lève une exception si le code de réponse est 4xx ou 5xx
        print("Connexion au modem réussie.")
    except requests.ConnectionError as e:
        print("Erreur : Impossible de se connecter au modem. Vérifiez que l'appareil est allumé et connecté.")
        print(str(e))
        raise  # Relance l'exception pour arrêter l'exécution du test si la connexion au modem échoue

    # Deuxième partie : Initialisation du WebDriver Selenium
    options = Options()
    options.add_argument("--start-maximized")  # Maximiser la fenêtre du navigateur
    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),  # Gestion automatique du ChromeDriver
        options=options
    )
def after_all(context):
    if context.driver:
        context.driver.quit()  # Fermer le navigateur après les tests
    else:
        print("Aucun WebDriver n'a été initialisé.")