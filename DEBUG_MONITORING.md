# 🔍 Guide de Débogage - ML Monitoring

## Comment identifier les problèmes du workflow GitHub Actions

### 1. Vérifier les logs GitHub Actions

Dans GitHub, allez dans l'onglet **Actions** → Sélectionnez le workflow qui a échoué → Cliquez sur le job `monitor-models` → Consultez les logs de chaque étape.

### 2. Problèmes courants et solutions

#### ❌ Problème : "ModuleNotFoundError" ou "ImportError"

**Cause** : Les dépendances ne sont pas installées correctement.

**Solution** :
```bash
# Vérifier que mlops_requirements.txt existe
cat mlops_requirements.txt

# Installer manuellement pour tester
pip install -r mlops_requirements.txt
```

#### ❌ Problème : "FileNotFoundError" ou chemins incorrects

**Cause** : Les chemins relatifs ne fonctionnent pas dans GitHub Actions.

**Solution** : Vérifier que le script utilise des chemins relatifs au répertoire de travail.

#### ❌ Problème : "Permission denied" ou erreurs de fichiers

**Cause** : Problèmes de permissions ou répertoires manquants.

**Solution** : Le script `run_monitoring.py` crée automatiquement les répertoires nécessaires.

### 3. Tester localement avant de push

```bash
# 1. Installer les dépendances
pip install -r mlops_requirements.txt

# 2. Initialiser MLOps
python mlops/scripts/setup_mlops.py

# 3. Exécuter le monitoring
python mlops/scripts/run_monitoring.py

# 4. Vérifier le code de sortie
echo $?  # Devrait être 0 si tout va bien
```

### 4. Vérifier les fichiers générés

```bash
# Vérifier que les répertoires existent
ls -la .monitoring/
ls -la logs/mlops/

# Vérifier les alertes
ls -la .monitoring/alerts/
```

### 5. Activer le mode debug

Pour plus de détails, modifiez temporairement le script :

```python
# Dans run_monitoring.py, changer :
logging.basicConfig(level=logging.DEBUG)  # Au lieu de INFO
```

### 6. Vérifier les variables d'environnement

Le workflow peut nécessiter certaines variables :

```yaml
env:
  MLFLOW_TRACKING_URI: file:./.mlflow
  PYTHONPATH: ${{ github.workspace }}
```

### 7. Commandes utiles pour déboguer

```bash
# Vérifier Python et les modules
python --version
python -c "import mlflow; print(mlflow.__version__)"

# Vérifier la structure du projet
find . -name "*.py" -path "./mlops/*" | head -10

# Tester l'import
python -c "from mlops.monitoring.model_monitor import ModelMonitor; print('OK')"
```

### 8. Logs à consulter dans GitHub Actions

1. **Checkout code** : Vérifier que le code est bien récupéré
2. **Set up Python** : Vérifier la version Python (3.10)
3. **Install dependencies** : Vérifier que toutes les dépendances sont installées
4. **Initialize MLOps** : Vérifier que l'initialisation fonctionne
5. **Run monitoring checks** : C'est ici que l'erreur se produit généralement

### 9. Si le problème persiste

1. **Vérifier les permissions** : Le workflow a-t-il les bonnes permissions ?
2. **Vérifier les secrets** : Y a-t-il des secrets nécessaires non configurés ?
3. **Vérifier la syntaxe YAML** : Utiliser un validateur YAML
4. **Tester avec workflow_dispatch** : Déclencher manuellement pour voir les logs en temps réel

### 10. Structure attendue

```
skin-twin-ai/
├── .github/
│   └── workflows/
│       └── ml_monitoring.yml
├── mlops/
│   ├── scripts/
│   │   ├── setup_mlops.py
│   │   └── run_monitoring.py  ← Nouveau script
│   ├── monitoring/
│   │   └── model_monitor.py
│   └── ...
├── mlops_requirements.txt
└── .monitoring/  ← Créé automatiquement
    ├── alerts/
    └── predictions_history.json
```

## 📝 Checklist de débogage

- [ ] Les dépendances sont installées (`mlops_requirements.txt` existe)
- [ ] Le script `run_monitoring.py` existe et est exécutable
- [ ] Le script `setup_mlops.py` fonctionne localement
- [ ] Les chemins relatifs sont corrects
- [ ] Les répertoires `.monitoring/` peuvent être créés
- [ ] Python 3.10 est utilisé
- [ ] Les logs GitHub Actions sont consultés
- [ ] Le workflow peut être déclenché manuellement (`workflow_dispatch`)

