import pytest
from pydantic import ValidationError

from printtune.vision import validate_inspection, _image_data_url


def example():
    return {
        "benchmark": "3DBenchy",
        "image_quality": "good",
        "observations": [{
            "defect": "ringing", "view": "port", "region": "cabin",
            "severity": 2, "confidence": 0.7, "evidence": "fading ripples",
        }],
        "uncertainty": ["cannot infer exact acceleration"],
        "summary": "Possible ringing",
        "recommended_next_checks": ["inspect accelerometer measurements"],
        "status": "review_required",
    }


def test_valid_inspection():
    assert validate_inspection(example(), {"port"}).status == "review_required"


def test_reject_unprovided_view():
    with pytest.raises(ValueError):
        validate_inspection(example(), {"bow"})


def test_reject_unknown_defect():
    item = example()
    item["observations"][0]["defect"] = "invented"
    with pytest.raises(ValueError):
        validate_inspection(item, {"port"})


def test_reject_invalid_confidence():
    item = example()
    item["observations"][0]["confidence"] = 1.5
    with pytest.raises(ValidationError):
        validate_inspection(item, {"port"})


def test_reject_unsupported_image(tmp_path):
    file = tmp_path / "photo.svg"
    file.write_text("no")
    with pytest.raises(ValueError):
        _image_data_url(file)
