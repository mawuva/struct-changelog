"""
Exemple d'utilisation du ChangeLogManager avec des listes et tableaux.
"""

# mypy: ignore-errors

from struct_changelog import ChangeLogManager


def main():
    changelog = ChangeLogManager()
    
    # Données initiales avec des listes
    data = {
        "shopping_cart": {
            "items": [
                {"name": "Laptop", "price": 999.99, "quantity": 1},
                {"name": "Mouse", "price": 29.99, "quantity": 2},
                {"name": "Keyboard", "price": 79.99, "quantity": 1}
            ],
            "discount_codes": ["SAVE10", "WELCOME"],
            "customer_info": {
                "name": "John Doe",
                "preferences": ["electronics", "gaming"]
            }
        },
        "order_history": [
            {"id": "ORD001", "total": 150.00, "status": "completed"},
            {"id": "ORD002", "total": 75.50, "status": "shipped"}
        ],
        "tags": ["urgent", "electronics"]
    }
    
    print("=== Exemple avec listes et tableaux ===")
    print("Données initiales du panier d'achat:")
    print(f"  Articles: {len(data['shopping_cart']['items'])}")
    print(f"  Codes de réduction: {data['shopping_cart']['discount_codes']}")
    print(f"  Historique des commandes: {len(data['order_history'])}")
    print()
    
    with changelog.capture(data) as d:
        # Modifier la quantité d'un article existant
        d["shopping_cart"]["items"][0]["quantity"] = 2
        
        # Modifier le prix d'un article
        d["shopping_cart"]["items"][1]["price"] = 24.99
        
        # Ajouter un nouvel article à la liste
        d["shopping_cart"]["items"].append({
            "name": "Monitor",
            "price": 299.99,
            "quantity": 1
        })
        
        # Supprimer un article de la liste (en modifiant la liste)
        d["shopping_cart"]["items"] = d["shopping_cart"]["items"][:-1]  # Supprime le dernier
        
        # Ajouter un nouveau code de réduction
        d["shopping_cart"]["discount_codes"].append("SUMMER20")
        
        # Modifier les préférences du client
        d["shopping_cart"]["customer_info"]["preferences"].append("accessories")
        
        # Ajouter une nouvelle commande à l'historique
        d["order_history"].append({
            "id": "ORD003",
            "total": 324.97,
            "status": "pending"
        })
        
        # Modifier le statut d'une commande existante
        d["order_history"][1]["status"] = "delivered"
        
        # Modifier les tags
        d["tags"].remove("urgent")
        d["tags"].append("gift")
        
        # Ajouter une nouvelle propriété avec une liste
        d["shipping_options"] = ["standard", "express", "overnight"]
    
    print("Changements détectés:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']}")
        if entry['old_value'] is not None:
            print(f"    Ancien: {entry['old_value']}")
        if entry['new_value'] is not None:
            print(f"    Nouveau: {entry['new_value']}")
        print()
    
    print("Données finales:")
    print(f"  Articles dans le panier: {len(data['shopping_cart']['items'])}")
    for i, item in enumerate(data['shopping_cart']['items']):
        print(f"    {i+1}. {item['name']} - ${item['price']} x {item['quantity']}")
    
    print(f"  Codes de réduction: {data['shopping_cart']['discount_codes']}")
    print(f"  Préférences client: {data['shopping_cart']['customer_info']['preferences']}")
    print(f"  Commandes dans l'historique: {len(data['order_history'])}")
    print(f"  Tags: {data['tags']}")
    print(f"  Options de livraison: {data['shipping_options']}")


if __name__ == "__main__":
    main()
