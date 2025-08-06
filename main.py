import cv2
import pytesseract
import time
from deep_translator import GoogleTranslator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from gtts import gTTS
import os
import RPi.GPIO as GPIO

# GPIO Pins
CAPTURE_BUTTON_PIN = 17
FULL_TEXT_BUTTON_PIN = 27
SUMMARY_BUTTON_PIN = 22
REPEAT_BUTTON_PIN = 23
PAUSE_BUTTON_PIN = 24  # You mentioned you changed this to 24

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAPTURE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FULL_TEXT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SUMMARY_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(REPEAT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PAUSE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to speak text with pause/resume capability
from threading import Thread, Event
import pygame

pygame.mixer.init()
pause_event = Event()
audio_file = "output.mp3"

def play_audio():
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if pause_event.is_set():
            pygame.mixer.music.pause()
            while pause_event.is_set():
                time.sleep(0.1)
            pygame.mixer.music.unpause()
        time.sleep(0.1)

def speak_text(text):
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(audio_file)
    Thread(target=play_audio).start()

# Translator
translator = GoogleTranslator(source='auto', target='en')

# Use USB webcam
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Tesseract language config
tesseract_languages = 'eng+deu+hin+mar'
custom_config = "--oem 3 --psm 3 --dpi 300"

# Store last outputs
last_translation = ""
last_summary = ""
last_output_type = None  # 'full' or 'summary'

# Summarizer
def summarize_text(text, num_sentences=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

while True:
    try:
        ret, frame = webcam.read()
        if not ret:
            print("Camera not detected.")
            break

        cv2.imshow("Live Feed", frame)
        cv2.waitKey(1)

        if GPIO.input(CAPTURE_BUTTON_PIN) == GPIO.LOW:
            time.sleep(0.2)
            print("Image Captured. Processing...")

            # Image Scaling (enlarge image)
            scaled_frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            extracted_text = pytesseract.image_to_string(scaled_frame, lang=tesseract_languages, config=custom_config)
            print("Extracted Text:\n", extracted_text)

            if extracted_text.strip():
                try:
                    translated_text = translator.translate(extracted_text)
                    last_translation = translated_text
                    print("\nTranslated Text:\n", translated_text)
                    print("Press 'Full Text' or 'Summary'...")

                    while True:
                        cv2.waitKey(1)

                        if GPIO.input(FULL_TEXT_BUTTON_PIN) == GPIO.LOW:
                            time.sleep(0.2)
                            print("Speaking full translated text...")
                            speak_text(translated_text)
                            last_output_type = 'full'
                            break

                        elif GPIO.input(SUMMARY_BUTTON_PIN) == GPIO.LOW:
                            time.sleep(0.2)
                            summary = summarize_text(translated_text)
                            print("Summarized Text:\n", summary)
                            speak_text(summary)
                            last_summary = summary
                            last_output_type = 'summary'
                            break

                except Exception as e:
                    print(f"Translation failed: {e}")
            else:
                print("No text detected.")

            print("Ready for next capture...")
            time.sleep(2)

        if GPIO.input(REPEAT_BUTTON_PIN) == GPIO.LOW:
            time.sleep(0.2)
            print("Repeating last output...")
            if last_output_type == 'full' and last_translation:
                speak_text(last_translation)
            elif last_output_type == 'summary' and last_summary:
                speak_text(last_summary)

        if GPIO.input(PAUSE_BUTTON_PIN) == GPIO.LOW:
            time.sleep(0.2)
            if pygame.mixer.music.get_busy():
                if pause_event.is_set():
                    print("Resuming speech...")
                    pause_event.clear()
                else:
                    print("Pausing speech...")
                    pause_event.set()

    except KeyboardInterrupt:
        print("Interrupted by user.")
        break

    except Exception as e:
        print(f"Error: {e}")
        break

# Cleanup
webcam.release()
cv2.destroyAllWindows()
GPIO.cleanup()
