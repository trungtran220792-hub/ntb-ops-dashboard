# -*- coding: utf-8 -*-
import gzip
import os
import sys
import zlib

sys.stdout.reconfigure(encoding='utf-8')

cache_dir = r"C:\Users\lap4all\.gemini\antigravity-browser-profile\Default\Cache\Cache_Data"
target = b"switchNtbRegion"

def try_decompress(data):
    # Try gzip
    try:
        return gzip.decompress(data)
    except Exception:
        pass
    
    # Try zlib (deflate)
    try:
        return zlib.decompress(data)
    except Exception:
        pass
    
    # Try raw deflate
    try:
        return zlib.decompress(data, -15)
    except Exception:
        pass
        
    return None

if not os.path.exists(cache_dir):
    print("Cache dir does not exist.")
    sys.exit(1)

print(f"Scanning all files in {cache_dir}...")
count = 0
found_count = 0

for root, dirs, files in os.walk(cache_dir):
    for f in files:
        path = os.path.join(root, f)
        count += 1
        try:
            size = os.path.getsize(path)
            if size < 5000: # Skip small files
                continue
            with open(path, 'rb') as file_obj:
                content = file_obj.read()
            
            # 1. Search raw content
            if target in content:
                print(f"  FOUND in raw file: {path} (size: {size} bytes)")
                out_path = f"c:\\Users\\lap4all\\Desktop\\New folder\\scratch\\found_raw_{f}.html"
                with open(out_path, 'wb') as out_f:
                    out_f.write(content)
                print(f"  Saved raw content to {out_path}")
                found_count += 1
                continue
                
            # 2. Search decompressed segments
            gzip_magic = b'\x1f\x8b'
            idx = 0
            while True:
                idx = content.find(gzip_magic, idx)
                if idx == -1:
                    break
                decompressed = try_decompress(content[idx:])
                if decompressed:
                    if target in decompressed:
                        print(f"  FOUND in decompressed gzip at index {idx} in file: {path} (size: {size} bytes)")
                        out_path = f"c:\\Users\\lap4all\\Desktop\\New folder\\scratch\\found_decompressed_{f}.html"
                        with open(out_path, 'wb') as out_f:
                            out_f.write(decompressed)
                        print(f"  Saved decompressed content to {out_path}")
                        found_count += 1
                        break
                idx += 1
                
        except Exception as e:
            pass

print(f"\nScan complete. Scanned {count} files. Found {found_count} matching files.")
