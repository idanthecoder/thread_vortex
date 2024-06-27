import os
import pygame
from gtts import gTTS


pygame.init()
pygame.mixer.init()

def speak_text(text):
    """
    Turn a given text into speech and play the sound that is created.
    The speech will be moved into a temporary mp3 file that will be deleted after the speech is done.

    Args:
        text (str): Text that will turn to speech.
    """
    
    # Create a gTTS object, set to English.
    tts = gTTS(text=text, lang="en")
    
    # Specify the full path to save the file (current working dir)
    file_path = os.path.join(os.getcwd(), "temp.mp3")

    # Save the audio as a file in the filepath
    tts.save(file_path)
    
    # Load and play the audio file
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)  # Delay for 100 milliseconds
        
        pygame.mixer.music.unload()
        os.remove(os.path.join(os.getcwd(), "temp.mp3"))

        
    except pygame.error:
        print("mixer error")

def stop_speech():
    """
    Stop the current running speech.
    """
    
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        print("mixer error")
