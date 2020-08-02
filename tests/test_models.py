from urnie.models import User

def test_user_password():
    u = User()
    u.set_password('abcdef')
    assert u.check_password('abcdef') == True
    assert u.check_password('aabbcc') == False
