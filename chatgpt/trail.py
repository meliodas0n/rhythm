import pygame
import pgzero

# # Initialize Pygame Zero
# pgzero.init()

# Initialize Pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()

# Set the window size
WIDTH = 800
HEIGHT = 600

# Create a list of songs
# songs = ['song1.mp3', 'song2.mp3', 'song3.mp3']
songs = ['chatgpt/sundown.mp3']

# Set the current song index
current_song = 0

# Load the first song
pygame.mixer.music.load(songs[current_song])

# Set the volume (0.0 to 1.0)
pygame.mixer.music.set_volume(0.5)

def draw():
    # Clear the screen
    screen.clear()

    # Draw the current song text
    screen.draw.text("Current Song: " + songs[current_song], (10, 10), color='black')

    # Draw the play button
    screen.draw.filled_rect(pgzero.rect((10, 50), (50, 50)), (0, 255, 0))
    screen.draw.text("Play", (20, 65), color='black')

    # Draw the pause button
    screen.draw.filled_rect(pgzero.rect((70, 50), (50, 50)), (255, 255, 0))
    screen.draw.text("Pause", (80, 65), color='black')

    # Draw the stop button
    screen.draw.filled_rect(pgzero.rect((130, 50), (50, 50)), (255, 0, 0))
    screen.draw.text("Stop", (140, 65), color='black')

    # Draw the song list
    screen.draw.text("Song List:", (10, 120), color='black')
    for i, song in enumerate(songs):
        screen.draw.text(song, (10, 150 + i * 30), color='black')

def on_mouse_down(pos, button):
    # Get the mouse position
    x, y = pos

    # Check if the play button was clicked
    if x >= 10 and x <= 60 and y >= 50 and y <= 100:
        # Play the current song
        pygame.mixer.music.play()

    # Check if the pause button was clicked
    elif x >= 70 and x <= 120 and y >= 50 and y <= 100:
        # Pause the current song
        pygame.mixer.music.pause()

    # Check if the stop button was clicked
    elif x >= 130 and x <= 180 and y >= 50 and y <= 100:
        # Stop the current song
        pygame.mixer.music.stop()

pgzero.run()
