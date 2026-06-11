import os

csv_configs = {
    'ops_gtc.csv': (
        'Cấp Quản Lý,Chi tiết,Loại Hàng,Time,Volume,% Gán,% GTC,% Chuyển trả,Leadtime,Sản Lượng Giao Thành Công,Sản Lượng Chuyển Trả,Sản Lượng Gán,Sản Lượng Trả,Sản Lượng Tồn,Sản Lượng Chưa Gán,% Chưa Gán,%Tồn,Hàng Mới Về Trong Ngày,Tỉnh,Vùng,AM\n'
        'NTB - Khánh Hòa,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Hàng Mới Ca 1,2026-06-09 - Thứ 3,100,0.9,0.8,0.02,6.0,80.0,2.0,90.0,2.0,18.0,10.0,0.1,0.18,100,Khánh Hòa,NTB,Thái Thị Thanh Thư\n'
    ),
    'ops_ltc.csv': (
        'Cấp quản lý,Chi tiết,Ca,Time,Volume,%Gán,%LTC,%Đóng kiện,%LC,Leadtime\n'
        'NTB - Khánh Hòa,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Hàng Tồn,2026-06-09 - Thứ 3,50,0.85,0.75,0.7,0.68,12.0\n'
    ),
    'ops_co_cau.csv': (
        'warehouse_id,Bưu cục,Tỉnh,AM\n'
        '22830000,Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Khánh Hòa,Thái Thị Thanh Thư\n'
        '20495000,Bưu Cục 40A Yết Kiêu-Nha Trang-Khánh Hòa,Khánh Hòa,Phan Đình Duy\n'
        '20320000,Bưu Cục 466 Đường 23/10-Nha Trang-Khánh Hòa,Khánh Hòa,Phan Đình Duy\n'
        '22746000,Bưu Cục 229 Phước Long-Nam Nha Trang-Khánh Hòa,Khánh Hòa,Thái Thị Thanh Thư\n'
        '22549000,Bưu Cục 21 Trần Hưng Đạo-Xã Phan Rí Cửa-Bình Thuận,Bình Thuận,Nguyễn Duy Long\n'
    ),
    'co_cau_ntb.csv': (
        'warehouse_id,Bưu cục,AM,Tỉnh\n'
        '22830000,Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Thái Thị Thanh Thư,Khánh Hòa\n'
    ),
    'ops_tts.csv': (
        'Cấp Quản Lý,Chi tiết,Loại Hàng,Time,Volume,% Gán,% GTC,% Chuyển trả,Leadtime,Sản Lượng Giao Thành Công,Sản Lượng Chuyển Trả,Sản Lượng Gán,Sản Lượng Trả,Sản Lượng Tồn,Sản Lượng Chưa Gán,% Chưa Gán,%Tồn,Hàng Mới Về Trong Ngày,Tỉnh,Vùng,AM\n'
        'NTB - Khánh Hòa,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Hàng Mới Ca 1,2026-06-09 - Thứ 3,20,0.9,0.8,0.02,6.0,80.0,2.0,90.0,2.0,18.0,10.0,0.1,0.18,20,Khánh Hòa,NTB,Thái Thị Thanh Thư\n'
    ),
    'opr_opr.csv': (
        'tutinh,kholay,NgayLTC,khung_gio_tao_don,ly_do_tre_12h,sellername,vol_ltc,tuan,vung,ot,Tuần,AM,Khung giờ tạo,Đơn trễ\n'
        'Khánh Hòa,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,2026-06-09,10:00,,Seller A,10,24,NTB,1,Tuần 24,Thái Thị Thanh Thư,10h,0\n'
    ),
    'opr_oe.csv': (
        'vung,madh,BC lấy,Thời gian tạo,Thời gian LTC,sellername,ly_do_tre_12h,AM\n'
        'NTB,VNGH80608636306,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,2026-06-09 10:00,2026-06-09 12:00,Seller A,,Thái Thị Thanh Thư\n'
    ),
    'opr_raw.csv': (
        'tutinh,kholay,NgayLTC,khung_gio_tao_don,ly_do_tre_12h,sellername,vol_ltc,tuan,vung,ot,Tuần,AM,Khung giờ tạo,Đơn trễ\n'
        'Khánh Hòa,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,2026-06-09,10:00,,Seller A,10,24,NTB,1,Tuần 24,Thái Thị Thanh Thư,10h,0\n'
    ),
    'aging_raw.csv': (
        'Mã đơn,Mã bưu cục gửi,Tên bưu cục gửi,Mã bưu cục nhận,Tên bưu cục nhận,Tỉnh/thành bưu cục nhận,Số ngày tồn,Số ngày đã nhập BC,BC,am_name,Tỉnh\n'
        'VNGH80410986306,22830000,Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,22830000,Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Khánh Hòa,6,6,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Thái Thị Thanh Thư,Khánh Hòa\n'
    ),
    'treo_stuck.csv': (
        'Mã đơn hàng,Trạng thái,warehouse_name,am_name,Tỉnh\n'
        'VNGH80767836306,Chưa đóng kiện,Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Thái Thị Thanh Thư,Khánh Hòa\n'
    ),
    'buu_cuc_bat_on.csv': (
        'Thời gian cập nhật,Vùng,Tỉnh,Mã bưu cục,Tên bưu cục,Loại bưu cục,Sản lượng gán,Sản lượng chưa gán,% Chưa Gán,Sản lượng tồn,Sản lượng giao thành công,% Giao thành công,Sản lượng chuyển trả,% Chuyển trả,Leadtime giao,Sản lượng,Sản lượng trung bình tuần n-1,Tăng trưởng sản lượng,Sản lượng chênh lệch,Trạng thái bưu cục,Trạng thái\n'
        '2026-06-10 07:30:56.160000,NTB,Khánh Hòa,22830000,Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,BC,1719,50,0.029,777,80,0.103,768,0.446,2.73,858,627,0.36,231,Bất ổn,Bất ổn\n'
    ),
    'off_tuyen_spe.csv': (
        'Tỉnh,Quận/ huyện,Phường/xã cần tắt,Bưu cục,Kết quả (KA) update,% Cap Down (KA),Thời gian tắt,Thời gian mở,Note\n'
        'Khánh Hòa,Cam Lâm,Xã Cam Hải Đông,Bưu Cục 42 Nguyễn Du-Cam Lâm-Khánh Hoà,DUYỆT,1.0,2026-06-09,2026-06-20,Tuyến Đang OFF\n'
    ),
    'vols_tao_don.csv': (
        'Date,Vùng,Tỉnh,Quận/Huyện,Phường/Xã,Bưu cục,Khách hàng,Volume,Khối lượng,warehouse_id,bat_on,province_name\n'
        '2026-06-09,NTB,Khánh Hòa,Cam Ranh,Cam Linh,Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Khách hàng A,100,50.0,22830000,Bình thường,Khánh Hòa\n'
        '2026-06-09,NTB,Khánh Hòa,Nha Trang,Xương Huân,Bưu Cục 40A Yết Kiêu-Nha Trang-Khánh Hòa,Khách hàng B,50,25.0,20495000,Bình thường,Khánh Hòa\n'
        '2026-06-09,NTB,Khánh Hòa,Nha Trang,Vĩnh Hải,Bưu Cục 466 Đường 23/10-Nha Trang-Khánh Hòa,Khách hàng C,60,30.0,20320000,Bình thường,Khánh Hòa\n'
    ),
    'ODR TTS.csv': (
        'Time,Vùng,Tỉnh,parsed_name,LTC_Done,LTC_Vol,LTC_Rate,GTC_Done,GTC_Vol,GTC_Rate,GTC_WTD_Done,GTC_WTD_Vol,GTC_WTD_Rate,LTC_WTD_Done,LTC_WTD_Vol,LTC_WTD_Rate\n'
        '2026-06-09,NTB,Khánh Hòa,BC 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,10,12,0.83,15,20,0.75,100,120,0.83,90,110,0.81\n'
    ),
    'ops_nhan_su.csv': (
        'ID,Tên nhân viên,Chức vụ,Ngày vào làm,Ngày nghỉ việc,Trạng thái,Bưu cục,Zone,AM,Loại HĐ,Tỉnh,Vùng,Thâm niên,SP Team?\n'
        '3173887,Nguyễn Tuấn Duy Khanh,Business Development Field Executive,2026-06-10,,Đang làm việc,22830000 - Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa,Zone Khanh Hoa,Thái Thị Thanh Thư,HĐDV,Khánh Hòa,NTB,G01: Dưới 1 tháng,False\n'
        '3173884,Võ Minh Phương,Business Development Field Executive,2026-06-10,,Đang làm việc,20495000 - Bưu Cục 40A Yết Kiêu-Nha Trang-Khánh Hòa,Zone Khanh Hoa,Thái Thị Thanh Thư,HĐDV,Khánh Hòa,NTB,G01: Dưới 1 tháng,False\n'
        '3173815,Phạm Văn Thương,Business Development Field Executive,2026-06-10,,Đang làm việc,20320000 - Bưu Cục 466 Đường 23/10-Nha Trang-Khánh Hòa,Zone Lam Dong,Huỳnh Tấn Hiền,HĐDV,Bình Thuận,NTB,G01: Dưới 1 tháng,False\n'
    )
}

print("Creating sample CSV files...")
for filename, content in csv_configs.items():
    filepath = filename
    print(f"Writing {filepath}...")
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)

print("Sample CSV files created successfully.")
