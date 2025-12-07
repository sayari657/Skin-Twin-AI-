#!/usr/bin/env python
"""
Script de monitoring pour GitHub Actions
Vérifie la santé des modèles et génère des alertes si nécessaire
"""
import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire parent au path
BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_monitoring_files():
    """Vérifier si les fichiers de monitoring existent"""
    monitoring_dir = Path('.monitoring')
    
    if not monitoring_dir.exists():
        logger.warning("Monitoring directory does not exist. Creating it...")
        monitoring_dir.mkdir(parents=True, exist_ok=True)
        return True
    
    # Vérifier les fichiers d'historique
    history_file = monitoring_dir / 'predictions_history.json'
    metrics_file = monitoring_dir / 'performance_metrics.json'
    
    logger.info(f"History file exists: {history_file.exists()}")
    logger.info(f"Metrics file exists: {metrics_file.exists()}")
    
    return True

def check_alerts():
    """Vérifier s'il y a des alertes récentes"""
    alerts_dir = Path('.monitoring/alerts')
    
    if not alerts_dir.exists():
        logger.info("No alerts directory found. No alerts detected.")
        return False
    
    # Chercher les alertes des dernières 24h
    alert_files = list(alerts_dir.glob('*.json'))
    
    if not alert_files:
        logger.info("No alert files found.")
        return False
    
    # Filtrer les alertes récentes (dernières 24h)
    recent_alerts = []
    cutoff_time = datetime.now().timestamp() - (24 * 3600)
    
    for alert_file in alert_files:
        if alert_file.stat().st_mtime > cutoff_time:
            recent_alerts.append(alert_file)
    
    if recent_alerts:
        logger.warning(f"Found {len(recent_alerts)} recent alert(s):")
        for alert_file in recent_alerts:
            logger.warning(f"  - {alert_file.name}")
        return True
    
    logger.info("No recent alerts found.")
    return False

def check_mlflow_setup():
    """Vérifier si MLflow est configuré (sans charger les modèles)"""
    try:
        import mlflow
        logger.info("MLflow is available")
        
        # Vérifier si le tracking URI est accessible (sans charger de modèles)
        tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'file:./.mlflow')
        logger.info(f"MLflow tracking URI: {tracking_uri}")
        
        # Vérifier que le répertoire existe
        if tracking_uri.startswith('file:'):
            mlflow_dir = tracking_uri.replace('file:', '')
            if Path(mlflow_dir).exists():
                logger.info(f"✓ MLflow directory exists: {mlflow_dir}")
            else:
                logger.warning(f"⚠ MLflow directory does not exist: {mlflow_dir}")
        
        return True
    except ImportError:
        logger.warning("MLflow is not installed. Some features may not work.")
        return False
    except Exception as e:
        logger.warning(f"⚠ MLflow check failed: {e}")
        return False

def main():
    """Fonction principale"""
    logger.info("=" * 60)
    logger.info("Starting ML Monitoring Checks")
    logger.info("=" * 60)
    
    exit_code = 0
    
    # 1. Vérifier les fichiers de monitoring
    logger.info("\n[1/4] Checking monitoring files...")
    try:
        check_monitoring_files()
        logger.info("✓ Monitoring files check passed")
    except Exception as e:
        logger.error(f"✗ Error checking monitoring files: {e}")
        exit_code = 1
    
    # 2. Vérifier MLflow
    logger.info("\n[2/4] Checking MLflow setup...")
    try:
        mlflow_ok = check_mlflow_setup()
        if mlflow_ok:
            logger.info("✓ MLflow setup check passed")
        else:
            logger.warning("⚠ MLflow not fully configured")
    except Exception as e:
        logger.error(f"✗ Error checking MLflow: {e}")
        exit_code = 1
    
    # 3. Vérifier les alertes
    logger.info("\n[3/4] Checking for alerts...")
    try:
        has_alerts = check_alerts()
        if has_alerts:
            logger.warning("⚠ Recent alerts detected!")
            exit_code = 1
        else:
            logger.info("✓ No recent alerts found")
    except Exception as e:
        logger.error(f"✗ Error checking alerts: {e}")
        exit_code = 1
    
    # 4. Résumé
    logger.info("\n[4/4] Summary...")
    logger.info("=" * 60)
    if exit_code == 0:
        logger.info("✓ All monitoring checks passed")
    else:
        logger.warning("⚠ Some monitoring checks failed or alerts detected")
    logger.info("=" * 60)
    
    return exit_code

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Fatal error in monitoring script: {e}", exc_info=True)
        sys.exit(1)

