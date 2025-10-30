<?php
// Interface web pour visualiser la base de données SQLite
$db_path = 'db.sqlite3';

if (!file_exists($db_path)) {
    die("❌ Base de données non trouvée : $db_path");
}

try {
    $pdo = new PDO("sqlite:$db_path");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Récupérer les tables
    $tables_query = "SELECT name FROM sqlite_master WHERE type='table'";
    $tables = $pdo->query($tables_query)->fetchAll(PDO::FETCH_COLUMN);
    
    // Statistiques
    $stats = [];
    
    // Compter les produits scrapés
    try {
        $stmt = $pdo->query("SELECT COUNT(*) FROM scraped_products_scrapedproduct");
        $stats['scraped_products'] = $stmt->fetchColumn();
    } catch (Exception $e) {
        $stats['scraped_products'] = 0;
    }
    
    // Compter les utilisateurs
    try {
        $stmt = $pdo->query("SELECT COUNT(*) FROM users_user");
        $stats['users'] = $stmt->fetchColumn();
    } catch (Exception $e) {
        $stats['users'] = 0;
    }
    
    // Derniers produits
    $recent_products = [];
    try {
        $stmt = $pdo->query("SELECT name, brand, price, category FROM scraped_products_scrapedproduct ORDER BY created_at DESC LIMIT 10");
        $recent_products = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (Exception $e) {
        $recent_products = [];
    }
    
} catch (Exception $e) {
    die("❌ Erreur de connexion à la base de données : " . $e->getMessage());
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🗄️ Base de Données Skin Twin AI</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1976d2, #42a5f5);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 3em;
            font-weight: bold;
            color: #1976d2;
            margin: 0;
        }
        
        .stat-label {
            color: #666;
            margin-top: 10px;
            font-size: 1.1em;
        }
        
        .section {
            margin: 40px 0;
        }
        
        .section h2 {
            color: #333;
            border-bottom: 3px solid #1976d2;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        
        th {
            background: linear-gradient(135deg, #f5f5f5, #e0e0e0);
            font-weight: 600;
            color: #333;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .tables-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .table-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #1976d2;
            transition: all 0.3s ease;
        }
        
        .table-card:hover {
            background: #e3f2fd;
            transform: translateX(5px);
        }
        
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #1976d2, #42a5f5);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin: 10px 5px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
        }
        
        .success {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗄️ Base de Données Skin Twin AI</h1>
            <p>Interface de visualisation SQLite via XAMPP</p>
        </div>
        
        <div class="content">
            <div class="success">
                ✅ <strong>Connexion réussie !</strong> Base de données SQLite chargée avec succès.
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number"><?php echo $stats['scraped_products']; ?></div>
                    <div class="stat-label">🕷️ Produits Scrapés</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><?php echo $stats['users']; ?></div>
                    <div class="stat-label">👥 Utilisateurs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><?php echo count($tables); ?></div>
                    <div class="stat-label">📋 Tables</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Tables Disponibles</h2>
                <div class="tables-list">
                    <?php foreach ($tables as $table): ?>
                    <div class="table-card">
                        <strong><?php echo htmlspecialchars($table); ?></strong>
                        <br>
                        <small>Table de données</small>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>
            
            <?php if (!empty($recent_products)): ?>
            <div class="section">
                <h2>🕷️ Derniers Produits Scrapés</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Marque</th>
                            <th>Prix</th>
                            <th>Catégorie</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($recent_products as $product): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($product['name']); ?></td>
                            <td><?php echo htmlspecialchars($product['brand']); ?></td>
                            <td><?php echo $product['price']; ?>€</td>
                            <td><?php echo htmlspecialchars($product['category']); ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <?php endif; ?>
            
            <div class="section">
                <h2>🔗 Liens Utiles</h2>
                <a href="http://127.0.0.1:8000/admin/" class="btn">Interface Django Admin</a>
                <a href="http://localhost:3000/products" class="btn">Page des Produits</a>
                <a href="http://localhost/phpmyadmin/" class="btn">phpMyAdmin</a>
            </div>
            
            <div class="section">
                <h2>📊 Informations Techniques</h2>
                <p><strong>Chemin de la base :</strong> <?php echo realpath($db_path); ?></p>
                <p><strong>Taille du fichier :</strong> <?php echo number_format(filesize($db_path) / 1024, 2); ?> KB</p>
                <p><strong>Date de modification :</strong> <?php echo date('Y-m-d H:i:s', filemtime($db_path)); ?></p>
            </div>
        </div>
    </div>
</body>
</html>




