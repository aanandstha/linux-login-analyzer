import re
from collections import defaultdict

pattern = r"Failed password for (?:invalid user )?(\S+) from (\S+) port"

FAIL_THRESHOLD = 5
USER_THRESHOLD = 3

attempts = defaultdict(int)
users = defaultdict(set)

with open("data/sample_auth.log") as f:
    for line in f:
        match = re.search(pattern, line)
        if match:
            username = match.group(1)
            ip = match.group(2)
            attempts[ip] += 1
            users[ip].add(username)

lines = ["=== Failed Login Report ==="]
for ip, count in attempts.items():
    if count >= FAIL_THRESHOLD or len(users[ip]) >= USER_THRESHOLD:
        severity = "HIGH"
    elif count >= 2:
        severity = "MEDIUM"
    else:
        severity = "LOW"
    lines.append(f"[{severity}] {ip} - {count} failures, users: {sorted(users[ip])}")

report = "\n".join(lines)
print(report)

with open("reports/report.txt", "w") as out:
    out.write(report + "\n")
