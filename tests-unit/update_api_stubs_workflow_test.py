from pathlib import Path
import shlex

import yaml


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / ".github/workflows/update-api-stubs.yml"


def load_workflow():
    with WORKFLOW_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_step(step_name: str):
    workflow = load_workflow()
    steps = workflow["jobs"]["generate-models"]["steps"]
    return next(step for step in steps if step["name"] == step_name)


def test_update_api_stubs_redocly_config_path_exists():
    run = get_step("Filter OpenAPI spec with Redocly")["run"]
    parts = shlex.split(run)

    if "--config" not in parts:
        return

    config_path = WORKFLOW_PATH.parents[1] / parts[parts.index("--config") + 1]
    assert config_path.is_file()


def test_update_api_stubs_workflow_requests_pr_permissions():
    permissions = load_workflow()["permissions"]
    assert permissions["contents"] == "write"
    assert permissions["pull-requests"] == "write"
