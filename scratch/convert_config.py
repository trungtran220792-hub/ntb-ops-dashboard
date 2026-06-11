import json
import os

new_config = {
    "ops_gtc_url": "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit?gid=0#gid=0",
    "ops_ltc_url": "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit?gid=1365110988#gid=1365110988",
    "ops_co_cau_url": "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit?gid=1666412390#gid=1666412390",
    "ops_tts_url": "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit?gid=1821576198#gid=1821576198",
    "opr_opr_url": "https://docs.google.com/spreadsheets/d/1B-QCbEnPpILFFEWPYheGdmkgYV9gSf4lAyQMlhzwOCM/edit?gid=352488066#gid=352488066",
    "opr_oe_url": "https://docs.google.com/spreadsheets/d/1B-QCbEnPpILFFEWPYheGdmkgYV9gSf4lAyQMlhzwOCM/edit?gid=1796648042#gid=1796648042",
    "opr_raw_url": "https://docs.google.com/spreadsheets/d/1B-QCbEnPpILFFEWPYheGdmkgYV9gSf4lAyQMlhzwOCM/edit?gid=870632257#gid=870632257",
    "aging_raw_url": "https://docs.google.com/spreadsheets/d/1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU/edit?gid=1040733966#gid=1040733966",
    "aging_co_cau_url": "https://docs.google.com/spreadsheets/d/1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU/edit?gid=1907138547#gid=1907138547",
    "treo_stuck_url": "https://docs.google.com/spreadsheets/d/1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8/edit?gid=1550204633#gid=1550204633",
    "treo_co_cau_url": "https://docs.google.com/spreadsheets/d/1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8/edit?gid=1880816497#gid=1880816497",
    "bat_on_url": "https://docs.google.com/spreadsheets/d/1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec/edit?gid=250113221#gid=250113221",
    "off_spe_url": "https://docs.google.com/spreadsheets/d/1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg/edit?gid=1524249564#gid=1524249564",
    "tao_don_url": "https://docs.google.com/spreadsheets/d/1OygEPTn6Qu8okwAqpbx_RBiYQr1cfpO5hiaxqu4AMNE/edit?gid=0#gid=0"
}

# Write config.json
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(new_config, f, indent=4, ensure_ascii=False)
print("Updated config.json successfully.")

# Write .env
env_lines = []
for k, v in new_config.items():
    env_name = k.upper()
    env_lines.append(f'{env_name}="{v}"\n')

with open('.env', 'w', encoding='utf-8') as f:
    f.writelines(env_lines)
print("Updated .env successfully.")
