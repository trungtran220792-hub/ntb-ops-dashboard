# -*- coding: utf-8 -*-
import requests
import time
import sys

def run_sync_test():
    sys.stdout.reconfigure(encoding='utf-8')
    BASE_URL = "http://127.0.0.1:5000"
    session = requests.Session()
    
    # Login as admin
    print("Logging in...")
    login_res = session.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "admin123"})
    if login_res.status_code != 200:
        print("Login failed:", login_res.text)
        return
    
    # Fetch current config
    print("Getting current config...")
    config_res = session.get(f"{BASE_URL}/api/config")
    if config_res.status_code != 200:
        print("Failed to get config:", config_res.text)
        return
    current_config = config_res.json()
    print("Current consolidated_url:", current_config.get("consolidated_url"))
    
    # If consolidated_url is empty, set it
    consolidated_url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
    if not current_config.get("consolidated_url") or "*" in current_config.get("consolidated_url"):
        print(f"Setting consolidated_url to {consolidated_url}...")
        save_res = session.post(f"{BASE_URL}/api/config", json={
            "consolidated_url": consolidated_url,
            "telegram_bot_token": current_config.get("telegram_bot_token", ""),
            "telegram_chat_id": current_config.get("telegram_chat_id", ""),
            "gemini_api_key": current_config.get("gemini_api_key", "")
        })
        if save_res.status_code != 200:
            print("Failed to save config:", save_res.text)
            return
        print("Saved config successfully.")
    
    # Trigger Sync
    print("Triggering sync...")
    sync_res = session.post(f"{BASE_URL}/api/sync")
    if sync_res.status_code != 200:
        print("Failed to trigger sync:", sync_res.text)
        return
    
    print("Sync started. Monitoring progress...")
    for _ in range(30):
        status_res = session.get(f"{BASE_URL}/api/sync/status")
        if status_res.status_code != 200:
            print("Failed to get sync status:", status_res.text)
            break
        status = status_res.json()
        print(f"[{status.get('status')}] Progress: {status.get('progress')} | Error: {status.get('error')}")
        if status.get("status") in ["success", "error"]:
            break
        time.sleep(2)

if __name__ == "__main__":
    run_sync_test()
