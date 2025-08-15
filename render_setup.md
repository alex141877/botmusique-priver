# Déploiement sur Render

## Fichiers créés pour Render

- `render_requirements.txt` - Dépendances Python pour Render
- `render_main.py` - Point d'entrée principal qui détecte l'environnement
- `render_install.py` - Installation FFmpeg pour Ubuntu (Render)
- `Procfile` - Configuration Render

## Instructions de déploiement

### 1. Préparer les fichiers
**Pour Render :**
1. Copiez tout le contenu de votre projet
2. Renommez `render_requirements.txt` en `requirements.txt`
3. Le script `render_main.py` sera utilisé comme point d'entrée

**Pour rester sur Replit :**
- Rien à changer ! Le bot continue de fonctionner normalement

### 2. Configuration Render
1. Connectez votre repository GitHub à Render
2. Créez un nouveau "Web Service"
3. Configurez :
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python render_main.py`

### 3. Variables d'environnement
Ajoutez dans Render :
- `DISCORD_TOKEN` : Votre token Discord

### 4. Fonctionnalités conservées
✅ Interface Discord avec boutons interactifs
✅ Dashboard web accessible
✅ Auto-détection environnement (Render/Replit)
✅ Installation automatique FFmpeg
✅ Keep-alive system

## Différences Render vs Replit

**Render :**
- Port automatique via `$PORT`
- FFmpeg via apt-get Ubuntu
- Restart automatique en cas de crash

**Replit :**
- Port fixe 5000
- FFmpeg via nix/conda/apt
- Keep-alive manuel nécessaire

## Test local
```bash
python render_main.py
```

Le script détecte automatiquement l'environnement et s'adapte.