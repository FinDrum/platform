import pytest
from findrum.interfaces import DataSource
from findrum.engine.pipeline_runner import PipelineRunner
from findrum.registry.registry import DATASOURCE_REGISTRY

class IncompleteDataSource(DataSource):
    pass

class DummyDataSource(DataSource):
    def fetch(self):
        return "dummy_data"

def test_datasource_fetch_not_implemented():
    with pytest.raises(TypeError):
        IncompleteDataSource()

def test_datasource_fetch_execution(monkeypatch):
    DATASOURCE_REGISTRY["dummy"] = DummyDataSource

    pipeline_def = {"pipeline":[{"id": "step1", "datasource": "dummy"}]}
    runner = PipelineRunner(pipeline_def)
    result = runner.run()

    assert result["step1"] == "dummy_data"

def test_step_missing_operator_and_datasource():
    pipeline_def = {"pipeline":[{"id": "step1"}]}
    runner = PipelineRunner(pipeline_def)
    with pytest.raises(ValueError, match="must have either 'operator' or 'datasource'"):
        runner.run()
