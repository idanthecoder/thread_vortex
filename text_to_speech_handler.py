import os
import pygame
from gtts import gTTS


pygame.init()
pygame.mixer.init()

def speak_text(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang="en")
    
    # Specify the full path to save the file
    file_path = os.path.join(os.getcwd(), "temp.mp3")

    # Save the audio to the specified file path
    tts.save(file_path)
    print("file created")
    
    # Load and play the audio file
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        #threading.Thread(target=check_finish_speech).start()
        
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)  # Delay for 100 milliseconds
        
        pygame.mixer.music.unload()
        os.remove(os.path.join(os.getcwd(), "temp.mp3"))

        
    except pygame.error:
        print("mixer error")

def stop_speech():
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        print("mixer error")
        

def check_finish_speech():
    while pygame.mixer.get_busy():
        continue
    if not pygame.mixer.get_busy():
        pygame.mixer.music.unload()
        os.remove(os.path.join(os.getcwd(), "temp.mp3"))
    
if __name__ == "__main__":
    speak_text("Hello world, this is the captain speaking.")
