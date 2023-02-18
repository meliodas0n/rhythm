    """
   def playsong(self):
     current_song = self.playlist.get(ACTIVE)
     self.track.set(current_song)
     self.status.set("Playing")
     playable_song = current_song.split('.')[0]
     if os.path.exists(f'{playable_song}.ogg'):
       playable_song = f'{playable_song}.ogg'
       pygame.mixer.music.load(playable_song)
       pygame.mixer.music.play()
     else:
       try:
         s = subprocess.call(['ffmpeg', '-i', current_song, f'{playable_song}.ogg'])
         if s == 0:
           playable_song = f'{playable_song}.ogg'
           pygame.mixer.music.load(playable_song)
           pygame.mixer.music.play()
         else:
           print('u suck - conversion failed')
       except Exception as e:
         print(e)
      """
