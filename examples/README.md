# Exemples d'utilisation de struct-changelog

Ce dossier contient des exemples d'utilisation du `ChangeLogManager` pour différents cas d'usage.

## Fichiers d'exemples

### 1. `basic_usage.py`
Exemple d'utilisation basique avec des dictionnaires simples. Montre comment :
- Capturer des modifications de valeurs existantes
- Ajouter de nouvelles clés
- Supprimer des clés
- Modifier des valeurs imbriquées

### 2. `nested_structures.py`
Exemple avec des structures imbriquées complexes. Démontre :
- La gestion de structures à plusieurs niveaux d'imbrication
- Les modifications dans des dictionnaires imbriqués
- L'ajout de nouvelles sections complètes
- La modification de propriétés profondément imbriquées

### 3. `lists_arrays.py`
Exemple d'utilisation avec des listes et tableaux. Illustre :
- La modification d'éléments de liste existants
- L'ajout et la suppression d'éléments de liste
- La gestion des listes imbriquées dans des dictionnaires
- Les modifications de listes de chaînes et d'objets

### 4. `objects.py`
Exemple avec des objets personnalisés. Montre :
- Le suivi des modifications dans des objets avec `__dict__`
- La modification des propriétés d'objets imbriqués
- L'ajout de nouvelles propriétés à des objets
- La gestion des listes d'objets

### 5. `manual_tracking.py`
Exemple d'ajout manuel d'entrées. Démontre :
- L'ajout manuel d'entrées sans utiliser le context manager
- L'utilisation des différents types d'actions (ADDED, EDITED, REMOVED)
- La gestion des chemins de clés complexes
- L'utilisation de la méthode `reset()`

### 6. `helper_approaches.py`
Exemple des différentes approches helper pour éviter de devoir initialiser `ChangeLogManager` à chaque fois. Montre :
- L'approche originale (pour comparaison)
- La fonction factory `create_changelog()`
- Le context manager global `track_changes()`
- La classe wrapper `ChangeTracker`
- Comparaison et recommandations d'usage

### 7. `run_all_examples.py`
Script utilitaire pour exécuter tous les exemples et générer un rapport détaillé. Fonctionnalités :
- Exécution automatique de tous les exemples Python
- Génération d'un rapport avec statistiques complètes
- Analyse des fonctionnalités démontrées
- Détection et rapport des erreurs
- Modes d'exécution : normal, verbeux, silencieux

## Comment exécuter les exemples

### Exécution individuelle

```bash
# Depuis la racine du projet
python examples/basic_usage.py
python examples/nested_structures.py
python examples/lists_arrays.py
python examples/objects.py
python examples/manual_tracking.py
python examples/helper_approaches.py
```

### Exécution de tous les exemples avec rapport

```bash
# Exécuter tous les exemples et générer un rapport détaillé
python examples/run_all_examples.py

# Mode verbeux (affiche la sortie de chaque exemple)
python examples/run_all_examples.py --verbose

# Mode silencieux (rapport uniquement)
python examples/run_all_examples.py --quiet
```

Le script `run_all_examples.py` fournit :
- ✅ Exécution automatique de tous les exemples
- 📊 Rapport détaillé avec statistiques
- ⏱️ Temps d'exécution par exemple
- 🎯 Analyse des fonctionnalités démontrées
- ❌ Détection et rapport des erreurs
- 💡 Recommandations d'usage

## Fonctionnalités démontrées

- **Context Manager** : Utilisation de `with changelog.capture(data)` pour capturer automatiquement les changements
- **Types de changements** : ADDED, EDITED, REMOVED
- **Chemins de clés** : Support des chemins imbriqués avec notation pointée (ex: `user.address.city`)
- **Structures complexes** : Dictionnaires, listes, tuples, objets personnalisés
- **Sérialisation JSON** : Les entrées sont sérialisables en JSON
- **Gestion manuelle** : Ajout d'entrées sans context manager
- **Reset** : Nettoyage du changelog

## Cas d'usage typiques

- **Audit de données** : Suivi des modifications dans des structures de données
- **Versioning** : Création d'historiques de changements
- **Debugging** : Compréhension des modifications apportées aux données
- **Logging** : Enregistrement des changements pour des systèmes de logs
- **Synchronisation** : Détection des différences entre structures de données
