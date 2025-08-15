import discord
from discord.ext import commands
import asyncio
import os
import subprocess
from keep_alive import keep_alive

# Install FFmpeg on startup
def install_ffmpeg():
    """Install FFmpeg if not already installed"""
    try:
        # Check if FFmpeg is already installed
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("FFmpeg is already installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg not found, installing...")
        try:
            # Install FFmpeg using the installation script
            import install_ffmpeg
            install_ffmpeg.install()
            return True
        except Exception as e:
            print(f"Failed to install FFmpeg: {e}")
            return False

# Install FFmpeg before starting the bot
if not install_ffmpeg():
    print("Could not install FFmpeg. Bot may not work properly.")

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Global variables for music playback
current_voice_client = None
music_folder = "./music"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

@bot.command(name='join')
async def join_voice_channel(ctx):
    """Join the voice channel that the user is currently in"""
    global current_voice_client
    
    if ctx.author.voice is None:
        await ctx.send("❌ Vous devez être dans un canal vocal!")
        return
    
    voice_channel = ctx.author.voice.channel
    
    try:
        # If already connected to the same channel
        if current_voice_client and current_voice_client.channel == voice_channel:
            await ctx.send(f"✅ Déjà connecté à **{voice_channel.name}**!")
            return
        
        # Disconnect from current channel if connected elsewhere
        if current_voice_client is not None:
            await current_voice_client.disconnect()
        
        current_voice_client = await voice_channel.connect(timeout=60.0, reconnect=True)
        await ctx.send(f"✅ Rejoint **{voice_channel.name}** - Prêt à jouer de la musique!")
        
    except Exception as e:
        await ctx.send(f"❌ Impossible de rejoindre le canal vocal: {str(e)}")
        print(f"Error joining voice channel: {e}")

@bot.command(name='leave')
async def leave_voice_channel(ctx):
    """Leave the current voice channel"""
    global current_voice_client
    
    if current_voice_client is None:
        await ctx.send("❌ Bot is not connected to any voice channel!")
        return
    
    try:
        await current_voice_client.disconnect()
        current_voice_client = None
        await ctx.send("✅ Left the voice channel")
        
    except Exception as e:
        await ctx.send(f"❌ Failed to leave voice channel: {str(e)}")
        print(f"Error leaving voice channel: {e}")

