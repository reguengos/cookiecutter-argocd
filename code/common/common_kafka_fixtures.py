import os
import pytest
import requests
from pathlib import Path
from confluent_kafka import Producer


def is_responsive(url):
    try:
        producer_configuration = {"bootstrap.servers": url}
        # test configuration, and connection to kafka
        producer = Producer(producer_configuration)
        producer.list_topics(timeout=1)
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def kafka_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # Disable DeprecationWarning: PY_SSIZE_T_CLEAN will be required for '#' formats
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("kafka", 9092)
    url = f"{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig, docker_ip: str, tmp_path_factory: Path):
    docker_compose_input = (
        Path(pytestconfig.rootdir) / "common" / "kafka.yaml"
    )

    docker_compose_file_content = docker_compose_input.read_text().replace(
        "<<DOCKER_IP>>", docker_ip
    )

    docker_compose_output = tmp_path_factory.mktemp("docker") / "kafka.yaml"
    docker_compose_output.write_text(docker_compose_file_content)
    yield str(docker_compose_output)
    docker_compose_output.unlink()
