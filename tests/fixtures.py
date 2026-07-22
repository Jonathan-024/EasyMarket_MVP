# tests/fixtures.py

MOCK_VENDEURS = [
    {
        "nom": "Jean-Marc Kabuya",
        "whatsapp": "+243810000001",
        "code_clair": "vendeur123",
        "statut": "actif",
        "boutique": {
            "id": "marche-frais",
            "nom": "Au Marché Frais",
            "categorie_principale": "Alimentation",
            "description": "Produits frais locaux et de qualité supérieure.",
            "produits": [
                {"id": "PRD-0101", "nom": "Tomates (Panier)", "type_produit": "Légumes", "prix": "5000", "devise": "CDF", "disponible": True, "autres": "Panier d'environ 2kg"},
                {"id": "PRD-0102", "nom": "Oignons (Tas)", "type_produit": "Légumes", "prix": "2500", "devise": "CDF", "disponible": True, "autres": "Tas de 5 gros oignons"}
            ]
        }
    },
    {
        "nom": "Sarah Tshimanga",
        "whatsapp": "+243820000002",
        "code_clair": "vendeur456",
        "statut": "actif",
        "boutique": {
            "id": "saveurs-pastels",
            "nom": "Saveurs & Pâtisserie",
            "categorie_principale": "Gastronomie",
            "description": "Samoussas croustillants et douceurs faits maison.",
            "produits": [
                {"id": "PRD-0201", "nom": "Samoussas Viande (x10)", "type_produit": "Snack", "prix": "10000", "devise": "CDF", "disponible": True, "autres": "Bien chauds et croustillants"},
                {"id": "PRD-0202", "nom": "Jus de Gingembre (1L)", "type_produit": "Boisson", "prix": "4000", "devise": "CDF", "disponible": True, "autres": "Fait maison, légèrement sucré"}
            ]
        }
    }
]