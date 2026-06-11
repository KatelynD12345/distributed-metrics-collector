
# Distributed Metrics Collector

## Overview

A Python-based tool for collecting data from multiple remote hosts in parallel.

This project demonstrates:
- Parallel execution with ThreadPoolExecutor
- Command execution via subprocess
- Basic fault tolerance with retries
- File-based result aggregation
- Unit testing with pytest and mocking

## Features

- Run commands across multiple hosts
- Retry logic for failed executions
- Concurrent data collection
- Output stored per host in separate files
- Test coverage with mocked dependencies

## Example Usage

### Single Host

```bash
python distributed_collector.py \
  --hosts localhost \
  --command echo Hello \
  --output-dir results
```

---

### Multiple Hosts

```bash
python distributed_collector.py \
  --hosts host1 host2 host3 \
  --command echo "Hello from host" \
  --output-dir results
```

### Expected Output

```
results/
├── host1_output.txt
├── host2_output.txt
├── host3_output.txt
```

Each file contains:
```
Hello from host
```

> Note: `host1`, `host2`, etc. are placeholders. In a real environment these must be reachable via SSH.

---

### Local Testing (No SSH Required)

```bash
python distributed_collector.py \
--hosts localhost \
--command echo "Local test" \
--output-dir results
```

This allows testing without remote access.

---

## Project Structure

```
project/
├── distributed_collector.py
├── tests/
│   └── test_distributed_collector.py
├── README.md
```

---

## Running Tests

```bash
pytest
```

---

## What This Project Demonstrates

- Writing concurrent Python applications
- Handling subprocess execution safely
- Designing for testability
- Mocking external dependencies using pytest

---

## Future Improvements

- Config file support (JSON/YAML)
- Logging configuration options
- Better error reporting
- Integration with real monitoring tools