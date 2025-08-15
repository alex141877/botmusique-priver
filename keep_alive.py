from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Discord Music Bot - Keep Alive</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px;
                    background-color: #2c2f33;
                    color: #ffffff;
                }
                .container { 
                    background-color: #36393f; 
                    padding: 30px; 
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                }
                h1 { color: #7289da; text-align: center; }
                .status { 
                    background-color: #43b581; 
                    padding: 10px; 
                    border-radius: 5px; 
                    text-align: center;
                    margin: 20px 0;
                }
                .info { 
                    background-color: #4f545c; 
                    padding: 15px; 
                    border-radius: 5px;
                    margin: 10px 0;
                }
                .commands {
                    background-color: #4f545c;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }
                .command {
                    background-color: #2c2f33;
                    padding: 8px;
                    margin: 5px 0;
                    border-radius: 3px;
                    font-family: monospace;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎵 Discord Music Bot</h1>
                <div class="status">
                    ✅ Keep-Alive Server Running
                </div>
                
                <div class="info">
                    <h3>📊 Server Status</h3>
                    <p><strong>Status:</strong> Online and Ready</p>
                    <p><strong>Purpose:</strong> 24/7 Discord Music Bot</p>
                    <p><strong>Uptime:</strong> Maintained by UptimeRobot</p>
                </div>
                
                <div class="commands">
                    <h3>🎮 Commandes Disponibles</h3>
                    <div class="command">!aide - Interface interactive avec boutons</div>
                    <div class="command">!join - Rejoindre votre canal vocal</div>
                    <div class="command">!play &lt;fichier&gt; - Jouer un fichier MP3</div>
                    <div class="command">!stop - Arrêter la lecture</div>
                    <div class="command">!leave - Quitter le canal vocal</div>
                    <div class="command">!list - Voir les fichiers MP3 disponibles</div>
                    <div class="command">!status - Statut du bot</div>
                </div>
                
                <div class="commands">
                    <h3>🎵 Fonctionnalités Interactives</h3>
                    <div class="command">• Boutons pour sélectionner et jouer les musiques</div>
                    <div class="command">• Interface d'aide avec contrôles visuels</div>
                    <div class="command">• Statut en temps réel du bot</div>
                    <div class="command">• Lecture directe sans taper les noms de fichiers</div>
                </div>
                
                <div class="info">
                    <h3>📁 Music Files</h3>
                    <p>Upload your MP3 files to the <code>music/</code> folder in your Replit project.</p>
                    <p>Files remain private and are only accessible through bot commands.</p>
                </div>
                
                <div class="info">
                    <h3>🚀 Comment Utiliser</h3>
                    <ol>
                        <li>Utilisez <code>!aide</code> pour voir l'interface interactive</li>
                        <li>Cliquez sur "🎵 Voir Musiques" pour accéder à vos fichiers</li>
                        <li>Cliquez directement sur les boutons pour jouer vos MP3</li>
                        <li>Plus besoin de taper les noms de fichiers !</li>
                    </ol>
                </div>
                
                <div class="info">
                    <h3>🔧 Configuration</h3>
                    <ol>
                        <li>Token Discord ajouté aux Secrets Replit comme <code>DISCORD_TOKEN</code> ✅</li>
                        <li>Téléchargez vos MP3 dans le dossier <code>music/</code></li>
                        <li>Utilisez UptimeRobot pour maintenir le bot 24h/24</li>
                        <li>Invitez le bot sur votre serveur Discord</li>
                    </ol>
                </div>
                
                <div class="info">
                    <h3>🔗 Pages Disponibles</h3>
                    <p><a href="/dashboard" style="color: #ffffff; text-decoration: none; background: rgba(114,137,218,0.8); padding: 12px 20px; border-radius: 8px; display: inline-block; margin: 8px 0; font-weight: bold;">📊 Dashboard Complet</a></p>
                    <p><small>Statut en temps réel + Liste des musiques qui se met à jour automatiquement</small></p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/status')
def status():
    """Simple status endpoint for monitoring"""
    return {
        "status": "online",
        "service": "discord-music-bot",
        "uptime": True
    }

@app.route('/dashboard')
def dashboard():
    """Dashboard page with live bot status and music list"""
    return """
    <html>
        <head>
            <title>Discord Music Bot - Dashboard</title>
            <meta charset="UTF-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #ffffff;
                    min-height: 100vh;
                }
                .dashboard {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .card { 
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    padding: 25px;
                    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                }
                .status-indicator {
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    margin-right: 8px;
                }
                .online { background-color: #43b581; }
                .offline { background-color: #f04747; }
                .music-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 15px;
                    margin-top: 20px;
                }
                .music-item {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transition: transform 0.2s;
                }
                .music-item:hover {
                    transform: translateY(-2px);
                    background: rgba(255, 255, 255, 0.15);
                }
                .refresh-btn {
                    background: #7289da;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    margin: 10px 0;
                    transition: background 0.2s;
                }
                .refresh-btn:hover {
                    background: #5b6eae;
                }
                .title { 
                    color: #ffffff; 
                    text-align: center; 
                    margin-bottom: 30px;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .last-update {
                    font-size: 0.9em;
                    opacity: 0.8;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <h1 class="title">🎵 Discord Music Bot Dashboard</h1>
            
            <div class="dashboard">
                <div class="card">
                    <h3>🤖 Statut du Bot</h3>
                    <div id="bot-status">
                        <div><span class="status-indicator online"></span>Chargement...</div>
                    </div>
                    <button class="refresh-btn" onclick="updateStatus()">🔄 Actualiser</button>
                </div>
                
                <div class="card">
                    <h3>📊 Informations</h3>
                    <div id="bot-info">
                        <p>Chargement des informations...</p>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>🎵 Bibliothèque Musicale</h3>
                <button class="refresh-btn" onclick="updateMusicList()">🔄 Actualiser la liste</button>
                <div id="music-list">
                    <p>Chargement de la liste musicale...</p>
                </div>
                <div class="last-update" id="last-update"></div>
            </div>

            <script>
                function updateStatus() {
                    fetch('/api/status')
                        .then(response => response.json())
                        .then(data => {
                            const statusDiv = document.getElementById('bot-status');
                            const infoDiv = document.getElementById('bot-info');
                            
                            let statusClass = data.bot_online ? 'online' : 'offline';
                            let statusText = data.bot_online ? 'En ligne' : 'Hors ligne';
                            
                            statusDiv.innerHTML = `
                                <div><span class="status-indicator ${statusClass}"></span>${statusText}</div>
                                <div>Connexion vocale: ${data.voice_connected ? '✅ Connecté' : '❌ Non connecté'}</div>
                                <div>Audio en cours: ${data.audio_playing ? '🎵 Oui' : '⏹️ Non'}</div>
                            `;
                            
                            infoDiv.innerHTML = `
                                <p>📁 Fichiers MP3: ${data.music_count}</p>
                                <p>🔧 FFmpeg: ${data.ffmpeg_available ? '✅ Disponible' : '❌ Indisponible'}</p>
                                <p>🔑 Token Discord: ${data.discord_token ? '✅ Configuré' : '❌ Manquant'}</p>
                            `;
                        })
                        .catch(error => {
                            document.getElementById('bot-status').innerHTML = 
                                '<div><span class="status-indicator offline"></span>Erreur de connexion</div>';
                        });
                }

                function updateMusicList() {
                    fetch('/api/music')
                        .then(response => response.json())
                        .then(data => {
                            const musicDiv = document.getElementById('music-list');
                            const updateDiv = document.getElementById('last-update');
                            
                            if (data.files && data.files.length > 0) {
                                const musicGrid = data.files.map(file => `
                                    <div class="music-item">
                                        <strong>🎵 ${file.name}</strong><br>
                                        <small>Taille: ${file.size}</small><br>
                                        <small>Ajouté: ${file.date}</small>
                                    </div>
                                `).join('');
                                
                                musicDiv.innerHTML = `<div class="music-grid">${musicGrid}</div>`;
                            } else {
                                musicDiv.innerHTML = '<p>📁 Aucun fichier MP3 trouvé dans le dossier music/</p>';
                            }
                            
                            updateDiv.innerHTML = `Dernière mise à jour: ${new Date().toLocaleString('fr-FR')}`;
                        })
                        .catch(error => {
                            document.getElementById('music-list').innerHTML = 
                                '<p>❌ Erreur lors du chargement de la liste musicale</p>';
                        });
                }

                // Auto-refresh every 30 seconds
                setInterval(() => {
                    updateStatus();
                    updateMusicList();
                }, 30000);

                // Initial load
                updateStatus();
                updateMusicList();
            </script>
        </body>
    </html>
    """

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    try:
        # Import here to avoid circular imports
        import discord
        import subprocess
        
        # Check if music folder exists and count files
        music_count = 0
        if os.path.exists('./music'):
            music_count = len([f for f in os.listdir('./music') if f.endswith('.mp3')])
        
        # Check if FFmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            ffmpeg_available = True
        except:
            ffmpeg_available = False
        
        return {
            "bot_online": True,  # If this endpoint responds, bot is running
            "voice_connected": False,  # This would need to be updated from main.py
            "audio_playing": False,   # This would need to be updated from main.py
            "music_count": music_count,
            "ffmpeg_available": ffmpeg_available,
            "discord_token": bool(os.getenv('DISCORD_TOKEN'))
        }
    except Exception as e:
        return {
            "bot_online": False,
            "error": str(e)
        }, 500

@app.route('/api/music')
def api_music():
    """API endpoint for music list"""
    try:
        music_files = []
        
        if os.path.exists('./music'):
            for filename in os.listdir('./music'):
                if filename.endswith('.mp3'):
                    filepath = os.path.join('./music', filename)
                    stat = os.stat(filepath)
                    
                    # Format file size
                    size_bytes = stat.st_size
                    if size_bytes < 1024:
                        size_str = f"{size_bytes} B"
                    elif size_bytes < 1024**2:
                        size_str = f"{size_bytes/1024:.1f} KB"
                    else:
                        size_str = f"{size_bytes/(1024**2):.1f} MB"
                    
                    # Format date
                    import datetime
                    date_str = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M')
                    
                    music_files.append({
                        'name': filename,
                        'size': size_str,
                        'date': date_str
                    })
        
        # Sort by name
        music_files.sort(key=lambda x: x['name'].lower())
        
        return {
            "files": music_files,
            "count": len(music_files)
        }
    except Exception as e:
        return {
            "error": str(e),
            "files": []
        }, 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check if music folder exists
        music_folder_exists = os.path.exists('./music')
        
        # Check if FFmpeg is available
        import subprocess
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            ffmpeg_available = True
        except:
            ffmpeg_available = False
        
        return {
            "status": "healthy",
            "music_folder": music_folder_exists,
            "ffmpeg": ffmpeg_available,
            "discord_token": bool(os.getenv('DISCORD_TOKEN'))
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }, 500

def run():
    """Run the Flask server"""
    # Bind to 0.0.0.0:5000 for Replit compatibility
    app.run(host='0.0.0.0', port=5000, debug=False)

def keep_alive():
    """Start the keep-alive server in a separate thread"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("🌐 Keep-alive server started on http://0.0.0.0:5000")
