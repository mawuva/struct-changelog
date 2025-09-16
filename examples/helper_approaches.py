"""
Exemples d'utilisation des différentes approches helper pour éviter de devoir 
initialiser ChangeLogManager à chaque fois.
"""

# mypy: ignore-errors

from struct_changelog import (
    ChangeLogManager,  # Approche originale
    create_changelog,  # Factory function
    track_changes,     # Context manager global
    ChangeTracker,     # Classe wrapper
    ChangeActions,
)


def example_original_approach():
    """Exemple avec l'approche originale (pour comparaison)."""
    print("=== Approche originale ===")
    
    # Création manuelle du manager
    changelog = ChangeLogManager()
    
    data = {"user": {"name": "John", "age": 30}}
    
    with changelog.capture(data) as d:
        d["user"]["name"] = "Jane"
        d["user"]["age"] = 31
        d["user"]["email"] = "jane@example.com"
    
    print("Changements détectés:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']} = {entry['new_value']}")
    print()


def example_factory_function():
    """Exemple avec la fonction factory create_changelog()."""
    print("=== Factory Function (create_changelog) ===")
    
    # Plus explicite que l'approche originale
    changelog = create_changelog()
    
    data = {"settings": {"theme": "light", "language": "en"}}
    
    with changelog.capture(data) as d:
        d["settings"]["theme"] = "dark"
        d["settings"]["language"] = "fr"
        d["settings"]["notifications"] = True
    
    print("Changements détectés:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']} = {entry['new_value']}")
    print()


def example_context_manager():
    """Exemple avec le context manager global track_changes()."""
    print("=== Context Manager Global (track_changes) ===")
    
    data = {"inventory": {"items": ["apple", "banana"], "count": 2}}
    
    # Plus concis - pas besoin de créer le manager manuellement
    with track_changes(data) as (changelog, tracked_data):
        tracked_data["inventory"]["items"].append("orange")
        tracked_data["inventory"]["count"] = 3
        tracked_data["inventory"]["last_updated"] = "2024-01-15"
    
    print("Changements détectés:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']} = {entry['new_value']}")
    print()


def example_change_tracker():
    """Exemple avec la classe wrapper ChangeTracker."""
    print("=== Classe Wrapper (ChangeTracker) ===")
    
    # Approche orientée objet - utile pour maintenir l'état
    tracker = ChangeTracker()
    
    data = {"session": {"user_id": 123, "active": True}}
    
    # Premier lot de changements
    with tracker.track(data) as d:
        d["session"]["user_id"] = 456
        d["session"]["active"] = False
        d["session"]["logout_time"] = "2024-01-15T10:30:00Z"
    
    print("Premier lot de changements:")
    for entry in tracker.entries:
        print(f"  {entry['action']}: {entry['key_path']} = {entry['new_value']}")
    
    # Ajout manuel d'entrées
    tracker.add(
        ChangeActions.ADDED,
        "session.notes",
        new_value="User logged out due to inactivity"
    )
    
    print("\nAprès ajout manuel:")
    for entry in tracker.entries:
        print(f"  {entry['action']}: {entry['key_path']} = {entry['new_value']}")
    
    # Reset et nouveau tracking
    tracker.reset()
    print(f"\nAprès reset: {len(tracker.entries)} entrées")
    
    with tracker.track(data) as d:
        d["session"]["user_id"] = 789
        d["session"]["active"] = True
    
    print("Nouveau tracking après reset:")
    for entry in tracker.entries:
        print(f"  {entry['action']}: {entry['key_path']} = {entry['new_value']}")
    print()


def example_comparison():
    """Comparaison des différentes approches."""
    print("=== Comparaison des approches ===")
    
    data = {"config": {"debug": False, "version": "1.0"}}
    
    print("1. Approche originale:")
    print("   changelog = ChangeLogManager()")
    print("   with changelog.capture(data) as d: ...")
    print()
    
    print("2. Factory function:")
    print("   changelog = create_changelog()")
    print("   with changelog.capture(data) as d: ...")
    print()
    
    print("3. Context manager global:")
    print("   with track_changes(data) as (changelog, d): ...")
    print()
    
    print("4. Classe wrapper:")
    print("   tracker = ChangeTracker()")
    print("   with tracker.track(data) as d: ...")
    print()
    
    print("=== Recommandations ===")
    print("• Utilisez track_changes() pour un usage simple et ponctuel")
    print("• Utilisez ChangeTracker() quand vous avez besoin de maintenir l'état")
    print("• Utilisez create_changelog() pour plus d'explicité")
    print("• Évitez les singletons globaux (problèmes d'état partagé)")


def main():
    """Exécute tous les exemples."""
    example_original_approach()
    example_factory_function()
    example_context_manager()
    example_change_tracker()
    example_comparison()


if __name__ == "__main__":
    main()
