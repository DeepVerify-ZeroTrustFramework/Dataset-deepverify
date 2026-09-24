╔══════════════════════════════════════════════════════════════════╗
║     DeepVerify — Volunteer Data Collection Kit                   ║
║     Team 62 · Amrita Vishwa Vidyapeetham · 2025                 ║
║     Share with students / juniors / volunteers                   ║
╚══════════════════════════════════════════════════════════════════╝

THANK YOU FOR HELPING US!
════════════════════════════════════════════════════════════════════
You are contributing data for a real academic research project on
deepfake detection in remote interviews. Your data is used ONLY for
testing and is kept private. Estimated time: 20-35 minutes.

WHAT THIS KIT CONTAINS
════════════════════════════════════════════════════════════════════
  README_STUDENT_KIT.txt              ← This file (read first)
  CONSENT_FORM.txt                    ← Read before starting
  collect_dataset.py                  ← The collection script
  DeepVerify_Dataset_Collection_Guide.docx  ← Full guide with photos

STEP 1 — INSTALL PYTHON (if not already installed)
════════════════════════════════════════════════════════════════════
  Download Python 3.8+ from: https://www.python.org/downloads/
  During install: CHECK the box "Add Python to PATH"

  Verify it works: open Terminal and type:
    python --version
  Should show: Python 3.x.x

STEP 2 — INSTALL REQUIREMENTS (one time only)
════════════════════════════════════════════════════════════════════
  Open Terminal in this folder and run:

    pip install opencv-python numpy

  Wait for it to finish. Takes 1-2 minutes.

STEP 3 — RUN THE COLLECTION SCRIPT
════════════════════════════════════════════════════════════════════
  Windows:
    Open this folder → click the address bar → type cmd → press Enter
    Then type:  python collect_dataset.py  → press Enter

  Mac:
    Open Terminal → type: cd  then drag the kit folder in → press Enter
    Then type:  python3 collect_dataset.py  → press Enter

  Linux:
    Same as Mac but navigate with cd command

STEP 4 — FOLLOW ON-SCREEN INSTRUCTIONS
════════════════════════════════════════════════════════════════════
  The script asks a few questions then walks you through each module.
  Choose A to collect ALL modules (recommended).

  ┌─────────────────────────────────────────────────────────────┐
  │  MODULE 1 · PRNU                                            │
  │  Point camera at PLAIN WHITE WALL or paper                  │
  │  Keep camera STILL. Takes 5 seconds.                        │
  ├─────────────────────────────────────────────────────────────┤
  │  MODULE 2 · rPPG                                            │
  │  Sit facing camera. Face in frame. Sit STILL for 60 sec.   │
  │  Even lighting on face. Normal breathing.                   │
  ├─────────────────────────────────────────────────────────────┤
  │  MODULE 3 · JITTER                                          │
  │  Sit normally. 30 sec idle. Then 30 sec with heavy apps.   │
  ├─────────────────────────────────────────────────────────────┤
  │  MODULE 4 · BEHAVIORAL                                      │
  │  6 short clips. Each has specific gaze instructions.        │
  │  Read posture guide carefully before each clip.             │
  └─────────────────────────────────────────────────────────────┘

MODULE 4 BEHAVIORAL — QUICK POSTURE GUIDE
════════════════════════════════════════════════════════════════════
  Clip 1 — NORMAL (30s):   Look at camera naturally. Relax.
  Clip 2 — LEFT (20s):     Place phone to your LEFT outside camera.
                            Glance left every 3-4 sec to "read" it.
  Clip 3 — RIGHT (20s):    Phone to your RIGHT. Glance right same way.
  Clip 4 — DOWN (20s):     Phone on LAP. Look down every 3-4 sec.
  Clip 5 — TAB SWITCH (20s): Look at camera then sharply away (5s cycle).
  Clip 6 — NOTES (20s):    Paper below camera. Eyes drift down to read.

  !! DO NOT OVERACT. Natural movement is more useful than dramatic gestures.

STEP 5 — ZIP AND UPLOAD
════════════════════════════════════════════════════════════════════
  After collection, a folder  deepverify_dataset/participant_XXXX/
  will appear in this kit folder.

  1. Right-click that folder → Compress / Send to Zip
  2. Name it:  dataset_YOURPARTICIPANTID.zip
     (Your participant ID is shown at the start of the script)
  3. Upload to Google Drive link:
     → LINK WILL BE PROVIDED BY DEEPVERIFY TEAM
  4. Fill Google Form:
     → FORM LINK WILL BE PROVIDED BY DEEPVERIFY TEAM
  5. WhatsApp your Participant ID to confirm.

QUICK TROUBLESHOOTING
════════════════════════════════════════════════════════════════════
  Camera not opening?
    → Close Zoom, Teams, Meet, Discord, any video call app
    → Try restarting the script

  pip not found?
    → Try:  pip3 install opencv-python numpy
    → Or:   python -m pip install opencv-python numpy

  Script gives cv2 error?
    → Run:  pip install opencv-python --upgrade

  Recording looks dark?
    → Sit facing a window or lamp. Avoid sitting with window behind you.

  Can I do it in parts?
    → Yes! Run the script multiple times and pick different modules.

FOR QUESTIONS
════════════════════════════════════════════════════════════════════
  Contact: DeepVerify Team 62
  WhatsApp: [YOUR NUMBER HERE]
  Email: [YOUR EMAIL HERE]

  Guide: Dr T Senthilkumar, Professor, Dept. of CSE
         Amrita Vishwa Vidyapeetham

════════════════════════════════════════════════════════════════════
  Thank you! Your contribution directly helps improve
  the security of remote interviews for everyone.
════════════════════════════════════════════════════════════════════
