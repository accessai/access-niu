import yaml

from access_niu.pipeline import build_pipeline


def test_build_pipeline():
    with open("samples/colors/template.yml", "r") as f:
        sample_template = yaml.safe_load(f)

    pipeline = build_pipeline(sample_template)

    assert len(pipeline) > 0
