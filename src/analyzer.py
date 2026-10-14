import re
from datetime import datetime
from collections import defaultdict

pattern = r"^(\w{3} +\d+ \d{2}:\d{2}:\d{2}) .*Failed password for (?:invalid user )?(\S+) from (\S+) port"

FAIL_THRESHOLD = 5
USER_THRESHOLD = 3
BURST_THRESHOLD = 5
WINDOW_SECONDS = 60

attempts = defaultdict(int)
users = defaultdict(set)
times = defaultdict(list)


def max_burst(timestamps, window):
    timestamps.sort()
    best = 0
    start = 0
    for end in range(len(timestamps)):
        while (timestamps[end] - timestamps[start]).total_seconds() > window:
            start += 1
        best = max(best, end - start + 1)
    return best


with open("data/sample_auth.log") as f:
    for line in f:
        match = re.search(pattern, line)
        if match:
            when = datetime.strptime("2026 " + match.group(1), "%Y %b %d %H:%M:%S")
            username = match.group(2)
            ip = match.group(3)
            attempts[ip] += 1
            users[ip].add(username)
            times[ip].append(when)

lines = ["=== Failed Login Report ==="]
for ip, count in attempts.items():
    burst = max_burst(times[ip], WINDOW_SECONDS)
    if count >= FAIL_THRESHOLD or len(users[ip]) >= USER_THRESHOLD or burst >= BURST_THRESHOLD:
        severity = "HIGH"
    elif count >= 2:
        severity = "MEDIUM"
    else:
        severity = "LOW"
    score = count + 3 * len(users[ip]) + (10 if burst >= BURST_THRESHOLD else 0)
    lines.append(f"[{severity}] {ip} - score {score}, {count} failures, {burst} within {WINDOW_SECONDS}s, users: {sorted(users[ip])}")

report = "\n".join(lines)
print(report)

with open("reports/report.txt", "w") as out:
    out.write(report + "\n")
