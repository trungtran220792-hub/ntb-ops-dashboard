# -*- coding: utf-8 -*-
import gzip
import os
import sys
import zlib

sys.stdout.reconfigure(encoding='utf-8')

cache_files = [
    r"C:\Users\lap4all\.gemini\antigravity-browser-profile\Default\Cache\Cache_Data\f_0003ea",
    r"C:\Users\lap4all\.gemini\antigravity-browser-profile\Default\Cache\Cache_Data\f_0003f5",
    r"C:\Users\lap4all\.gemini\antigravity-browser-profile\Default\Cache\Cache_Data\f_000410"
]

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

for path in cache_files:
    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        continue
        
    size = os.path.getsize(path)
    print(f"\nInspecting {path} (size: {size} bytes)...")
    
    with open(path, 'rb') as f:
        content = f.read()
        
    # Search raw content first
    if b"switchNtbRegion" in content:
        print("  FOUND 'switchNtbRegion' in raw content!")
        continue
        
    # Search for gzip/zlib header, or try decompressing segments
    # Browser cache files (especially in Chromium) have a header before the actual HTTP payload.
    # The HTTP payload itself might be gzip-compressed.
    # Let's search for the gzip magic bytes (0x1f 0x8b) inside the content.
    gzip_magic = b'\x1f\x8b'
    idx = 0
    decompressed_success = False
    while True:
        idx = content.find(gzip_magic, idx)
        if idx == -1:
            break
        # Try decompressing from this index
        decompressed = try_decompress(content[idx:])
        if decompressed:
            print(f"  Decompressed gzip segment starting at index {idx} (size: {len(decompressed)} bytes)")
            if b"switchNtbRegion" in decompressed:
                print("    FOUND 'switchNtbRegion' in decompressed content!")
                # Save decompressed content to a file
                out_path = f"c:\\Users\\lap4all\\Desktop\\New folder\\scratch\\decompressed_{os.path.basename(path)}.html"
                with open(out_path, 'wb') as out_f:
                    out_f.write(decompressed)
                print(f"    Saved decompressed HTML to {out_path}")
                decompressed_success = True
                break
        idx += 1
        
    if not decompressed_success:
        # Try zlib headers
        # Some caches are just raw deflate or have simple headers.
        # Let's try to decompress starting from various offsets (0 to 1000)
        for offset in range(0, min(1000, len(content))):
            decompressed = try_decompress(content[offset:])
            if decompressed:
                print(f"  Decompressed zlib segment starting at offset {offset} (size: {len(decompressed)} bytes)")
                if b"switchNtbRegion" in decompressed:
                    print("    FOUND 'switchNtbRegion' in decompressed zlib content!")
                    out_path = f"c:\\Users\\lap4all\\Desktop\\New folder\\scratch\\decompressed_zlib_{os.path.basename(path)}.html"
                    with open(out_path, 'wb') as out_f:
                        out_f.write(decompressed)
                    print(f"    Saved decompressed HTML to {out_path}")
                    decompressed_success = True
                    break
        
    if not decompressed_success:
        print("  Could not find 'switchNtbRegion' in raw or decompressed contents.")
