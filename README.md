# Orchestration des Vulnérabilités avec DefectDojo

Plateforme centralisée de gestion des vulnérabilités utilisant DefectDojo et des analyseurs open-source.

## 📋 Description

Ce projet implémente une solution d'orchestration automatisée pour la détection, la centralisation et l'analyse des vulnérabilités de sécurité. Il intègre plusieurs outils open-source spécialisés avec la plateforme DefectDojo pour offrir une vue unifiée de l'état de sécurité.

### Outils intégrés

- **Nmap** : Analyse réseau et découverte de services
- **OpenVAS** : Évaluation des vulnérabilités système
- **OWASP ZAP** : Tests de sécurité applicative (DAST)
- **Trivy** : Analyse des conteneurs Docker et dépendances

## 🎯 Objectifs

- Centraliser la gestion des vulnérabilités dans une plateforme unique
- Automatiser les processus de scan et d'import des résultats
- Normaliser et corréler les vulnérabilités détectées
- Faciliter le suivi et la priorisation des risques

## 🏗️ Architecture

```
┌─────────────┐
│ Orchestration│
│  (run_all.py)│
└──────┬──────┘
       │
   ┌───┴────┬─────────┬─────────┐
   │        │         │         │
┌──▼──┐ ┌──▼──┐ ┌────▼───┐ ┌──▼──┐
│Nmap │ │ ZAP │ │OpenVAS │ │Trivy│
└──┬──┘ └──┬──┘ └────┬───┘ └──┬──┘
   │       │         │        │
   └───────┴─────────┴────────┘
              │
      ┌───────▼────────┐
      │  Résultats     │
      │  (XML/JSON)    │
      └───────┬────────┘
              │
      ┌───────▼────────┐
      │ upload_scans.py│
      └───────┬────────┘
              │
      ┌───────▼────────┐
      │  API REST      │
      │  DefectDojo    │
      └───────┬────────┘
              │
      ┌───────▼────────┐
      │  PostgreSQL    │
      │  + Dashboard   │
      └────────────────┘
```

## 🚀 Installation

### Prérequis

- Ubuntu 22.04 LTS (ou similaire)
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.8+
- 4 CPU cores, 8 Go RAM minimum

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/orchestration-vulnerabilities.git
cd orchestration-vulnerabilities
```

### 2. Installer DefectDojo

```bash
# Cloner DefectDojo
git clone https://github.com/DefectDojo/django-DefectDojo
cd django-DefectDojo

# Lancer avec Docker Compose
docker-compose up -d
```

Accéder à DefectDojo : `http://localhost:8080`

### 3. Installer les scanners

**Nmap**
```bash
sudo apt update
sudo apt install nmap -y
```

**OWASP ZAP**
```bash
docker pull zaproxy/zap-stable
```

**Trivy**
```bash
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install trivy -y
```

**OpenVAS**
```bash
docker pull greenbone/openvas
docker run -d -p 9393:9392 --name openvas greenbone/openvas
```

### 4. Configurer les scripts

```bash
cd scripts/

# Créer un fichier de configuration
cp config.example.py config.py

# Éditer avec vos paramètres
nano config.py
```

Ajoutez votre clé API DefectDojo dans `config.py` :

```python
DEFECTDOJO_URL = "http://localhost:8080"
API_KEY = "votre_cle_api_ici"
PRODUCT_ID = 1
ENGAGEMENT_ID = 1
```

### 5. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

## 📖 Utilisation

### Lancer tous les scans

```bash
python3 scripts/run_all.py
```

### Lancer un scan spécifique

```bash
# Nmap uniquement
nmap -sV -oX scans/nmap_result.xml 192.168.85.0/24

# ZAP uniquement
docker run --rm --network host -v $(pwd):/zap/wrk \
  zaproxy/zap-stable zap-baseline.py \
  -t http://localhost:8081 -x /zap/wrk/scans/zap_result.xml

# Trivy uniquement
trivy image --format json -o scans/trivy_result.json nginx:latest
```

### Importer les résultats dans DefectDojo

```bash
python3 scripts/upload_scans.py "Nmap Scan" scans/nmap_result.xml
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` :

```env
DEFECTDOJO_URL=http://localhost:8080
DEFECTDOJO_API_KEY=votre_cle_api
PRODUCT_ID=1
ENGAGEMENT_ID=1
DVWA_URL=http://localhost:8081
NMAP_NETWORK=192.168.85.0/24
```

### Personnalisation des scans

Éditez `scripts/run_all.py` pour modifier :
- Les cibles de scan
- Les types d'analyses
- Les paramètres des scanners

## 📊 Résultats

Après exécution, consultez DefectDojo pour visualiser :
- Vulnérabilités par criticité (Critical, High, Medium, Low)
- Répartition par type de vulnérabilité
- Tendances et évolution dans le temps
- Rapports exportables (PDF, Excel, JSON)

## 🔒 Sécurité

⚠️ **IMPORTANT** : 
- Ne jamais commiter de clés API
- Utiliser uniquement en environnement de test isolé
- Ne pas scanner de systèmes sans autorisation
- Respecter les politiques de sécurité de votre organisation

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

Projet réalisé dans le cadre du module Ethical Hacking :
- Laila Hammouch
- Aya Abbadi
- Ahmed Chater
- David Daouda Coulibaly
- Khalid Baghdadi

**Encadré par** : Pr. Yassine Maleh

## 📚 Ressources

- [Documentation DefectDojo](https://documentation.defectdojo.com/)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [OpenVAS Documentation](https://greenbone.github.io/docs/)

## 🐛 Problèmes connus

- Les scans OpenVAS peuvent prendre plusieurs heures
- ZAP nécessite une configuration proxy pour certains scans
- Trivy nécessite un accès internet pour les mises à jour CVE

## 🔮 Roadmap

- [ ] Intégration CI/CD (GitLab CI, GitHub Actions)
- [ ] Support des scans cloud (AWS, Azure, GCP)
- [ ] Interface web de gestion
- [ ] Notifications automatiques (email, Slack)
- [ ] Scanners additionnels (Nikto, WPScan, Clair)

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile sur GitHub !
