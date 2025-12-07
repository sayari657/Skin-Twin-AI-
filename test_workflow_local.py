#!/usr/bin/env python
"""
Script de test local pour vérifier que le workflow fonctionne correctement
Simule les étapes du workflow GitHub Actions
"""
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

def print_step(step_num, step_name):
    """Afficher une étape"""
    print("\n" + "="*60)
    print(f"ÉTAPE {step_num}: {step_name}")
    print("="*60)

def run_command(cmd, description):
    """Exécuter une commande et afficher le résultat"""
    print(f"\n▶ {description}")
    print(f"Commande: {cmd}")
    
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Succès ({elapsed:.2f}s)")
            if result.stdout:
                print(result.stdout[:500])  # Limiter l'output
            return True
        else:
            print(f"❌ Échec (code {result.returncode}, {elapsed:.2f}s)")
            if result.stderr:
                print("Erreur:", result.stderr[:500])
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_file_exists(filepath):
    """Vérifier qu'un fichier existe"""
    exists = Path(filepath).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {filepath}: {'Existe' if exists else 'MANQUANT'}")
    return exists

def main():
    """Fonction principale de test"""
    print("\n" + "="*60)
    print("🧪 TEST LOCAL DU WORKFLOW ML MONITORING")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_tests_passed = True
    start_total = time.time()
    
    # Étape 1: Vérifier les fichiers nécessaires
    print_step(1, "Vérification des fichiers nécessaires")
    files_to_check = [
        "mlops_requirements_monitoring.txt",
        ".github/workflows/ml_monitoring.yml",
        "mlops/scripts/run_monitoring.py",
        "mlops/scripts/setup_mlops.py"
    ]
    
    for filepath in files_to_check:
        if not check_file_exists(filepath):
            all_tests_passed = False
    
    # Étape 2: Vérifier Python
    print_step(2, "Vérification de Python")
    python_ok = run_command("python --version", "Version Python")
    if not python_ok:
        all_tests_passed = False
    
    # Étape 3: Vérifier pip
    print_step(3, "Vérification de pip")
    pip_ok = run_command("pip --version", "Version pip")
    if not pip_ok:
        all_tests_passed = False
    
    # Étape 4: Vérifier le fichier requirements
    print_step(4, "Vérification du fichier requirements")
    if Path("mlops_requirements_monitoring.txt").exists():
        with open("mlops_requirements_monitoring.txt", "r") as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]
        print(f"✅ {len(lines)} dépendances dans mlops_requirements_monitoring.txt")
        
        # Vérifier qu'il n'y a pas de dépendances lourdes
        heavy_deps = ["torch", "ultralytics", "torchvision", "dvc[s3]", "evidently", "whylogs"]
        found_heavy = [dep for dep in heavy_deps if any(dep in line.lower() for line in lines)]
        if found_heavy:
            print(f"⚠️  ATTENTION: Dépendances lourdes trouvées: {found_heavy}")
            print("   Le workflow devrait utiliser mlops_requirements_monitoring.txt")
        else:
            print("✅ Aucune dépendance lourde trouvée (bon signe!)")
    else:
        all_tests_passed = False
    
    # Étape 5: Test d'installation (dry-run ou vérification)
    print_step(5, "Vérification des dépendances (sans installation)")
    print("ℹ️  Note: On ne va pas installer les dépendances pour gagner du temps")
    print("   Mais on vérifie que le fichier requirements est valide")
    
    # Vérifier que le fichier requirements est lisible
    try:
        with open("mlops_requirements_monitoring.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if "mlflow" in content.lower():
                print("✅ Fichier requirements contient MLflow")
            else:
                print("⚠️  MLflow non trouvé dans requirements")
    except Exception as e:
        print(f"⚠️  Erreur lecture requirements: {e}")
    
    # Étape 6: Test du script setup_mlops.py (syntaxe)
    print_step(6, "Vérification syntaxe setup_mlops.py")
    setup_syntax = run_command(
        "python -m py_compile mlops/scripts/setup_mlops.py",
        "Compilation syntaxe setup_mlops.py"
    )
    if not setup_syntax:
        all_tests_passed = False
    
    # Étape 7: Test du script run_monitoring.py (syntaxe)
    print_step(7, "Vérification syntaxe run_monitoring.py")
    monitoring_syntax = run_command(
        "python -m py_compile mlops/scripts/run_monitoring.py",
        "Compilation syntaxe run_monitoring.py"
    )
    if not monitoring_syntax:
        all_tests_passed = False
    
    # Étape 8: Vérifier le workflow YAML
    print_step(8, "Vérification du workflow YAML")
    workflow_exists = Path(".github/workflows/ml_monitoring.yml").exists()
    if workflow_exists:
        try:
            with open(".github/workflows/ml_monitoring.yml", "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Essayer avec un autre encodage
            with open(".github/workflows/ml_monitoring.yml", "r", encoding="latin-1") as f:
                content = f.read()
            if "mlops_requirements_monitoring.txt" in content:
                print("✅ Workflow utilise mlops_requirements_monitoring.txt")
            else:
                print("⚠️  Workflow ne semble pas utiliser mlops_requirements_monitoring.txt")
                all_tests_passed = False
            
            if "timeout-minutes: 10" in content:
                print("✅ Timeout de 10 minutes configuré")
            else:
                print("⚠️  Timeout non trouvé dans le workflow")
            
            if "cache: 'pip'" in content or "actions/cache" in content:
                print("✅ Cache pip configuré")
            else:
                print("⚠️  Cache pip non trouvé")
    else:
        all_tests_passed = False
    
    # Résumé final
    total_time = time.time() - start_total
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    if all_tests_passed:
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print(f"⏱️  Temps total: {total_time:.2f}s")
        print("\n🎯 Le workflow devrait fonctionner correctement sur GitHub Actions")
        print("\n📝 Prochaines étapes:")
        print("   1. Allez sur GitHub Actions")
        print("   2. Relancez le workflow 'ML Monitoring'")
        print("   3. Vérifiez que le temps d'exécution est < 10 minutes")
        return 0
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print(f"⏱️  Temps total: {total_time:.2f}s")
        print("\n⚠️  Veuillez corriger les erreurs avant de push")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

