from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_FILE = Path(__file__).resolve().parents[1] / "app.py"


def test_app_starts_with_default_values():
    app = AppTest.from_file(str(APP_FILE), default_timeout=20)
    app.run()

    assert not app.exception
    assert any("FlowLab" in block.value for block in app.markdown)
    assert any(metric.label == "Actual discharge" for metric in app.metric)
    assert any("13.97 L/s" in metric.value for metric in app.metric)


def test_invalid_diameter_is_reported_without_crash():
    app = AppTest.from_file(str(APP_FILE), default_timeout=20)
    app.run()

    # D2 is the second number input in the sidebar.
    app.number_input[1].set_value(100.0).run()

    assert not app.exception
    assert app.error
    assert "must be smaller than inlet" in app.error[0].value
