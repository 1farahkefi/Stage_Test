Feature: Rapport de comparaison des fichiers INI
  Cette fonctionnalité compare les fichiers extraction_infos.ini et Data_Test.ini, puis génère un rapport HTML des différences et similarités.

  Scenario: Génération du rapport de comparaison HTML
    Given le fichier INI "extraction_infos.ini" est chargé et le fichier correspondant est récupéré depuis la base de données
    When les sections et clés sont comparées entre les deux fichiers
    Then un fichier HTML rapport est généré et ouvert dans le navigateur