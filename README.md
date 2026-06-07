# uHandPi Rock Paper Scissors

A real-time Rock Paper Scissors game using the Hiwonder uHandPi robotic arm and MediaPipe hand gesture recognition. The arm physically plays its move against you — no screen, just a robot hand responding to yours.

## Demo
> Robot arm detecting hand gesture and physically playing Rock, Paper, or Scissors in real time.
> *(Video coming soon)*

## How It Works
Camera captures hand
↓
MediaPipe detects 21 hand landmarks
↓
Calculate bending angle of each finger
↓
Classify gesture — Rock, Paper, or Scissors
↓
Robot randomly selects its move
↓
Arm physically moves to show gesture
↓
Winner determined, score updated

## Gesture Classification

No ML model needed — pure geometry.

Each finger's bending angle is calculated using 2D vectors between key landmarks. A bent finger has a high angle, an open finger has a low angle.

| Gesture | Thumb | Index | Middle | Ring | Pinky |
|---------|-------|-------|--------|------|-------|
| Rock | Bent | Bent | Bent | Bent | Bent |
| Scissors | Bent | Open | Open | Bent | Bent |
| Paper | Open | Open | Open | Open | Open |

**Thresholds:**
- `thr_angle = 65°` — finger clearly bent
- `thr_angle_s = 49°` — finger clearly open
- `thr_angle_thumb = 53°` — thumb specific threshold

## Hardware
- Hiwonder uHandPi Robotic Hand
- Raspberry Pi 5 (onboard)
- USB Camera (built-in, 130° FOV)

## Stack
- Python 3.8
- MediaPipe (hand landmark detection)
- OpenCV (camera capture and display)
- Hiwonder SDK (ActionGroupController for arm movement)

## Robot Arm Actions
| Gesture | Action Group |
|---------|-------------|
| Rock | `15_5_12345` |
| Scissors | `0_0_0` |
| Paper | `6_2_23` |

## Score Tracking
```python
score = {
    "Rwins": 0,   # Robot wins
    "Uwins": 0,   # Player wins  
    "Tie": 0      # Draws
}
```

Displayed live on camera feed alongside player move, robot move, and result.

## Setup

### Requirements
```bash
pip install mediapipe opencv-python numpy
```

### Run
```bash
python3 rps.py
```

Press `ESC` to exit.

## Known Issues & Limitations
- **Reaction time lag** — arm takes time to physically move between gestures, causing slight delay between detection and response
- **Hand detection consistency** — performance varies with lighting conditions and hand angle relative to camera
- **Score triggers every frame** — same gesture detected multiple times per second causes rapid score updates (fix in progress)

## Next Steps
- [ ] 3 second countdown before gesture is locked
- [ ] Freeze player gesture at countdown end
- [ ] Robot reveals move after countdown
- [ ] Score updates once per round — not every frame
- [ ] Audio feedback — countdown beeps, win/lose sounds
- [ ] Full live score-based game loop

## Part of uHandPi AI Project Suite
This is Project 1 in a series of AI projects on the uHandPi platform.
See the [main repository README](../README.md) for the full roadmap.

## Why This Project
Built as a demo for a robotics club — nothing gets people interested in robotics faster than playing a game against a physical robot arm.
