"""
Exemple d'utilisation manuelle du ChangeLogManager (ajout d'entrées sans context manager).
"""

from struct_changelog import ChangeActions, ChangeLogManager


def main():
    changelog = ChangeLogManager()
    
    print("=== Exemple d'ajout manuel d'entrées ===")
    print("Ajout d'entrées de changelog manuellement...")
    print()
    
    # Ajouter des entrées manuellement
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.name",
        new_value="John Doe"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.email",
        new_value="john@example.com"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.age",
        new_value=30
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.preferences.theme",
        new_value="dark"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.preferences.language",
        new_value="fr"
    )
    
    # Simuler une modification
    changelog.add(
        action=ChangeActions.EDITED,
        key_path="user.age",
        old_value=30,
        new_value=31
    )
    
    # Simuler un changement de préférence
    changelog.add(
        action=ChangeActions.EDITED,
        key_path="user.preferences.theme",
        old_value="dark",
        new_value="light"
    )
    
    # Ajouter une nouvelle préférence
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.preferences.notifications",
        new_value=True
    )
    
    # Simuler la suppression d'une propriété
    changelog.add(
        action=ChangeActions.REMOVED,
        key_path="user.temp_data",
        old_value="temporary_value"
    )
    
    # Ajouter des entrées pour des listes
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.hobbies[0]",
        new_value="programming"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.hobbies[1]",
        new_value="reading"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.hobbies[2]",
        new_value="gaming"
    )
    
    # Modifier un élément de liste
    changelog.add(
        action=ChangeActions.EDITED,
        key_path="user.hobbies[1]",
        old_value="reading",
        new_value="cooking"
    )
    
    # Ajouter des entrées pour des structures complexes
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.address.street",
        new_value="123 Main Street"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.address.city",
        new_value="New York"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="user.address.country",
        new_value="USA"
    )
    
    # Modifier l'adresse
    changelog.add(
        action=ChangeActions.EDITED,
        key_path="user.address.city",
        old_value="New York",
        new_value="Los Angeles"
    )
    
    print("Toutes les entrées du changelog:")
    for i, entry in enumerate(changelog.get_entries(), 1):
        print(f"{i:2d}. {entry['action']}: {entry['key_path']}")
        if entry['old_value'] is not None:
            print(f"     Ancien: {entry['old_value']}")
        if entry['new_value'] is not None:
            print(f"     Nouveau: {entry['new_value']}")
        print()
    
    # Afficher un résumé par type d'action
    print("Résumé par type d'action:")
    action_counts = {}
    for entry in changelog.get_entries():
        action = entry['action']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    for action, count in action_counts.items():
        print(f"  {action}: {count} entrée(s)")
    
    print()
    
    # Exemple d'utilisation avec reset
    print("=== Exemple avec reset ===")
    print(f"Nombre d'entrées avant reset: {len(changelog.get_entries())}")
    
    changelog.reset()
    print(f"Nombre d'entrées après reset: {len(changelog.get_entries())}")
    
    # Ajouter de nouvelles entrées après reset
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="new_session.id",
        new_value="session_123"
    )
    
    changelog.add(
        action=ChangeActions.ADDED,
        key_path="new_session.timestamp",
        new_value="2024-01-15T10:30:00Z"
    )
    
    print("Nouvelles entrées après reset:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']} = {entry['new_value']}")


if __name__ == "__main__":
    main()
