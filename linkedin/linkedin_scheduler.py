"""
LinkedIn Auto Scheduler
Runs LinkedIn automation on schedule

Usage:
    python linkedin_scheduler.py
"""

import time
from datetime import datetime, time as dt_time
import subprocess
import sys
from pathlib import Path


def run_linkedin_automation(task: str = "full"):
    """Run LinkedIn automation task."""
    try:
        result = subprocess.run(
            [sys.executable, "linkedin_automation.py", f"--{task}"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("⚠️  Task timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running task: {e}")
        return False


def wait_until(target_time: dt_time):
    """Wait until target time."""
    now = datetime.now()

    # Calculate target datetime
    target = datetime.combine(now.date(), target_time)

    # If target time has passed today, wait for tomorrow
    if target <= now:
        from datetime import timedelta
        target = target + timedelta(days=1)

    wait_seconds = (target - now).total_seconds()

    print(f"⏰ Next run: {target.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏳ Waiting {wait_seconds / 3600:.1f} hours...")

    time.sleep(wait_seconds)


def run_daily_schedule(post_time: str = "11:00", check_time: str = "14:00"):
    """
    Run daily schedule.

    Args:
        post_time: Time to post daily content (HH:MM format)
        check_time: Time to check notifications/connections (HH:MM format)
    """
    post_hour, post_minute = map(int, post_time.split(':'))
    check_hour, check_minute = map(int, check_time.split(':'))

    post_time_obj = dt_time(post_hour, post_minute)
    check_time_obj = dt_time(check_hour, check_minute)

    print("=" * 60)
    print("🤖 LinkedIn Auto Scheduler")
    print("=" * 60)
    print(f"📅 Post time: {post_time}")
    print(f"🔔 Check time: {check_time}")
    print("=" * 60)

    while True:
        try:
            now = datetime.now()
            current_time = now.time()

            # Post daily content
            if current_time.hour == post_time_obj.hour and current_time.minute == post_time_obj.minute:
                print(f"\n{'=' * 60}")
                print(f"📝 Running daily post at {now.strftime('%H:%M:%S')}")
                print(f"{'=' * 60}")
                run_linkedin_automation("post")
                time.sleep(60)  # Wait to avoid double run

            # Check notifications/connections
            elif current_time.hour == check_time_obj.hour and current_time.minute == check_time_obj.minute:
                print(f"\n{'=' * 60}")
                print(f"🔔 Running check at {now.strftime('%H:%M:%S')}")
                print(f"{'=' * 60}")
                run_linkedin_automation("monitor")
                time.sleep(60)  # Wait to avoid double run

            # Small sleep to prevent high CPU usage
            time.sleep(10)

        except KeyboardInterrupt:
            print("\n\n⏹️  Scheduler stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in scheduler: {e}")
            time.sleep(60)  # Wait before retrying


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Auto Scheduler')
    parser.add_argument('--post-time', default='09:00', help='Daily post time (HH:MM)')
    parser.add_argument('--check-time', default='14:00', help='Check time (HH:MM)')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--task', default='full', help='Task to run: post, monitor, accept, full')

    args = parser.parse_args()

    if args.once:
        print("🚀 Running once...")
        run_linkedin_automation(args.task)
    else:
        run_daily_schedule(args.post_time, args.check_time)
