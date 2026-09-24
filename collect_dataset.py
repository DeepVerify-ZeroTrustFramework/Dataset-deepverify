"""
DeepVerify Dataset Collection Tool
====================================
Team 62 · Amrita Vishwa Vidyapeetham · 2025
--------------------------------------------
Run this script to contribute your dataset for all four modules.
Follow the on-screen instructions carefully.

Requirements:
    pip install opencv-python numpy requests

Usage:
    python collect_dataset.py
"""

import cv2
import numpy as np
import os
import time
import json
import uuid
import platform
import datetime
import shutil
import sys
import subprocess

# Load OpenCV Haar Cascade for Face Detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ─────────────────────────────────────────────────────────────
# CONFIGURATION — Do NOT edit below unless instructed
# ─────────────────────────────────────────────────────────────
GOOGLE_FORM_URL = "https://forms.gle/YOUR_FORM_LINK_HERE"   # Replace before distributing
OUTPUT_ROOT     = "deepverify_dataset"
FPS_TARGET      = 30
PRNU_FRAME_COUNT  = 90      # ~3 seconds of I-frames
RPPG_DURATION_SEC = 30      # 30-second face video
JITTER_DURATION_SEC = 30    # 30-second network capture (passive)
BEHAVIORAL_CLIPS  = {       # scenario → duration (seconds)
    "normal_gaze"     : 17,
    "offscreen_left"  : 17,
    "offscreen_right" : 17,
    "offscreen_down"  : 17,
    "tab_switch_sim"  : 17,
}

# ─────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def banner(text, color=CYAN):
    w = 60
    print(f"\n{color}{BOLD}{'='*w}{RESET}")
    print(f"{color}{BOLD}  {text}{RESET}")
    print(f"{color}{BOLD}{'='*w}{RESET}\n")

def step(n, total, text):
    print(f"{YELLOW}{BOLD}[Step {n}/{total}]{RESET} {text}")

def ok(text):
    print(f"{GREEN}  ✔  {text}{RESET}")

def warn(text):
    print(f"{YELLOW}  ⚠  {text}{RESET}")

def err(text):
    print(f"{RED}  ✘  {text}{RESET}")

def countdown(secs, msg="Starting in"):
    for i in range(secs, 0, -1):
        print(f"\r{YELLOW}  {msg} {i}s ...{RESET}", end="", flush=True)
        time.sleep(1)
    print()

def make_dir(*parts):
    path = os.path.join(*parts)
    os.makedirs(path, exist_ok=True)
    return path

def open_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        err("Could not open camera. Make sure your webcam is connected and not used by another app.")
        sys.exit(1)
    cap.set(cv2.CAP_PROP_FPS, FPS_TARGET)
    return cap

def get_participant_id():
    uid = str(uuid.uuid4())[:8].upper()
    return uid

def save_meta(folder, data):
    with open(os.path.join(folder, "meta.json"), "w") as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────────────────────────
# STEP 0 — PARTICIPANT REGISTRATION
# ─────────────────────────────────────────────────────────────
def register_participant():
    banner("PARTICIPANT REGISTRATION", CYAN)
    print("  Please answer a few quick questions. This info labels your dataset.\n")

    name       = input("  Full name (e.g. Vijay R A)                     : ").strip()
    os_info    = platform.platform()
    room_light = input("  Room lighting now? [bright / dim / artificial] : ").strip()
    glasses    = input("  Do you wear glasses during recording? [y/n]    : ").strip().lower()

    # Use sanitized name as folder-friendly ID
    # e.g. "Vijay R A" → "Vijay_R_A"
    name_slug = "_".join(name.split()) if name else "unknown"

    print(f"\n  {GREEN}{BOLD}Dataset will be saved under: participant_{name_slug}{RESET}\n")

    info = {
        "participant_id" : name_slug,
        "name"           : name,
        "os"             : os_info,
        "lighting"       : room_light,
        "glasses"        : glasses == "y",
        "recorded_at"    : datetime.datetime.now().isoformat(),
    }
    return info

