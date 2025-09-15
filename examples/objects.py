"""
Exemple d'utilisation du ChangeLogManager avec des objets personnalisés.
"""

from struct_changelog import ChangeActions, ChangeLogManager


class Person:
    """Classe représentant une personne."""
    
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        self.addresses = []
        self.preferences = {}
    
    def add_address(self, street, city, country):
        """Ajouter une adresse."""
        self.addresses.append({
            "street": street,
            "city": city,
            "country": country
        })
    
    def set_preference(self, key, value):
        """Définir une préférence."""
        self.preferences[key] = value


class Company:
    """Classe représentant une entreprise."""
    
    def __init__(self, name, founded_year):
        self.name = name
        self.founded_year = founded_year
        self.employees = []
        self.departments = {}
    
    def add_employee(self, person):
        """Ajouter un employé."""
        self.employees.append(person)
    
    def add_department(self, name, budget):
        """Ajouter un département."""
        self.departments[name] = {"budget": budget, "employees": []}


def main():
    changelog = ChangeLogManager()
    
    # Créer des objets personnalisés
    person1 = Person("Alice Johnson", 28, "alice@example.com")
    person1.add_address("123 Main St", "New York", "USA")
    person1.set_preference("theme", "dark")
    person1.set_preference("language", "en")
    
    person2 = Person("Bob Smith", 35, "bob@example.com")
    person2.add_address("456 Oak Ave", "Los Angeles", "USA")
    person2.set_preference("theme", "light")
    
    company = Company("TechCorp", 2010)
    company.add_employee(person1)
    company.add_employee(person2)
    company.add_department("Engineering", 500000)
    company.add_department("Marketing", 200000)
    
    # Structure de données avec des objets
    data = {
        "company": company,
        "active_projects": ["Project Alpha", "Project Beta"],
        "settings": {
            "notifications": True,
            "auto_save": False
        }
    }
    
    print("=== Exemple avec objets personnalisés ===")
    print(f"Entreprise: {data['company'].name} (fondée en {data['company'].founded_year})")
    print(f"Employés: {len(data['company'].employees)}")
    print(f"Départements: {list(data['company'].departments.keys())}")
    print()
    
    with changelog.capture(data) as d:
        # Modifier les propriétés d'un objet
        d["company"].name = "TechCorp Solutions"
        d["company"].founded_year = 2012
        
        # Modifier les propriétés d'un employé
        d["company"].employees[0].name = "Alice Johnson-Smith"
        d["company"].employees[0].age = 29
        d["company"].employees[0].email = "alice.johnson@techcorp.com"
        
        # Ajouter une nouvelle adresse à un employé
        d["company"].employees[0].add_address("789 Tech Blvd", "San Francisco", "USA")
        
        # Modifier les préférences d'un employé
        d["company"].employees[0].set_preference("theme", "auto")
        d["company"].employees[0].set_preference("notifications", True)
        
        # Modifier le budget d'un département
        d["company"].departments["Engineering"]["budget"] = 600000
        
        # Ajouter un nouveau département
        d["company"].add_department("Sales", 300000)
        
        # Modifier les projets actifs
        d["active_projects"].append("Project Gamma")
        d["active_projects"][0] = "Project Alpha v2"
        
        # Modifier les paramètres
        d["settings"]["auto_save"] = True
        d["settings"]["theme"] = "dark"
        
        # Ajouter une nouvelle propriété
        d["last_updated"] = "2024-01-15"
    
    print("Changements détectés:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']}")
        if entry['old_value'] is not None:
            print(f"    Ancien: {entry['old_value']}")
        if entry['new_value'] is not None:
            print(f"    Nouveau: {entry['new_value']}")
        print()
    
    print("Données finales:")
    print(f"  Nom de l'entreprise: {data['company'].name}")
    print(f"  Année de fondation: {data['company'].founded_year}")
    print(f"  Nombre d'employés: {len(data['company'].employees)}")
    print(f"  Employé 1: {data['company'].employees[0].name} ({data['company'].employees[0].age} ans)")
    print(f"  Adresses de l'employé 1: {len(data['company'].employees[0].addresses)}")
    print(f"  Préférences de l'employé 1: {data['company'].employees[0].preferences}")
    print(f"  Départements: {list(data['company'].departments.keys())}")
    print(f"  Budget Engineering: ${data['company'].departments['Engineering']['budget']:,}")
    print(f"  Projets actifs: {data['active_projects']}")
    print(f"  Paramètres: {data['settings']}")
    print(f"  Dernière mise à jour: {data['last_updated']}")


if __name__ == "__main__":
    main()
