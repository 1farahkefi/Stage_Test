Feature: Extraction des données du modem GetWay
  Cette fonctionnalité permet d'extraire automatiquement les données de plusieurs sections du modem depuis l'interface web et de les enregistrer dans un fichier INI.

  Scenario: Extraction des données Général
    When l'utilisateur clique sur l'icône "Paramètres avancés"
    And l'utilisateur clique sur l'onglet "Informations système"
    And sélectionne l'iframe contenant les données
    Then les données sont extraites du tableau et enregistrées dans la section "General" du fichier INI

  Scenario: Extraction des données Internet
    When l'utilisateur clique sur l'onglet "Internet"
    Then les données sont extraites du tableau et enregistrées dans la section "Internet" du fichier INI

  Scenario: Extraction des données WIFI
    When l'utilisateur clique sur l'onglet "WIFI"
    Then les données sont extraites du tableau et enregistrées dans la section "WIFI" du fichier INI

  Scenario: Extraction des données LAN
    When l'utilisateur clique sur l'onglet "LAN"
    Then les données générales sont extraites et stockées dans la section "LAN" du fichier INI
    And les informations spécifiques aux ports LAN (1 à 4, 10G) sont enregistrées sous les sections correspondantes

  Scenario: Extraction des données VoIP
    When l'utilisateur clique sur l'onglet "VoIP"
    Then les données sont extraites du tableau et enregistrées dans la section "VoIP" du fichier INI

  Scenario: Extraction des données USB
    When l'utilisateur clique sur l'onglet "USB"
    Then les données sont extraites du tableau et enregistrées dans la section "USB" du fichier INI

  Scenario: Extraction des données TV
    When l'utilisateur clique sur l'onglet "TV"
    Then les données de service, chaîne 1, vidéo à la demande et zapping sont extraites et enregistrées dans les sections respectives

  Scenario: Extraction des données ONT
    When l'utilisateur clique sur l'onglet "ONT"
    Then les données sont extraites du tableau et enregistrées dans la section "ONT" du fichier INI
    And l'utilisateur clique sur "Retour"