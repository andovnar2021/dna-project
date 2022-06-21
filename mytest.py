
from myapp import searchletters, client

def test_searchletters():
   assert {'e','o'} == searchletters("hello","aeoiu")
    
    

def test_main_page():
   res = client.get("/")
   assert res.status_code == 200

def test_login():
   res = client.get("/login")
   assert res.status_code == 200

def test_logout():
   res = client.get("/logout")
   assert res.status_code == 200
    
def test_simple3():
    mylist = [1,3,5]
    
    assert 5 in mylist