"""
Exemple d'utilisation du ChangeLogManager avec des structures imbriquées complexes.
"""

# mypy: ignore-errors

from struct_changelog import ChangeLogManager


def main():
    changelog = ChangeLogManager()

    # Structure de données complexe avec plusieurs niveaux d'imbrication
    data = {
        "company": {
            "name": "TechCorp",
            "departments": {
                "engineering": {
                    "manager": "Alice Johnson",
                    "employees": [
                        {
                            "name": "Bob Smith",
                            "role": "Senior Developer",
                            "skills": ["Python", "JavaScript"],
                        },
                        {
                            "name": "Carol Davis",
                            "role": "DevOps Engineer",
                            "skills": ["Docker", "Kubernetes"],
                        },
                    ],
                    "budget": 500000,
                },
                "marketing": {
                    "manager": "David Wilson",
                    "employees": [
                        {
                            "name": "Eve Brown",
                            "role": "Marketing Manager",
                            "skills": ["SEO", "Analytics"],
                        }
                    ],
                    "budget": 200000,
                },
            },
            "headquarters": {
                "address": "123 Tech Street",
                "city": "San Francisco",
                "country": "USA",
            },
        },
        "founded": 2010,
        "public": False,
    }

    print("=== Exemple avec structures imbriquées complexes ===")
    print("Structure initiale créée avec des départements, employés, etc.")
    print()

    with changelog.capture(data) as d:
        # Modifier le nom de l'entreprise
        d["company"]["name"] = "TechCorp Solutions"

        # Ajouter un nouveau département
        d["company"]["departments"]["sales"] = {
            "manager": "Frank Miller",
            "employees": [
                {
                    "name": "Grace Lee",
                    "role": "Sales Director",
                    "skills": ["CRM", "Negotiation"],
                }
            ],
            "budget": 300000,
        }

        # Modifier un employé existant
        d["company"]["departments"]["engineering"]["employees"][0]["skills"].append(
            "React"
        )

        # Ajouter un nouvel employé à l'équipe d'ingénierie
        d["company"]["departments"]["engineering"]["employees"].append(
            {
                "name": "Henry Taylor",
                "role": "Junior Developer",
                "skills": ["Python", "SQL"],
            }
        )

        # Modifier le budget du département marketing
        d["company"]["departments"]["marketing"]["budget"] = 250000

        # Changer l'adresse du siège social
        d["company"]["headquarters"]["city"] = "New York"
        d["company"]["headquarters"]["address"] = "456 Business Ave"

        # L'entreprise devient publique
        d["public"] = True

        # Ajouter une nouvelle propriété
        d["stock_symbol"] = "TECH"

    print("Changements détectés:")
    for entry in changelog.get_entries():
        print(f"  {entry['action']}: {entry['key_path']}")
        if entry["old_value"] is not None:
            print(f"    Ancien: {entry['old_value']}")
        if entry["new_value"] is not None:
            print(f"    Nouveau: {entry['new_value']}")
        print()

    print("Structure finale:")
    print(f"  Nom de l'entreprise: {data['company']['name']}")
    print(f"  Départements: {list(data['company']['departments'].keys())}")
    print(
        f"  Employés en ingénierie: {len(data['company']['departments']['engineering']['employees'])}"
    )
    print(f"  Public: {data['public']}")
    print(f"  Symbole boursier: {data.get('stock_symbol', 'N/A')}")


if __name__ == "__main__":
    main()
