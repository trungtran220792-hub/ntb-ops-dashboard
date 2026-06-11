import os
import sys
import pandas as pd

# Add root folder to sys.path so we can import app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import get_db_engine, save_df_to_db, load_df_from_db, save_json_to_db, load_json_from_db, load_config, resolve_path

def test_db_fallback():
    print("Testing DB fallback logic (no DATABASE_URL set)...")
    # Backup environment variable
    db_env = os.environ.pop("DATABASE_URL", None)
    pg_env = os.environ.pop("POSTGRES_URL", None)
    
    engine = get_db_engine()
    assert engine is None, "Engine should be None when DATABASE_URL is not set"
    
    df = pd.DataFrame([{"a": 1, "b": 2}])
    saved = save_df_to_db(df, "test_file.csv")
    assert not saved, "Should return False when DB not configured"
    
    loaded = load_df_from_db("test_file.csv")
    assert loaded is None, "Should return None when DB not configured"
    
    # Restore environment variable
    if db_env:
        os.environ["DATABASE_URL"] = db_env
    if pg_env:
        os.environ["POSTGRES_URL"] = pg_env
    print("Fallback logic works perfectly.")

def test_sqlite_db():
    print("\nTesting DB functions using local SQLite file DB...")
    db_file = "test_temp.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except Exception:
            pass
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    
    # Reset internal engine cache
    import app
    app._db_engine = None
    
    engine = get_db_engine()
    assert engine is not None, "Engine should be created for sqlite"
    
    # Test DataFrame CRUD
    df_orig = pd.DataFrame([{"col1": "hello", "col2": 123}, {"col1": "world", "col2": 456}])
    saved = save_df_to_db(df_orig, "test_ops.csv")
    assert saved, "Should successfully save to SQLite DB"
    
    df_loaded = load_df_from_db("test_ops.csv")
    assert df_loaded is not None, "Should successfully load from SQLite DB"
    assert len(df_loaded) == 2
    assert df_loaded.iloc[0]["col1"] == "hello"
    assert df_loaded.iloc[1]["col2"] == 456
    
    # Test JSON CRUD
    json_orig = {"users": [{"name": "Admin", "role": "admin"}], "active": True}
    saved_json = save_json_to_db(json_orig, "test_config.json")
    assert saved_json, "Should successfully save JSON to SQLite DB"
    
    json_loaded = load_json_from_db("test_config.json")
    assert json_loaded is not None, "Should successfully load JSON from SQLite DB"
    assert json_loaded["active"] is True
    assert json_loaded["users"][0]["name"] == "Admin"
    
    # Reset env
    os.environ.pop("DATABASE_URL", None)
    app._db_engine = None
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except Exception:
            pass
    print("SQLite DB helper CRUD works perfectly.")

if __name__ == "__main__":
    try:
        test_db_fallback()
        test_sqlite_db()
        print("\nAll tests passed successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
