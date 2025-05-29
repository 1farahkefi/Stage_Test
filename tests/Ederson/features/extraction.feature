Feature: Extraction des informations produit et réseau

  Scenario: Extraire les informations affichées dans les sections "produit" et "réseau"
    When l'utilisateur clique sur l'onglet "Ma Box"
    And l'utilisateur attend le chargement des données système
    And il extrait les blocs d'informations visibles
    Then les informations produit et réseau doivent être affichées dans le fichier .ini


  Scenario: Extraire Nom et Mot de passe WIFI
    When l'utilisateur clique sur info WIFI
    And il extrait les informations Wi-Fi
    Then les informations WIFI doivent être affichées dans le fichier .ini

  Scenario: Extraire les appareils connectés
    When l'utilisateur clique sur "Appareils connectés"
    And il parcourt la liste des appareils connectés

  Scenario: Extraire les informations du téléphone
    When l'utilisateur vérifie la disponibilité du téléphone

  Scenario: Extraire les informations de l'USB
    When l'utilisateur vérifie la disponibilité de l'USB
