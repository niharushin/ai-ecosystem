import psutil
import time
from datetime import date, datetime
from database import SessionLocal
from models import ActivityLog, Alert, PCUsage

# Apps that count as gaming
GAMING_APPS = [
    "steam.exe", "epicgameslauncher.exe", "leagueclient.exe",
    "minecraft.exe", "valorant.exe", "gta5.exe", "fortnite.exe",
    "robloxplayerbeta.exe", "origin.exe", "battlenet.exe"
]

# Apps that count as studying
STUDY_APPS = [
    "code.exe", "notion.exe", "obsidian.exe", "anki.exe",
    "chrome.exe", "firefox.exe", "msedge.exe", "acrobat.exe",
    "winword.exe", "onenote.exe"
]

# Apps that count as movies
MOVIE_APPS = [
    "netflix.exe", "vlc.exe", "mpc-hc64.exe", "potplayer64.exe",
    "disneyplus.exe", "primevideo.exe", "youtube"
]

def get_active_processes():
    active = []
    for proc in psutil.process_iter(['name', 'status']):
        try:
            if proc.info['status'] == 'running':
                active.append(proc.info['name'].lower())
        except:
            pass
    return active

def classify_activity(processes):
    for proc in processes:
        if any(game in proc for game in GAMING_APPS):
            return "gaming", proc
        if any(movie in proc for movie in MOVIE_APPS):
            return "movie", proc
        if any(study in proc for study in STUDY_APPS):
            return "study", proc
    return "idle", "unknown"

def log_activity(activity_type, app_name, duration_minutes):
    db = SessionLocal()
    try:
        log = ActivityLog(
            activity_type=activity_type,
            app_name=app_name,
            duration_minutes=duration_minutes,
            date=str(date.today())
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

def create_alert(message, alert_type="warning"):
    db = SessionLocal()
    try:
        alert = Alert(message=message, alert_type=alert_type)
        db.add(alert)
        db.commit()
        # Also show desktop notification
        try:
            from plyer import notification
            notification.notify(
                title="🤖 Jarvis Alert",
                message=message,
                timeout=10
            )
        except:
            print(f"JARVIS ALERT: {message}")
    finally:
        db.close()

def check_limits():
    db = SessionLocal()
    try:
        today = str(date.today())
        logs = db.query(ActivityLog).filter(ActivityLog.date == today).all()

        gaming_minutes = sum(l.duration_minutes for l in logs if l.activity_type == "gaming")
        movie_minutes = sum(l.duration_minutes for l in logs if l.activity_type == "movie")
        study_minutes = sum(l.duration_minutes for l in logs if l.activity_type == "study")

        # Gaming limit — 2 hours
        if gaming_minutes >= 120:
            create_alert(f"🎮 Bro you've been gaming for {round(gaming_minutes/60,1)} hours! Take a break and study!", "gaming")

        # Movie limit — 1 movie (roughly 2 hours)
        if movie_minutes >= 120:
            create_alert(f"🎬 You watched {round(movie_minutes/60,1)} hours of movies today! That's enough bro!", "movie")

        # Study reminder — if no study after 3 hours
        if study_minutes == 0 and (gaming_minutes + movie_minutes) >= 180:
            create_alert("📚 Bro you haven't studied at all today! MEXT won't pass itself 😭", "study")

        return {
            "gaming_minutes": gaming_minutes,
            "movie_minutes": movie_minutes,
            "study_minutes": study_minutes
        }
    finally:
        db.close()

def start_monitoring(interval_seconds=300):
    print("🤖 Jarvis is watching... (every 5 minutes)")
    session_start = time.time()
    last_activity = None

    while True:
        processes = get_active_processes()
        activity_type, app_name = classify_activity(processes)

        if activity_type != "idle":
            duration = interval_seconds / 60
            log_activity(activity_type, app_name, duration)
            print(f"[{datetime.now().strftime('%H:%M')}] Detected: {activity_type} — {app_name}")

        check_limits()
        time.sleep(interval_seconds)