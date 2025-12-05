# 📦 Module d'Intégration - Diagnostic Dermatologique

Ce dossier contient tous les composants React/TypeScript nécessaires pour intégrer les sections de résultats de diagnostic dans votre projet Skin-Twin-AI.

## 📁 Structure

```
med/
├── components/           # Composants React
│   ├── QuickInfo.tsx           # 💧 Infos rapides
│   ├── DiagnosticSection.tsx   # 🩺 Diagnostic dermatologique
│   ├── AdviceSection.tsx       # 💡 Conseils pratiques
│   ├── RecommendationsSection.tsx  # 🛍️ Recommandations personnalisées
│   └── DiagnosisResults.tsx    # Composant principal (combine tout)
│
├── services/             # Services API
│   └── diagnosticApi.ts        # Communication avec Django backend
│
├── types/                # Types TypeScript
│   └── diagnostic.types.ts     # Interfaces et types
│
├── hooks/                # Hooks React personnalisés
│   └── useDiagnosis.ts         # Hook pour gérer les diagnostics
│
├── index.ts              # Exports principaux
└── README.md            # Ce fichier
```

## 🚀 Installation

### 1. Copier les fichiers dans votre projet React

Copiez tout le contenu du dossier `med/` dans votre projet React :

```bash
# Option 1 : Copier dans src/components/
cp -r med/ src/components/diagnostic/

# Option 2 : Copier à la racine de src/
cp -r med/ src/
```

### 2. Installer les dépendances

Assurez-vous d'avoir installé Material-UI :

```bash
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled
```

### 3. Configurer l'URL de l'API

Créez un fichier `.env` à la racine de votre projet React :

```env
REACT_APP_API_URL=http://localhost:8000
```

## 📖 Utilisation

### Option 1 : Utiliser le composant principal (recommandé)

```tsx
import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import DiagnosisResults from './med/components/DiagnosisResults';
import { useDiagnosis } from './med/hooks/useDiagnosis';

const ResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { diagnosis, loading, error, fetchDiagnosis } = useDiagnosis();
  
  useEffect(() => {
    if (id) {
      const token = localStorage.getItem('token');
      fetchDiagnosis(parseInt(id), token || undefined);
    }
  }, [id, fetchDiagnosis]);

  return (
    <DiagnosisResults 
      data={diagnosis} 
      loading={loading} 
      error={error} 
    />
  );
};

export default ResultsPage;
```

### Option 2 : Utiliser les composants individuellement

```tsx
import React from 'react';
import QuickInfo from './med/components/QuickInfo';
import DiagnosticSection from './med/components/DiagnosticSection';
import AdviceSection from './med/components/AdviceSection';
import RecommendationsSection from './med/components/RecommendationsSection';
import { DiagnosisResult } from './med/types/diagnostic.types';

const ResultsPage: React.FC<{ diagnosis: DiagnosisResult }> = ({ diagnosis }) => {
  return (
    <Container maxWidth="lg">
      <QuickInfo data={diagnosis.quickInfo} />
      <DiagnosticSection data={diagnosis.diagnostic} />
      <AdviceSection conseils={diagnosis.conseils_pratiques} />
      <RecommendationsSection recommendations={diagnosis.recommendations} />
    </Container>
  );
};
```

### Option 3 : Analyser une nouvelle image

```tsx
import React, { useState } from 'react';
import { useDiagnosis } from './med/hooks/useDiagnosis';
import DiagnosisResults from './med/components/DiagnosisResults';

const AnalyzePage: React.FC = () => {
  const { diagnosis, loading, error, analyzeImage } = useDiagnosis();
  const [imageFile, setImageFile] = useState<File | null>(null);

  const handleAnalyze = async () => {
    if (!imageFile) return;

    await analyzeImage(
      imageFile,
      {
        age: 25,
        gender: 'Female',
        sleep_hours: 7,
        stress_level: 5,
        diet_quality: 'Average',
        smoker: 'No',
        alcohol_consumption: 'No',
      },
      localStorage.getItem('token') || undefined
    );
  };

  return (
    <div>
      <input 
        type="file" 
        accept="image/*" 
        onChange={(e) => setImageFile(e.target.files?.[0] || null)} 
      />
      <button onClick={handleAnalyze}>Analyser</button>
      
      <DiagnosisResults data={diagnosis} loading={loading} error={error} />
    </div>
  );
};
```

