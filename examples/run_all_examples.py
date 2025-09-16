#!/usr/bin/env python3
"""
Script pour exécuter tous les exemples de struct-changelog et générer un rapport.

Usage:
    python run_all_examples.py
    python run_all_examples.py --verbose
    python run_all_examples.py --quiet
"""

# mypy: ignore-errors

import sys
import time
import traceback
from pathlib import Path
from typing import Dict, List
import argparse


class ExampleRunner:
    """Classe pour exécuter tous les exemples et générer un rapport."""

    def __init__(self, verbose: bool = False, quiet: bool = False):
        """
        Initialise le runner d'exemples.

        Args:
            verbose (bool): Affiche la sortie de chaque exemple.
            quiet (bool): Mode silencieux, n'affiche que le rapport final.
        """
        self.verbose = verbose
        self.quiet = quiet
        self.results: List[Dict] = []
        self.start_time = time.time()

        # Définir le répertoire des exemples
        self.examples_dir = Path(__file__).parent
        self.project_root = self.examples_dir.parent

        # Ajouter le répertoire src au path pour les imports
        sys.path.insert(0, str(self.project_root / "src"))

    def run_example(self, example_file: Path) -> Dict:
        """
        Exécute un exemple et retourne les résultats.

        Args:
            example_file (Path): Chemin vers le fichier d'exemple.

        Returns:
            Dict: Résultats de l'exécution avec statut, temps, erreurs, etc.
        """
        example_name = example_file.stem
        start_time = time.time()

        result = {
            "name": example_name,
            "file": str(example_file),
            "status": "unknown",
            "duration": 0.0,
            "error": None,
            "output": "",
            "changelog_entries": 0,
            "features_demonstrated": [],
        }

        try:
            if not self.quiet:
                print(f"🔄 Exécution de {example_name}...")

            # Capturer la sortie standard
            import io
            from contextlib import redirect_stdout, redirect_stderr

            output_buffer = io.StringIO()
            error_buffer = io.StringIO()

            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                # Exécuter le module
                exec(
                    open(example_file, "r", encoding="utf-8").read(),
                    {"__name__": "__main__", "__file__": str(example_file)},
                )

            result["status"] = "success"
            result["output"] = output_buffer.getvalue()
            result["error"] = error_buffer.getvalue()

            # Analyser les fonctionnalités démontrées
            result["features_demonstrated"] = self._analyze_features(result["output"])

            # Compter les entrées de changelog (approximation)
            result["changelog_entries"] = self._count_changelog_entries(
                result["output"]
            )

            if self.verbose and not self.quiet:
                print(f"✅ {example_name} - Succès")
                if result["output"].strip():
                    print("📄 Sortie:")
                    print(result["output"])
                print()

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()

            if not self.quiet:
                print(f"❌ {example_name} - Erreur: {e}")
                if self.verbose:
                    print(f"Traceback: {result['traceback']}")
                print()

        finally:
            result["duration"] = time.time() - start_time

        return result

    def _analyze_features(self, output: str) -> List[str]:
        """Analyse la sortie pour identifier les fonctionnalités démontrées."""
        features = []
        output_lower = output.lower()

        if "changelog" in output_lower:
            features.append("ChangeLogManager")
        if "track_changes" in output_lower:
            features.append("Context Manager Global")
        if "create_changelog" in output_lower:
            features.append("Factory Function")
        if "changetracker" in output_lower:
            features.append("ChangeTracker Class")
        if (
            "added" in output_lower
            or "edited" in output_lower
            or "removed" in output_lower
        ):
            features.append("Change Types")
        if "json" in output_lower:
            features.append("JSON Serialization")
        if "nested" in output_lower or "imbriqué" in output_lower:
            features.append("Nested Structures")
        if "list" in output_lower or "array" in output_lower:
            features.append("Lists/Arrays")
        if "object" in output_lower or "objet" in output_lower:
            features.append("Custom Objects")
        if "manual" in output_lower or "manuel" in output_lower:
            features.append("Manual Tracking")
        if "reset" in output_lower:
            features.append("Reset Functionality")

        return features

    def _count_changelog_entries(self, output: str) -> int:
        """Compte approximativement le nombre d'entrées de changelog dans la sortie."""
        lines = output.split("\n")
        count = 0

        for line in lines:
            if any(action in line.lower() for action in ["added", "edited", "removed"]):
                if ":" in line and ("key_path" in line or "action" in line):
                    count += 1

        return count

    def run_all_examples(self) -> None:
        """Exécute tous les exemples Python dans le répertoire examples."""
        if not self.quiet:
            print("🚀 Démarrage de l'exécution de tous les exemples struct-changelog")
            print("=" * 60)
            print()

        # Trouver tous les fichiers d'exemples Python
        example_files = [
            f
            for f in self.examples_dir.glob("*.py")
            if f.name != "run_all_examples.py" and f.name != "__init__.py"
        ]

        if not example_files:
            print("❌ Aucun exemple trouvé dans le répertoire examples/")
            return

        # Exécuter chaque exemple
        for example_file in sorted(example_files):
            result = self.run_example(example_file)
            self.results.append(result)

        # Générer le rapport
        self.generate_report()

    def generate_report(self) -> None:
        """Génère un rapport détaillé des résultats."""
        total_time = time.time() - self.start_time
        successful = [r for r in self.results if r["status"] == "success"]
        failed = [r for r in self.results if r["status"] == "error"]

        print("\n" + "=" * 60)
        print("📊 RAPPORT D'EXÉCUTION DES EXEMPLES")
        print("=" * 60)

        # Résumé général
        print(f"\n📈 Résumé général:")
        print(f"   • Total d'exemples: {len(self.results)}")
        print(f"   • Succès: {len(successful)} ✅")
        print(f"   • Échecs: {len(failed)} ❌")
        print(f"   • Temps total: {total_time:.2f}s")

        # Détails par exemple
        print(f"\n📋 Détails par exemple:")
        for result in self.results:
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"   {status_icon} {result['name']:<20} ({result['duration']:.2f}s)")

            if result["status"] == "success":
                if result["changelog_entries"] > 0:
                    print(
                        f"      📝 {result['changelog_entries']} entrée(s) de changelog"
                    )
                if result["features_demonstrated"]:
                    features_str = ", ".join(result["features_demonstrated"])
                    print(f"      🎯 Fonctionnalités: {features_str}")
            else:
                print(f"      💥 Erreur: {result['error']}")

        # Statistiques des fonctionnalités
        all_features = []
        for result in self.results:
            all_features.extend(result["features_demonstrated"])

        if all_features:
            feature_counts = {}
            for feature in all_features:
                feature_counts[feature] = feature_counts.get(feature, 0) + 1

            print(f"\n🎯 Fonctionnalités démontrées:")
            for feature, count in sorted(feature_counts.items()):
                print(f"   • {feature}: {count} exemple(s)")

        # Temps d'exécution
        if successful:
            avg_time = sum(r["duration"] for r in successful) / len(successful)
            print(f"\n⏱️  Temps d'exécution:")
            print(f"   • Moyenne: {avg_time:.2f}s")
            print(f"   • Plus rapide: {min(r['duration'] for r in successful):.2f}s")
            print(f"   • Plus lent: {max(r['duration'] for r in successful):.2f}s")

        # Recommandations
        print(f"\n💡 Recommandations:")
        if len(successful) == len(self.results):
            print("   🎉 Tous les exemples s'exécutent correctement!")
        else:
            print(f"   ⚠️  {len(failed)} exemple(s) nécessitent une attention")

        if any(
            "Context Manager Global" in r["features_demonstrated"] for r in self.results
        ):
            print("   📚 L'approche 'Context Manager Global' est démontrée")
        if any("ChangeTracker" in r["features_demonstrated"] for r in self.results):
            print("   📚 L'approche 'ChangeTracker Class' est démontrée")

        print(f"\n🔗 Pour plus de détails, consultez:")
        print(f"   • README.md - Documentation principale")
        print(f"   • examples/README.md - Guide des exemples")
        print(f"   • Chaque fichier d'exemple pour des cas d'usage spécifiques")

        print("\n" + "=" * 60)

        # Code de sortie
        if failed:
            sys.exit(1)
        else:
            sys.exit(0)


def main():
    """Point d'entrée principal du script."""
    parser = argparse.ArgumentParser(
        description="Exécute tous les exemples struct-changelog et génère un rapport",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'usage:
  python run_all_examples.py              # Mode normal
  python run_all_examples.py --verbose   # Affiche la sortie de chaque exemple
  python run_all_examples.py --quiet     # Mode silencieux, rapport uniquement
        """,
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Affiche la sortie de chaque exemple",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Mode silencieux, n'affiche que le rapport final",
    )

    args = parser.parse_args()

    # Validation des arguments
    if args.verbose and args.quiet:
        print("❌ Erreur: --verbose et --quiet sont mutuellement exclusifs")
        sys.exit(1)

    # Exécuter les exemples
    runner = ExampleRunner(verbose=args.verbose, quiet=args.quiet)
    runner.run_all_examples()


if __name__ == "__main__":
    main()
