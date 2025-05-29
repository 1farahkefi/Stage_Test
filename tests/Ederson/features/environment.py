import requests  # Assurez-vous que cette bibliothèque est bien importée
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):

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