# ─────────────────────────────────────────────────────────────
# MODULE 1 — PRNU (Camera Fingerprint)
# ─────────────────────────────────────────────────────────────
def collect_prnu(participant_info, root):
    banner("MODULE 1 · PRNU — Camera Fingerprint", CYAN)

    print("""  What this captures:
  The tiny manufacturing imperfections in your camera sensor create a
  unique 'fingerprint' in every photo it takes. We capture 90 still
  frames of a FLAT SURFACE (wall, white paper, ceiling) to extract
  your device's fingerprint.

  ─────────────────────────────────────────────────────────────
  WHAT YOU NEED TO DO:
  ─────────────────────────────────────────────────────────────
  1. Point your camera at a PLAIN FLAT SURFACE
     → White wall, blank white paper, or your ceiling under normal light
     → Do NOT point at your face
     → Keep camera STILL (rest laptop on table)
  2. Make sure the surface is EVENLY LIT (no harsh shadows)
  3. Do NOT move the camera during capture
  ─────────────────────────────────────────────────────────────
""")

    folder = make_dir(root, "module1_prnu", "genuine_device")
    save_meta(folder, {**participant_info, "module": "PRNU", "type": "genuine_webcam"})

    input("  Press ENTER when you are ready (camera pointed at plain surface)...")
    countdown(3)

    cap = open_camera()
    saved = 0
    print(f"\n  Capturing {PRNU_FRAME_COUNT} frames. Hold the camera still...\n")

    prev_gray = None

    while saved < PRNU_FRAME_COUNT:
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Motion Check
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            if np.mean(diff) > 2.0:
                cv2.putText(frame, "WARNING: CAMERA MOVING! HOLD STILL", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        prev_gray = gray

        # Save as PNG (lossless — critical for PRNU)
        fname = os.path.join(folder, f"prnu_{saved+1:03d}.png")
        cv2.imwrite(fname, frame)
        saved += 1
        bar = int(saved / PRNU_FRAME_COUNT * 40)
        print(f"\r  [{GREEN}{'█'*bar}{'░'*(40-bar)}{RESET}] {saved}/{PRNU_FRAME_COUNT}", end="", flush=True)
        # Show live preview
        cv2.imshow("PRNU Capture — Press Q to abort", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print()
    ok(f"PRNU capture complete → {folder}")


# ─────────────────────────────────────────────────────────────
# MODULE 2 — rPPG (Pulse / Liveness)
# ─────────────────────────────────────────────────────────────
def collect_rppg(participant_info, root):
    banner("MODULE 2 · rPPG — Biological Pulse / Liveness", CYAN)

    print("""  What this captures:
  Your heart pumps blood through your face continuously. This causes
  tiny color changes in your skin. We record a 60-second face video
  to extract your pulse signal (no hardware needed — just camera).

  ─────────────────────────────────────────────────────────────
  WHAT YOU NEED TO DO:
  ─────────────────────────────────────────────────────────────
  GENUINE capture (real person — you):
  1. Sit facing your camera, face centered in frame
  2. Keep face within the green guide box visible on screen
  3. Stay STILL — minimal head movement for 60 seconds
  4. Normal breathing is fine. Do NOT hold your breath.
  5. Lighting: face should be evenly lit (not backlit)
  6. Remove glasses if possible (reduces glare on skin ROI)

  ─────────────────────────────────────────────────────────────
""")

    def record_face_video(label, folder, duration):
        os.makedirs(folder, exist_ok=True)
        out_path = os.path.join(folder, f"rppg_{label}.avi")
        cap = open_camera()
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(out_path, fourcc, FPS_TARGET, (w, h))
        start = time.time()
        print(f"\n  Recording {duration}s ... keep face still!\n")
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            elapsed = time.time() - start
            remaining = duration - elapsed
            if remaining <= 0:
                break
            # Quality Checks
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Guide box overlay
            cx, cy = w // 2, h // 2
            bw, bh = int(w * 0.4), int(h * 0.6)
            
            # Check lighting in ROI
            roi = gray[max(0, cy-bh//2):min(h, cy+bh//2), max(0, cx-bw//2):min(w, cx+bw//2)]
            avg_brightness = np.mean(roi) if roi.size > 0 else 100
            
            cv2.rectangle(frame, (cx-bw//2, cy-bh//2), (cx+bw//2, cy+bh//2), (0,255,0), 2)
            cv2.putText(frame, f"Keep face inside box  |  {int(remaining)}s left",
                        (10, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,0), 1)
                        
            if len(faces) == 0:
                cv2.putText(frame, "WARNING: NO FACE DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif avg_brightness < 40:
                cv2.putText(frame, "WARNING: TOO DARK! TURN ON LIGHTS", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif avg_brightness > 220:
                cv2.putText(frame, "WARNING: TOO BRIGHT/WASHED OUT", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
            writer.write(frame)
            cv2.imshow(f"rPPG Capture — {label}", frame)
            # Progress bar
            bar = int((elapsed / duration) * 40)
            print(f"\r  [{GREEN}{'█'*bar}{'░'*(40-bar)}{RESET}] {int(elapsed)}s / {duration}s", end="", flush=True)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        writer.release()
        cap.release()
        cv2.destroyAllWindows()
        print()
        ok(f"rPPG video saved → {out_path}")
        return out_path

    # ── Genuine ──
    folder_genuine = make_dir(root, "module2_rppg", "genuine_live")
    save_meta(folder_genuine, {**participant_info, "module": "rPPG", "type": "genuine_live_person"})
    input("  Press ENTER to start the 30-second GENUINE face recording...")
    countdown(3)
    record_face_video("genuine", folder_genuine, RPPG_DURATION_SEC)


# ─────────────────────────────────────────────────────────────
# MODULE 3 — JITTER (Network Timing Analysis)
# ─────────────────────────────────────────────────────────────
def collect_jitter(participant_info, root):
    banner("MODULE 3 · Jitter — Network Timing Analysis", CYAN)

    print("""  What this captures:
  Real webcam streams send data packets at very regular intervals.
  A deepfake rendered by GPU adds extra delay to each packet,
  creating irregular timing (jitter). We record a 30-second face
  video and log the frame timestamps so we can simulate IAT analysis.

  ─────────────────────────────────────────────────────────────
  WHAT YOU NEED TO DO:
  ─────────────────────────────────────────────────────────────
  GENUINE capture:
  1. Sit normally in front of your camera (face in frame)
  2. Just relax and stay normal — 30 seconds
  3. This is a real webcam stream (low jitter)
  ─────────────────────────────────────────────────────────────
""")

    def record_jitter_session(label, folder, duration):
        os.makedirs(folder, exist_ok=True)
        cap = open_camera()
        timestamps = []
        frames_path = os.path.join(folder, "frames")
        os.makedirs(frames_path, exist_ok=True)
        start = time.time()
        frame_idx = 0
        print(f"\n  Recording {duration}s jitter session [{label}]...\n")
        while True:
            t0 = time.time()
            ret, frame = cap.read()
            t1 = time.time()
            if not ret:
                continue
            elapsed = t1 - start
            if elapsed > duration:
                break
            timestamps.append({
                "frame"          : frame_idx,
                "capture_time_s" : round(elapsed, 6),
                "read_latency_ms": round((t1 - t0) * 1000, 3),
            })
            fname = os.path.join(frames_path, f"frame_{frame_idx:04d}.jpg")
            cv2.imwrite(fname, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            frame_idx += 1
            bar = int((elapsed / duration) * 40)
            print(f"\r  [{CYAN}{'█'*bar}{'░'*(40-bar)}{RESET}] {int(elapsed)}s / {duration}s", end="", flush=True)
            cv2.imshow(f"Jitter Capture — {label}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        # Save timestamp log
        ts_path = os.path.join(folder, "timestamps.json")
        with open(ts_path, "w") as f:
            json.dump({"label": label, "timestamps": timestamps}, f, indent=2)
        print()
        ok(f"Jitter session saved → {folder}  ({frame_idx} frames, timestamps logged)")

    # ── Genuine (idle system) ──
    folder_genuine = make_dir(root, "module3_jitter", "genuine_idle")
    save_meta(folder_genuine, {**participant_info, "module": "Jitter", "type": "genuine_idle_system"})
    print("  GENUINE capture: Close all heavy apps first. Just browser + this script.")
    input("  Press ENTER when ready...")
    countdown(3)
    record_jitter_session("genuine_idle", folder_genuine, JITTER_DURATION_SEC)


# ─────────────────────────────────────────────────────────────
# MODULE 4 — BEHAVIORAL (Gaze & Tab Switching)
# ─────────────────────────────────────────────────────────────
def collect_behavioral(participant_info, root):
    banner("MODULE 4 · Behavioral — Gaze & Tab Switching", CYAN)

    print("""  What this captures:
  When candidates cheat using a second screen, their eyes repeatedly
  drift off-camera in a consistent direction. We need videos of:
  (A) Normal interview gaze — looking at camera naturally
  (B) Off-screen reading — simulating reading from a phone/screen
      placed to your LEFT, RIGHT, or BELOW
  (C) Tab-switch simulation — looking away then back periodically

  ─────────────────────────────────────────────────────────────
  GENERAL SETUP FOR ALL CLIPS:
  ─────────────────────────────────────────────────────────────
  • Sit upright, face centered in frame
  • The green guide box on screen shows your face position
  • Maintain natural posture — do not overact
  • Each clip is 20-30 seconds
  ─────────────────────────────────────────────────────────────
""")

    scenarios = {
        "normal_gaze": {
            "duration": 17,
            "instructions": """
  SCENARIO: NORMAL INTERVIEW GAZE (17 seconds)
  ─────────────────────────────────────────────
  ✔ Look directly at the camera (or slightly around it)
  ✔ Act as if you are listening to an interviewer
  ✔ Occasional natural blinks and small head shifts are fine
  ✔ Do NOT look left, right, or down repeatedly
  This is our CLEAN / NOT CHEATING baseline.""",
        },
        "offscreen_left": {
            "duration": 17,
            "instructions": """
  SCENARIO: OFF-SCREEN LEFT (17 seconds)
  ─────────────────────────────────────────────
  ✔ Place your phone or a book to your LEFT (outside camera view)
  ✔ Repeatedly glance LEFT to 'read' it every 3-4 seconds
  ✔ Look back at camera briefly, then left again
  ✔ Simulate actually reading text from it
  This mimics a candidate reading a cheat sheet on the left.""",
        },
        "offscreen_right": {
            "duration": 17,
            "instructions": """
  SCENARIO: OFF-SCREEN RIGHT (17 seconds)
  ─────────────────────────────────────────────
  ✔ Place your phone or a book to your RIGHT (outside camera view)
  ✔ Repeatedly glance RIGHT to 'read' it every 3-4 seconds
  ✔ Look back at camera briefly, then right again
  This mimics a candidate reading answers from the right side.""",
        },
        "offscreen_down": {
            "duration": 17,
            "instructions": """
  SCENARIO: OFF-SCREEN DOWN (17 seconds)
  ─────────────────────────────────────────────
  ✔ Place your phone on your LAP (below camera field of view)
  ✔ Repeatedly look DOWN to 'read' it every 3-4 seconds
  ✔ Look back up at camera, then down again
  This mimics reading from a phone on the lap.""",
        },
        "tab_switch_sim": {
            "duration": 17,
            "instructions": """
  SCENARIO: TAB SWITCHING (17 seconds)
  ─────────────────────────────────────────────
  ✔ While looking at camera, periodically look sharply to one side
    (as if glancing at another monitor or tab)
  ✔ Do this every 5 seconds or so — look away, pause 1s, look back
  ✔ Simulate the motion of someone switching windows
  This captures the head pose and gaze pattern of tab switching.""",
        }
    }

    for key, scenario in scenarios.items():
        print(scenario["instructions"])
        ans = input(f"\n  Record this scenario? [y/n]: ").strip().lower()
        if ans != "y":
            warn(f"Skipping {key}")
            continue

        folder = make_dir(root, "module4_behavioral", key)
        save_meta(folder, {**participant_info, "module": "Behavioral",
                            "type": key, "label": "cheating" if key != "normal_gaze" else "genuine"})

        out_path = os.path.join(folder, f"behavioral_{key}.avi")
        cap = open_camera()
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(out_path, fourcc, FPS_TARGET, (w, h))
        duration = scenario["duration"]

        input(f"\n  Press ENTER to start {duration}s recording...")
        countdown(3)

        start = time.time()
        frame_meta = []
        frame_idx = 0
        print(f"\n  Recording {duration}s [{key}]...\n")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            elapsed = time.time() - start
            if elapsed > duration:
                break
            frame_meta.append({"frame": frame_idx, "time_s": round(elapsed, 4)})
            # Quality Check
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Guide overlay
            cx, cy = w // 2, h // 2
            bw, bh = int(w * 0.45), int(h * 0.65)
            color = (0, 255, 0) if key == "normal_gaze" else (0, 165, 255)
            cv2.rectangle(frame, (cx-bw//2, cy-bh//2), (cx+bw//2, cy+bh//2), color, 2)
            label_text = "NORMAL" if key == "normal_gaze" else "CHEATING SIM"
            cv2.putText(frame, f"{label_text}  |  {int(duration-elapsed)}s left",
                        (10, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1)
            
            if len(faces) == 0:
                cv2.putText(frame, "WARNING: NO FACE DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            writer.write(frame)
            cv2.imshow(f"Behavioral — {key}", frame)
            bar = int((elapsed / duration) * 40)
            clr = GREEN if key == "normal_gaze" else YELLOW
            print(f"\r  [{clr}{'█'*bar}{'░'*(40-bar)}{RESET}] {int(elapsed)}s / {duration}s", end="", flush=True)
            frame_idx += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        writer.release()
        cap.release()
        cv2.destroyAllWindows()
        with open(os.path.join(folder, "frame_meta.json"), "w") as f:
            json.dump(frame_meta, f, indent=2)
        print()
        ok(f"Behavioral clip saved → {out_path}")

# ─────────────────────────────────────────────────────────────
# SUMMARY + UPLOAD INSTRUCTIONS
# ─────────────────────────────────────────────────────────────
def show_summary(participant_info, root):
    banner("COLLECTION COMPLETE!", GREEN)

    pid = participant_info["participant_id"]
    print(f"""  Your Participant ID : {BOLD}{GREEN}{pid}{RESET}
  Dataset folder      : {BOLD}{root}{RESET}

  ─────────────────────────────────────────────────────────────
  NEXT STEPS — Upload your dataset
  ─────────────────────────────────────────────────────────────

  1. ZIP your dataset folder:
       Right-click '{root}' → Compress / Send to Zip
       Name it:  dataset_{pid}.zip

  2. Upload to Google Drive:
       Link: {GOOGLE_FORM_URL}

  3. Fill in the Google Form:
       Use your Participant ID: {pid}
       Paste the Drive link of your zip file

  4. WhatsApp your Participant ID to your DeepVerify contact
     so we can verify your upload.

  ─────────────────────────────────────────────────────────────
  WHAT WAS COLLECTED:
  ─────────────────────────────────────────────────────────────
""")

    for mod_folder in sorted(os.listdir(root)):
        full = os.path.join(root, mod_folder)
        if os.path.isdir(full):
            size_mb = sum(
                os.path.getsize(os.path.join(dp, f))
                for dp, dn, filenames in os.walk(full)
                for f in filenames
            ) / (1024 * 1024)
            print(f"    {GREEN}✔{RESET}  {mod_folder:<35} {size_mb:.1f} MB")

    print(f"""
  ─────────────────────────────────────────────────────────────
  Thank you for contributing to DeepVerify!
  Your data is used only for academic research at Amrita VV.
  ─────────────────────────────────────────────────────────────
""")

# ─────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────
def main():
    banner("DeepVerify Dataset Collection Tool — Classroom Session", CYAN)
    print(f"""  Welcome! This tool collects rPPG and Behavioral datasets
  for the DeepVerify research project (Team 62, Amrita Vishwa Vidyapeetham).

  You will record:
    Module 2 — rPPG      (30-sec face video for pulse detection)   ~4 min
    Module 4 — Behavioral (6 short gaze scenario clips)            ~15 min

  Total estimated time: ~20 minutes
""")

    participant_info = register_participant()
    pid = participant_info["participant_id"]
    root = os.path.join(OUTPUT_ROOT, f"participant_{pid}")
    make_dir(root)
    save_meta(root, participant_info)

    # ── Auto-run rPPG and Behavioral only ──
    # PRNU (Module 1) disabled — same laptop/camera for all participants, no sensor diversity
    # collect_prnu(participant_info, root)

    collect_rppg(participant_info, root)

    # Jitter (Module 3) disabled — same laptop hardware, all jitter profiles will be identical
    # collect_jitter(participant_info, root)

    collect_behavioral(participant_info, root)

    show_summary(participant_info, root)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}  Collection interrupted. Partial data saved.{RESET}\n")
        sys.exit(0)
