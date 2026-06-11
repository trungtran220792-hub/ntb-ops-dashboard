with open("scratch/initial_data_line.txt", "r", encoding="utf-8") as f:
    text = f.read()

titles = ["OPR", "rawopr", "CoCauVung", "Data", "TTS", "DataLTC", "ODR TTS", "shopee_tiktok", "Aging trên 5 ngày", "Treo LC", "Nhân Sự", "Đang off"]

out = []
for title in titles:
    pos = 0
    while True:
        pos = text.find(title, pos)
        if pos == -1:
            break
        out.append(f"Title: {title} at index {pos}")
        out.append(f"  Surrounding: {text[max(0, pos-100):min(len(text), pos+100)]}")
        pos += len(title)

with open("scratch/find_gids_in_bootstrap_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Done writing scratch/find_gids_in_bootstrap_res.txt")