@bot.command(name='play')
async def play_music(ctx, *, filename):
    """Play an MP3 file from the music folder"""
    global current_voice_client
    
    if current_voice_client is None:
        await ctx.send("❌ Bot is not connected to any voice channel! Use `!join` first.")
        return
    
    if current_voice_client.is_playing():
        await ctx.send("❌ Already playing audio! Use `!stop` to stop current playback.")
        return
    
    # Clean filename and ensure it has .mp3 extension
    filename = filename.strip()
    if not filename.endswith('.mp3'):
        filename += '.mp3'
    
    file_path = os.path.join(music_folder, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        await ctx.send(f"❌ File `{filename}` not found in music folder!")
        return
    
    try:
        # Test if file can be accessed
        if not os.access(file_path, os.R_OK):
            await ctx.send(f"❌ Cannot access file `{filename}` - permission denied")
            return
        
        # Try FFmpegOpusAudio first (more stable on Linux), fallback to PCM
        try:
            audio_source = discord.FFmpegOpusAudio(file_path)
            print(f"Using Opus audio source for {filename}")
        except Exception as opus_error:
            print(f"Opus failed, trying PCM: {opus_error}")
            audio_source = discord.FFmpegPCMAudio(file_path)
        
        # Play the audio with detailed error reporting
        def after_playing(error):
            if error:
                print(f'Playback finished with error: {error}')
            else:
                print('Playback finished successfully')
        
        current_voice_client.play(audio_source, after=after_playing)
        
        await ctx.send(f"🎵 Now playing: `{filename}`")
        
    except Exception as e:
        await ctx.send(f"❌ Failed to play audio: {str(e)}")
        print(f"Error playing audio: {e}")
        print(f"File path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        print(f"File readable: {os.access(file_path, os.R_OK) if os.path.exists(file_path) else 'N/A'}")

@bot.command(name='stop')
async def stop_music(ctx):
    """Stop the currently playing audio"""
    global current_voice_client
    
    if current_voice_client is None:
        await ctx.send("❌ Bot is not connected to any voice channel!")
        return
    
    if not current_voice_client.is_playing():
        await ctx.send("❌ No audio is currently playing!")
        return
    
    try:
        current_voice_client.stop()
        await ctx.send("⏹️ Stopped audio playback")
        
    except Exception as e:
        await ctx.send(f"❌ Failed to stop audio: {str(e)}")
        print(f"Error stopping audio: {e}")

@bot.command(name='list')
async def list_music(ctx):
    """List available MP3 files with interactive play buttons"""
    try:
        if not os.path.exists(music_folder):
            await ctx.send("❌ Dossier music introuvable!")
            return
        
        mp3_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
        
        if not mp3_files:
            await ctx.send("📁 Aucun fichier MP3 trouvé dans le dossier music")
            return
        
        from discord.ui import View, Button
        
        class MusicListView(View):
            def __init__(self):
                super().__init__(timeout=300)  # 5 minutes timeout
                
                # Add buttons for each music file (max 25 buttons per view)
                for i, filename in enumerate(sorted(mp3_files)[:25]):
                    # Truncate filename for button label
                    display_name = filename[:-4] if filename.endswith('.mp3') else filename
                    if len(display_name) > 80:
                        display_name = display_name[:77] + "..."
                    
                    button = Button(
                        label=display_name,
                        style=discord.ButtonStyle.green,
                        emoji="🎵",
                        custom_id=f"play_{i}"
                    )
                    button.callback = self.create_play_callback(filename)
                    self.add_item(button)
            
            def create_play_callback(self, filename):
                async def play_callback(interaction):
                    global current_voice_client
                    await interaction.response.defer()
                    
                    # Check if user is in a voice channel
                    if not interaction.user.voice or not interaction.user.voice.channel:
                        await interaction.followup.send("❌ Vous devez être dans un canal vocal!")
                        return
                    
                    user_channel = interaction.user.voice.channel
                    
                    # Auto-join if not connected or in different channel
                    if not current_voice_client or current_voice_client.channel != user_channel:
                        try:
                            if current_voice_client:
                                await current_voice_client.disconnect()
                            current_voice_client = await user_channel.connect()
                            await interaction.followup.send(f"🎵 Rejoint **{user_channel.name}** et joue **{filename[:-4]}**")
                        except Exception as e:
                            await interaction.followup.send(f"❌ Impossible de rejoindre le canal: {str(e)}")
                            return
                    else:
                        await interaction.followup.send(f"🎵 Lecture de **{filename[:-4]}**")
                    
                    # Stop current audio if playing
                    if current_voice_client.is_playing():
                        current_voice_client.stop()
                    
                    # Play the selected file
                    try:
                        file_path = os.path.join(music_folder, filename)
                        audio_source = discord.FFmpegOpusAudio(file_path)
                        current_voice_client.play(audio_source)
                        print(f"Using Opus audio source for {filename}")
                    except Exception as e:
                        await interaction.followup.send(f"❌ Erreur lors de la lecture: {str(e)}")
                        print(f"Error playing {filename}: {e}")
                
                return play_callback
        
        # Create embed showing the music library
        embed = discord.Embed(
            title="🎵 Bibliothèque Musicale",
            description=f"**{len(mp3_files)} fichiers disponibles**\n\nCliquez sur un bouton pour jouer instantanément:",
            color=0x7289da
        )
        
        embed.add_field(
            name="🤖 Fonctionnement Automatique",
            value="• Le bot rejoindra automatiquement votre canal vocal\n• Aucune commande à taper, juste cliquer!",
            inline=False
        )
        
        if len(mp3_files) > 25:
            embed.add_field(
                name="⚠️ Note",
                value=f"Seuls les 25 premiers fichiers sont affichés. Total: {len(mp3_files)} fichiers.",
                inline=False
            )
        
        embed.set_footer(text="💡 Vous devez être dans un canal vocal pour que ça marche")
        
        view = MusicListView()
        await ctx.send(embed=embed, view=view)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur lors du listage: {str(e)}")
        print(f"Error listing files: {e}")

@bot.command(name='aide')
async def help_command(ctx):
    """Show help with interactive buttons"""
    from discord.ui import View, Button
    
    help_embed = discord.Embed(
        title="🎵 Bot Musical Discord",
        description="Voici toutes les commandes disponibles :",
        color=0x7289da
    )
    
    help_embed.add_field(
        name="📻 Commandes Audio",
        value="`!join` - Rejoindre votre canal vocal\n"
              "`!play <fichier>` - Jouer un fichier MP3\n"
              "`!stop` - Arrêter la lecture\n"
              "`!leave` - Quitter le canal vocal",
        inline=False
    )
    
    help_embed.add_field(
        name="📋 Commandes Info",
        value="`!list` - Voir tous les fichiers disponibles\n"
              "`!status` - Statut du bot\n"
              "`!aide` - Afficher cette aide",
        inline=False
    )
    
    # Create view with music selection buttons
    class MusicView(View):
        def __init__(self):
            super().__init__(timeout=300)  # 5 minutes timeout
            
        @discord.ui.button(label="🎵 Voir Musiques", style=discord.ButtonStyle.primary)
        async def show_music(self, interaction: discord.Interaction, button: Button):
            await self.show_music_list(interaction)
            
        @discord.ui.button(label="ℹ️ Statut Bot", style=discord.ButtonStyle.secondary)
        async def show_status(self, interaction: discord.Interaction, button: Button):
            await self.show_bot_status(interaction)
            
        async def show_music_list(self, interaction):
            try:
                if not os.path.exists(music_folder):
                    await interaction.response.send_message("❌ Dossier musique introuvable !", ephemeral=True)
                    return
                
                mp3_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
                
                if not mp3_files:
                    await interaction.response.send_message("📁 Aucun fichier MP3 trouvé", ephemeral=True)
                    return
                
                # Create music selection view
                music_view = MusicSelectionView(mp3_files)
                
                embed = discord.Embed(
                    title="🎵 Musiques Disponibles",
                    description="Cliquez sur un bouton pour jouer une musique :",
                    color=0x43b581
                )
                
                file_list = "\n".join(f"• {file}" for file in sorted(mp3_files))
                embed.add_field(name="Fichiers", value=file_list, inline=False)
                
                await interaction.response.send_message(embed=embed, view=music_view, ephemeral=True)
                
            except Exception as e:
                await interaction.response.send_message(f"❌ Erreur : {str(e)}", ephemeral=True)
                
        async def show_bot_status(self, interaction):
            global current_voice_client
            
            embed = discord.Embed(title="🤖 Statut du Bot", color=0x7289da)
            
            if current_voice_client is None:
                embed.add_field(name="🔊 Vocal", value="Non connecté", inline=True)
            else:
                embed.add_field(name="🔊 Vocal", value=f"Connecté à {current_voice_client.channel.name}", inline=True)
                if current_voice_client.is_playing():
                    embed.add_field(name="🎵 Audio", value="En lecture", inline=True)
                else:
                    embed.add_field(name="🎵 Audio", value="Arrêté", inline=True)
            
            try:
                mp3_count = len([f for f in os.listdir(music_folder) if f.endswith('.mp3')])
                embed.add_field(name="📁 Musiques", value=f"{mp3_count} fichiers MP3", inline=True)
            except:
                embed.add_field(name="📁 Musiques", value="Impossible de vérifier", inline=True)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    class MusicSelectionView(View):
        def __init__(self, mp3_files):
            super().__init__(timeout=300)
            self.mp3_files = mp3_files
            
            # Add buttons for each MP3 file (max 25 buttons per view)
            for i, file in enumerate(mp3_files[:25]):  # Discord limit
                filename_without_ext = file.replace('.mp3', '')
                # Truncate long filenames for button labels
                label = filename_without_ext[:80] if len(filename_without_ext) > 80 else filename_without_ext
                button = Button(
                    label=label,
                    style=discord.ButtonStyle.success,
                    custom_id=f"play_{i}"
                )
                button.callback = self.create_play_callback(file)
                self.add_item(button)
        
        def create_play_callback(self, filename):
            async def play_callback(interaction):
                global current_voice_client
                await interaction.response.defer(ephemeral=True)
                
                # Check if user is in a voice channel
                if not interaction.user.voice or not interaction.user.voice.channel:
                    await interaction.followup.send("❌ Vous devez être dans un canal vocal!")
                    return
                
                user_channel = interaction.user.voice.channel
                
                # Auto-join if not connected or in different channel
                if not current_voice_client or current_voice_client.channel != user_channel:
                    try:
                        if current_voice_client:
                            await current_voice_client.disconnect()
                        current_voice_client = await user_channel.connect()
                        await interaction.followup.send(f"🎵 Rejoint **{user_channel.name}** et joue **{filename[:-4]}**")
                    except Exception as e:
                        await interaction.followup.send(f"❌ Impossible de rejoindre le canal: {str(e)}")
                        return
                else:
                    await interaction.followup.send(f"🎵 Lecture de **{filename[:-4]}**")
                
                # Stop current audio if playing
                if current_voice_client.is_playing():
                    current_voice_client.stop()
                
                file_path = os.path.join(music_folder, filename)
                
                if not os.path.exists(file_path):
                    await interaction.followup.send(f"❌ Fichier `{filename}` introuvable !")
                    return
                
                try:
                    audio_source = discord.FFmpegOpusAudio(file_path)
                    
                    def after_playing(error):
                        if error:
                            print(f'Playback finished with error: {error}')
                        else:
                            print('Playback finished successfully')
                    
                    current_voice_client.play(audio_source, after=after_playing)
                    print(f"Using Opus audio source for {filename}")
                    
                except Exception as e:
                    await interaction.followup.send(f"❌ Erreur de lecture : {str(e)}")
                    print(f"Error playing {filename}: {e}")
                    
            return play_callback
    
    view = MusicView()
    await ctx.send(embed=help_embed, view=view)

@bot.command(name='status')
async def bot_status(ctx):
    """Show bot status and connection info"""
    global current_voice_client
    
    status_msg = "🤖 **Bot Status:**\n"
    
    if current_voice_client is None:
        status_msg += "• Voice: Not connected\n"
    else:
        status_msg += f"• Voice: Connected to {current_voice_client.channel.name}\n"
        if current_voice_client.is_playing():
            status_msg += "• Audio: Playing\n"
        else:
            status_msg += "• Audio: Stopped\n"
    
    # Check music folder
    try:
        mp3_count = len([f for f in os.listdir(music_folder) if f.endswith('.mp3')])
        status_msg += f"• Music files: {mp3_count} MP3s available\n"
    except:
        status_msg += "• Music files: Unable to check\n"
    
    await ctx.send(status_msg)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found! Available commands: `!join`, `!play`, `!stop`, `!leave`, `!list`, `!status`")
    elif isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.name == 'play':
            await ctx.send("❌ Please specify a filename! Usage: `!play <filename>`")
        else:
            await ctx.send(f"❌ Missing required argument for `!{ctx.command.name}`")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Command error: {error}")

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state updates - disconnect if alone in channel"""
    global current_voice_client
    
    if current_voice_client is None:
        return
    
    # Don't auto-disconnect for now to avoid connection issues
    # Check if bot is alone in voice channel
    # if len(current_voice_client.channel.members) == 1:  # Only the bot
    #     await asyncio.sleep(300)  # Wait 5 minutes
    #     if current_voice_client and len(current_voice_client.channel.members) == 1:
    #         print("Bot alone in channel for 5 minutes, disconnecting...")
    #         await current_voice_client.disconnect()
    #         current_voice_client = None

def main():
    # Create music folder if it doesn't exist
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)
        print(f"Created music folder: {music_folder}")
    
    # Install FFmpeg if needed (only when running directly, not from render_main)
    import sys
    if 'render_main' not in sys.modules:
        install_ffmpeg()
        # Start keep-alive server in background
        keep_alive()
    
    # Get Discord bot token from environment
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ DISCORD_TOKEN environment variable not set!")
        print("Please set your Discord bot token in the secrets.")
        return
    
    try:
        # Run the bot
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Invalid Discord token! Please check your DISCORD_TOKEN.")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")

if __name__ == "__main__":
    main()
