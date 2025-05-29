Feature: Connexion au modem GetWay
  Cette fonctionnalité permet de tester la connexion à l'interface web du modem.

  Background:
    Given la commande get_lb_info.py est exécutée
    And un fichier texte est généré pour le scan douchette
    And le fichier "credentials.txt" contient le mot de passe administrateur
    And la page d'accueil du modem est ouverte à l'adresse "http://192.168.1.1/"

  Scenario: Connexion avec mot de passe et changement de mot de passe
    When l'utilisateur entre le mot de passe dans le champ "password" si la première page est disponible
    And valide la connexion
    Then la page d'accueil s'affiche après authentification