from datetime import datetime
from collections import defaultdict
THRESHOLD = 5 # failed attempts
TIME_WINDOW = 60 # seconds
def detectattack(logfile):
    failed_logins = defaultdict(list)
    with open(logfile, "r") as file:
        for line in file:
            try:
                time_str, ip, status = line.strip().rsplit(" ", 2)
                timestamp = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            if status == "FAIL":
                failed_logins[ip].append(timestamp)
        for ip, times in failed_logins.items():
            times.sort()
            for i in range(len(times)):
                if i + THRESHOLD - 1 < len(times):
                    if (times[i + THRESHOLD - 1] - times[i]).seconds <= TIME_WINDOW:
                        return True
                return False
