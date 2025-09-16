"""
Exemple d'utilisation basique du ChangeLogManager avec des dictionnaires.
"""

# mypy: ignore-errors

from struct_changelog import ChangeLogManager


def main():
    # Créer un gestionnaire de changelog
    changelog = ChangeLogManager()
    
    # Données initiales
    data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zipcode": "10001"
        }
    }
    
    print("=== Exemple d'utilisation basique ===")
    print(f"Données initiales: {data}")
    print()
    
    # Capturer les changements avec le context manager
    with changelog.capture(data) as d:
        # Modifier des valeurs existantes
        d["name"] = "Jane Smith"
        d["age"] = 31
        
        # Ajouter une nouvelle clé
        d["phone"] = "+1-555-0123"
        
        # Modifier une valeur imbriquée
        d["address"]["city"] = "Los Angeles"
        d["address"]["zipcode"] = "90210"
        
        # Supprimer une clé
        del d["email"]
    
    # Afficher les changements capturés
    print("Changements détectés:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']}")
        if entry['old_value'] is not None:
            print(f"    Ancien: {entry['old_value']}")
        if entry['new_value'] is not None:
            print(f"    Nouveau: {entry['new_value']}")
        print()
    
    print(f"Données finales: {data}")


if __name__ == "__main__":
    main()