## 🔌 Intégration avec Django Backend

### Endpoint requis dans Django

Votre backend Django doit exposer un endpoint `/api/analyze/` qui accepte :

**POST `/api/analyze/`**
- `file`: File (image)
- `age`: int
- `gender`: string
- `sleep_hours`: int
- `stress_level`: int
- `diet_quality`: string
- `smoker`: string
- `alcohol_consumption`: string
- `name`: string (optionnel)
- `email`: string (optionnel)
- `save_to_db`: boolean

**Réponse attendue :**
```json
{
  "success": true,
  "diagnosis_id": 1,
  "skin_type": "Normal",
  "skin_type_probs": {
    "Dry": 0.1,
    "Normal": 0.8,
    "Oily": 0.1
  },
  "confidence": 0.987,
  "detected_troubles": ["Acne", "Dark-Spots", "Dry-Skin", "Wrinkles"],
  "detections": [
    {
      "label": "Acne",
      "confidence": 0.75,
      "box": [100, 100, 200, 200]
    }
  ],
  "diagnostic": "L'examen dermatologique révèle...",
  "conseils_pratiques": "✅ Établir une routine...",
  "recommendations": [
    {
      "categorie": "Nettoyant visage",
      "produits": [
        {
          "nom": "La Roche-Posay Effaclar",
          "description_detaillee": "...",
          "links": [
            {
              "title": "Acheter sur...",
              "link": "https://...",
              "snippet": "..."
            }
          ]
        }
      ]
    }
  ],
  "annotated_image": "base64_string..."
}
```

## 🎨 Personnalisation

### Modifier les couleurs

Dans `QuickInfo.tsx`, modifiez les fonctions :
- `getSkinTypeColor()` : couleurs pour les types de peau
- `getSeverityColor()` : couleurs pour les sévérités

### Modifier le style

Tous les composants utilisent Material-UI. Vous pouvez :
- Modifier les props `sx` dans chaque composant
- Créer un thème personnalisé Material-UI
- Ajouter vos propres classes CSS

## 📝 Exemple complet d'intégration dans /results/

```tsx
// src/pages/ResultsPage.tsx
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Button, Box } from '@mui/material';
import DiagnosisResults from '../med/components/DiagnosisResults';
import { useDiagnosis } from '../med/hooks/useDiagnosis';

const ResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { diagnosis, loading, error, fetchDiagnosis } = useDiagnosis();

  useEffect(() => {
    if (id) {
      const token = localStorage.getItem('token');
      fetchDiagnosis(parseInt(id), token || undefined);
    }
  }, [id, fetchDiagnosis]);

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Button onClick={() => navigate('/dashboard')}>
          ← Retour au dashboard
        </Button>
      </Box>

      <DiagnosisResults data={diagnosis} loading={loading} error={error} />
    </Container>
  );
};

export default ResultsPage;
```

## ✅ Checklist d'intégration

- [ ] Copier tous les fichiers du dossier `med/` dans votre projet
- [ ] Installer Material-UI et ses dépendances
- [ ] Configurer `REACT_APP_API_URL` dans `.env`
- [ ] Créer l'endpoint `/api/analyze/` dans Django
- [ ] Tester l'analyse d'une image
- [ ] Tester l'affichage des résultats
- [ ] Personnaliser les styles si nécessaire

## 🆘 Dépannage

**Erreur : "Cannot find module"**
→ Vérifiez que tous les fichiers sont copiés et que les imports sont corrects

**Erreur CORS**
→ Configurez CORS dans Django pour accepter les requêtes depuis React

**Les données ne s'affichent pas**
→ Vérifiez le format de la réponse de l'API Django (doit correspondre à `AnalysisResponse`)

**Erreur TypeScript**
→ Vérifiez que tous les types sont correctement importés

---

**Prêt à intégrer !** 🚀

