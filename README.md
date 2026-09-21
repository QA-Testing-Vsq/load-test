# load-test
# Concurrent HTTP Load Testing Tool

## Overview

This project is a lightweight Python-based HTTP concurrent load testing utility designed to validate the availability and response behavior of a web application under multiple simultaneous HTTP requests.

The tool uses Python's built-in `threading` module to create concurrent users/threads. Each thread sends an HTTP GET request to the configured target URL and records:

- PASS/FAIL status
- Response time
- HTTP status code
- Error details, if any

After execution, the tool provides:
1. A console-based test summary
2. A detailed HTML load test report

---

## Objective

The primary objective of this tool is to verify whether the target dashboard/application can handle multiple concurrent HTTP requests without request failures.

The test captures basic performance indicators such as:

- Total concurrent users
- Successful requests
- Failed requests
- Error rate
- Average response time
- Minimum response time
- Maximum response time
- Total test duration

---

## Technology Used

- **Python 3**
- `threading`
- `urllib.request`
- `time`
- `html`
- `datetime`

All libraries used by the script are part of the Python standard library, so no external Python package installation is required.

---

## Test Architecture

The test follows the below execution flow:

```text
Start Test
    |
    v
Read Test Configuration
    |
    v
Create Concurrent Threads
    |
    v
Each Thread Sends HTTP GET Request
    |
    +----------------------+
    |                      |
    v                      v
Request Successful      Request Failed
    |                      |
    v                      v
Record PASS             Record FAIL
Response Time           Error Details
HTTP Status
    |                      |
    +----------+-----------+
               |
               v
        Wait for All Threads
               |
               v
       Calculate Test Metrics
               |
       +-------+-------+
       |               |
       v               v
Console Summary     HTML Report
