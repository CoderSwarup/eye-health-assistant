"""Unit tests for result type."""

import pytest

from eye_health_assistant.core.result import Err, Ok


def test_ok_is_ok():
    """Ok result should report is_ok=True."""
    result = Ok(42)
    assert result.is_ok is True
    assert result.is_err is False


def test_ok_unwrap():
    """Ok unwrap should return the value."""
    result = Ok("hello")
    assert result.unwrap() == "hello"


def test_ok_unwrap_or():
    """Ok unwrap_or should return the contained value."""
    result = Ok(42)
    assert result.unwrap_or(0) == 42


def test_err_is_err():
    """Err result should report is_err=True."""
    result = Err(ValueError("bad"))
    assert result.is_err is True
    assert result.is_ok is False


def test_err_unwrap_raises():
    """Err unwrap should raise the error."""
    result = Err(ValueError("bad"))
    with pytest.raises(ValueError, match="bad"):
        result.unwrap()


def test_err_unwrap_or_returns_default():
    """Err unwrap_or should return the default."""
    result = Err(ValueError("bad"))
    assert result.unwrap_or(99) == 99
