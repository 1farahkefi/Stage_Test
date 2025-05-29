Feature: Rapport de comparaison des fichiers INI
  Cette fonctionnalité compare les fichiers TABLE_DATA.ini et Data_Test.ini, puis génère un rapport HTML des différences et similarités.

  Scenario: Génération du rapport de comparaison HTML
    Given les fichiers INI "TABLE_DATA.ini" est chargé et le fichier correspondant est récupéré depuis la base de données
    When les sections et clés sont comparées entre les deux fichiers
    Then le rapport HTML est généré

  Scenario: Réinitialisation
    When l'utilisateur clique sur l'icône "Assistance et dépannage"
    And l'utilisateur clique sur "Réinitialiser"
    And sélectionner l'iframe contenant le bouton de réinitialisation
    And l'utilisateur clique sur le bouton "Réinitialiser"
    Then l'utilisateur clique sur le bouton "Confirmer"
    And le rapport HTML est affiché dans le navigateur