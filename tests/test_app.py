def test_app_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert "test.db" in app.config["SQLALCHEMY_DATABASE_URI"]


def test_cli_command_to_initialize_database(runner):
    output = runner.invoke(args=["init-db"])
    assert output.exit_code == 0
    assert "Initialized the database!" in output.output
