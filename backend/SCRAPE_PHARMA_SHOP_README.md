# Script de Scraping Pharma-Shop.tn

## Description
Ce script Python scrape tous les produits depuis https://pharma-shop.tn/839-visage (2383 produits) et les sauvegardent directement dans la base de données Django.

## Prérequis
- Python 3.8+
- Django configuré
- Dépendances installées : `requests`, `beautifulsoup4`

## Utilisation

### Méthode 1 : Via Django Shell (Recommandé)
```bash
cd skin-twin-ai/backend
python manage.py shell < scrape_pharma_shop.py
```

### Méthode 2 : Exécution directe
```bash
cd skin-twin-ai/backend
python scrape_pharma_shop.py
```

## Fonctionnalités
- ✅ Scrape automatiquement toutes les pages (détection automatique du nombre de pages)
- ✅ Extrait : nom, marque, prix, image, URL, catégorie, taille
- ✅ Détecte automatiquement les catégories et problèmes ciblés
- ✅ Évite les doublons (basé sur l'URL)
- ✅ Sauvegarde directement dans la base de données Django
- ✅ Affiche la progression en temps réel
- ✅ Gère les erreurs et timeouts

## Temps estimé
- ~100 pages × 2 minutes/page = ~200 minutes (3h20)
- Le script fait une pause de 1.5 secondes entre chaque page pour éviter les blocages

## Résultat attendu
- 2383 produits scrapés et sauvegardés dans la base de données
- Statistiques détaillées affichées à la fin





