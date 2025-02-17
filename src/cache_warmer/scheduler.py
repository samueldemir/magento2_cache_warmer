import sys
import time

import schedule

from cache_warmer.main import main

sys.path.append("/usr/local/lib/python3.11")


def job():
    main()


# Schedule the job every 30 minutes
schedule.every(30).minutes.do(job)

# Keep running the scheduler
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
