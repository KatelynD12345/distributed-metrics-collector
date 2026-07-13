#!/usr/bin/env python3
import argparse
import subprocess
import logging
from typing import List
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommandRunner:
    """Utility class to run shell commands."""

    @staticmethod
    def run_command(command: List[str], timeout: int = 30) -> str:
        """Run a shell command and return the output."""
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False,
            )

            return result.stdout.strip().strip('"')
        except subprocess.CalledProcessError:
            logger.error("Command %s failed", " ".join(command))
            return ""
        except subprocess.TimeoutExpired:
            logger.error(
                "Command %s timed out after %d seconds", " ".join(command), timeout
            )
            return ""


class RemoteCollector:
    """Class to collect data from remote servers."""

    def __init__(self, hosts: List[str], command: List[str]):
        self.hosts = hosts
        self.command = command

    def _collect_from_host(self, host: str, output_dir: Path) -> None:
        """Collect data from a single server."""
        logger.info(f"Collecting data from {host}...")
        if host == "localhost":
            ssh_command = self.command
        else:
            ssh_command = ["ssh", host, *self.command]
        for attempt in range(3):
            output = CommandRunner.run_command(ssh_command)
            if output:
                break

            logger.warning(f"Attempt {attempt + 1} failed for {host}. Retrying...")
            time.sleep(1)
            if attempt == 2:
                logger.error(f"Failed to collect data from {host} after 3 attempts.")
                return

        output_file = output_dir / f"{host.replace('.', '_')}_output.txt"
        output_file.write_text(output)
        logger.info(f"Data collected from {host} and saved to {output_file}")

    def collect_from_all_hosts(self, output_dir: Path) -> None:
        """Collect data from all servers concurrently."""
        output_dir.mkdir(parents=True, exist_ok=True)
        max_workers = max(1, len(self.hosts))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._collect_from_host, host, output_dir): host
                for host in self.hosts
            }
            for future in as_completed(futures):
                host = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error collecting data from {host}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Distributed Collector for Remote Servers"
    )
    parser.add_argument(
        "--hosts",
        nargs="+",
        required=True,
        help="List of remote hosts to collect data from",
    )
    parser.add_argument(
        "--command", nargs="+", required=True, help="Command to run on remote servers"
    )
    parser.add_argument(
        "--output-dir",
        default="collected_data",
        help="Directory to save collected data",
    )

    args = parser.parse_args()

    collector = RemoteCollector(args.hosts, args.command)
    collector.collect_from_all_hosts(Path(args.output_dir))


if __name__ == "__main__":
    main()
