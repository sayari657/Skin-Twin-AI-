<?php
// Script pour utiliser SQLite avec XAMPP
$db_path = 'db.sqlite3';

echo "<h1>🗄️ Base de Données SQLite dans XAMPP</h1>";

if (!file_exists($db_path)) {
    echo "<p style='color: red;'>❌ Fichier de base de données non trouvé : $db_path</p>";
    exit;
}

try {
    $pdo = new PDO("sqlite:$db_path");
    echo "<p style='color: green;'>✅ Connexion à la base de données réussie !</p>";
    
    // Lister les tables
    $tables = $pdo->query("SELECT name FROM sqlite_master WHERE type='table'")->fetchAll(PDO::FETCH_COLUMN);
    
    echo "<h2>📋 Tables disponibles :</h2>";
    echo "<ul>";
    foreach ($tables as $table) {
        echo "<li>$table</li>";
    }
    echo "</ul>";
    
    // Afficher les données des produits scrapés
    if (in_array('scraped_products_scrapedproduct', $tables)) {
        echo "<h2>🕷️ Produits Scrapés :</h2>";
        $products = $pdo->query("SELECT name, brand, price FROM scraped_products_scrapedproduct LIMIT 5")->fetchAll(PDO::FETCH_ASSOC);
        
        echo "<table border='1' style='border-collapse: collapse; width: 100%;'>";
        echo "<tr><th>Nom</th><th>Marque</th><th>Prix</th></tr>";
        foreach ($products as $product) {
            echo "<tr>";
            echo "<td>" . htmlspecialchars($product['name']) . "</td>";
            echo "<td>" . htmlspecialchars($product['brand']) . "</td>";
            echo "<td>" . $product['price'] . "€</td>";
            echo "</tr>";
        }
        echo "</table>";
    }
    
} catch (Exception $e) {
    echo "<p style='color: red;'>❌ Erreur : " . $e->getMessage() . "</p>";
}
?>




