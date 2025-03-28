import pytest

# List of dependencies
dependencies = [
    "colored_logging",
    "ECOv002_CMR",
    "ECOv002_granules",
    "GEOS5FP",
    "numpy",
    "pandas",
    "rasters"
]

# Generate individual test functions for each dependency
@pytest.mark.parametrize("dependency", dependencies)
def test_dependency_import(dependency):
    __import__(dependency)
