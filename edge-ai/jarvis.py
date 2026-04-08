import threading
import schedule
import time
from monitors.pc_monitor import start_monitoring
from report import generate_weekly_report
from database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

def run_weekly_report():
    print("📊 Generating weekly report...")
    report = generate_weekly_report()
    print(f"Weekly Report Generated!\n{report['ai_report']}")

# Schedule weekly report every Sunday
schedule.every().sunday.at("09:00").do(run_weekly_report)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("🤖 JARVIS IS ONLINE! 🔥")
    print("Monitoring your PC activity...")
    print("Press Ctrl+C to stop")

    # Run scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Start PC monitoring (main thread)
    start_monitoring(interval_seconds=300)