import requests

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    print("Testing GET / ...")
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200
    print("GET / passed (200 OK)")

def test_invalid_login():
    print("Testing /api/login with invalid credentials ...")
    res = requests.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "wrongpassword"})
    assert res.status_code == 401
    assert "Sai mã nhân viên hoặc mật khẩu" in res.json().get("error", "")
    print("Invalid login passed (401 Unauthorized)")

def test_valid_login_admin():
    print("Testing /api/login with valid admin credentials ...")
    session = requests.Session()
    res = session.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    data = res.json()
    assert data.get("success") is True
    assert data.get("role") == "admin"
    print("Valid admin login passed (200 OK)")
    
    # Test accessing user-role endpoint with session
    res_role = session.get(f"{BASE_URL}/api/user-role")
    assert res_role.status_code == 200
    role_data = res_role.json()
    assert role_data.get("username") == "admin"
    assert role_data.get("role") == "admin"
    print("Session-based role access passed (200 OK)")

def test_valid_login_staff():
    print("Testing /api/login with valid staff credentials ...")
    session = requests.Session()
    res = session.post(f"{BASE_URL}/api/login", json={"username": "staff", "password": "staff123"})
    assert res.status_code == 200
    data = res.json()
    assert data.get("success") is True
    assert data.get("role") == "staff"
    print("Valid staff login passed (200 OK)")
    
    # Test accessing user-role endpoint with session
    res_role = session.get(f"{BASE_URL}/api/user-role")
    assert res_role.status_code == 200
    role_data = res_role.json()
    assert role_data.get("username") == "staff"
    assert role_data.get("role") == "staff"
    print("Session-based staff role access passed (200 OK)")
    
    # Test accessing admin-only users endpoint (should fail for staff)
    res_users = session.get(f"{BASE_URL}/api/users")
    assert res_users.status_code == 403
    print("Admin gating for staff passed (403 Forbidden)")

def test_basic_auth_fallback():
    print("Testing Basic Auth fallback (no session) ...")
    res = requests.get(f"{BASE_URL}/api/user-role", auth=("admin", "admin123"))
    assert res.status_code == 200
    role_data = res.json()
    assert role_data.get("username") == "admin"
    assert role_data.get("role") == "admin"
    print("Basic Auth fallback passed (200 OK)")

def test_api_gating_no_auth():
    print("Testing API gating when not authenticated ...")
    res = requests.get(f"{BASE_URL}/api/user-role")
    assert res.status_code == 401
    assert "Yêu cầu đăng nhập" in res.json().get("error", "")
    print("API gating passed (401 Unauthorized)")

def test_user_crud_operations():
    print("Testing User CRUD operations as admin ...")
    session = requests.Session()
    session.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "admin123"})
    
    # 1. Create a user
    new_user = {
        "username": "test_user",
        "password": "testpassword123",
        "role": "staff",
        "permissions": ["tab-dashboard", "tab-opr"]
    }
    res_create = session.post(f"{BASE_URL}/api/users", json=new_user)
    assert res_create.status_code == 200
    assert res_create.json().get("success") is True
    print("Create user passed (200 OK)")
    
    # 2. Get list of users and verify new user exists
    res_get = session.get(f"{BASE_URL}/api/users")
    assert res_get.status_code == 200
    users_list = res_get.json()
    usernames = [u["username"] for u in users_list]
    assert "test_user" in usernames
    
    # Find the test user data
    test_user_data = next(u for u in users_list if u["username"] == "test_user")
    assert test_user_data["role"] == "staff"
    assert "tab-opr" in test_user_data["permissions"]
    print("Get user list and verification passed (200 OK)")
    
    # 3. Test logging in as the new user
    new_session = requests.Session()
    res_login = new_session.post(f"{BASE_URL}/api/login", json={"username": "test_user", "password": "testpassword123"})
    assert res_login.status_code == 200
    print("Login as new user passed (200 OK)")
    
    # Verify the roles/permissions endpoint for the new user
    res_role = new_session.get(f"{BASE_URL}/api/user-role")
    assert res_role.status_code == 200
    assert res_role.json().get("role") == "staff"
    assert "tab-opr" in res_role.json().get("permissions")
    print("Verify roles/permissions for new user passed (200 OK)")
    
    # 4. Delete the user
    res_delete = session.delete(f"{BASE_URL}/api/users/test_user")
    assert res_delete.status_code == 200
    assert res_delete.json().get("success") is True
    print("Delete user passed (200 OK)")
    
    # 5. Verify the user is gone and login fails
    res_get2 = session.get(f"{BASE_URL}/api/users")
    usernames2 = [u["username"] for u in res_get2.json()]
    assert "test_user" not in usernames2
    
    res_login2 = new_session.post(f"{BASE_URL}/api/login", json={"username": "test_user", "password": "testpassword123"})
    assert res_login2.status_code == 401
    print("Verification of deleted user passed (401 Unauthorized on login)")

if __name__ == "__main__":
    try:
        test_home()
        test_invalid_login()
        test_valid_login_admin()
        test_valid_login_staff()
        test_basic_auth_fallback()
        test_api_gating_no_auth()
        test_user_crud_operations()
        print("\nALL TESTS PASSED SUCCESSFULLY!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nTESTS FAILED: {e}")
