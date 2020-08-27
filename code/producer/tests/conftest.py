import os
import sys
import pytest
from pathlib import Path

component_root_dir = Path(__file__).parent.parent
src_dir = component_root_dir / "src"
root_dir = component_root_dir.parent
common_dir = root_dir / "common"

for path in (src_dir, common_dir):
    if path not in sys.path:
        sys.path.append(str(path))

from common_kafka_fixtures import *
