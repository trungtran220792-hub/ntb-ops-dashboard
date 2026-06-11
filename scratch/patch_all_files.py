# -*- coding: utf-8 -*-
import os

def patch_index_html():
    index_path = "templates/index.html"
    backup_path = "scratch/templates_index_backup_before_reset.html"
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Add sidebar tab 'nav-tab-nhan-su' right before 'nav-tab-sync'
    sync_tab_li = '<li class="menu-item" id="nav-tab-sync" onclick="switchTab(\'tab-sync\', this)">'
    nhan_su_li = '''                <li class="menu-item" id="nav-tab-nhan-su" onclick="switchTab('tab-nhan-su', this)">
                    <i class="fa-solid fa-users"></i> Quản lý Nhân sự
                </li>\n'''
    if nhan_su_li.strip() not in content:
        content = content.replace(sync_tab_li, nhan_su_li + "                " + sync_tab_li)
    
    # 2. Extract and insert '#tab-nhan-su' content panel right before '#tab-sync'
    nhan_su_panel_path = "scratch/nhan_su_panel.html"
    if os.path.exists(nhan_su_panel_path):
        with open(nhan_su_panel_path, "r", encoding="utf-8") as f:
            nhan_su_panel_html = f.read()
            
        sync_panel_div = '<div id="tab-sync" class="content-panel">'
        if 'id="tab-nhan-su"' not in content:
            content = content.replace(sync_panel_div, nhan_su_panel_html + "\n            " + sync_panel_div)
            
    # 3. Insert '#card-telegram-ai-config' right after '#card-google-sheets-config' inside '#tab-sync'
    telegram_card_html = '''                <!-- Telegram & AI Config Card -->
                <div class="card" id="card-telegram-ai-config" style="margin-top: 24px; margin-bottom: 24px;">
                    <div class="card-header">
                        <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 18px; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                            <i class="fa-solid fa-robot" style="color: var(--color-ghn-orange);"></i>
                            Cấu hình Telegram & Trợ lý AI Cảnh báo
                        </h3>
                    </div>
                    <div style="background: rgba(79, 70, 229, 0.05); border-left: 4px solid var(--color-indigo); padding: 16px; border-radius: 0 8px 8px 0; margin-bottom: 24px; font-size: 13px; line-height: 1.6;">
                        <p style="font-weight: 600; color: var(--color-indigo); margin-bottom: 4px;">
                            <i class="fa-solid fa-circle-info"></i> Hướng dẫn cấu hình AI Bot Telegram:
                        </p>
                        <ul style="margin-left: 20px; color: var(--text-secondary); list-style-type: disc;">
                            <li>Nhập <strong>Telegram Bot Token</strong> và <strong>Chat ID / Group ID</strong> của nhóm nhận tin báo cáo.</li>
                            <li>Nhập <strong>Gemini API Key</strong> để cho trợ lý AI đọc dữ liệu số của ngày báo cáo và tự động soạn bản tin gửi nhóm.</li>
                            <li>Bấm <strong>"Gửi bản tin phân tích AI"</strong> để AI tạo báo cáo chi tiết gửi Telegram, hoặc <strong>"Gửi cảnh báo sản lượng đột biến"</strong> để gửi nhanh danh sách bưu cục có sản lượng tăng vọt.</li>
                        </ul>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px;">
                        <div class="filter-group" style="width: 100%;">
                            <label style="font-weight: 600; font-size: 12px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                                <i class="fa-brands fa-telegram" style="color: #229ED9;"></i> Telegram Bot Token
                            </label>
                            <input type="password" id="telegram-bot-token" class="text-input" style="width: 100%;" placeholder="Nhập Token của Bot Telegram...">
                        </div>
                        <div class="filter-group" style="width: 100%;">
                            <label style="font-weight: 600; font-size: 12px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                                <i class="fa-solid fa-comments" style="color: #229ED9;"></i> Chat ID / Group ID nhận tin
                            </label>
                            <input type="text" id="telegram-chat-id" class="text-input" style="width: 100%;" placeholder="Ví dụ: -100xxxxxxxxxx hoặc Chat ID...">
                        </div>
                        <div class="filter-group" style="width: 100%;">
                            <label style="font-weight: 600; font-size: 12px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                                <i class="fa-solid fa-key" style="color: var(--color-indigo);"></i> Gemini API Key (AI)
                            </label>
                            <input type="password" id="gemini-api-key" class="text-input" style="width: 100%;" placeholder="Nhập Gemini API Key...">
                        </div>
                    </div>
                    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                        <button class="btn" style="background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: white; padding: 10px 20px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2); border: none; font-weight: 600; display: inline-flex; align-items: center; gap: 8px;" onclick="sendTelegramAiBriefing()">
                            <i class="fa-solid fa-wand-magic-sparkles"></i> Gửi bản tin phân tích AI
                        </button>
                        <button class="btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 10px 20px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2); border: none; font-weight: 600; display: inline-flex; align-items: center; gap: 8px;" onclick="sendTelegramWarning()">
                            <i class="fa-solid fa-triangle-exclamation"></i> Gửi cảnh báo sản lượng đột biến
                        </button>
                    </div>
                </div>'''
                
    google_sheets_config_end = '''                        <button class="btn btn-primary" style="padding: 10px 20px;" onclick="saveGoogleSheetsConfig()">
                            <i class="fa-solid fa-floppy-disk"></i> Lưu cấu hình Google Sheet
                        </button>
                    </div>
                </div>'''
                
    if 'id="card-telegram-ai-config"' not in content:
        content = content.replace(google_sheets_config_end, google_sheets_config_end + "\n\n" + telegram_card_html)
        
    # 4. Update gateMenuTabs() to include 'tab-nhan-su'
    tab_list_target = """            const tabIds = [
                'tab-dashboard',
                'tab-introduction',
                'tab-ntb-summary',
                'tab-operational',
                'tab-opr',
                'tab-backlog',
                'tab-unstable-po',
                'tab-off-spe',
                'tab-volume-creation',
                'tab-sync'
            ];"""
            
    tab_list_replacement = """            const tabIds = [
                'tab-dashboard',
                'tab-introduction',
                'tab-ntb-summary',
                'tab-operational',
                'tab-opr',
                'tab-backlog',
                'tab-unstable-po',
                'tab-off-spe',
                'tab-volume-creation',
                'tab-nhan-su',
                'tab-sync'
            ];"""
    content = content.replace(tab_list_target, tab_list_replacement)
    
    # 5. Update switchTab() to load nhan su data when switching to 'tab-nhan-su'
    switch_tab_end = """            // Force donut chart update when switching to backlog tab
            if (tabId === 'tab-backlog') {
                setTimeout(() => {
                    const bl = globalData.backlog;
                    if (bl && backlogPieChart) {
                        const blAging = bl.aging ? bl.aging.total_backlog : 0;
                        const blTreoGiao = bl.treo ? bl.treo.total_giao : 0;
                        const blTreoTra = bl.treo ? bl.treo.total_tra : 0;
                        backlogPieChart.updateSeries([blAging, blTreoGiao, blTreoTra]);
                    }
                }, 100);
            }
        }"""
        
    switch_tab_replacement = """            // Force donut chart update when switching to backlog tab
            if (tabId === 'tab-backlog') {
                setTimeout(() => {
                    const bl = globalData.backlog;
                    if (bl && backlogPieChart) {
                        const blAging = bl.aging ? bl.aging.total_backlog : 0;
                        const blTreoGiao = bl.treo ? bl.treo.total_giao : 0;
                        const blTreoTra = bl.treo ? bl.treo.total_tra : 0;
                        backlogPieChart.updateSeries([blAging, blTreoGiao, blTreoTra]);
                    }
                }, 100);
            }
            if (tabId === 'tab-nhan-su') {
                loadNhanSuData();
            }
        }"""
    content = content.replace(switch_tab_end, switch_tab_replacement)
    
    # 6. Update loadGoogleSheetsConfig() and saveGoogleSheetsConfig() JS functions
    load_config_target = """        function loadGoogleSheetsConfig() {
            try {
                const res = await fetch(getApiUrl('/api/config'), getFetchOptions());
                if (res.ok) {
                    const config = await res.json();
                    document.getElementById('sheet-consolidated-url').value = config.consolidated_url || '';
                }
            } catch (err) {
                console.error("Lỗi load cấu hình Google Sheets: ", err);
            }
        }"""
        
    load_config_replacement = """        async function loadGoogleSheetsConfig() {
            try {
                const res = await fetch(getApiUrl('/api/config'), getFetchOptions());
                if (res.ok) {
                    const config = await res.json();
                    document.getElementById('sheet-consolidated-url').value = config.consolidated_url || '';
                    const botTokenEl = document.getElementById('telegram-bot-token');
                    const chatIdEl = document.getElementById('telegram-chat-id');
                    const geminiKeyEl = document.getElementById('gemini-api-key');
                    if (botTokenEl) botTokenEl.value = config.telegram_bot_token || '';
                    if (chatIdEl) chatIdEl.value = config.telegram_chat_id || '';
                    if (geminiKeyEl) geminiKeyEl.value = config.gemini_api_key || '';
                }
            } catch (err) {
                console.error("Lỗi load cấu hình: ", err);
            }
        }"""
    content = content.replace(load_config_target, load_config_replacement)
    
    save_config_target = """        async function saveGoogleSheetsConfig() {
            const config = {
                consolidated_url: document.getElementById('sheet-consolidated-url').value.trim()
            };

            showLoading("Đang lưu cấu hình...");
            try {
                const res = await fetch(getApiUrl('/api/config'), getFetchOptions({
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(config)
                }));
                if (res.ok) {
                    alert("Lưu cấu hình Google Sheet thành công!");
                } else {
                    const err = await res.json();
                    alert("Lưu cấu hình thất bại: " + err.error);
                }
            } catch (err) {
                alert("Lỗi kết nối khi lưu cấu hình: " + err.message);
            } finally {
                hideLoading();
            }
        }"""
        
    save_config_replacement = """        async function saveGoogleSheetsConfig() {
            const config = {
                consolidated_url: document.getElementById('sheet-consolidated-url').value.trim(),
                telegram_bot_token: document.getElementById('telegram-bot-token') ? document.getElementById('telegram-bot-token').value.trim() : '',
                telegram_chat_id: document.getElementById('telegram-chat-id') ? document.getElementById('telegram-chat-id').value.trim() : '',
                gemini_api_key: document.getElementById('gemini-api-key') ? document.getElementById('gemini-api-key').value.trim() : ''
            };

            showLoading("Đang lưu cấu hình...");
            try {
                const res = await fetch(getApiUrl('/api/config'), getFetchOptions({
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(config)
                }));
                if (res.ok) {
                    alert("Lưu cấu hình thành công!");
                    loadGoogleSheetsConfig(); // reload to get masked keys
                } else {
                    const err = await res.json();
                    alert("Lưu cấu hình thất bại: " + err.error);
                }
            } catch (err) {
                alert("Lỗi kết nối khi lưu cấu hình: " + err.message);
            } finally {
                hideLoading();
            }
        }"""
    content = content.replace(save_config_target, save_config_replacement)
    
    # 7. Add Table Stripes & alignment Styles in head
    style_target = "    </style>"
    style_addition = """
        /* Alternating row stripes and center alignment for custom tables */
        .custom-table tbody tr:nth-child(even) {
            background-color: rgba(241, 245, 249, 0.5);
        }
        .custom-table td {
            text-align: center;
        }
    </style>"""
    if "Alternating row stripes" not in content:
        content = content.replace(style_target, style_addition)
        
    # 8. Append JavaScript functions from backup_js_functions.js
    js_funcs_path = "scratch/backup_js_functions.js"
    if os.path.exists(js_funcs_path):
        with open(js_funcs_path, "r", encoding="utf-8") as f:
            js_funcs = f.read()
            
        js_clean = ""
        for line in js_funcs.splitlines():
            if line.startswith("===") and line.endswith("==="):
                continue
            js_clean += line + "\n"
            
        script_end_tag = "    </script>\n</body>"
        if 'function loadNhanSuData()' not in content:
            content = content.replace(script_end_tag, js_clean + "\n" + script_end_tag)
            
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Index HTML patched successfully.")

