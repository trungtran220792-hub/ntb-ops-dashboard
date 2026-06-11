# -*- coding: utf-8 -*-
with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's locate the target block of code and replace it cleanly
target = """        if 'Sản Lượng Lấy Thành Công' in df_ltc.columns:
            df_ltc['Sản Lượng Lấy Thành Công'] = pd.to_numeric(df_ltc['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(0)
            df_ltc['ltc_vol'] = df_ltc['Sản Lượng Lấy Thành Công']
        else:
                    # Center mapping or read from column K ('Sản Lượng Lấy Thành Công') if it exists
        df_ltc.columns = [c.strip() for c in df_ltc.columns]
        if 'Sản Lượng Lấy Thành Công' in df_ltc.columns:
            df_ltc['ltc_vol'] = pd.to_numeric(df_ltc['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(df_ltc['Volume'] * df_ltc['%LTC'])
        else:
            df_ltc['ltc_vol'] = df_ltc['Volume'] * df_ltc['%LTC']"""

replacement = """        df_ltc.columns = [c.strip() for c in df_ltc.columns]
        if 'Sản Lượng Lấy Thành Công' in df_ltc.columns:
            df_ltc['ltc_vol'] = pd.to_numeric(df_ltc['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(df_ltc['Volume'] * df_ltc['%LTC'])
        else:
            df_ltc['ltc_vol'] = df_ltc['Volume'] * df_ltc['%LTC']"""

if target in content:
    content = content.replace(target, replacement)
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed indentation and consolidated LTC logic in app.py successfully!")
else:
    print("Target block not found in app.py!")
