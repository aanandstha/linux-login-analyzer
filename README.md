# Linux Failed Login Analyzer

A Python tool that reads a Linux auth.log, finds failed SSH logins, counts attempts per source IP, and flags suspicious activity with a severity rating.

## Objective

Practice the core SOC skill of turning raw log data into an investigation: extract evidence, count it, decide what is suspicious, and report it.

## Tools

- Linux (WSL)
- Python 3
- Git and GitHub

## How it works

1. Reads data/sample_auth.log line by line.
2. Uses a regular expression to pull the username and source IP from each Failed password line.
3. Counts failures per IP and records which usernames each IP tried.
4. Assigns a severity:
   - HIGH: 5 or more failures, or 3 or more different usernames
   - MEDIUM: 2 or more failures
   - LOW: anything else
5. Prints the report and saves it to reports/report.txt.

## Run it

Run: python3 src/analyzer.py
