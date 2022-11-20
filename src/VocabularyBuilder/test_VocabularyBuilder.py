from typer.testing import CliRunner
from VocabularyBuilder import app
import pytest

runner=CliRunner()

# standard bye test
def test_bye():
    result = runner.invoke(app, ["bye"])
    assert result.exit_code == 0
    assert "👋 Bye bye!" in result.stdout


# test for simple definition
def test_define():
    result = runner.invoke(app, ["define", "hello"])
    assert result.exit_code == 0
    assert "5. An expression" in result.stdout
    
# test for short definition
def test_define_short():
    result = runner.invoke(app, ["define", "hello", "--short"])
    assert result.exit_code == 0
    assert """noun: "Hello!" or an equivalent greeting""" in result.stdout
    
# test for pronunciation

# test for tagging