def patch_app_py():
    app_path = "app.py"
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Modify LTC volume calculations in process_operational_report
    ltc_vol_target = "df_ltc['ltc_vol'] = df_ltc['Volume'] * df_ltc['%LTC']"
    ltc_vol_replacement = """        # Center mapping or read from column K ('Sản Lượng Lấy Thành Công') if it exists
        df_ltc.columns = [c.strip() for c in df_ltc.columns]
        if 'Sản Lượng Lấy Thành Công' in df_ltc.columns:
            df_ltc['ltc_vol'] = pd.to_numeric(df_ltc['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(df_ltc['Volume'] * df_ltc['%LTC'])
        else:
            df_ltc['ltc_vol'] = df_ltc['Volume'] * df_ltc['%LTC']"""
            
    if ltc_vol_target in content:
        content = content.replace(ltc_vol_target, ltc_vol_replacement)
        
    # 2. Remove "chưa đạt" from chatbot response
    chua_dat_target = 'reply += "⚠️ Hiệu suất OPR hiện tại chưa đạt mục tiêu tối thiểu (Target: >= 80%). Cần tập trung cải thiện thời gian xử lý đơn hàng."'
    chua_dat_replacement = 'reply += "⚠️ Hiệu suất OPR hiện tại dưới mục tiêu tối thiểu (Target: >= 80%). Cần tập trung cải thiện thời gian xử lý đơn hàng."'
    if chua_dat_target in content:
        content = content.replace(chua_dat_target, chua_dat_replacement)
        
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("App.py patched successfully.")

if __name__ == "__main__":
    patch_index_html()
    patch_app_py()
