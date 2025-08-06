

![Vocal Vision Thumbnail](images/project_thumbnail.png)


# 🔊 Vocal Vision: Real Time Audio Accessibility

An assistive device built using Raspberry Pi 4 for visually impaired individuals. It captures text using a webcam, translates it (if needed), summarizes it, and converts it into speech — all controlled through physical push buttons.

---

## 📌 Features

- OCR using Tesseract to extract printed text
- Real-time translation to English using Google Translate
- Summarization of extracted text using Sumy
- Text-to-speech (TTS) conversion using gTTS and playback via pygame
- Multiple physical buttons for:
  - Capturing and reading text
  - Listening to summarized content
  - Repeating last spoken output
  - Pausing/Resuming speech

---

## 🛠️ Hardware Used

| Component        | Details                              |
|------------------|--------------------------------------|
| 🎯 Microcontroller | Raspberry Pi 4 (4GB/8GB)             |
| 📷 Camera         | 720p USB Webcam                      |
| 🔘 Buttons        | 5 Push buttons connected to GPIO pins |
| 🔊 Output         | 3.5mm Jack/Bluetooth Speaker          |
| 🧠 Others         | Breadboard, jumper wires, resistors  |

---

## ⚡ GPIO Pin Mapping

| Function                | GPIO Pin |
|-------------------------|----------|
| Capture & Speak         | GPIO 17  |
| Speak Summary           | GPIO 27  |
| Repeat Last Output      | GPIO 22  |
| Pause/Resume Audio      | GPIO 23  |
| Exit/Shutdown (optional)| GPIO 24  |

> Defined inside the `main.py` and easily configurable.

---

## 📷 Image Scaling for OCR Accuracy

Due to low resolution of 720p webcam, image quality was insufficient for Tesseract.  
To improve OCR accuracy, we used **image resizing** using OpenCV before sending the image for OCR processing.

```python
resized = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


## ⚙️ Installation Guide (For Raspberry Pi)

Follow these steps to set up the environment on a Raspberry Pi:

```bash
# ✅ 1. Update your system
sudo apt update
sudo apt upgrade

# 📷 2. Install Tesseract OCR
sudo apt install tesseract-ocr

# Verify the installation
tesseract --version

# 🐍 3. Install pip (if not already installed)
sudo apt install python3-pip

# 📦 4. Install Python dependencies
# (Make sure you are in the directory with requirements.txt)
pip3 install -r requirements.txt

# 🔊 5. Install aud