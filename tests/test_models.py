from project.models import User


def test_new_user():
    user = User("usertest", "FlaskIsAwesome")
    assert user.username == "usertest"
    assert user.password_hashed != "FlaskIsAwesome"
    assert user.__repr__() == "<User: usertest>"


def test_new_user_with_fixture(new_user):
    assert new_user.username == "usertest"
    assert new_user.password_hashed != "test"


def test_setting_password(new_user):
    new_user.set_password("MyNewPassword")
    assert new_user.password_hashed != "MyNewPassword"
    assert new_user.is_password_correct("MyNewPassword")
    assert not new_user.is_password_correct("MyNewPassword2")
    assert not new_user.is_password_correct("Password")


def test_user_id(new_user):
    new_user.id = 17
    assert isinstance(new_user.id , int)
    assert not isinstance(new_user.id, str)
    assert new_user.id == 17
