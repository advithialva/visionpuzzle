# 🧩 Vision-Based Fingertip-Controlled Puzzle Assembly

An interactive computer vision-based puzzle game that uses real-time hand tracking to let players drag and drop puzzle pieces using their index finger—no mouse or keyboard required. 

This project is built with OpenCV and `cvzone`, showcases gesture-based interaction for immersive experiences.

---

## 📌 Project Overview

- **Mode of interaction**: Fingertip via webcam (no mouse/keyboard)
- **Objective**: Drag and snap 4 puzzle pieces into their correct positions
- **Time Limit**: Complete the puzzle within 30 seconds
- **User Feedback**:
  - ✅ Puzzle Complete screen
  - 🛑 Game Over screen with interactive "Try Again" and "Exit" buttons

---

## 🧠 Technologies Used

| Technology   | Purpose                                      |
|--------------|----------------------------------------------|
| ![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)   | Core programming language                    |
| ![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)      | Real-time video processing and UI rendering  |
| ![cvzone](https://img.shields.io/badge/cvzone-1.x-orange?style=for-the-badge)       | Simplified hand tracking & drawing utilities |
| ![MediaPipe](https://img.shields.io/badge/MediaPipe-GoogleFFCD00?style=for-the-badge&logo=google&logoColor=black)    | Hand landmark detection via deep learning    |
| ![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?style=for-the-badge&logo=numpy&logoColor=white)         | Fast numerical operations and vector math    |


---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/advithialva/vision-based-puzzle-assembly
cd vision-based-puzzle-assembly
```

### 2. Install Dependencies
```
pip install opencv-python cvzone mediapipe numpy
```

Or use the provided Python version:
```
pyenv local 3.10.13
```

### 3. Run the App
```
python app.py
```
Make sure your webcam is active.

---

## ✨ Possible Extensions

| Feature Idea                            | Description                                                                 |
|----------------------------------------|-----------------------------------------------------------------------------|
| 🧩 Puzzle Image Integration             | Replace solid color blocks with shuffled puzzle image tiles.               |
| 🔢 Higher Difficulty Levels             | Extend to 3×3, 4×4, or more complex puzzle grids.                           |
| 🔊 Sound Feedback                       | Add audio cues like snap sounds, success chimes, or time-up alerts.        |
| 🖐️ Touchless UI Interaction            | Allow navigating menus or selecting difficulty levels with hand gestures.  |

