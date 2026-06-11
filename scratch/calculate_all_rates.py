import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    df_gtc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='Data')
    df_ltc = pd.read_excel('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', sheet_name='DataLTC')
    
    latest = '2026-06-08 - Thứ 2'
    
    g_latest = df_gtc[df_gtc['Time'] == latest]
    l_latest = df_ltc[df_ltc['Time'] == latest]
    
    print("GTC SUMS:")
    for col in g_latest.columns:
        try:
            num_sum = pd.to_numeric(g_latest[col], errors='coerce').sum()
            print(f"  {col}: {num_sum}")
        except Exception:
            pass
            
    print("\nLTC SUMS:")
    for col in l_latest.columns:
        try:
            num_sum = pd.to_numeric(l_latest[col], errors='coerce').sum()
            print(f"  {col}: {num_sum}")
        except Exception:
            pass
            
    # Calculate GTC metrics
    g_vol = g_latest['Volume'].sum()
    g_gan = g_latest['Sản Lượng Gán'].sum()
    g_gtc = g_latest['Sản Lượng Giao Thành Công'].sum()
    g_tra = g_latest['Sản Lượng Chuyển Trả'].sum()
    g_ton = g_latest['Sản Lượng Tồn'].sum()
    g_chua_gan = g_latest['Sản Lượng Chưa Gán'].sum()
    
    print("\nCalculated GTC overall rates:")
    print(f"  Gán / Volume: {g_gan / g_vol * 100:.6f}%")
    print(f"  GTC / Volume: {g_gtc / g_vol * 100:.6f}%")
    print(f"  Tráo / Volume: {g_tra / g_vol * 100:.6f}%")
    print(f"  Tồn / Volume: {g_ton / g_vol * 100:.6f}%")
    print(f"  Chưa Gán / Volume: {g_chua_gan / g_vol * 100:.6f}%")
    
    # Calculate LTC metrics
    l_vol = l_latest['Volume'].sum()
    l_gan = l_latest['Sản Lượng Gán'].sum()
    l_lay = l_latest['Sản Lượng Lấy Thành Công'].sum()
    l_chua_gan = l_latest['Sản Lượng Chưa Gán'].sum()
    
    print("\nCalculated LTC overall rates:")
    print(f"  Gán / Volume: {l_gan / l_vol * 100:.6f}%")
    print(f"  Lấy / Volume: {l_lay / l_vol * 100:.6f}%")
    print(f"  Chưa Gán / Volume: {l_chua_gan / l_vol * 100:.6f}%")
    
    # What about other files?
    # Are there any other excel workbooks?
    # Let's list files in the workspace and check if they contain 87.77% on 2026-06-08.

except Exception as e:
    print("Error:", e)
