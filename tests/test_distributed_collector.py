import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import distributed_collector


def test_command_runner_success():
    results = distributed_collector.CommandRunner.run_command(["echo", "Hello, World!"])
    assert results == "Hello, World!"

def test_command_runner_failure():
    results = distributed_collector.CommandRunner.run_command(["false"])
    assert results == ""

def test_command_runner_timeout():
    results = distributed_collector.CommandRunner.run_command(["sleep", "5"], timeout=1)
    assert results == ""

def test_remote_collector(tmp_path):
    hosts = ["localhost"]
    command = ["echo", "Test Data"]
    collector = distributed_collector.RemoteCollector(hosts, command)
    collector.collect_from_all_hosts(tmp_path)
    
    output_file = tmp_path / "localhost_output.txt"
    assert output_file.exists()
    assert output_file.read_text().strip() == "Test Data"

def test_remote_collector_failure(tmp_path):
    hosts = ["localhost"]
    command = ["false"]
    collector = distributed_collector.RemoteCollector(hosts, command)
    
    collector.collect_from_all_hosts(tmp_path)
    
    output_file = tmp_path / "localhost_output.txt"
    assert not output_file.exists()

def test_remote_collector_timeout(tmp_path):
    hosts = ["localhost"]
    command = ["sleep", "5"]

    collector = distributed_collector.RemoteCollector(hosts, command)
    collector.collect_from_all_hosts(tmp_path)
    
    output_file = tmp_path / "localhost_output.txt"
    assert not output_file.exists()

def test_remote_collector_multiple_hosts(monkeypatch,tmp_path):

    def fake_run(command, timeout=30):
        return "Mocked Data"

    monkeypatch.setattr(
        distributed_collector.CommandRunner,
        "run_command",
        fake_run
    )

    hosts = ["host1", "host2", "host3"]
    collector = distributed_collector.RemoteCollector(
        hosts,
        ["anything"]
    )

    collector.collect_from_all_hosts(tmp_path)
    
    for host in hosts:
        output_file = tmp_path / f"{host.replace('.', '_')}_output.txt"
        assert output_file.exists()
        assert output_file.read_text().strip() == "Mocked Data"