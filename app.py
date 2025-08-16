import pytesseract
from PIL import ImageGrab
import serial
import time

# Define the path 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

# Define serial port 
SERIAL_PORT = 'COM9'  
BAUD_RATE = 9600

# Initialize serial 
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  
except serial.SerialException as e:
    print(f"Error initializing serial communication: {e}")
    exit()

# Dictionary to map characters to Braille binary patterns
braille_map = {
    'a': 0b100000,
    'b': 0b101000,
    'c': 0b110000,
    'd': 0b110100,
    'e': 0b100100,
    'f': 0b111000,
    'g': 0b111100,
    'h': 0b101100,
    'i': 0b011000,
    'j': 0b011100,
    'k': 0b100010,
    'l': 0b101010,
    'm': 0b110010,
    'n': 0b110110,
    'o': 0b100110,
    'p': 0b111010,
    'q': 0b111110,
    'r': 0b101110,
    's': 0b011010,
    't': 0b011110,
    'u': 0b100011,
    'v': 0b101011,
    'w': 0b011101,
    'x': 0b110011,
    'y': 0b110111,
    'z': 0b100111,
    ' ': 0b000000  # Space character
}

def capture_screen_text():
    screenshot = ImageGrab.grab()
    text = pytesseract.image_to_string(screenshot)
    return text.lower()  

def text_to_braille(text):
    braille_patterns = [braille_map.get(char, 0b000000) for char in text]
    return braille_patterns

def send_to_arduino(braille_patterns):
    for pattern in braille_patterns:
        arduino.write(bytes([pattern]))  # Send pattern as a single byte
        time.sleep(1)  # Adjust delay as needed for readability

try:
    while True:
        screen_text = capture_screen_text()
        print(f"Captured Text: {screen_text}")

        braille_patterns = text_to_braille(screen_text)
        send_to_arduino(braille_patterns)

        time.sleep(5)  # Adjust the interval between each capture
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    arduino.close()
  
