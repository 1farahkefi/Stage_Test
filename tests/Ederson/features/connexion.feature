Feature: Ouverture de la page d'installation

  Scenario: L'utilisateur ouvre la page d'installation et clique sur le bouton
    Given un fichier texte est généré pour le scan douchette
    And le fichier "credentials.txt" contient le mot de passe
    And l'utilisateur est sur la page d'installation
    When l'utilisateur procède à l'installation ou à la connexion
    Then l'installation démarre ou la page suivante s'affiche