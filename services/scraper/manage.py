
from project import create_app
from flask.cli import FlaskGroup
import pytest

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def test():
    """Runs the tests."""
    pytest.main(["-s", "project/tests"])


if __name__ == "__main__":
    cli()
