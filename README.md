# 🐍 AI Hand-Controlled Snake Game

An interactive Snake Game controlled using **hand movements in front of a webcam**.

This project combines **Artificial Intelligence, Computer Vision, Hand Landmark Detection, and Game Development** to create a touchless Snake Game.

Instead of using traditional keyboard controls, the player controls the snake by moving their palm in different directions in front of the webcam.

The system uses **MediaPipe Hand Landmarker** for hand detection, **OpenCV** for real-time webcam processing, and **Pygame** for game development.

---

## 🎮 Features

- 🖐️ Real-time hand-controlled gameplay
- 📷 Webcam-based hand tracking
- 🤖 AI-powered hand landmark detection
- 🎮 Classic Snake Game mechanics
- 🕹️ Virtual joystick-style hand control
- 🎯 Palm-center based direction detection
- 🚫 Dead zone to reduce unwanted movements
- 🐍 Continuous automatic snake movement
- 🍎 Apple/food generation
- 📈 Snake growth after eating food
- 💯 Score system
- 📏 Snake length display
- 🔊 Eating sound effect
- 💀 Game-over sound effect
- 🔄 Game restart option
- 📹 Live camera feed inside the game window
- ✋ Hand landmarks and connections displayed on camera
- 🚧 Wall collision detection
- 🐍 Self-collision detection

---

## 🧠 How It Works

The webcam captures the player's hand in real time.

MediaPipe detects the hand landmarks and the system calculates the approximate center of the palm.

The palm position is then compared with a virtual joystick center to determine the direction of the snake.


### System Flow

```text
                Webcam
                   │
                   ▼
                OpenCV
                   │
                   ▼
       MediaPipe Hand Landmarker
                   │
                   ▼
          Hand Landmark Detection
                   │
                   ▼
          Palm Center Calculation
                   │
                   ▼
             Virtual Joystick
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
        LEFT      UP      RIGHT
                   │
                  DOWN
                   │
                   ▼
            Snake Direction
                   │
                   ▼
            Snake Movement
                   │
                   ▼
             Game Processing
                   │
                   ▼
             Score / Growth


                  UP
                  ↑
                  │
                  │
          LEFT ←  ●  → RIGHT
                  │
                  │
                  ↓
                DOWN

        🍎
         │
         ▼
       🐍
         │
         ▼
     Apple Eaten
         │
         ├── Score +10
         │
         ├── Snake Grows
         │
         ├── New Apple
         │
         └── Eating Sound

┌────────────────────────┐
│                        │
│ 🐍 → → → → → → → ❌    │
│                        │
└────────────────────────┘

     🐍
      ↓
  → → ↓
      ↓
  ← ← 🐍

GAME OVER

Press R to Restart

AI-Hand-Controlled-Snake
│
├── README.md
├── requirements.txt
├── .gitignore
├── create_sounds.py
│
├── models
│   └── hand_landmarker.task
│
├── sounds
│   ├── eat.wav
│   └── game_over.wav
│
├── src
│   ├── main.py
│   ├── snake.py
│   └── hand_tracker.py
│
└── venv

┌──────────────────────────────────────────────────────────┐
│              AI HAND CONTROLLED SNAKE                    │
├─────────────────────────┬────────────────────────────────┤
│                         │                                │
│                         │       HAND CONTROL CAMERA      │
│                         │                                │
│       SNAKE GAME        │             ✋                 │
│                         │                                │
│                         │      Hand Landmarks           │
│                         │                                │
│                         │                                │
├─────────────────────────┴────────────────────────────────┤
│ Score: 10    Length: 6       R = Restart    Q = Quit    │
└──────────────────────────────────────────────────────────┘

UP
              ↑

          ┌───────┐
          │       │
LEFT  ←   │   ●   │   → RIGHT
          │       │
          └───────┘

              ↓
             DOWN

---
```
---

## 👩‍💻 Author & Developer Details

| Attribute | Details |
| :--- | :--- |
| **Name** | **Kalpani M. Liyanage** |
| **Role** | BICT (Hons) Undergraduate |
| **Department** | Department of Information & Communication Technology |
| **Faculty** | Faculty of Technology |
| **University** | University of Sri Jayewardenepura, Sri Lanka |
| **GitHub** | [@kalpaniliyanage](https://github.com/kalpaniliyanage) |

---

### 🤝 Connect with Me

- 🌐 **GitHub:** [https://github.com/kalpaniliyanage](https://github.com/kalpaniliyanage)

---

## 📜 License

This project is created for educational and learning purposes. Feel free to study, modify, and extend it.
