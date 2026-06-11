
        // Helper to handle local file:// api routing smoothly
        function getApiUrl(endpoint) {
            const baseUrl = window.location.protocol === 'file:' ? 'http://127.0.0.1:5000' : '';
            return baseUrl + endpoint;
        }

        // Builder for fetch options (headers)
        function getFetchOptions(options = {}) {
            options.credentials = 'include';
            if (window.location.protocol === 'file:') {
                if (!options.headers) options.headers = {};
                options.headers['Authorization'] = 'Basic ' + btoa('admin:admin123');
            }
            return options;
        }

        // Helper to escape HTML and prevent XSS
        function escapeHTML(str) {
            if (str === null || str === undefined) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }
        // State management
        let globalData = {
            operational: {},
            opr: {},
            backlog: {},
            unstablePo: {}
        };

        let filteredData = {
            oe_details: [],
            aging_details: [],
            treo_details: []
        };

        let paginationState = {
            opr: { current: 1, perPage: 15 },
            aging: { current: 1, perPage: 15 },
            treo: { current: 1, perPage: 15 }
        };

        // Header Subtitle update helper
        function updateHeaderSubtitle(tabId) {
            const lastSyncEl = document.getElementById('last-sync-time');
            if (!lastSyncEl) return;
            
            if (tabId === 'tab-dashboard') {
                const ops = globalData.operational;
                const latestDate = ops && ops.trend_gtc && ops.trend_gtc.length > 0 
                    ? ops.trend_gtc[ops.trend_gtc.length - 1].Time 
                    : "Chưa có";
                lastSyncEl.innerText = "Ngày báo cáo: " + latestDate;
            } else if (tabId === 'tab-backlog') {
                const bl = globalData.backlog;
                if (bl && bl.baseline_timestamp) {
                    lastSyncEl.innerText = "Đang so sánh với mốc: " + bl.baseline_timestamp;
                } else {
                    lastSyncEl.innerText = "Lần đồng bộ cuối: " + new Date().toLocaleTimeString();
                }
            } else {
                lastSyncEl.innerText = "Lần đồng bộ cuối: " + new Date().toLocaleTimeString();
            }
        }

        // Sub-tab switching for backlog tab
        function switchSubTab(subTabId) {
            document.querySelectorAll('#tab-backlog .sub-panel').forEach(panel => panel.classList.remove('active'));
            document.querySelectorAll('#tab-backlog .sub-tab-btn').forEach(btn => btn.classList.remove('active'));

            const activePanel = document.getElementById(`sub-panel-${subTabId}`);
            if (activePanel) activePanel.classList.add('active');

            const activeBtn = document.getElementById(`btn-${subTabId}`);
            if (activeBtn) activeBtn.classList.add('active');
            
            // Re-render donut chart if it's the summary panel to make sure it draws properly in case of size mismatch
            if (subTabId === 'backlog-summary') {
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
        }

        // Tab switching
        function switchTab(tabId, el) {
            document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('active'));
            document.querySelectorAll('.content-panel').forEach(panel => panel.classList.remove('active'));

            el.classList.add('active');
            document.getElementById(tabId).classList.add('active');

            // Set header title
            const tabName = el.innerText.trim();
            if (tabId === 'tab-introduction') {
                document.getElementById('page-title').innerText = "GIỚI THIỆU VÙNG NAM TRUNG BỘ";
            } else {
                document.getElementById('page-title').innerText = tabName + " Dashboard";
            }

            // Show/Hide baseline comparison selector based on tab
            const isBacklogTab = tabId === 'tab-backlog';
            document.getElementById('baseline-selector-container').style.display = isBacklogTab ? 'flex' : 'none';

            // Show/Hide global filters panel based on tab (xóa cái này - hifnh3)
            const isOpsTab = tabId === 'tab-operational' || tabId === 'tab-opr' || tabId === 'tab-backlog';
            const globalFilters = document.getElementById('global-filters');
            if (globalFilters) {
                globalFilters.style.display = isOpsTab ? 'flex' : 'none';
            }

            // Update header subtitle
            updateHeaderSubtitle(tabId);

            // Handle Leaflet map resizing and positioning on tab switch
            if (tabId === 'tab-introduction' && typeof _ntbMap !== 'undefined' && _ntbMap) {
                setTimeout(() => {
                    _ntbMap.invalidateSize();
                    _ntbMap.setView([12.2, 108.2], 7);
                }, 100);
            }

            // Force donut chart update when switching to backlog tab
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
        }

        let userRole = 'staff';
        let userPermissions = [];
        let loggedInUsername = '';

        async function checkUserRole() {
            try {
                const res = await fetch(getApiUrl('/api/user-role'), getFetchOptions());
                if (res.status === 401) {
                    // Show login overlay
                    document.querySelector('.app-layout').style.display = 'none';
                    document.getElementById('login-container').style.display = 'flex';
                    hideLoading();
                    return false;
                }
                
                if (res.ok) {
                    const data = await res.json();
                    userRole = data.role;
                    userPermissions = data.permissions || [];
                    loggedInUsername = data.username;

                    // Hide login overlay, show app layout
                    document.getElementById('login-container').style.display = 'none';
                    document.querySelector('.app-layout').style.display = 'flex';

                    // Update UI elements based on role & permissions
                    gateMenuTabs();

                    if (userRole === 'admin') {
                        // Show Google Sheets config card
                        const configCard = document.getElementById('card-google-sheets-config');
                        if (configCard) configCard.style.display = 'block';
                        
                        // Show sync buttons
                        const headerSyncBtn = document.getElementById('header-sync-btn');
                        if (headerSyncBtn) headerSyncBtn.style.display = 'inline-flex';
                        
                        const footerSyncBtn = document.getElementById('footer-sync-btn');
                        if (footerSyncBtn) footerSyncBtn.style.display = 'inline-block';

                        // Show user management card
                        const userMgmtCard = document.getElementById('card-user-management');
                        if (userMgmtCard) {
                            userMgmtCard.style.display = 'block';
                            loadUsersList();
                        }
                    } else {
                        // Hide Google Sheets config card
                        const configCard = document.getElementById('card-google-sheets-config');
                        if (configCard) configCard.style.display = 'none';
                        
                        // Show sync buttons
                        const headerSyncBtn = document.getElementById('header-sync-btn');
                        if (headerSyncBtn) headerSyncBtn.style.display = 'none';
                        
                        const footerSyncBtn = document.getElementById('footer-sync-btn');
                        if (footerSyncBtn) footerSyncBtn.style.display = 'none';

                        // Hide user management card
                        const userMgmtCard = document.getElementById('card-user-management');
                        if (userMgmtCard) userMgmtCard.style.display = 'none';
                    }
                    return true;
                }
            } catch (err) {
                console.error("Lỗi kiểm tra quyền người dùng: ", err);
            }
            return false;
        }

        function gateMenuTabs() {
            // Define all tab mappings
            const tabIds = [
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
            ];

            let firstAllowedTab = null;

            tabIds.forEach(tabId => {
                const navItem = document.getElementById('nav-' + tabId);
                if (!navItem) return;

                // Admin has all permissions. Otherwise check if tabId in userPermissions
                const isAllowed = userRole === 'admin' || userPermissions.includes(tabId);
                
                if (isAllowed) {
                    navItem.style.display = 'flex';
                    if (!firstAllowedTab) firstAllowedTab = tabId;
                } else {
                    navItem.style.display = 'none';
                }
            });

            // If current active tab is not allowed, switch to the first allowed tab
            const activePanel = document.querySelector('.content-panel.active');
            const activeTabId = activePanel ? activePanel.id : 'tab-dashboard';

            const isCurrentAllowed = userRole === 'admin' || userPermissions.includes(activeTabId);
            if (!isCurrentAllowed && firstAllowedTab) {
                const navBtn = document.getElementById('nav-' + firstAllowedTab);
                if (navBtn) {
                    switchTab(firstAllowedTab, navBtn);
                }
            }
        }

        async function handleLoginSubmit(event) {
            event.preventDefault();
            const usernameInput = document.getElementById('login-username');
            const passwordInput = document.getElementById('login-password');
            const errorMsg = document.getElementById('login-error-msg');
            const errorText = document.getElementById('login-error-text');

            const username = usernameInput.value.trim();
            const password = passwordInput.value;

            if (!username || !password) return;

            showLoading("Đang xác thực...");
            errorMsg.style.display = 'none';

            try {
                const res = await fetch(getApiUrl('/api/login'), getFetchOptions({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                }));

                if (res.ok) {
                    const data = await res.json();
                    usernameInput.value = '';
                    passwordInput.value = '';
                    
                    const loggedIn = await checkUserRole();
                    if (loggedIn) {
                        loadAllData();
                        loadFilesStatus();
                        loadHistoryDropdown();
                        loadNtbSummaryData();
                        loadGoogleSheetsConfig();
                        loadNtbStructure();
                    }
                } else {
                    const errData = await res.json();
                    errorText.innerText = errData.error || "Mã nhân viên hoặc mật khẩu không đúng.";
                    errorMsg.style.display = 'flex';
                }
            } catch (err) {
                errorText.innerText = "Lỗi kết nối máy chủ: " + err.message;
                errorMsg.style.display = 'flex';
            } finally {
                hideLoading();
            }
        }

        async function handleLogout() {
            if (!confirm("Bạn có chắc chắn muốn đăng xuất không?")) return;
            showLoading("Đang đăng xuất...");
            try {
                const res = await fetch(getApiUrl('/api/logout'), getFetchOptions({
                    method: 'POST'
                }));
                if (res.ok) {
                    userRole = 'staff';
                    userPermissions = [];
                    loggedInUsername = '';
                    
                    document.querySelector('.app-layout').style.display = 'none';
                    document.getElementById('login-container').style.display = 'flex';
                }
            } catch (err) {
                console.error("Lỗi khi đăng xuất: ", err);
            } finally {
                hideLoading();
            }
        }

        // USER CRUD LOGIC FOR ADMIN
        async function loadUsersList() {
            try {
                const res = await fetch(getApiUrl('/api/users'), getFetchOptions());
                if (res.ok) {
                    const users = await res.json();
                    const tbody = document.getElementById('table-users-mgmt-body');
                    tbody.innerHTML = '';

                    const friendlyTabNames = {
                        'tab-dashboard': 'Tổng quan',
                        'tab-introduction': 'Giới thiệu',
                        'tab-ntb-summary': 'Chỉ số',
                        'tab-operational': 'Vận hành',
                        'tab-opr': 'OPR',
                        'tab-backlog': 'Backlog',
                        'tab-unstable-po': 'Bất ổn',
                        'tab-off-spe': 'OFF SPE',
                        'tab-volume-creation': 'Sản lượng',
                        'tab-sync': 'Đồng bộ'
                    };

                    users.forEach(u => {
                        const tr = document.createElement('tr');
                        
                        let badgeHtml = '';
                        if (u.role === 'admin') {
                            badgeHtml = '<span class="status-badge stable">Admin</span>';
                        } else {
                            badgeHtml = '<span class="status-badge warning">Staff</span>';
                        }

                        let permissionsHtml = '';
                        if (u.role === 'admin') {
                            permissionsHtml = '<span style="color: var(--text-muted); font-style: italic;">Có toàn quyền hệ thống</span>';
                        } else {
                            const pNames = (u.permissions || []).map(p => friendlyTabNames[p] || p);
                            permissionsHtml = pNames.length > 0 
                                ? pNames.map(p => `<span class="status-badge" style="background: rgba(0,123,195,0.08); color: var(--color-ghn-blue); margin-right: 4px; border: 1px solid rgba(0,123,195,0.15);">${p}</span>`).join(' ')
                                : '<span style="color: var(--color-danger); font-size: 11px;">Không được xem tab nào</span>';
                        }

                        const isSelf = u.username === loggedInUsername;

                        tr.innerHTML = `
                            <td style="text-align: left; font-weight: 700;">
                                ${escapeHTML(u.username)} ${isSelf ? ' <span style="color: var(--text-muted); font-weight: normal; font-size: 11px;">(Bạn)</span>' : ''}
                            </td>
                            <td style="text-align: center;">${badgeHtml}</td>
                            <td style="text-align: left; line-height: 1.8;">${permissionsHtml}</td>
                            <td style="text-align: center; display: flex; gap: 8px; justify-content: center; align-items: center;">
                                <button class="btn btn-secondary btn-sm" onclick="editUser('${escapeHTML(u.username)}', '${escapeHTML(u.role)}', '${escapeHTML(JSON.stringify(u.permissions))}')" style="padding: 4px 8px; font-size: 11px; cursor: pointer; border-radius: 4px;">
                                    <i class="fa-solid fa-pen-to-square"></i> Sửa
                                </button>
                                <button class="btn btn-secondary btn-sm" onclick="deleteUser('${escapeHTML(u.username)}')" ${isSelf ? 'disabled style="opacity: 0.5; cursor: not-allowed; padding: 4px 8px; font-size: 11px;"' : 'style="padding: 4px 8px; font-size: 11px; cursor: pointer; border-radius: 4px;"'}>
                                    <i class="fa-solid fa-trash-can" style="color: var(--color-danger);"></i> Xóa
                                </button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) {
                console.error("Lỗi load danh sách user: ", err);
            }
        }

        function showAddUserModal() {
            document.getElementById('user-form-title').innerText = "Thêm Người Dùng Mới";
            document.getElementById('mgmt-username').value = '';
            document.getElementById('mgmt-username').disabled = false;
            document.getElementById('mgmt-password').value = '';
            document.getElementById('mgmt-password').required = true;
            document.getElementById('mgmt-password-help').style.display = 'none';
            document.getElementById('mgmt-user-is-edit').value = 'false';
            document.getElementById('mgmt-role').value = 'staff';
            
            document.querySelectorAll('#mgmt-permissions-grid input[type="checkbox"]').forEach(cb => {
                cb.checked = cb.value !== 'tab-sync';
                cb.disabled = false;
            });

            document.getElementById('user-form-container').style.display = 'block';
            document.getElementById('mgmt-username').focus();
        }

        function editUser(username, role, permissionsStr) {
            const permissions = JSON.parse(permissionsStr);
            
            document.getElementById('user-form-title').innerText = "Cập Nhật Người Dùng: " + username;
            document.getElementById('mgmt-username').value = username;
            document.getElementById('mgmt-username').disabled = true;
            document.getElementById('mgmt-password').value = '';
            document.getElementById('mgmt-password').required = false;
            document.getElementById('mgmt-password-help').style.display = 'block';
            document.getElementById('mgmt-user-is-edit').value = 'true';
            document.getElementById('mgmt-role').value = role;

            onMgmtRoleChange(role);

            if (role === 'admin') {
                document.querySelectorAll('#mgmt-permissions-grid input[type="checkbox"]').forEach(cb => {
                    cb.checked = true;
                    cb.disabled = true;
                });
            } else {
                document.querySelectorAll('#mgmt-permissions-grid input[type="checkbox"]').forEach(cb => {
                    cb.checked = permissions.includes(cb.value);
                    cb.disabled = false;
                });
            }

            document.getElementById('user-form-container').style.display = 'block';
            document.getElementById('mgmt-password').focus();
        }

        function onMgmtRoleChange(role) {
            if (role === 'admin') {
                document.querySelectorAll('#mgmt-permissions-grid input[type="checkbox"]').forEach(cb => {
                    cb.checked = true;
                    cb.disabled = true;
                });
            } else {
                document.querySelectorAll('#mgmt-permissions-grid input[type="checkbox"]').forEach(cb => {
                    cb.disabled = false;
                });
            }
        }

        function hideUserForm() {
            document.getElementById('user-form-container').style.display = 'none';
        }

        async function saveUser(event) {
            event.preventDefault();
            const username = document.getElementById('mgmt-username').value.trim();
            const password = document.getElementById('mgmt-password').value;
            const role = document.getElementById('mgmt-role').value;
            const isEdit = document.getElementById('mgmt-user-is-edit').value === 'true';

            if (!username) return;

            const permissions = [];
            document.querySelectorAll('#mgmt-permissions-grid input[type="checkbox"]').forEach(cb => {
                if (cb.checked) {
                    permissions.push(cb.value);
                }
            });

            const payload = { username, role, permissions };
            if (password) payload.password = password;

            showLoading("Đang lưu...");
            try {
                const res = await fetch(getApiUrl('/api/users'), getFetchOptions({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                }));

                if (res.ok) {
                    hideUserForm();
                    await loadUsersList();
                    if (username === loggedInUsername) {
                        await checkUserRole();
                    }
                    alert("Đã lưu thông tin người dùng thành công!");
                } else {
                    const err = await res.json();
                    alert("Lỗi lưu người dùng: " + err.error);
                }
            } catch (err) {
                alert("Lỗi kết nối máy chủ: " + err.message);
            } finally {
                hideLoading();
            }
        }

        async function deleteUser(username) {
            if (!confirm(`Bạn có chắc chắn muốn xóa người dùng ${username} không?`)) return;
            
            showLoading("Đang xóa...");
            try {
                const res = await fetch(getApiUrl('/api/users/' + encodeURIComponent(username)), getFetchOptions({
                    method: 'DELETE'
                }));

                if (res.ok) {
                    await loadUsersList();
                    alert(`Đã xóa người dùng ${username} thành công!`);
                } else {
                    const err = await res.json();
                    alert("Lỗi xóa người dùng: " + err.error);
                }
            } catch (err) {
                alert("Lỗi kết nối máy chủ: " + err.message);
            } finally {
                hideLoading();
            }
        }

        // Initialize and load data
        window.addEventListener('DOMContentLoaded', async () => {
            const isLoggedIn = await checkUserRole();
            if (isLoggedIn) {
                loadAllData();
                loadFilesStatus();
                loadHistoryDropdown();
                loadNtbSummaryData();
                loadGoogleSheetsConfig();
                loadNtbStructure();
            }
        });

        async function loadGoogleSheetsConfig() {
            try {
                const res = await fetch(getApiUrl('/api/config'), getFetchOptions());
                if (res.ok) {
                    const config = await res.json();
                    document.getElementById('sheet-ops-url').value = config.ops_url || '';
                    document.getElementById('sheet-opr-url').value = config.opr_url || '';
                    document.getElementById('sheet-aging-url').value = config.aging_url || '';
                    document.getElementById('sheet-treo-url').value = config.treo_url || '';
                    document.getElementById('sheet-bat-on-url').value = config.bat_on_url || '';
                    document.getElementById('sheet-off-spe-url').value = config.off_spe_url || '';
                    document.getElementById('sheet-tao-don-url').value = config.tao_don_url || '';
                    
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
        }

        async function saveGoogleSheetsConfig() {
            const config = {
                ops_url: document.getElementById('sheet-ops-url').value.trim(),
                opr_url: document.getElementById('sheet-opr-url').value.trim(),
                aging_url: document.getElementById('sheet-aging-url').value.trim(),
                treo_url: document.getElementById('sheet-treo-url').value.trim(),
                bat_on_url: document.getElementById('sheet-bat-on-url').value.trim(),
                off_spe_url: document.getElementById('sheet-off-spe-url').value.trim(),
                tao_don_url: document.getElementById('sheet-tao-don-url').value.trim(),
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
        }

        async function sendTelegramAiBriefing() {
            const botToken = document.getElementById('telegram-bot-token').value.trim();
            const chatId = document.getElementById('telegram-chat-id').value.trim();
            const geminiKey = document.getElementById('gemini-api-key').value.trim();

            if (!botToken) {
                alert("Vui lòng nhập Telegram Bot Token.");
                return;
            }
            if (!chatId) {
                alert("Vui lòng nhập Chat ID hoặc Group ID nhận tin.");
                return;
            }
            if (!geminiKey) {
                alert("Vui lòng nhập Gemini API Key.");
                return;
            }

            showLoading("AI đang phân tích dữ liệu vận hành và soạn bản tin gửi Telegram...");
            try {
                const res = await fetch(getApiUrl('/api/send-telegram-ai-briefing'), getFetchOptions({
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        telegram_bot_token: botToken,
                        telegram_chat_id: chatId,
                        gemini_api_key: geminiKey
                    })
                }));
                const result = await res.json();
                if (res.ok) {
                    alert(result.message || "Gửi bản tin phân tích AI thành công!");
                    loadGoogleSheetsConfig();
                } else {
                    alert("Lỗi: " + (result.error || "Gửi bản tin thất bại."));
                }
            } catch (err) {
                alert("Lỗi kết nối khi gửi bản tin AI: " + err.message);
            } finally {
                hideLoading();
            }
        }

        async function sendTelegramWarning() {
            const botToken = document.getElementById('telegram-bot-token').value.trim();
            const chatId = document.getElementById('telegram-chat-id').value.trim();
            const geminiKey = document.getElementById('gemini-api-key').value.trim();

            if (!botToken) {
                alert("Vui lòng nhập Telegram Bot Token.");
                return;
            }
            if (!chatId) {
                alert("Vui lòng nhập Chat ID hoặc Group ID nhận tin.");
                return;
            }

            showLoading("Đang kiểm tra và gửi cảnh báo sản lượng đột biến qua Telegram...");
            try {
                const res = await fetch(getApiUrl('/api/send-telegram-warning'), getFetchOptions({
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        telegram_bot_token: botToken,
                        telegram_chat_id: chatId,
                        gemini_api_key: geminiKey
                    })
                }));
                const result = await res.json();
                if (res.ok) {
                    alert(result.message || "Gửi cảnh báo sản lượng thành công!");
                    loadGoogleSheetsConfig();
                } else {
                    alert("Lỗi: " + (result.error || "Gửi cảnh báo thất bại."));
                }
            } catch (err) {
                alert("Lỗi kết nối khi gửi cảnh báo Telegram: " + err.message);
            } finally {
                hideLoading();
            }
        }

        function showLoading(text = "Đang tải dữ liệu...") {
            document.getElementById('loading-text').innerText = text;
            document.getElementById('loading-overlay').classList.add('active');
        }

        function hideLoading() {
            document.getElementById('loading-overlay').classList.remove('active');
        }

        async function loadAllData(baseline = "") {
            showLoading("Đang tải dữ liệu báo cáo...");
            try {
                // Fetch in parallel
                const opsPromise = fetch(getApiUrl('/api/operational'), getFetchOptions()).then(r => r.json());
                const oprPromise = fetch(getApiUrl('/api/opr'), getFetchOptions()).then(r => r.json());
                const backlogPromise = fetch(getApiUrl(`/api/backlog?baseline=${baseline}`), getFetchOptions()).then(r => r.json());
                const unstablePromise = fetch(getApiUrl('/api/unstable-po'), getFetchOptions()).then(r => r.json());
                const offSpePromise = fetch(getApiUrl('/api/off-spe'), getFetchOptions()).then(r => r.json());
                const volCreationPromise = fetch(getApiUrl('/api/volume-creation'), getFetchOptions()).then(r => r.json());

                const [opsData, oprData, blData, unstableData, offSpeData, volCreationData] = await Promise.all([
                    opsPromise,
                    oprPromise,
                    backlogPromise,
                    unstablePromise,
                    offSpePromise,
                    volCreationPromise
                ]);

                globalData.operational = opsData;
                globalData.opr = oprData;
                globalData.backlog = blData;
                globalData.unstablePo = unstableData;
                globalData.offSpe = offSpeData;
                globalData.volumeCreation = volCreationData;

                // Update timestamps
                const activePanel = document.querySelector('.content-panel.active');
                const activeTabId = activePanel ? activePanel.id : 'tab-dashboard';
                updateHeaderSubtitle(activeTabId);

                // Populate filters
                populateFilters();

                // Render Dashboard view
                renderOverviewDashboard();
                renderOperationalDashboard();
                renderOprDashboard();
                renderAgingDashboard();
                renderTreoDashboard();
                loadNtbSummaryData();
                renderUnstablePo(unstableData);
                renderOffSpe(offSpeData);
                renderVolumeCreation(volCreationData);

            } catch (err) {
                console.error(err);
                alert("Lỗi tải dữ liệu. Hãy đồng bộ lại dữ liệu!");
            } finally {
                hideLoading();
            }
        }

        async function loadFilesStatus() {
            try {
                const res = await fetch(getApiUrl('/api/files-status'), getFetchOptions());
                const data = await res.json();
                const container = document.getElementById('files-status-container');
                container.innerHTML = '';

                data.forEach(f => {
                    const card = document.createElement('div');
                    card.className = 'file-card';
                    card.style.flexDirection = 'column';
                    card.style.alignItems = 'stretch';
                    card.style.padding = '20px';
                    card.style.cursor = 'pointer';
                    
                    card.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
                            <div class="file-icon ${f.exists ? '' : 'missing'}">
                                <i class="fa-regular fa-file-excel"></i>
                            </div>
                            <div class="file-info">
                                <h4 style="font-weight: 700;">${f.name}</h4>
                                <p>${f.exists ? `Kích thước: ${f.size_mb} MB &bull; Cập nhật: ${f.mtime}` : '<span style="color: var(--color-danger)">Mất file / Chưa có dữ liệu</span>'}</p>
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; justify-content: space-between; align-items: center; border-top: 1px dashed var(--border-color); padding-top: 12px;">
                            <span style="font-size: 11px; color: var(--text-muted);">
                                <i class="fa-solid fa-arrow-down-long"></i> Hoặc kéo thả file vào đây
                            </span>
                            <div style="display: flex; gap: 8px;">
                                <a href="${getApiUrl('/api/download-template?filename=' + encodeURIComponent(f.name))}" 
                                   class="btn btn-secondary" 
                                   style="padding: 6px 12px; font-size: 11px; margin: 0; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;"
                                   download>
                                    <i class="fa-solid fa-download" style="color: var(--color-indigo);"></i> File mẫu
                                </a>
                                <label class="btn btn-secondary" style="padding: 6px 12px; font-size: 11px; margin: 0; cursor: pointer; display: inline-flex; align-items: center; gap: 4px;">
                                    <i class="fa-solid fa-cloud-arrow-up" style="color: var(--color-indigo);"></i> Chọn file
                                    <input type="file" style="display: none;" onchange="uploadFile(this.files[0], '${f.name}')" accept=".xlsx, .xls">
                                </label>
                            </div>
                        </div>
                    `;

                    // Setup HTML5 Drag and Drop Events for each card
                    card.addEventListener('dragover', (e) => {
                        e.preventDefault();
                        card.classList.add('drag-over');
                    });

                    card.addEventListener('dragleave', () => {
                        card.classList.remove('drag-over');
                    });

                    card.addEventListener('drop', (e) => {
                        e.preventDefault();
                        card.classList.remove('drag-over');
                        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                            uploadFile(e.dataTransfer.files[0], f.name);
                        }
                    });

                    container.appendChild(card);
                });
            } catch (err) {
                console.error(err);
            }
        }

        async function uploadFile(file, targetFilename) {
            if (!file) return;
            
            const ext = file.name.split('.').pop().toLowerCase();
            if (ext !== 'xlsx' && ext !== 'xls') {
                alert("Định dạng file không hợp lệ! Vui lòng chỉ tải lên file Excel (.xlsx hoặc .xls).");
                return;
            }

            const formData = new FormData();
            formData.append('file', file);
            formData.append('filename', targetFilename);

            showLoading(`Đang tải lên và phân tích file ${targetFilename}...`);
            try {
                const res = await fetch(getApiUrl('/api/upload'), getFetchOptions({
                    method: 'POST',
                    body: formData
                }));

                if (res.ok) {
                    const result = await res.json();
                    alert(result.message);
                    
                    // Reload all dashboard views
                    await loadHistoryDropdown();
                    await loadAllData();
                    await loadFilesStatus();
                } else {
                    const err = await res.json();
                    alert("Tải lên thất bại: " + err.error);
                }
            } catch (e) {
                alert("Lỗi kết nối khi tải lên file: " + e.message);
            } finally {
                hideLoading();
            }
        }

        async function loadHistoryDropdown() {
            try {
                const res = await fetch(getApiUrl('/api/history'), getFetchOptions());
                const data = await res.json();
                const select = document.getElementById('baseline-select');
                select.innerHTML = '';

                if (data.length === 0) {
                    select.innerHTML = '<option value="">Lần chạy trước đó</option>';
                    return;
                }

                data.forEach((ts, idx) => {
                    const option = document.createElement('option');
                    option.value = ts;
                    option.innerText = ts + (idx === 0 ? " (Mới nhất)" : "");
                    select.appendChild(option);
                });

                // Add default "Previous run" option at the end if we have history
                if (data.length >= 2) {
                    const defaultOption = document.createElement('option');
                    defaultOption.value = "";
                    defaultOption.innerText = "Chạy trước đó (Mặc định)";
                    select.appendChild(defaultOption);
                }
            } catch (err) {
                console.error(err);
            }
        }

        async function syncData() {
            showLoading("Đang khởi tạo đồng bộ...");
            try {
                const res = await fetch(getApiUrl('/api/sync'), getFetchOptions({ method: 'POST' }));
                if (!res.ok) {
                    const err = await res.json();
                    alert("Đồng bộ thất bại: " + err.error);
                    hideLoading();
                    return;
                }
                
                const pollInterval = setInterval(async () => {
                    try {
                        const statusRes = await fetch(getApiUrl('/api/sync/status'), getFetchOptions());
                        if (statusRes.ok) {
                            const statusData = await statusRes.json();
                            if (statusData.status === "processing") {
                                showLoading(statusData.progress || "Đang đồng bộ...");
                            } else if (statusData.status === "success") {
                                clearInterval(pollInterval);
                                await loadHistoryDropdown();
                                await loadAllData();
                                await loadFilesStatus();
                                hideLoading();
                                alert("Đồng bộ dữ liệu thành công!");
                            } else if (statusData.status === "error") {
                                clearInterval(pollInterval);
                                hideLoading();
                                alert("Đồng bộ thất bại:\n" + statusData.error);
                            }
                        } else {
                            clearInterval(pollInterval);
                            hideLoading();
                            alert("Mất kết nối với máy chủ khi kiểm tra trạng thái.");
                        }
                    } catch (err) {
                        clearInterval(pollInterval);
                        hideLoading();
                        alert("Lỗi kết nối khi kiểm tra trạng thái: " + err.message);
                    }
                }, 2000);
                
            } catch (e) {
                hideLoading();
                alert("Lỗi kết nối server: " + e.message);
            }
        }

        async function loadBacklogData(baseline) {
            showLoading("Đang tải dữ liệu so sánh...");
            try {
                const res = await fetch(getApiUrl(`/api/backlog?baseline=${baseline}`), getFetchOptions());
                const data = await res.json();
                globalData.backlog = data;

                if (data.baseline_timestamp) {
                    document.getElementById('last-sync-time').innerText = "Đang so sánh với mốc: " + data.baseline_timestamp;
                }

                renderOverviewDashboard();
                renderAgingDashboard();
                renderTreoDashboard();
            } catch (e) {
                alert("Lỗi so sánh: " + e.message);
            } finally {
                hideLoading();
            }
        }

        // Populating filters dynamically from data
        function populateFilters() {
            const amSet = new Set();
            const provinceSet = new Set();
            const poSet = new Set();

            // OPR AMs
            if (globalData.opr.am_performance) {
                globalData.opr.am_performance.forEach(r => r.AM && amSet.add(r.AM));
            }
            // Aging AMs & Post offices
            if (globalData.backlog.aging && globalData.backlog.aging.raw_records) {
                globalData.backlog.aging.raw_records.forEach(r => {
                    r.final_am && amSet.add(r.final_am);
                    r.final_province && provinceSet.add(r.final_province);
                    r.BC && poSet.add(r.BC);
                });
            }
            // Treo AMs & Post offices
            if (globalData.backlog.treo && globalData.backlog.treo.raw_records) {
                globalData.backlog.treo.raw_records.forEach(r => {
                    r.final_am && amSet.add(r.final_am);
                    r.final_province && provinceSet.add(r.final_province);
                    r.warehouse_name && poSet.add(r.warehouse_name);
                });
            }

            const amSelect = document.getElementById('filter-am');
            const currentAm = amSelect.value;
            amSelect.innerHTML = '<option value="">-- Tất cả AM --</option>';
            Array.from(amSet).sort().forEach(am => {
                const opt = document.createElement('option');
                opt.value = am;
                opt.innerText = am;
                amSelect.appendChild(opt);
            });
            amSelect.value = currentAm;

            const provSelect = document.getElementById('filter-province');
            const currentProv = provSelect.value;
            provSelect.innerHTML = '<option value="">-- Tất cả Tỉnh --</option>';
            Array.from(provinceSet).sort().forEach(p => {
                const opt = document.createElement('option');
                opt.value = p;
                opt.innerText = p;
                provSelect.appendChild(opt);
            });
            provSelect.value = currentProv;

            const poSelect = document.getElementById('filter-po');
            const currentPo = poSelect.value;
            poSelect.innerHTML = '<option value="">-- Tất cả Bưu cục --</option>';
            Array.from(poSet).sort().forEach(po => {
                const opt = document.createElement('option');
                opt.value = po;
                opt.innerText = po;
                poSelect.appendChild(opt);
            });
            poSelect.value = currentPo;
        }

        // Apply filters locally on detail grids
        function applyFilters() {
            const am = document.getElementById('filter-am').value;
            const prov = document.getElementById('filter-province').value;
            const po = document.getElementById('filter-po').value;
            const search = document.getElementById('search-input').value.toLowerCase();

            // Helper function to match record
            const matchRecord = (r, searchFields, amField, provField, poField) => {
                const matchAm = !am || r[amField] === am;
                const matchProv = !prov || r[provField] === prov;
                const matchPo = !po || r[poField] === po;

                let matchSearch = true;
                if (search) {
                    matchSearch = searchFields.some(f => r[f] && String(r[f]).toLowerCase().includes(search));
                }
                return matchAm && matchProv && matchPo && matchSearch;
            };

            // Filter OPR
            if (globalData.opr.oe_details) {
                filteredData.oe_details = globalData.opr.oe_details.filter(r =>
                    matchRecord(r, ['madh', 'sellername', 'kholay'], 'AM', 'tutinh', 'kholay')
                );
            }

            // Filter Aging
            if (globalData.backlog.aging.raw_records) {
                filteredData.aging_details = globalData.backlog.aging.raw_records.filter(r =>
                    matchRecord(r, ['Mã đơn', 'BC'], 'final_am', 'final_province', 'BC')
                );
            }

            // Filter Treo
            if (globalData.backlog.treo.raw_records) {
                filteredData.treo_details = globalData.backlog.treo.raw_records.filter(r =>
                    matchRecord(r, ['Mã đơn hàng', 'warehouse_name'], 'final_am', 'final_province', 'warehouse_name')
                );
            }

            // Reset page numbers
            paginationState.opr.current = 1;
            paginationState.aging.current = 1;
            paginationState.treo.current = 1;

            // Re-render tables
            renderOprDetailsTable();
            renderAgingDetailsTable();
            renderTreoDetailsTable();
            loadNtbSummaryData();
        }

        // ==========================================
        // RENDER: OVERVIEW DASHBOARD (TAB 1)
        // ==========================================
        let shiftsChart = null;
        let backlogPieChart = null;

        // Delta display helpers
        function getCompareDeltas(trendList, key) {
            if (!trendList || trendList.length === 0) {
                return { n1: null, wk: null };
            }
            
            // Sort by Time
            const sorted = [...trendList].sort((a, b) => {
                const dateA = new Date(a.Time.split(" - ")[0]);
                const dateB = new Date(b.Time.split(" - ")[0]);
                return dateA - dateB;
            });
            
            const latestEntry = sorted[sorted.length - 1];
            if (!latestEntry) return { n1: null, wk: null };
            
            const latestVal = latestEntry[key];
            const latestDateStr = latestEntry.Time.split(" - ")[0]; // YYYY-MM-DD
            
            // Find n-1 (1 day offset)
            const n1Entry = findTrendEntryByDateOffset(sorted, latestDateStr, 1);
            // Find cùng kỳ thứ (7 days offset)
            const wkEntry = findTrendEntryByDateOffset(sorted, latestDateStr, 7);
            
            const getDelta = (compareEntry) => {
                if (!compareEntry) return null;
                const compareVal = compareEntry[key];
                return latestVal - compareVal;
            };
            
            return {
                n1: getDelta(n1Entry),
                wk: getDelta(wkEntry)
            };
        }

        function findTrendEntryByDateOffset(trendList, latestDateStr, daysOffset) {
            const [y, m, d] = latestDateStr.split('-').map(Number);
            const targetDate = new Date(y, m - 1, d - daysOffset);
            const targetYear = targetDate.getFullYear();
            const targetMonth = String(targetDate.getMonth() + 1).padStart(2, '0');
            const targetDay = String(targetDate.getDate()).padStart(2, '0');
            const targetDateStr = `${targetYear}-${targetMonth}-${targetDay}`;
            return trendList.find(item => item.Time.startsWith(targetDateStr));
        }

        function getDeltaClass(val) {
            if (val === null || val === undefined) return 'text-muted';
            if (val > 0.005) return 'text-success';
            if (val < -0.005) return 'text-danger';
            return 'text-muted';
        }

        function formatDelta(val) {
            if (val === null || val === undefined) return '-';
            const absVal = Math.abs(val).toFixed(2);
            if (val > 0.005) return `▲ +${absVal}%`;
            if (val < -0.005) return `▼ -${absVal}%`;
            return `— 0.00%`;
        }

        function renderOverviewDashboard() {
            const ops = globalData.operational;
            const opr = globalData.opr;
            const bl = globalData.backlog;

            // Fill metrics
            document.getElementById('kpi-gtc').innerText = ops.overall_gtc ? ops.overall_gtc + " %" : "- %";
            document.getElementById('kpi-ltc').innerText = ops.overall_ltc ? ops.overall_ltc + " %" : "- %";
            document.getElementById('kpi-opr').innerText = opr.overall_opr ? opr.overall_opr + " %" : "- %";

            const unstable = globalData.unstablePo || {};
            const unstableCountEl = document.getElementById('kpi-unstable-po-count');
            if (unstableCountEl) {
                if (unstable.error) {
                    unstableCountEl.innerText = "Lỗi";
                } else {
                    unstableCountEl.innerText = unstable.total_warning !== undefined ? unstable.total_warning : "-";
                }
            }
            const unstableUpdateEl = document.getElementById('kpi-unstable-po-update');
            if (unstableUpdateEl) {
                if (unstable.error) {
                    unstableUpdateEl.innerText = "File lỗi/chưa có";
                } else {
                    unstableUpdateEl.innerText = unstable.update_time ? `Cập nhật: ${unstable.update_time}` : "Cập nhật: Chưa rõ";
                }
            }

            // Fill comparisons dynamically
            const gtcDeltas = getCompareDeltas(ops.trend_gtc, '% GTC');
            const gtcCompEl = document.getElementById('kpi-gtc-comparison');
            if (gtcCompEl) {
                gtcCompEl.innerHTML = `
                    <div class="comp-row">
                        <span class="comp-label">So với n-1:</span>
                        <span class="comp-val ${getDeltaClass(gtcDeltas.n1)}">${formatDelta(gtcDeltas.n1)}</span>
                    </div>
                    <div class="comp-row">
                        <span class="comp-label">Cùng kỳ Thứ:</span>
                        <span class="comp-val ${getDeltaClass(gtcDeltas.wk)}">${formatDelta(gtcDeltas.wk)}</span>
                    </div>
                `;
            }

            const ltcDeltas = getCompareDeltas(ops.trend_ltc, '% LTC');
            const ltcCompEl = document.getElementById('kpi-ltc-comparison');
            if (ltcCompEl) {
                ltcCompEl.innerHTML = `
                    <div class="comp-row">
                        <span class="comp-label">So với n-1:</span>
                        <span class="comp-val ${getDeltaClass(ltcDeltas.n1)}">${formatDelta(ltcDeltas.n1)}</span>
                    </div>
                    <div class="comp-row">
                        <span class="comp-label">Cùng kỳ Thứ:</span>
                        <span class="comp-val ${getDeltaClass(ltcDeltas.wk)}">${formatDelta(ltcDeltas.wk)}</span>
                    </div>
                `;
            }

            const oprCompEl = document.getElementById('kpi-opr-comparison');
            if (oprCompEl) {
                const deltaN1 = opr.delta_n1;
                const deltaWk = opr.delta_wk;
                oprCompEl.innerHTML = `
                    <div class="comp-row">
                        <span class="comp-label">So với n-1:</span>
                        <span class="comp-val ${getDeltaClass(deltaN1)}">${formatDelta(deltaN1)}</span>
                    </div>
                    <div class="comp-row">
                        <span class="comp-label">Cùng kỳ Thứ:</span>
                        <span class="comp-val ${getDeltaClass(deltaWk)}">${formatDelta(deltaWk)}</span>
                    </div>
                `;
            }

            const totalBacklog = (bl.aging ? bl.aging.total_backlog : 0) + (bl.treo ? bl.treo.total_backlog : 0);
            document.getElementById('kpi-backlog').innerText = totalBacklog.toLocaleString();

            const summaryAgingEl = document.getElementById('summary-backlog-aging-val');
            if (summaryAgingEl) {
                summaryAgingEl.innerText = (bl.aging ? bl.aging.total_backlog : 0).toLocaleString();
            }
            const summaryTreoEl = document.getElementById('summary-backlog-treo-val');
            if (summaryTreoEl) {
                summaryTreoEl.innerText = (bl.treo ? bl.treo.total_backlog : 0).toLocaleString();
            }

            // Difference +/- trend info
            const diffAging = bl.aging ? (bl.aging.diff_total || 0) : 0;
            const diffTreo = bl.treo ? (bl.treo.diff_total || 0) : 0;
            const diffTotal = diffAging + diffTreo;

            const blCompEl = document.getElementById('kpi-backlog-comparison');
            if (blCompEl) {
                let diffText = "";
                let diffClass = "";
                if (diffTotal > 0) {
                    diffText = `▲ +${diffTotal.toLocaleString()} đơn`;
                    diffClass = "text-danger"; // for backlog, increase is bad
                } else if (diffTotal < 0) {
                    diffText = `▼ ${diffTotal.toLocaleString()} đơn`;
                    diffClass = "text-success"; // decrease is good
                } else {
                    diffText = `— 0 đơn`;
                    diffClass = "text-muted";
                }
                
                blCompEl.innerHTML = `
                    <div class="comp-row">
                        <span class="comp-label">So với lần chạy trước:</span>
                        <span class="comp-val ${diffClass}">${diffText}</span>
                    </div>
                    <div class="comp-row">
                        <span class="comp-label">Cùng kỳ Thứ:</span>
                        <span class="comp-val text-muted">-</span>
                    </div>
                `;
            }

            // Shifts Distribution Chart (Ca 1, Ca 2, Tồn)
            const shiftsOptions = {
                chart: { type: 'bar', height: 250, toolbar: { show: false }, background: 'transparent' },
                series: [{ name: 'Sản lượng', data: [ops.ca1_vol || 0, ops.ca2_vol || 0, ops.ton_vol || 0] }],
                xaxis: { categories: ['Ca 1', 'Ca 2', 'Hàng tồn'], labels: { style: { colors: '#64748b' } } },
                yaxis: { labels: { style: { colors: '#64748b' } } },
                colors: ['#ff5f00', '#007bc3', '#94a3b8'],
                plotOptions: { bar: { borderRadius: 4, columnWidth: '50%', distributed: true } },
                theme: { mode: 'light' },
                legend: { show: false }
            };

            if (shiftsChart) shiftsChart.destroy();
            shiftsChart = new ApexCharts(document.querySelector("#chart-shifts"), shiftsOptions);
            shiftsChart.render();

            // Backlog distribution chart (Aging > 5d, Treo Giao, Treo Trả)
            const blAging = bl.aging ? bl.aging.total_backlog : 0;
            const blTreoGiao = bl.treo ? bl.treo.total_giao : 0;
            const blTreoTra = bl.treo ? bl.treo.total_tra : 0;

            const backlogPieOptions = {
                chart: { type: 'donut', height: 250, background: 'transparent' },
                series: [blAging, blTreoGiao, blTreoTra],
                labels: ['Aging > 5 ngày', 'Treo LC Giao', 'Treo LC Trả'],
                colors: ['#ff5f00', '#ef4444', '#007bc3'],
                theme: { mode: 'light' },
                legend: { position: 'bottom', labels: { colors: '#64748b' } },
                dataLabels: { enabled: true }
            };

            if (backlogPieChart) backlogPieChart.destroy();
            backlogPieChart = new ApexCharts(document.querySelector("#chart-backlog-pie"), backlogPieOptions);
            backlogPieChart.render();
        }

        // ==========================================
        // RENDER: OPERATIONAL DASHBOARD (TAB 2)
        // ==========================================
        let opsTrendChart = null;

        function renderOperationalDashboard() {
            const ops = globalData.operational;

            // Render Trend Chart
            const dates = ops.trend_gtc ? ops.trend_gtc.map(r => r.Time.split(" - ")[0]) : [];
            const gtcVals = ops.trend_gtc ? ops.trend_gtc.map(r => roundNum(r['% GTC'])) : [];
            const ltcVals = ops.trend_ltc ? ops.trend_ltc.map(r => roundNum(r['% LTC'])) : [];
            const vols = ops.trend_gtc ? ops.trend_gtc.map(r => r.Volume) : [];

            const trendOptions = {
                chart: { type: 'line', height: 300, toolbar: { show: false }, background: 'transparent' },
                series: [
                    { name: '% GTC', type: 'line', data: gtcVals },
                    { name: '% LTC', type: 'line', data: ltcVals },
                    { name: 'Sản lượng đơn', type: 'column', data: vols }
                ],
                xaxis: { categories: dates, labels: { style: { colors: '#64748b' } } },
                yaxis: [
                    { title: { text: 'Tỷ lệ %', style: { color: '#ff5f00' } }, labels: { style: { colors: '#64748b' } } },
                    { title: { text: 'Tỷ lệ %', style: { color: '#007bc3' } }, labels: { show: false } },
                    { opponent: true, title: { text: 'Sản lượng', style: { color: '#007bc3' } }, labels: { style: { colors: '#64748b' } }, opposite: true }
                ],
                colors: ['#ff5f00', '#007bc3', 'rgba(0, 123, 195, 0.15)'],
                stroke: { width: [3, 3, 0], curve: 'smooth' },
                theme: { mode: 'light' },
                legend: { position: 'top', labels: { colors: '#64748b' } }
            };

            if (opsTrendChart) opsTrendChart.destroy();
            opsTrendChart = new ApexCharts(document.querySelector("#chart-ops-trend"), trendOptions);
            opsTrendChart.render();

            // Populate Tables helper
            const populateTable = (tableId, list, keys, isPercent = false, ltcFlag = false) => {
                const tbody = document.querySelector(`#${tableId} tbody`);
                tbody.innerHTML = '';
                if (!list || list.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center">Không có dữ liệu</td></tr>';
                    return;
                }
                list.forEach(r => {
                    const tr = document.createElement('tr');
                    const val = roundNum(r[keys[1]]);
                    const valClass = isPercent ? (val >= 60 || (ltcFlag && val >= 80) ? 'badge-success' : 'badge-danger') : '';
                    const valText = isPercent ? `${val}%` : val;

                    tr.innerHTML = `
                        <td>${escapeHTML(r[keys[0]])}</td>
                        <td>${r.Volume.toLocaleString()}</td>
                        <td><span class="badge ${valClass}">${valText}</span></td>
                        <td>${roundNum(r.Leadtime)}h</td>
                    `;
                    tbody.appendChild(tr);
                });
            };

            populateTable('table-best-gtc', ops.top_10_gtc, ['Chi tiết', '% GTC'], true);
            populateTable('table-worst-gtc', ops.worst_10_gtc, ['Chi tiết', '% GTC'], true);
            populateTable('table-best-ltc', ops.top_10_ltc, ['Chi tiết', '% LTC'], true, true);
            populateTable('table-worst-ltc', ops.worst_10_ltc, ['Chi tiết', '% LTC'], true, true);
        }

        // ==========================================
        // RENDER: OPR TTS DASHBOARD (TAB 3)
        // ==========================================
        let oprSlotsChart = null;
        let oprAmChart = null;

        function renderOprDashboard() {
            const opr = globalData.opr;

            document.getElementById('opr-total-vol').innerText = (opr.total_volume || 0).toLocaleString();
            document.getElementById('opr-total-ot').innerText = (opr.total_ontime || 0).toLocaleString();
            document.getElementById('opr-total-late').innerText = (opr.total_late || 0).toLocaleString();

            // Render OPR Time slots bar chart
            const slots = opr.time_slots ? opr.time_slots.map(r => r['Khung giờ tạo'] || r['khung_gio_tao_don']) : [];
            const slotOpr = opr.time_slots ? opr.time_slots.map(r => roundNum(r['% OPR'])) : [];

            const slotsOptions = {
                chart: { type: 'bar', height: 250, toolbar: { show: false }, background: 'transparent' },
                series: [{ name: '% OPR', data: slotOpr }],
                xaxis: { categories: slots, labels: { style: { colors: '#64748b' } } },
                yaxis: { max: 100, labels: { style: { colors: '#64748b' } } },
                colors: ['#007bc3'],
                plotOptions: { bar: { borderRadius: 4, columnWidth: '40%' } },
                theme: { mode: 'light' },
                annotations: {
                    yaxis: [{ y: 80, borderColor: '#ef4444', label: { text: 'KPI 80%', style: { color: '#ffffff', background: '#ef4444' } } }]
                }
            };

            if (oprSlotsChart) oprSlotsChart.destroy();
            oprSlotsChart = new ApexCharts(document.querySelector("#chart-opr-slots"), slotsOptions);
            oprSlotsChart.render();

            // Render OPR by AM rankings
            const ams = opr.am_performance ? opr.am_performance.map(r => r.AM) : [];
            const amOpr = opr.am_performance ? opr.am_performance.map(r => roundNum(r['% OPR'])) : [];

            const amOptions = {
                chart: { type: 'bar', height: 250, toolbar: { show: false }, background: 'transparent' },
                series: [{ name: '% OPR', data: amOpr }],
                xaxis: { categories: ams, labels: { style: { colors: '#64748b' } } },
                yaxis: { max: 100, labels: { style: { colors: '#64748b' } } },
                colors: ['#ff5f00'],
                plotOptions: { bar: { borderRadius: 4, horizontal: true, barHeight: '60%' } },
                theme: { mode: 'light' },
                annotations: {
                    xaxis: [{ x: 80, borderColor: '#ef4444', label: { text: 'KPI 80%', style: { color: '#ffffff', background: '#ef4444' } } }]
                }
            };

            if (oprAmChart) oprAmChart.destroy();
            oprAmChart = new ApexCharts(document.querySelector("#chart-opr-am"), amOptions);
            oprAmChart.render();

            // Populate Error reasons table
            const tbodyErrors = document.querySelector('#table-opr-errors tbody');
            tbodyErrors.innerHTML = '';
            if (opr.error_reasons) {
                opr.error_reasons.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${r.ly_do_tre_12h}</td>
                        <td>${r.late_orders.toLocaleString()}</td>
                        <td><span class="badge badge-danger">${roundNum(r.weight)}%</span></td>
                    `;
                    tbodyErrors.appendChild(tr);
                });
            }

            // Set details search data
            filteredData.oe_details = opr.oe_details || [];
            applyFilters(); // applying local filters will render the page
        }

        function renderOprDetailsTable() {
            const tbody = document.querySelector('#table-opr-details tbody');
            tbody.innerHTML = '';

            const page = paginationState.opr.current;
            const perPage = paginationState.opr.perPage;
            const start = (page - 1) * perPage;
            const end = start + perPage;
            const list = filteredData.oe_details.slice(start, end);

            if (list.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align:center">Không tìm thấy đơn lỗi nào khớp với điều kiện</td></tr>';
                document.getElementById('opr-page-num').innerText = '1 / 1';
                return;
            }

            list.forEach(r => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${escapeHTML(r.madh)}</strong></td>
                    <td>${escapeHTML(r.tutinh || '')}</td>
                    <td>${escapeHTML(r.kholay || '')}</td>
                    <td>${escapeHTML(r.sellername || '')}</td>
                    <td>${escapeHTML(r.AM || '')}</td>
                    <td><span class="badge badge-warning">${r.ly_do_tre_12h || ''}</span></td>
                    <td>${r.khung_gio_tao_don || ''}</td>
                `;
                tbody.appendChild(tr);
            });

            const totalPages = Math.ceil(filteredData.oe_details.length / perPage);
            document.getElementById('opr-page-num').innerText = `${page} / ${totalPages}`;
        }

        // ==========================================
        // RENDER: BACKLOG AGING > 5 DAYS (TAB 4)
        // ==========================================
        function renderAgingDashboard() {
            const bl = globalData.backlog.aging;

            document.getElementById('aging-total-vol').innerText = (bl.total_backlog || 0).toLocaleString();

            const trendEl = document.getElementById('aging-trend-diff');
            const diff = bl.diff_total || 0;
            if (diff > 0) {
                trendEl.innerHTML = `<span class="trend-up"><i class="fa-solid fa-arrow-trend-up"></i> +${diff} đơn</span> so với mốc so sánh`;
            } else if (diff < 0) {
                trendEl.innerHTML = `<span class="trend-down"><i class="fa-solid fa-arrow-trend-down"></i> ${diff} đơn</span> so với mốc so sánh`;
            } else {
                trendEl.innerHTML = `<span class="trend-neutral">Không đổi</span> so với mốc so sánh`;
            }

            // Populate AM aging summary
            const tbodyAm = document.querySelector('#table-aging-am tbody');
            tbodyAm.innerHTML = '';
            if (bl.am_summary) {
                bl.am_summary.forEach(r => {
                    const tr = document.createElement('tr');
                    const diffText = r.diff > 0 ? `+${r.diff}` : r.diff < 0 ? `${r.diff}` : 'Không đổi';
                    const diffClass = r.diff > 0 ? 'trend-up' : r.diff < 0 ? 'trend-down' : 'trend-neutral';

                    tr.innerHTML = `
                        <td><strong>${escapeHTML(r.final_am)}</strong></td>
                        <td>${r["5 - 8 ngày"]}</td>
                        <td>${r["8 - 15 ngày"]}</td>
                        <td>${r["Trên 15 ngày"]}</td>
                        <td><strong>${r.Total}</strong></td>
                        <td><span class="${diffClass}">${diffText}</span></td>
                    `;
                    tbodyAm.appendChild(tr);
                });
            }

            // Populate PO aging summary
            const tbodyPo = document.querySelector('#table-aging-po tbody');
            tbodyPo.innerHTML = '';
            if (bl.po_summary) {
                bl.po_summary.forEach(r => {
                    const tr = document.createElement('tr');
                    const diffText = r.diff > 0 ? `+${r.diff}` : r.diff < 0 ? `${r.diff}` : 'Không đổi';
                    const diffClass = r.diff > 0 ? 'trend-up' : r.diff < 0 ? 'trend-down' : 'trend-neutral';

                    tr.innerHTML = `
                        <td>${escapeHTML(r.BC)}</td>
                        <td>${escapeHTML(r.final_province)}</td>
                        <td>${escapeHTML(r.final_am)}</td>
                        <td>${r["5 - 8 ngày"]}</td>
                        <td>${r["8 - 15 ngày"]}</td>
                        <td>${r["Trên 15 ngày"]}</td>
                        <td><strong>${r.Total}</strong></td>
                        <td><span class="${diffClass}">${diffText}</span></td>
                    `;
                    tbodyPo.appendChild(tr);
                });
            }

            filteredData.aging_details = bl.raw_records || [];
            applyFilters();
        }

        function renderAgingDetailsTable() {
            const tbody = document.querySelector('#table-aging-details tbody');
            tbody.innerHTML = '';

            const page = paginationState.aging.current;
            const perPage = paginationState.aging.perPage;
            const start = (page - 1) * perPage;
            const end = start + perPage;
            const list = filteredData.aging_details.slice(start, end);

            if (list.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" style="text-align:center">Không tìm thấy đơn tồn đọng nào khớp điều kiện</td></tr>';
                document.getElementById('aging-page-num').innerText = '1 / 1';
                return;
            }

            list.forEach(r => {
                const tr = document.createElement('tr');
                let bracketClass = 'badge-secondary';
                if (r.aging_bracket === '8 - 15 ngày') bracketClass = 'badge-warning';
                else if (r.aging_bracket === 'Trên 15 ngày') bracketClass = 'badge-danger';

                tr.innerHTML = `
                    <td><strong>${escapeHTML(r['Mã đơn'])}</strong></td>
                    <td>${escapeHTML(r.final_province || '')}</td>
                    <td>${escapeHTML(r.BC || '')}</td>
                    <td>${escapeHTML(r['Tệp khách'] || '')}</td>
                    <td>${escapeHTML(r.final_am || '')}</td>
                    <td><span class="badge ${bracketClass}">${roundNum(r['Số ngày đã nhập BC'])} ngày</span></td>
                    <td>${r['Số lần giao']}</td>
                    <td><span class="badge badge-secondary">${escapeHTML(r['Trạng thái'] || '')}</span></td>
                `;
                tbody.appendChild(tr);
            });

            const totalPages = Math.ceil(filteredData.aging_details.length / perPage);
            document.getElementById('aging-page-num').innerText = `${page} / ${totalPages}`;
        }

        // ==========================================
        // RENDER: PENDING TRANSIT DASHBOARD (TAB 5)
        // ==========================================
        function renderTreoDashboard() {
            const bl = globalData.backlog.treo;

            document.getElementById('treo-total-vol').innerText = (bl.total_backlog || 0).toLocaleString();
            document.getElementById('treo-total-giao').innerText = (bl.total_giao || 0).toLocaleString();
            document.getElementById('treo-total-tra').innerText = (bl.total_tra || 0).toLocaleString();

            // Total Trend
            const setDiffTrend = (elementId, diff) => {
                const el = document.getElementById(elementId);
                if (diff > 0) {
                    el.innerHTML = `<span class="trend-up"><i class="fa-solid fa-arrow-trend-up"></i> +${diff} đơn</span>`;
                } else if (diff < 0) {
                    el.innerHTML = `<span class="trend-down"><i class="fa-solid fa-arrow-trend-down"></i> ${diff} đơn</span>`;
                } else {
                    el.innerHTML = `<span class="trend-neutral">Không đổi</span>`;
                }
            };

            setDiffTrend('treo-trend-diff', bl.diff_total || 0);
            setDiffTrend('treo-trend-giao', bl.diff_giao || 0);
            setDiffTrend('treo-trend-tra', bl.diff_tra || 0);

            // Treo Giao AM summary table
            const tbodyGiao = document.querySelector('#table-treo-giao-am tbody');
            tbodyGiao.innerHTML = '';
            if (bl.giao_am_summary) {
                bl.giao_am_summary.forEach(r => {
                    const tr = document.createElement('tr');
                    const diffText = r.diff > 0 ? `+${r.diff}` : r.diff < 0 ? `${r.diff}` : 'Không đổi';
                    const diffClass = r.diff > 0 ? 'trend-up' : r.diff < 0 ? 'trend-down' : 'trend-neutral';

                    tr.innerHTML = `
                        <td><strong>${escapeHTML(r.final_am)}</strong></td>
                        <td>${r["36 - 72h"]}</td>
                        <td>${r["72 - 120h"]}</td>
                        <td>${r["120 - 192h"]}</td>
                        <td>${r["192h+"]}</td>
                        <td><strong>${r.Total}</strong></td>
                        <td><span class="${diffClass}">${diffText}</span></td>
                    `;
                    tbodyGiao.appendChild(tr);
                });
            }

            // Treo Tra AM summary table
            const tbodyTra = document.querySelector('#table-treo-tra-am tbody');
            tbodyTra.innerHTML = '';
            if (bl.tra_am_summary) {
                bl.tra_am_summary.forEach(r => {
                    const tr = document.createElement('tr');
                    const diffText = r.diff > 0 ? `+${r.diff}` : r.diff < 0 ? `${r.diff}` : 'Không đổi';
                    const diffClass = r.diff > 0 ? 'trend-up' : r.diff < 0 ? 'trend-down' : 'trend-neutral';

                    tr.innerHTML = `
                        <td><strong>${escapeHTML(r.final_am)}</strong></td>
                        <td>${r["36 - 72h"]}</td>
                        <td>${r["72 - 120h"]}</td>
                        <td>${r["120 - 192h"]}</td>
                        <td>${r["192h+"]}</td>
                        <td><strong>${r.Total}</strong></td>
                        <td><span class="${diffClass}">${diffText}</span></td>
                    `;
                    tbodyTra.appendChild(tr);
                });
            }

            filteredData.treo_details = bl.raw_records || [];
            applyFilters();
        }

        function renderTreoDetailsTable() {
            const tbody = document.querySelector('#table-treo-details tbody');
            tbody.innerHTML = '';

            const page = paginationState.treo.current;
            const perPage = paginationState.treo.perPage;
            const start = (page - 1) * perPage;
            const end = start + perPage;
            const list = filteredData.treo_details.slice(start, end);

            if (list.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" style="text-align:center">Không tìm thấy đơn treo luân chuyển nào khớp điều kiện</td></tr>';
                document.getElementById('treo-page-num').innerText = '1 / 1';
                return;
            }

            list.forEach(r => {
                const tr = document.createElement('tr');
                let bracketClass = 'badge-secondary';
                if (r.treo_bracket === '72 - 120h') bracketClass = 'badge-warning';
                else if (r.treo_bracket === '120 - 192h' || r.treo_bracket === '192h+') bracketClass = 'badge-danger';

                const typeClass = r['Loại đơn'] === 'Luân chuyển giao' ? 'badge-success' : 'badge-warning';

                tr.innerHTML = `
                    <td><strong>${escapeHTML(r['Mã đơn hàng'])}</strong></td>
                    <td>${escapeHTML(r.final_province || '')}</td>
                    <td>${escapeHTML(r.warehouse_name || '')}</td>
                    <td><span class="badge ${typeClass}">${escapeHTML(r['Loại đơn'] || '')}</span></td>
                    <td>${escapeHTML(r.final_am || '')}</td>
                    <td>${r['Thời gian tồn đọng'] || ''}h</td>
                    <td><span class="badge ${bracketClass}">${r.treo_bracket || ''}</span></td>
                    <td><span class="badge badge-secondary">${escapeHTML(r['Trạng thái'] || '')}</span></td>
                `;
                tbody.appendChild(tr);
            });

            const totalPages = Math.ceil(filteredData.treo_details.length / perPage);
            document.getElementById('treo-page-num').innerText = `${page} / ${totalPages}`;
        }

        // ==========================================
        // RENDER: UNSTABLE POST OFFICES (TAB 6)
        // ==========================================
        function filterUnstablePoTable() {
            const data = globalData.unstablePo;
            if (!data || !data.records) return;

            const searchQuery = document.getElementById('search-unstable-po').value.toLowerCase().trim();
            const unstableOnly = document.getElementById('toggle-unstable-only').checked;
            
            const tbody = document.getElementById('table-unstable-po-body');
            if (!tbody) return;

            let filtered = data.records;

            // Apply filters
            if (unstableOnly) {
                // Warning states: Bất ổn or Chuẩn bị nhảy nhóm
                filtered = filtered.filter(r => r.status === 'Bất ổn' || r.status === 'Chuẩn bị nhảy nhóm');
            }
            if (searchQuery) {
                filtered = filtered.filter(r => 
                    (r.name && r.name.toLowerCase().includes(searchQuery)) ||
                    (r.am && r.am.toLowerCase().includes(searchQuery)) ||
                    (r.province && r.province.toLowerCase().includes(searchQuery)) ||
                    (r.reason && r.reason.toLowerCase().includes(searchQuery)) ||
                    (r.status && r.status.toLowerCase().includes(searchQuery))
                );
            }

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 24px;"><i class="fa-solid fa-folder-open"></i> Không tìm thấy bưu cục nào phù hợp.</td></tr>`;
                return;
            }

            let html = '';
            filtered.forEach(row => {
                let statusClass = 'badge-secondary';
                let rowBg = '';
                if (row.status === 'Bất ổn') {
                    statusClass = 'badge-danger';
                    rowBg = 'background-color: rgba(239, 68, 68, 0.05);';
                } else if (row.status === 'Chuẩn bị nhảy nhóm') {
                    statusClass = 'badge-warning';
                    rowBg = 'background-color: rgba(245, 158, 11, 0.03);';
                } else {
                    statusClass = 'badge-success';
                }

                let daysBadge = '';
                if (row.status === 'Bình thường') {
                    daysBadge = `<span style="color: #10b981; font-weight: 700; font-size: 12.5px; display: inline-flex; align-items: center; gap: 4px;"><i class="fa-solid fa-circle-check"></i> Đã thoát</span>`;
                } else if (row.status === 'Chuẩn bị nhảy nhóm') {
                    daysBadge = `<span style="color: var(--text-muted); font-size: 12.5px;">-</span>`;
                } else if (row.days_unstable === 1 || row.days_unstable === 2) {
                    daysBadge = `<span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: 700; font-size: 12.5px; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 0 8px rgba(16, 185, 129, 0.1);"><i class="fa-solid fa-circle-arrow-down" style="color: #10b981;"></i> ${row.days_unstable} ngày (Sắp thoát)</span>`;
                } else if (row.days_unstable === 3 || row.days_unstable === 4) {
                    daysBadge = `<span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); font-weight: 700; font-size: 12.5px; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px;"><i class="fa-solid fa-hourglass-half"></i> ${row.days_unstable} ngày</span>`;
                } else if (row.days_unstable >= 5) {
                    daysBadge = `<span class="badge" style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); font-weight: 700; font-size: 12.5px; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 0 8px rgba(239, 68, 68, 0.1);"><i class="fa-solid fa-circle-exclamation"></i> ${row.days_unstable} ngày</span>`;
                } else {
                    daysBadge = `<span style="color: var(--text-muted); font-size: 12.5px;">-</span>`;
                }

                const tonLmHtml = row.ton_lm > 0 ? `<span style="${row.ton_lm_5n > 0 || row.ton_lm > 1000 ? 'color: #ef4444; font-weight: bold;' : ''}">${row.ton_lm.toLocaleString()}</span>` : '0';
                const tonKtcHtml = row.ton_ktc > 0 ? `<span style="${row.pct_ktc_cung_tinh > 10 ? 'color: #ef4444; font-weight: bold;' : ''}">${row.ton_ktc.toLocaleString()}</span>` : '0';
                const agingHtml = row.ton_lm_5n > 0 ? `<span style="color: #ef4444; font-weight: bold;">${row.ton_lm_5n.toLocaleString()} <small>(${row.pct_lm_5n}%)</small></span>` : '0';

                html += `
                    <tr style="${rowBg}">
                        <td style="font-weight: 600; color: var(--text-primary); text-align: left; vertical-align: middle;">${escapeHTML(row.name)}</td>
                        <td style="text-align: left; vertical-align: middle;">${escapeHTML(row.am)}</td>
                        <td style="text-align: left; vertical-align: middle;">${escapeHTML(row.province)}</td>
                        <td style="text-align: center; vertical-align: middle;">${tonLmHtml}</td>
                        <td style="text-align: center; vertical-align: middle;">${tonKtcHtml}</td>
                        <td style="text-align: center; vertical-align: middle;">${agingHtml}</td>
                        <td style="text-align: center; vertical-align: middle;">${daysBadge}</td>
                        <td style="text-align: left; vertical-align: middle;">
                            <span class="badge ${statusClass}">${escapeHTML(row.status)}</span>
                            ${row.reason ? `<div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px; line-height: 1.2;">${escapeHTML(row.reason)}</div>` : ''}
                        </td>
                    </tr>
                `;
            });
            tbody.innerHTML = html;
        }

        function renderUnstablePo(data) {
            const dateEl = document.getElementById('unstable-po-report-date');
            if (dateEl) {
                dateEl.innerText = data.update_time ? `Thời gian cập nhật: ${data.update_time}` : 'Cập nhật: Chưa rõ';
            }
            
            const kpiCountEl = document.getElementById('kpi-unstable-po-count');
            if (kpiCountEl) {
                kpiCountEl.innerText = data.total_warning !== undefined ? data.total_warning : '-';
            }
            
            const kpiUpdateEl = document.getElementById('kpi-unstable-po-update');
            if (kpiUpdateEl) {
                kpiUpdateEl.innerText = data.update_time ? `Cập nhật: ${data.update_time}` : 'Cập nhật: Chưa rõ';
            }

            // Render Leaderboard
            const leaderboardEl = document.getElementById('unstable-am-leaderboard');
            if (leaderboardEl) {
                leaderboardEl.innerHTML = '';
                if (data.am_deepdive && data.am_deepdive.length > 0) {
                    data.am_deepdive.forEach(item => {
                        const card = document.createElement('div');
                        card.className = 'kpi-card danger';
                        card.style.display = 'flex';
                        card.style.flexDirection = 'column';
                        card.style.justifyContent = 'space-between';
                        card.style.padding = '16px';
                        card.style.cursor = 'default';
                        card.style.transition = 'all 0.3s ease';
                        card.style.boxShadow = 'var(--shadow-sm)';
                        card.innerHTML = `
                            <div>
                                <div class="kpi-header" style="margin-bottom: 8px; font-weight: 700; display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 14.5px; color: var(--text-primary); font-family: 'Outfit', sans-serif;"><i class="fa-solid fa-user-shield" style="margin-right: 6px; color: #ef4444;"></i> ${escapeHTML(item.am)}</span>
                                    <span class="badge badge-danger" style="font-size: 11px; padding: 4px 8px; border-radius: 12px; font-weight: 700;">${item.count} BC cảnh báo</span>
                                </div>
                                <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px; line-height: 1.45; max-height: 80px; overflow-y: auto;">
                                    ${item.pos.map(po => `<span style="display:inline-block; background:rgba(239,68,68,0.08); color:#ef4444; border: 1px solid rgba(239,68,68,0.15); padding:2px 6px; border-radius:4px; margin:2px; font-size:11px; font-weight:600;">${escapeHTML(po)}</span>`).join('')}
                                </div>
                            </div>
                        `;
                        leaderboardEl.appendChild(card);
                    });
                } else {
                    leaderboardEl.innerHTML = `
                        <div class="kpi-card success" style="grid-column: 1 / -1; padding: 20px; text-align: center; border-left: 4px solid #10b981;">
                            <div style="font-size: 16px; font-weight: 700; color: #10b981; margin-bottom: 4px;">
                                <i class="fa-solid fa-circle-check"></i> Tuyệt vời! Không có bưu cục cảnh báo
                            </div>
                            <div style="font-size: 13px; color: var(--text-secondary);">
                                Tất cả các bưu cục trong khu vực NTB đều đang vận hành ở trạng thái bình thường.
                            </div>
                        </div>
                    `;
                }
            }

            const bodyEl = document.getElementById('table-unstable-po-body');
            if (!bodyEl) return;
            
            if (data.error) {
                bodyEl.innerHTML = `<tr><td colspan="8" style="text-align: center; color: #ef4444; padding: 24px;"><i class="fa-solid fa-circle-xmark"></i> Lỗi: ${data.error}</td></tr>`;
                return;
            }
            
            if (!data.records || data.records.length === 0) {
                bodyEl.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 24px;">Không có dữ liệu bưu cục.</td></tr>`;
                return;
            }

            // Perform initial filtering and rendering
            filterUnstablePoTable();
        }

        let volCustomerChart = null;
        let volProvinceChart = null;
        let volTreemapChart = null;
        let isVolFiltering = false;

        function cleanClassName(str) {
            if (!str) return '';
            return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]/g, '-');
        }

        function formatMatrixDate(dateStr) {
            if (!dateStr) return '';
            const datePart = dateStr.split(' ')[0];
            const parts = datePart.split('-');
            if (parts.length === 3) {
                return `${parts[2]}/${parts[1]}`;
            }
            return dateStr;
        }

        function getHeatmapColor(val, maxVal) {
            if (maxVal <= 0 || val <= 0) return 'transparent';
            const ratio = val / maxVal;
            return `rgba(0, 123, 195, ${ratio * 0.55})`;
        }

        function toggleMatrixProvince(provClass) {
            const rows = document.querySelectorAll(`.province-detail-${provClass}`);
            const chevron = document.getElementById(`chevron-${provClass}`);
            if (rows.length === 0) return;
            
            const isHidden = rows[0].style.display === 'none';
            rows.forEach(row => {
                row.style.display = isHidden ? 'table-row' : 'none';
            });
            
            if (chevron) {
                if (isHidden) {
                    chevron.classList.remove('fa-chevron-right');
                    chevron.classList.add('fa-chevron-down');
                } else {
                    chevron.classList.remove('fa-chevron-down');
                    chevron.classList.add('fa-chevron-right');
                }
            }
        }

        function toggleAllMatrixRows(expand) {
            const details = document.querySelectorAll('[class^="po-row province-detail-"]');
            details.forEach(row => {
                row.style.display = expand ? 'table-row' : 'none';
            });
            
            const chevrons = document.querySelectorAll('[id^="chevron-"]');
            chevrons.forEach(chev => {
                if (expand) {
                    chev.classList.remove('fa-chevron-right');
                    chev.classList.add('fa-chevron-down');
                } else {
                    chev.classList.remove('fa-chevron-down');
                    chev.classList.add('fa-chevron-right');
                }
            });
        }

        function populateVolFilters(filtersData, selectedProvince, selectedDistrict, selectedWard, selectedPO, selectedCustomer, selectedPoType) {
            const provinceSelect = document.getElementById('vol-filter-province');
            const districtSelect = document.getElementById('vol-filter-district');
            const wardSelect = document.getElementById('vol-filter-ward');
            const poSelect = document.getElementById('vol-filter-po');
            const customerSelect = document.getElementById('vol-filter-customer');
            const potypeSelect = document.getElementById('vol-filter-potype');
            
            const updateSelect = (selectEl, options, selectedVal, defaultLabel) => {
                if (!selectEl) return;
                const currentVal = selectedVal || selectEl.value;
                selectEl.innerHTML = `<option value="">${defaultLabel}</option>`;
                (options || []).forEach(opt => {
                    const selectedAttr = opt === currentVal ? 'selected' : '';
                    selectEl.innerHTML += `<option value="${escapeHTML(opt)}" ${selectedAttr}>${escapeHTML(opt)}</option>`;
                });
            };
            
            updateSelect(provinceSelect, filtersData.provinces, selectedProvince, '-- Tất cả Tỉnh --');
            updateSelect(districtSelect, filtersData.districts, selectedDistrict, '-- Tất cả Quận/Huyện --');
            updateSelect(wardSelect, filtersData.wards, selectedWard, '-- Tất cả Phường/Xã --');
            updateSelect(poSelect, filtersData.post_offices, selectedPO, '-- Tất cả Bưu cục --');
            updateSelect(customerSelect, filtersData.customers, selectedCustomer, '-- Tất cả Khách hàng --');
            updateSelect(potypeSelect, filtersData.po_types, selectedPoType, '-- Tất cả loại --');
        }

        async function onVolFilterChange(changedType) {
            if (isVolFiltering) return;
            isVolFiltering = true;
            
            const province = document.getElementById('vol-filter-province').value;
            let district = document.getElementById('vol-filter-district').value;
            let ward = document.getElementById('vol-filter-ward').value;
            let po = document.getElementById('vol-filter-po').value;
            const customer = document.getElementById('vol-filter-customer').value;
            const potype = document.getElementById('vol-filter-potype').value;
            const daterange = document.getElementById('vol-filter-daterange').value;
            
            if (changedType === 'province') {
                district = '';
                ward = '';
                po = '';
            } else if (changedType === 'district') {
                ward = '';
                po = '';
            } else if (changedType === 'ward') {
                po = '';
            }
            
            try {
                const queryParams = new URLSearchParams({
                    province: province,
                    district: district,
                    ward: ward,
                    post_office: po,
                    customer: customer,
                    po_type: potype,
                    date_range: daterange
                });
                
                showLoading("Đang cập nhật báo cáo volume...");
                const res = await fetch(getApiUrl(`/api/volume-creation?${queryParams.toString()}`), getFetchOptions());
                const data = await res.json();
                
                if (data.error) {
                    alert("Lỗi lọc dữ liệu: " + data.error);
                } else {
                    populateVolFilters(data.filters, province, district, ward, po, customer, potype);
                    renderVolumeCreation(data);
                }
            } catch (err) {
                console.error("Lỗi khi lọc volume:", err);
            } finally {
                hideLoading();
                isVolFiltering = false;
            }
        }

        function renderVolumeCreation(data) {
            const dateEl = document.getElementById('volume-creation-report-date');
            const kpiValEl = document.getElementById('kpi-volume-creation');
            const kpiCompEl = document.getElementById('kpi-volume-creation-comparison');
            const tbody = document.getElementById('table-volume-creation-pivot-body');

            if (!data || data.error) {
                if (kpiValEl) kpiValEl.innerText = "Lỗi";
                if (kpiCompEl) kpiCompEl.innerText = data && data.error ? data.error : "Không có dữ liệu";
                if (tbody) {
                    tbody.innerHTML = `<tr><td colspan="12" style="text-align: center; color: var(--text-danger); font-weight: 600; padding: 24px;"><i class="fa-solid fa-circle-exclamation"></i> ${data && data.error ? escapeHTML(data.error) : "Lỗi tải dữ liệu"}</td></tr>`;
                }
                return;
            }

            const provinceSelect = document.getElementById('vol-filter-province');
            if (provinceSelect && provinceSelect.options.length <= 1 && data.filters) {
                populateVolFilters(data.filters, '', '', '', '', '', '');
            }

            if (dateEl) {
                dateEl.innerText = `Ngày tạo đơn: ${data.kpi.latest_date}`;
            }

            if (kpiValEl) {
                kpiValEl.innerText = data.kpi.today_vol.toLocaleString() + " đơn";
            }

            const getRatioClass = (ratio) => {
                if (ratio === null || ratio === undefined || ratio === 0) return 'text-muted';
                if (ratio > 0.0) return 'text-success';
                if (ratio < 0.0) return 'text-danger';
                return 'text-muted';
            };

            const formatRatio = (ratio) => {
                if (ratio === null || ratio === undefined) return '-';
                if (ratio > 0.0) return `+${ratio}%`;
                return `${ratio}%`;
            };

            if (kpiCompEl) {
                kpiCompEl.innerHTML = `
                    <div class="comp-row">
                        <span class="comp-label">D/D-1:</span>
                        <span class="comp-val ${getRatioClass(data.kpi.d_d1)}" style="font-weight: 700;">${formatRatio(data.kpi.d_d1)}</span>
                    </div>
                    <div class="comp-row">
                        <span class="comp-label">D/D-7:</span>
                        <span class="comp-val ${getRatioClass(data.kpi.d_d7)}" style="font-weight: 700;">${formatRatio(data.kpi.d_d7)}</span>
                    </div>
                `;
            }

            if (tbody) {
                let html = "";
                
                (data.table || []).forEach(row => {
                    html += `
                        <tr>
                            <td style="text-align: left; font-weight: 600;">${escapeHTML(row.province)}</td>
                            <td>${row.wtd2.toLocaleString()}</td>
                            <td>${row.wtd1.toLocaleString()}</td>
                            <td>${row.wtd.toLocaleString()}</td>
                            <td style="font-weight: 700; background-color: rgba(79, 70, 229, 0.02);" class="${getRatioClass(row.wtd_wtd2)}">${formatRatio(row.wtd_wtd2)}</td>
                            <td style="font-weight: 700; background-color: rgba(79, 70, 229, 0.02);" class="${getRatioClass(row.wtd_wtd1)}">${formatRatio(row.wtd_wtd1)}</td>
                            <td style="font-weight: 700; background-color: rgba(79, 70, 229, 0.02);" class="${getRatioClass(row.d_d7)}">${formatRatio(row.d_d7)}</td>
                            <td style="font-weight: 700; background-color: rgba(79, 70, 229, 0.02);" class="${getRatioClass(row.d_d1)}">${formatRatio(row.d_d1)}</td>
                            <td>${row.d7.toLocaleString()}</td>
                            <td>${row.d2.toLocaleString()}</td>
                            <td>${row.d1.toLocaleString()}</td>
                            <td style="font-weight: 600;">${row.d.toLocaleString()}</td>
                        </tr>
                    `;
                });

                if (data.total) {
                    const r = data.total;
                    html += `
                        <tr style="font-weight: bold; background-color: rgba(79, 70, 229, 0.08); border-top: 2px solid var(--border-color);">
                            <td style="text-align: left;">${escapeHTML(r.province)}</td>
                            <td>${r.wtd2.toLocaleString()}</td>
                            <td>${r.wtd1.toLocaleString()}</td>
                            <td>${r.wtd.toLocaleString()}</td>
                            <td style="background-color: rgba(79, 70, 229, 0.05);" class="${getRatioClass(r.wtd_wtd2)}">${formatRatio(r.wtd_wtd2)}</td>
                            <td style="background-color: rgba(79, 70, 229, 0.05);" class="${getRatioClass(r.wtd_wtd1)}">${formatRatio(r.wtd_wtd1)}</td>
                            <td style="background-color: rgba(79, 70, 229, 0.05);" class="${getRatioClass(r.d_d7)}">${formatRatio(r.d_d7)}</td>
                            <td style="background-color: rgba(79, 70, 229, 0.05);" class="${getRatioClass(r.d_d1)}">${formatRatio(r.d_d1)}</td>
                            <td>${r.d7.toLocaleString()}</td>
                            <td>${r.d2.toLocaleString()}</td>
                            <td>${r.d1.toLocaleString()}</td>
                            <td>${r.d.toLocaleString()}</td>
                        </tr>
                    `;
                }
                
                tbody.innerHTML = html;
            }

            const mHead = document.getElementById('table-volume-creation-matrix-head');
            const mBody = document.getElementById('table-volume-creation-matrix-body');
            
            if (mHead && mBody && data.matrix && data.matrix.dates) {
                let headHtml = `
                    <tr>
                        <th style="text-align: left; font-weight: 700; font-size: 13px;">Tỉnh / Bưu cục</th>
                `;
                data.matrix.dates.forEach(d => {
                    headHtml += `<th style="text-align: center; font-weight: 700; font-size: 11px;">${formatMatrixDate(d)}</th>`;
                });
                headHtml += `
                        <th style="text-align: center; font-weight: 700; font-size: 13px; background-color: rgba(0, 123, 195, 0.05);">Tổng cộng</th>
                    </tr>
                `;
                mHead.innerHTML = headHtml;
                
                let bodyHtml = "";
                
                let maxProvVal = 0;
                let maxPoVal = 0;
                (data.matrix.rows || []).forEach(row => {
                    Object.values(row.data).forEach(v => {
                        if (v > maxProvVal) maxProvVal = v;
                    });
                    (row.pos || []).forEach(po => {
                        Object.values(po.data).forEach(v => {
                            if (v > maxPoVal) maxPoVal = v;
                        });
                    });
                });
                
                if (data.matrix.rows && data.matrix.rows.length > 0) {
                    data.matrix.rows.forEach(row => {
                        const provClass = cleanClassName(row.province);
                        
                        bodyHtml += `
                            <tr style="background-color: rgba(0, 123, 195, 0.02); font-weight: 600;">
                                <td style="text-align: left; padding: 10px;">
                                    <span style="cursor: pointer; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;" onclick="toggleMatrixProvince('${provClass}')">
                                        <i class="fa-solid fa-chevron-right toggle-icon" id="chevron-${provClass}"></i> ${escapeHTML(row.province)}
                                    </span>
                                </td>
                        `;
                        
                        data.matrix.dates.forEach(d => {
                            const val = row.data[d] || 0;
                            const bgColor = getHeatmapColor(val, maxProvVal);
                            const textColor = (val / maxProvVal > 0.5) ? '#ffffff' : 'var(--text-primary)';
                            bodyHtml += `<td style="background-color: ${bgColor}; color: ${textColor}; text-align: center; font-weight: 700;">${val.toLocaleString()}</td>`;
                        });
                        
                        bodyHtml += `
                                <td style="font-weight: 800; background-color: rgba(0, 123, 195, 0.05);">${row.total.toLocaleString()}</td>
                            </tr>
                        `;
                        
                        (row.pos || []).forEach(po => {
                            bodyHtml += `
                                <tr class="po-row province-detail-${provClass}" style="display: none; background-color: rgba(248, 250, 252, 0.6);">
                                    <td style="text-align: left; padding-left: 28px; color: var(--text-secondary);">${escapeHTML(po.bc)}</td>
                            `;
                            
                            data.matrix.dates.forEach(d => {
                                const val = po.data[d] || 0;
                                const bgColor = getHeatmapColor(val, maxPoVal);
                                const textColor = (val / maxPoVal > 0.5) ? '#ffffff' : 'var(--text-primary)';
                                bodyHtml += `<td style="background-color: ${bgColor}; color: ${textColor}; text-align: center;">${val.toLocaleString()}</td>`;
                            });
                            
                            bodyHtml += `
                                    <td style="font-weight: 600; color: var(--color-ghn-blue);">${po.total.toLocaleString()}</td>
                                </tr>
                            `;
                        });
                    });
                } else {
                    bodyHtml = `<tr><td colspan="${data.matrix.dates.length + 2}" style="text-align: center; color: var(--text-muted); padding: 24px;">Không có dữ liệu ma trận nhiệt</td></tr>`;
                }
                mBody.innerHTML = bodyHtml;
            }

            if (volCustomerChart) { volCustomerChart.destroy(); volCustomerChart = null; }
            if (volProvinceChart) { volProvinceChart.destroy(); volProvinceChart = null; }
            if (volTreemapChart) { volTreemapChart.destroy(); volTreemapChart = null; }

            if (data.charts && data.charts.line && data.charts.line.dates.length > 0) {
                const lineOptions = {
                    chart: {
                        type: 'line',
                        height: 350,
                        fontFamily: 'Inter, sans-serif',
                        toolbar: { show: false }
                    },
                    series: data.charts.line.series,
                    xaxis: {
                        categories: data.charts.line.dates.map(formatMatrixDate),
                        labels: {
                            style: { fontFamily: 'Inter, sans-serif', fontSize: '11px', colors: 'var(--text-secondary)' }
                        }
                    },
                    yaxis: {
                        labels: {
                            formatter: function(val) { return val.toLocaleString(); },
                            style: { fontFamily: 'Inter, sans-serif', fontSize: '11px', colors: 'var(--text-secondary)' }
                        }
                    },
                    colors: ['#007bc3', '#ff5f00', '#10b981', '#f59e0b', '#7c3aed'],
                    stroke: { curve: 'smooth', width: 3 },
                    markers: { size: 4 },
                    grid: { borderColor: 'var(--border-color)', strokeDashArray: 4 },
                    title: {
                        text: 'Xu hướng tạo đơn theo nhóm khách hàng',
                        align: 'left',
                        style: { fontFamily: 'Outfit, sans-serif', fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }
                    },
                    legend: { position: 'bottom', fontFamily: 'Inter, sans-serif', fontSize: '12px', labels: { colors: 'var(--text-primary)' } },
                    tooltip: {
                        y: { formatter: function(val) { return val.toLocaleString() + " đơn"; } }
                    }
                };
                volCustomerChart = new ApexCharts(document.querySelector("#chart-volume-customer-trends"), lineOptions);
                volCustomerChart.render();
            }

            if (data.charts && data.charts.bar && data.charts.bar.dates.length > 0) {
                const barOptions = {
                    chart: {
                        type: 'bar',
                        height: 350,
                        fontFamily: 'Inter, sans-serif',
                        toolbar: { show: false }
                    },
                    plotOptions: {
                        bar: { horizontal: false, columnWidth: '55%', borderRadius: 4 }
                    },
                    series: data.charts.bar.series,
                    xaxis: {
                        categories: data.charts.bar.dates.map(formatMatrixDate),
                        labels: {
                            style: { fontFamily: 'Inter, sans-serif', fontSize: '11px', colors: 'var(--text-secondary)' }
                        }
                    },
                    yaxis: {
                        labels: {
                            formatter: function(val) { return val.toLocaleString(); },
                            style: { fontFamily: 'Inter, sans-serif', fontSize: '11px', colors: 'var(--text-secondary)' }
                        }
                    },
                    colors: ['#007bc3', '#ff5f00', '#10b981', '#f59e0b', '#7c3aed'],
                    grid: { borderColor: 'var(--border-color)', strokeDashArray: 4 },
                    title: {
                        text: 'Sản lượng daily theo từng tỉnh',
                        align: 'left',
                        style: { fontFamily: 'Outfit, sans-serif', fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }
                    },
                    legend: { position: 'bottom', fontFamily: 'Inter, sans-serif', fontSize: '12px', labels: { colors: 'var(--text-primary)' } },
                    tooltip: {
                        y: { formatter: function(val) { return val.toLocaleString() + " đơn"; } }
                    }
                };
                volProvinceChart = new ApexCharts(document.querySelector("#chart-volume-province-bars"), barOptions);
                volProvinceChart.render();
            }

            if (data.charts && data.charts.treemap && data.charts.treemap.length > 0) {
                const getProvinceColor = (prov) => {
                    const colors = {
                        'Bình Thuận': '#007bc3',
                        'Khánh Hòa': '#ff5f00',
                        'Lâm Đồng': '#10b981',
                        'Ninh Thuận': '#f59e0b',
                        'Đắk Nông': '#7c3aed'
                    };
                    return colors[prov] || '#64748b';
                };
                
                const treemapSeriesData = data.charts.treemap.map(item => ({
                    x: item.name,
                    y: item.value,
                    color: getProvinceColor(item.province)
                }));
                
                const treemapOptions = {
                    chart: {
                        type: 'treemap',
                        height: 400,
                        fontFamily: 'Inter, sans-serif',
                        toolbar: { show: false }
                    },
                    series: [{ data: treemapSeriesData }],
                    title: {
                        text: 'Bưu cục tăng trưởng sản lượng tốt (Xếp hạng theo sản lượng tăng trưởng 7D tuyệt đối)',
                        align: 'left',
                        style: { fontFamily: 'Outfit, sans-serif', fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }
                    },
                    plotOptions: {
                        treemap: { enableShades: false, distributed: true }
                    },
                    legend: { show: false },
                    tooltip: {
                        custom: function({ series, seriesIndex, dataPointIndex, w }) {
                            const item = data.charts.treemap[dataPointIndex];
                            if (!item) return '';
                            const sign = item.growth_abs > 0 ? '+' : '';
                            const growthClass = item.growth_abs > 0 ? 'text-success' : (item.growth_abs < 0 ? 'text-danger' : 'text-muted');
                            
                            return `
                                <div class="custom-tooltip" style="padding: 12px; font-family: 'Inter', sans-serif; background: #ffffff; border: 1px solid var(--border-color); border-radius: 8px; box-shadow: var(--shadow-md); color: var(--text-primary);">
                                    <div style="font-weight: 700; margin-bottom: 6px; font-family: 'Outfit'; font-size: 14px;">${escapeHTML(item.name)}</div>
                                    <div style="font-size: 12px; margin-bottom: 4px; color: var(--text-secondary);">Tỉnh: <b style="color: var(--text-primary);">${escapeHTML(item.province)}</b></div>
                                    <div style="font-size: 12px; margin-bottom: 4px; color: var(--text-secondary);">Sản lượng hôm nay: <b style="color: var(--text-primary);">${item.value.toLocaleString()}</b></div>
                                    <div style="font-size: 12px; color: var(--text-secondary);">Tăng trưởng so với 7D trước: <span class="${growthClass}" style="font-weight: 700;">${sign}${item.growth_abs.toLocaleString()} (${sign}${item.growth_pct}%)</span></div>
                                </div>
                            `;
                        }
                    }
                };
                volTreemapChart = new ApexCharts(document.querySelector("#chart-volume-treemap"), treemapOptions);
                volTreemapChart.render();
            }
        }

        function renderOffSpe(data) {
            const dateEl = document.getElementById('off-spe-report-date');
            if (dateEl) {
                dateEl.innerText = data.update_time ? `Cập nhật: ${data.update_time}` : "Cập nhật: Chưa rõ";
            }
            
            // Render KPI on overview
            const activeCountEl = document.getElementById('kpi-off-spe-active');
            const pendingCountEl = document.getElementById('kpi-off-spe-pending');
            const updateTimeEl = document.getElementById('kpi-off-spe-update');
            
            if (data.error) {
                if (activeCountEl) activeCountEl.innerText = "Lỗi";
                if (pendingCountEl) pendingCountEl.innerText = "Lỗi";
                if (updateTimeEl) updateTimeEl.innerText = "File lỗi/chưa có";
            } else {
                if (activeCountEl) activeCountEl.innerText = data.total_off !== undefined ? data.total_off : "0";
                if (pendingCountEl) pendingCountEl.innerText = data.total_pending !== undefined ? data.total_pending : "0";
                if (updateTimeEl) {
                    updateTimeEl.innerText = data.update_time ? `Cập nhật: ${data.update_time}` : "Cập nhật: Chưa rõ";
                }
            }

            // Populate Province Dropdown Filter in OFF SPE Tab
            const provSelect = document.getElementById('filter-off-spe-province');
            if (provSelect && data.records && !data.error) {
                const currentVal = provSelect.value;
                provSelect.innerHTML = '<option value="">-- Tất cả Tỉnh --</option>';
                const provinces = [...new Set(data.records.map(r => r.province).filter(Boolean))].sort();
                provinces.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p;
                    opt.innerText = p;
                    provSelect.appendChild(opt);
                });
                provSelect.value = currentVal;
            }

            filterOffSpeTable();
        }

        function filterOffSpeTable() {
            const data = globalData.offSpe;
            const tbody = document.getElementById('table-off-spe-body');
            if (!tbody) return;

            if (!data || data.error) {
                tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; color: var(--text-danger); font-weight: 600; padding: 24px;"><i class="fa-solid fa-circle-exclamation"></i> ${data && data.error ? escapeHTML(data.error) : "Không có dữ liệu hoặc file cấu hình lỗi."}</td></tr>`;
                return;
            }

            const searchVal = document.getElementById('search-off-spe').value.toLowerCase().trim();
            const statusFilter = document.getElementById('filter-off-spe-status').value;
            const provFilter = document.getElementById('filter-off-spe-province').value;

            const filtered = (data.records || []).filter(row => {
                const matchesSearch = !searchVal || 
                    (row.district && row.district.toLowerCase().includes(searchVal)) ||
                    (row.ward && row.ward.toLowerCase().includes(searchVal)) ||
                    (row.post_office && row.post_office.toLowerCase().includes(searchVal));

                const matchesStatus = !statusFilter || row.status === statusFilter;
                const matchesProv = !provFilter || row.province === provFilter;

                return matchesSearch && matchesStatus && matchesProv;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; color: var(--text-muted); padding: 24px;">Không tìm thấy tuyến nào phù hợp bộ lọc.</td></tr>`;
                return;
            }

            tbody.innerHTML = '';
            filtered.forEach((row, idx) => {
                const tr = document.createElement('tr');
                
                // Style status badge
                let statusBadge = '';
                if (row.status === "Đang OFF") {
                    statusBadge = `<span class="badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); font-weight: 700;">Đang OFF</span>`;
                } else {
                    statusBadge = `<span class="badge" style="background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); font-weight: 700;">Chờ duyệt</span>`;
                }

                tr.innerHTML = `
                    <td style="text-align: center; font-weight: 600; color: var(--text-secondary);">${idx + 1}</td>
                    <td style="font-weight: 600; color: var(--text-primary);">${escapeHTML(row.province || '')}</td>
                    <td>${escapeHTML(row.district || '')}</td>
                    <td>${escapeHTML(row.ward || '')}</td>
                    <td>${escapeHTML(row.post_office || '')}</td>
                    <td style="text-align: center;">${statusBadge}</td>
                    <td style="text-align: center; font-weight: 700; color: var(--text-secondary);">${escapeHTML(row.pct_cap_down || '')}</td>
                    <td style="text-align: center; font-family: monospace;">${escapeHTML(row.off_time || '')}</td>
                    <td style="text-align: center; font-family: monospace;">${escapeHTML(row.on_time || '')}</td>
                    <td style="color: var(--text-muted); max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${escapeHTML(row.note || '')}">${escapeHTML(row.note || '')}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        // ==========================================
        // PAGINATION HELPERS
        // ==========================================
        function prevPage(type) {
            if (paginationState[type].current > 1) {
                paginationState[type].current--;
                if (type === 'opr') renderOprDetailsTable();
                if (type === 'aging') renderAgingDetailsTable();
                if (type === 'treo') renderTreoDetailsTable();
            }
        }

        function nextPage(type) {
            let total = 0;
            if (type === 'opr') total = filteredData.oe_details.length;
            if (type === 'aging') total = filteredData.aging_details.length;
            if (type === 'treo') total = filteredData.treo_details.length;

            const totalPages = Math.ceil(total / paginationState[type].perPage);
            if (paginationState[type].current < totalPages) {
                paginationState[type].current++;
                if (type === 'opr') renderOprDetailsTable();
                if (type === 'aging') renderAgingDetailsTable();
                if (type === 'treo') renderTreoDetailsTable();
            }
        }

        // ==========================================
        // UTILS
        // ==========================================
        function roundNum(num) {
            if (num === null || num === undefined) return 0;
            return Math.round(Number(num) * 100) / 100;
        }

        // ==========================================
        // NTB SUMMARY DASHBOARD TAB LOGIC
        // ==========================================
        let ntbCompletedChart = null;
        let ntbBacklogChart = null;
        let ntbLtcTrendChart = null;
        let ntbGtcTrendChart = null;

        async function loadNtbSummaryData() {
            const am = document.getElementById('filter-am').value;
            const prov = document.getElementById('filter-province').value;
            const po = document.getElementById('filter-po').value;
            const dateSelect = document.getElementById('ntb-date-select');
            const selectedDate = dateSelect ? dateSelect.value : '';

            const params = new URLSearchParams();
            if (am) params.append('am', am);
            if (prov) params.append('province', prov);
            if (po) params.append('post_office', po);
            if (selectedDate) params.append('date', selectedDate);

            try {
                // Fetch summary dashboard data
                const summaryRes = await fetch(getApiUrl(`/api/summary-dashboard?${params.toString()}`), getFetchOptions());
                const summaryData = await summaryRes.json();

                if (summaryData.error) {
                    console.error("Summary error:", summaryData.error);
                    return;
                }

                // Populate date dropdown
                if (dateSelect) {
                    const activeDate = summaryData.latest_date;
                    const currentOptions = Array.from(dateSelect.options).map(o => o.value);
                    const newOptions = summaryData.all_dates || [];
                    
                    const isDifferent = currentOptions.length !== newOptions.length || 
                                      !currentOptions.every((val, index) => val === newOptions[index]);
                    
                    if (isDifferent || dateSelect.children.length === 0) {
                        dateSelect.innerHTML = '';
                        newOptions.forEach(d => {
                            const opt = document.createElement('option');
                            opt.value = d;
                            opt.innerText = d;
                            dateSelect.appendChild(opt);
                        });
                    }
                    dateSelect.value = activeDate;
                }

                // Update 9 KPI Grid
                const kpis = summaryData.kpis;
                if (kpis) {
                    const updateKpiCard = (metric, provKey, kpiData) => {
                        const valEl = document.getElementById(`ntb-kpi-${metric}-${provKey}`);
                        const trendEl = document.getElementById(`ntb-kpi-${metric}-${provKey}-trend`);
                        if (!valEl || !trendEl) return;
                        
                        if (kpiData) {
                            valEl.innerText = kpiData[metric] + "%";
                            
                            let trendHtml = '';
                            if (kpiData.dod) {
                                const diff = kpiData.dod[metric];
                                if (diff > 0) {
                                    trendHtml += `<span style="color: var(--color-success); font-weight:600;"><i class="fa-solid fa-caret-up"></i> +${diff}%</span>`;
                                } else if (diff < 0) {
                                    trendHtml += `<span style="color: var(--color-danger); font-weight:600;"><i class="fa-solid fa-caret-down"></i> ${diff}%</span>`;
                                } else {
                                    trendHtml += `<span style="color: var(--text-muted);">-</span>`;
                                }
                            }
                            if (kpiData.wow) {
                                const diff = kpiData.wow[metric];
                                if (diff > 0) {
                                    trendHtml += ` <span style="color: #007bc3; font-weight:600;" title="So với cùng kỳ tuần trước"><i class="fa-solid fa-clock"></i> ↑ +${diff}%</span>`;
                                } else if (diff < 0) {
                                    trendHtml += ` <span style="color: #ef4444; font-weight:600;" title="So với cùng kỳ tuần trước"><i class="fa-solid fa-clock"></i> ↓ ${diff}%</span>`;
                                } else {
                                    trendHtml += ` <span style="color: var(--text-muted);" title="So với cùng kỳ tuần trước"><i class="fa-solid fa-clock"></i> -</span>`;
                                }
                            }
                            trendEl.innerHTML = trendHtml;
                        } else {
                            valEl.innerText = "0%";
                            trendEl.innerHTML = "";
                        }
                    };

                    updateKpiCard('ltc', 'overall', kpis.overall);
                    updateKpiCard('gtc', 'overall', kpis.overall);
                    updateKpiCard('ttc', 'overall', kpis.overall);

                    updateKpiCard('ltc', 'lamdong', kpis.lam_dong);
                    updateKpiCard('gtc', 'lamdong', kpis.lam_dong);
                    updateKpiCard('ttc', 'lamdong', kpis.lam_dong);

                    updateKpiCard('ltc', 'binhthuan', kpis.binh_thuan);
                    updateKpiCard('gtc', 'binhthuan', kpis.binh_thuan);
                    updateKpiCard('ttc', 'binhthuan', kpis.binh_thuan);
                }

                // Update new overview report date label
                const ovReportDateEl = document.getElementById('overview-report-date');
                if (ovReportDateEl) {
                    ovReportDateEl.innerText = "Ngày báo cáo: " + summaryData.latest_date;
                }

                // Populate new overview provinces table
                const ovTableBody = document.querySelector('#table-overview-provinces tbody');
                if (ovTableBody) {
                    ovTableBody.innerHTML = '';
                    
                    const compVols = summaryData.completed_vols || [];
                    
                    // Sort provinces alphabetically so they are neat
                    const sortedVols = [...compVols].sort((a, b) => a.province.localeCompare(b.province));
                    
                    sortedVols.forEach(provData => {
                        if (provData.province === "Không xác định") return;
                        
                        const tr = document.createElement('tr');
                        
                        const gtcVol = provData.Volume_gtc || 0;
                        const ltcVol = provData.Volume_ltc || 0;
                        
                        tr.innerHTML = `
                            <td style="text-align: left; font-weight: 600;">${escapeHTML(provData.province)}</td>
                            <td style="text-align: center;">${gtcVol.toLocaleString()}</td>
                            <td style="text-align: center;"><span class="badge ${provData.GTC_pct >= 60 ? 'badge-success' : 'badge-danger'}">${provData.GTC_pct}%</span></td>
                            <td style="text-align: center;">${ltcVol.toLocaleString()}</td>
                            <td style="text-align: center;"><span class="badge ${provData.LTC_pct >= 80 ? 'badge-success' : 'badge-danger'}">${provData.LTC_pct}%</span></td>
                            <td style="text-align: center;"><span class="badge badge-secondary">${provData.TTC_pct}%</span></td>
                        `;
                        ovTableBody.appendChild(tr);
                    });
                    
                    // Add region total row (Toàn vùng NTB)
                    const overall = summaryData.kpis ? summaryData.kpis.overall : null;
                    if (overall) {
                        const tr = document.createElement('tr');
                        tr.style.backgroundColor = 'rgba(255, 95, 0, 0.05)';
                        tr.style.borderTop = '2px solid var(--color-ghn-orange)';
                        
                        const gtcVol = overall.vol_gtc || 0;
                        const ltcVol = overall.vol_ltc || 0;
                        
                        tr.innerHTML = `
                            <td style="text-align: left; font-weight: 800; color: var(--color-ghn-orange);">Toàn vùng NTB</td>
                            <td style="text-align: center; font-weight: 700;">${gtcVol.toLocaleString()}</td>
                            <td style="text-align: center;"><span class="badge ${overall.gtc >= 60 ? 'badge-success' : 'badge-danger'}" style="font-weight: 700;">${overall.gtc}%</span></td>
                            <td style="text-align: center; font-weight: 700;">${ltcVol.toLocaleString()}</td>
                            <td style="text-align: center;"><span class="badge ${overall.ltc >= 80 ? 'badge-success' : 'badge-danger'}" style="font-weight: 700;">${overall.ltc}%</span></td>
                            <td style="text-align: center;"><span class="badge badge-secondary" style="font-weight: 700; background-color: var(--color-warning); color: white;">${overall.ttc}%</span></td>
                        `;
                        ovTableBody.appendChild(tr);
                    }
                }

                // Render Completed Volume Chart (Grouped bars by province)
                const compVols = summaryData.completed_vols || [];
                const compCategories = compVols.map(v => v.province);
                const ltcSeries = compVols.map(v => v.LTC);
                const gtcSeries = compVols.map(v => v.GTC);
                const ttcSeries = compVols.map(v => v.TTC);

                const compOptions = {
                    chart: { type: 'bar', height: 280, toolbar: { show: false }, background: 'transparent' },
                    series: [
                        { name: 'LTC', data: ltcSeries },
                        { name: 'GTC', data: gtcSeries },
                        { name: 'TTC', data: ttcSeries }
                    ],
                    xaxis: { categories: compCategories, labels: { style: { colors: '#64748b' } } },
                    yaxis: { title: { text: 'Sản lượng' }, labels: { style: { colors: '#64748b' } } },
                    colors: ['#007bc3', '#ff5f00', '#10b981'],
                    plotOptions: { bar: { horizontal: false, columnWidth: '55%', borderRadius: 4 } },
                    theme: { mode: 'light' },
                    dataLabels: { enabled: false },
                    legend: { position: 'bottom', labels: { colors: '#64748b' } }
                };

                if (ntbCompletedChart) ntbCompletedChart.destroy();
                ntbCompletedChart = new ApexCharts(document.querySelector("#chart-ntb-completed"), compOptions);
                ntbCompletedChart.render();

                // Render Backlog Chart by AM
                const blAM = summaryData.backlog_by_am || [];
                const blCategories = blAM.map(b => b.am);
                const clSeries = blAM.map(b => b.chua_lay);
                const cgSeries = blAM.map(b => b.chua_giao);
                const ctSeries = blAM.map(b => b.chua_tra);

                const blOptions = {
                    chart: { type: 'bar', height: 280, toolbar: { show: false }, background: 'transparent', stacked: true },
                    series: [
                        { name: 'Đơn chưa lấy', data: clSeries },
                        { name: 'Đơn chưa giao', data: cgSeries },
                        { name: 'Đơn chưa trả', data: ctSeries }
                    ],
                    xaxis: { categories: blCategories, labels: { style: { colors: '#64748b' } } },
                    yaxis: { title: { text: 'Sản lượng backlog' }, labels: { style: { colors: '#64748b' } } },
                    colors: ['#ef4444', '#ff5f00', '#007bc3'],
                    plotOptions: { bar: { horizontal: false, columnWidth: '55%' } },
                    theme: { mode: 'light' },
                    dataLabels: { enabled: false },
                    legend: { position: 'bottom', labels: { colors: '#64748b' } }
                };

                if (ntbBacklogChart) ntbBacklogChart.destroy();
                ntbBacklogChart = new ApexCharts(document.querySelector("#chart-ntb-backlog-am"), blOptions);
                ntbBacklogChart.render();

                // Fetch trends data
                const trendsRes = await fetch(getApiUrl(`/api/trends-dashboard?${params.toString()}`), getFetchOptions());
                const trendsData = await trendsRes.json();

                const trendDates = trendsData.dates || [];
                const trends = trendsData.trends || {};

                const ltcLines = [];
                if (trends.overall) ltcLines.push({ name: 'Toàn vùng', data: trends.overall.ltc });
                if (trends['lâm_đồng']) ltcLines.push({ name: 'Lâm Đồng', data: trends['lâm_đồng'].ltc });
                if (trends['bình_thuận']) ltcLines.push({ name: 'Bình Thuận', data: trends['bình_thuận'].ltc });

                const ltcTrendOptions = {
                    chart: { type: 'line', height: 280, toolbar: { show: false }, background: 'transparent' },
                    series: ltcLines,
                    xaxis: { categories: trendDates.map(d => d.split(" - ")[0]), labels: { style: { colors: '#64748b' } } },
                    yaxis: { title: { text: 'Tỷ lệ %' }, min: 40, max: 100, labels: { style: { colors: '#64748b' } } },
                    colors: ['#ff5f00', '#007bc3', '#10b981'],
                    stroke: { width: 3, curve: 'smooth' },
                    theme: { mode: 'light' },
                    legend: { position: 'bottom', labels: { colors: '#64748b' } },
                    dataLabels: { enabled: true, formatter: val => val + "%", style: { fontSize: '9px' } }
                };

                if (ntbLtcTrendChart) ntbLtcTrendChart.destroy();
                ntbLtcTrendChart = new ApexCharts(document.querySelector("#chart-ntb-ltc-trend"), ltcTrendOptions);
                ntbLtcTrendChart.render();

                const gtcLines = [];
                if (trends.overall) gtcLines.push({ name: 'Toàn vùng', data: trends.overall.gtc });
                if (trends['lâm_đồng']) gtcLines.push({ name: 'Lâm Đồng', data: trends['lâm_đồng'].gtc });
                if (trends['bình_thuận']) gtcLines.push({ name: 'Bình Thuận', data: trends['bình_thuận'].gtc });

                const gtcTrendOptions = {
                    chart: { type: 'line', height: 280, toolbar: { show: false }, background: 'transparent' },
                    series: gtcLines,
                    xaxis: { categories: trendDates.map(d => d.split(" - ")[0]), labels: { style: { colors: '#64748b' } } },
                    yaxis: { title: { text: 'Tỷ lệ %' }, min: 40, max: 100, labels: { style: { colors: '#64748b' } } },
                    colors: ['#ff5f00', '#007bc3', '#10b981'],
                    stroke: { width: 3, curve: 'smooth' },
                    theme: { mode: 'light' },
                    legend: { position: 'bottom', labels: { colors: '#64748b' } },
                    dataLabels: { enabled: true, formatter: val => val + "%", style: { fontSize: '9px' } }
                };

                if (ntbGtcTrendChart) ntbGtcTrendChart.destroy();
                ntbGtcTrendChart = new ApexCharts(document.querySelector("#chart-ntb-gtc-trend"), gtcTrendOptions);
                ntbGtcTrendChart.render();

                // Update trend cards
                const updateTrendKPI = (prefix, valKey) => {
                    const valEl = document.getElementById(`ntb-trend-${prefix}-val`);
                    const diffEl = document.getElementById(`ntb-trend-${prefix}-diff`);

                    if (trends.overall && trends.overall[valKey]) {
                        const len = trends.overall[valKey].length;
                        if (len >= 1) {
                            const latestVal = trends.overall[valKey][len - 1];
                            valEl.innerText = latestVal ? latestVal + "%" : "- %";

                            if (len >= 2) {
                                const prevVal = trends.overall[valKey][len - 2];
                                const diff = (latestVal - prevVal).toFixed(2);
                                if (diff > 0) {
                                    diffEl.innerHTML = `<span class="trend-up"><i class="fa-solid fa-arrow-trend-up"></i> +${diff}%</span> vs ngày trước (${prevVal}%)`;
                                } else if (diff < 0) {
                                    diffEl.innerHTML = `<span class="trend-down"><i class="fa-solid fa-arrow-trend-down"></i> ${diff}%</span> vs ngày trước (${prevVal}%)`;
                                } else {
                                    diffEl.innerHTML = `<span class="trend-neutral">Không đổi</span> vs ngày trước (${prevVal}%)`;
                                }
                            }
                        }
                    }

                    const ldValEl = document.getElementById(`ntb-trend-${prefix}-ld-val`);
                    const ldDiffEl = document.getElementById(`ntb-trend-${prefix}-ld-diff`);
                    if (trends['lâm_đồng'] && trends['lâm_đồng'][valKey]) {
                        const len = trends['lâm_đồng'][valKey].length;
                        const latestVal = trends['lâm_đồng'][valKey][len - 1];
                        ldValEl.innerText = latestVal ? latestVal + "%" : "- %";
                        if (len >= 2) {
                            const prevVal = trends['lâm_đồng'][valKey][len - 2];
                            const diff = (latestVal - prevVal).toFixed(2);
                            ldDiffEl.innerHTML = diff > 0 ? `<span style="color: var(--color-success)">↑ ${diff}%</span>` : (diff < 0 ? `<span style="color: var(--color-danger)">↓ ${Math.abs(diff)}%</span>` : `<span style="color: var(--text-muted)">-</span>`);
                        }
                    }

                    const btValEl = document.getElementById(`ntb-trend-${prefix}-bt-val`);
                    const btDiffEl = document.getElementById(`ntb-trend-${prefix}-bt-diff`);
                    if (trends['bình_thuận'] && trends['bình_thuận'][valKey]) {
                        const len = trends['bình_thuận'][valKey].length;
                        const latestVal = trends['bình_thuận'][valKey][len - 1];
                        btValEl.innerText = latestVal ? latestVal + "%" : "- %";
                        if (len >= 2) {
                            const prevVal = trends['bình_thuận'][valKey][len - 2];
                            const diff = (latestVal - prevVal).toFixed(2);
                            btDiffEl.innerHTML = diff > 0 ? `<span style="color: var(--color-success)">↑ ${diff}%</span>` : (diff < 0 ? `<span style="color: var(--color-danger)">↓ ${Math.abs(diff)}%</span>` : `<span style="color: var(--text-muted)">-</span>`);
                        }
                    }
                };

                updateTrendKPI('ltc', 'ltc');
                updateTrendKPI('gtc', 'gtc');

                // Fetch matrix tables data
                const matrixRes = await fetch(getApiUrl(`/api/matrix-tables?${params.toString()}`), getFetchOptions());
                const matrixData = await matrixRes.json();

                renderMatrixTable('table-ntb-ltc-matrix', matrixData.ltc, 'LTC');
                renderMatrixTable('table-ntb-gtc-matrix', matrixData.gtc, 'GTC');

            } catch (err) {
                console.error("Error loading NTB data:", err);
            }
        }

        function renderMatrixTable(tableId, matrix, typeLabel) {
            const table = document.getElementById(tableId);
            if (!table) return;

            table.innerHTML = '';

            if (!matrix || !matrix.dates || matrix.dates.length === 0 || !matrix.rows || matrix.rows.length === 0) {
                table.innerHTML = `<thead><tr><th>AM / Bưu cục</th><th>Không có dữ liệu</th></tr></thead>`;
                return;
            }

            const dates = matrix.dates;

            const thead = document.createElement('thead');
            const hRow = document.createElement('tr');

            hRow.innerHTML = `
                <th rowspan="2" style="width: 250px; text-align: left !important;">AM / Bưu cục</th>
            `;

            dates.forEach(d => {
                const displayDate = d.split(" - ")[0];
                hRow.innerHTML += `
                    <th colspan="2" style="text-align: center;">${displayDate}</th>
                `;
            });
            thead.appendChild(hRow);

            const subRow = document.createElement('tr');
            dates.forEach(() => {
                subRow.innerHTML += `
                    <th style="font-size: 10px; text-align: center;">Số đơn</th>
                    <th style="font-size: 10px; text-align: center;">% ${typeLabel}</th>
                `;
            });
            thead.appendChild(subRow);
            table.appendChild(thead);

            const tbody = document.createElement('tbody');

            matrix.rows.forEach((row, amIdx) => {
                const amId = tableId + '-am-' + amIdx;

                const amRow = document.createElement('tr');
                amRow.className = 'am-header-row';
                amRow.onclick = () => toggleAmGroup(amId);

                let cellsHtml = `
                    <td style="text-align: left;">
                        <i id="icon-${amId}" class="fa-solid fa-plus" style="margin-right: 8px; font-size: 11px; color: var(--color-indigo);"></i>
                        <strong>Totals for ${escapeHTML(row.am)}</strong>
                    </td>
                `;

                dates.forEach(d => {
                    const totalData = row.totals[d] || { vol: 0, pct: 0.0 };
                    cellsHtml += `
                        <td style="text-align: center;"><strong>${totalData.vol.toLocaleString()}</strong></td>
                        <td style="text-align: center;"><strong>${totalData.pct}%</strong></td>
                    `;
                });

                amRow.innerHTML = cellsHtml;
                tbody.appendChild(amRow);

                row.pos.forEach(po => {
                    const poRow = document.createElement('tr');
                    poRow.className = `po-row po-row-${amId} collapsed`;

                    let poCellsHtml = `
                        <td style="text-align: left; padding-left: 28px; color: var(--text-secondary);">${escapeHTML(po.bc)}</td>
                    `;

                    dates.forEach(d => {
                        const poData = po.data[d] || { vol: 0, pct: 0.0 };
                        const target = typeLabel === 'LTC' ? 80 : 60;
                        const badgeClass = poData.pct >= target ? 'badge-success' : 'badge-danger';
                        poCellsHtml += `
                            <td style="text-align: center; color: var(--text-secondary);">${poData.vol.toLocaleString()}</td>
                            <td style="text-align: center;">
                                <span class="badge ${badgeClass}">${poData.pct}%</span>
                            </td>
                        `;
                    });

                    poRow.innerHTML = poCellsHtml;
                    tbody.appendChild(poRow);
                });
            });

            table.appendChild(tbody);
        }

        function toggleAmGroup(amId) {
            const rows = document.querySelectorAll(`.po-row-${amId}`);
            rows.forEach(r => r.classList.toggle('collapsed'));

            const icon = document.querySelector(`#icon-${amId}`);
            if (icon) {
                if (icon.classList.contains('fa-plus')) {
                    icon.classList.remove('fa-plus');
                    icon.classList.add('fa-minus');
                } else {
                    icon.classList.remove('fa-minus');
                    icon.classList.add('fa-plus');
                }
            }
        }

        /* ==========================================================================
           GHN AI CHAT LOGIC
           ========================================================================== */
        function toggleChatWindow(show) {
            const trigger = document.getElementById('chat-trigger');
            const windowEl = document.getElementById('chat-window');
            if (show) {
                trigger.style.opacity = '0';
                trigger.style.pointerEvents = 'none';
                windowEl.classList.add('active');
                document.getElementById('chat-input').focus();
            } else {
                trigger.style.opacity = '1';
                trigger.style.pointerEvents = 'auto';
                windowEl.classList.remove('active');
            }
        }

        // Setup Box opening/closing animation on trigger hover
        document.addEventListener('DOMContentLoaded', () => {
            const trigger = document.getElementById('chat-trigger');
            if (trigger) {
                const boxIcon = trigger.querySelector('.ghn-package-box i');
                trigger.addEventListener('mouseenter', () => {
                    boxIcon.className = 'fa-solid fa-box-open';
                });
                trigger.addEventListener('mouseleave', () => {
                    boxIcon.className = 'fa-solid fa-box';
                });
            }
        });

        async function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const query = input.value.trim();
            if (!query) return;
            
            appendMessage(query, 'user');
            input.value = '';
            
            const typingIndicator = appendMessage('🤖 Đang tính toán dữ liệu...', 'ai loading');
            
            try {
                const res = await fetch(getApiUrl('/api/chat'), getFetchOptions({
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: query })
                }));
                
                if (res.ok) {
                    const data = await res.json();
                    typingIndicator.remove();
                    appendMessage(data.reply, 'ai');
                } else {
                    typingIndicator.remove();
                    appendMessage('Xin lỗi, đã xảy ra lỗi khi trao đổi với trợ lý AI.', 'ai');
                }
            } catch (e) {
                typingIndicator.remove();
                appendMessage('Lỗi kết nối server.', 'ai');
            }
        }

        function sendQuickPrompt(promptText) {
            document.getElementById('chat-input').value = promptText;
            sendChatMessage();
        }

        function handleChatKey(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        }

        function appendMessage(text, sender) {
            const container = document.getElementById('chat-messages');
            const msg = document.createElement('div');
            msg.className = `chat-message ${sender}`;
            msg.innerHTML = text;
            container.appendChild(msg);
            container.scrollTop = container.scrollHeight;
            return msg;
        }

        async function loadNtbStructure() {
            const root = document.getElementById('ntb-org-tree-root');
            if (!root) return;

            // Keywords to identify warehouses vs post offices
            const WAREHOUSE_KEYWORDS = ['Kho Trung Chuyển', 'Kho Trung Chuyen', 'Kho Chuyển Tiếp', 'Kho Chuyen Tiep', 'Kho TC', 'Transit Hub', 'Sub-hub'];
            function isWarehouse(name) {
                return WAREHOUSE_KEYWORDS.some(kw => name.toLowerCase().includes(kw.toLowerCase()));
            }

            try {
                const res = await fetch(getApiUrl('/api/ntb-structure'), getFetchOptions());
                if (!res.ok) throw new Error("Lỗi khi tải dữ liệu cơ cấu từ server");
                const structure = await res.json();
                if (structure.error) {
                    root.innerHTML = `<div style="color: var(--color-danger); text-align: center; padding: 20px;">
                        <i class="fa-solid fa-triangle-exclamation" style="margin-right: 8px;"></i> ${escapeHTML(structure.error)}
                    </div>`;
                    return;
                }

                // Update window.provinceStats dynamically from loaded Excel structure
                const provinceRegions = {
                    "Lâm Đồng": "Tây Nguyên",
                    "Khánh Hòa": "Duyên hải",
                    "Đắk Nông": "Tây Nguyên",
                    "Bình Thuận": "Duyên hải",
                    "Ninh Thuận": "Duyên hải"
                };

                let ntbTotalPOs = 0;
                let ntbTotalKTC = 0;
                let ntbTotalKCT = 0;
                const ntbUniqueAMs = new Set();

                for (const [prov, ams] of Object.entries(structure)) {
                    const normProv = prov.replace('Khánh Hoà','Khánh Hòa').trim();
                    const amNames = Object.keys(ams);
                    
                    let pCount = 0;
                    let tcCount = 0;
                    let ctCount = 0;

                    amNames.forEach(am => {
                        ntbUniqueAMs.add(am.trim());
                        ams[am].forEach(name => {
                            const trimmedName = name.trim();
                            const nameLower = trimmedName.toLowerCase();
                            if (isWarehouse(trimmedName)) {
                                if (nameLower.includes('trung chuyển') || nameLower.includes('trung chuyen') || nameLower.includes('transit')) {
                                    tcCount++;
                                    ntbTotalKTC++;
                                } else {
                                    ctCount++;
                                    ntbTotalKCT++;
                                }
                            } else {
                                pCount++;
                                ntbTotalPOs++;
                            }
                        });
                    });

                    window.provinceStats[normProv] = {
                        ams: amNames.length,
                        pos: pCount,
                        transitHubs: tcCount,
                        subHubs: ctCount,
                        region: provinceRegions[normProv] || "Khu vực"
                    };

                    // Update corresponding card footer stats
                    const cardStatsDiv = document.querySelector(`.prov-card-stats[data-province="${normProv}"]`);
                    if (cardStatsDiv) {
                        cardStatsDiv.innerHTML = `
                            <span><i class="fa-solid fa-user-tie"></i> <strong>${amNames.length}</strong> AM</span>
                            <span><i class="fa-solid fa-home"></i> <strong>${pCount}</strong> Bưu cục</span>
                            <span><i class="fa-solid fa-warehouse" style="color: #10b981;"></i> <strong>${ctCount}</strong> Kho CT</span>
                            <span><i class="fa-solid fa-star" style="color: var(--color-ghn-blue);"></i> <strong>${tcCount}</strong> Kho TC</span>
                        `;
                    }
                }

                // Update Hero Banner stats elements
                document.getElementById('ntb-total-ams').innerText = ntbUniqueAMs.size;
                document.getElementById('ntb-total-pos').innerText = ntbTotalPOs;
                document.getElementById('ntb-total-ktc').innerText = ntbTotalKTC;
                document.getElementById('ntb-total-kct').innerText = ntbTotalKCT;

                let html = '';
                
                // Add the Regional Director node at the very top of the tree, styled like a family tree root
                html += `
                <div class="tree-root-leader-node" style="margin-bottom: 15px;">
                    <div class="leader-node-header" style="display: inline-flex; align-items: center; padding: 12px 18px; background: #ffffff; border: 2px solid var(--color-ghn-orange); border-radius: 12px; box-shadow: 0 4px 12px rgba(255, 95, 0, 0.08); min-width: 240px; gap: 12px;">
                        <i class="fa-solid fa-user-tie" style="color: var(--color-ghn-orange); font-size: 18px; background: rgba(255, 95, 0, 0.08); padding: 8px; border-radius: 50%;"></i>
                        <div style="text-align: left;">
                            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Giám đốc vùng</div>
                            <div style="font-size: 14px; font-weight: 700; color: var(--text-primary);">Trần Ngọc Trung</div>
                        </div>
                    </div>
                    <div class="tree-children expanded" style="display: flex; margin-left: 24px; border-left: 2px dashed rgba(255, 95, 0, 0.25); padding-left: 18px; margin-top: 8px; flex-direction: column; gap: 10px;">
                `;

                const provinces = Object.keys(structure).sort();

                provinces.forEach(prov => {
                    const ams = structure[prov];

                    // Separate warehouses into Transit Hubs and Sub Hubs
                    const provTransitHubs = [];
                    const provSubHubs = [];

                    const amNames = Object.keys(ams).sort();
                    amNames.forEach(am => {
                        ams[am].forEach(name => {
                            const trimmedName = name.trim();
                            const nameLower = trimmedName.toLowerCase();
                            if (isWarehouse(trimmedName)) {
                                const isTransit = nameLower.includes('trung chuyển') || nameLower.includes('trung chuyen') || nameLower.includes('transit');
                                if (isTransit) {
                                    provTransitHubs.push({ name: trimmedName, am });
                                } else {
                                    provSubHubs.push({ name: trimmedName, am });
                                }
                            }
                        });
                    });

                    html += `
                    <div class="tree-node-item">
                        <div class="tree-header" onclick="toggleTreeNode(this)">
                            <span>
                                <i class="fa-solid fa-map-location-dot" style="color: var(--color-ghn-orange); margin-right: 8px;"></i>
                                ${escapeHTML(prov)}
                            </span>
                            <i class="fa-solid fa-chevron-right toggle-icon"></i>
                        </div>
                        <div class="tree-children">
                    `;

                    // --- Transit Hubs section ---
                    if (provTransitHubs.length > 0) {
                        html += `
                            <div class="tree-warehouse-group" style="margin-bottom: 8px; padding: 8px 10px; background: rgba(0,123,195,0.05); border: 1px solid rgba(0,123,195,0.15); border-radius: 8px; border-left: 3px solid var(--color-ghn-blue); position: relative;">
                                <div style="font-size: 11px; font-weight: 700; color: var(--color-ghn-blue); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.4px;">
                                    <i class="fa-solid fa-star" style="margin-right: 5px;"></i> Kho Trung Chuyển (${provTransitHubs.length})
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 4px;">
                          `;
                        provTransitHubs.forEach(wh => {
                            html += `
                                    <div style="display:flex; align-items:center; gap:8px; padding: 5px 8px; background:#fff; border-radius:6px; border:1px solid rgba(226,232,240,0.7);">
                                        <i class="fa-solid fa-star" style="color:var(--color-ghn-blue); font-size:11px; flex-shrink:0;"></i>
                                        <span style="font-size:12px; color: var(--text-primary); font-weight:500; flex:1;">${escapeHTML(wh.name)} <span style="font-size:11px; color: var(--text-muted); font-weight:400; font-style:italic;">(AM: ${escapeHTML(wh.am)})</span></span>
                                        <span style="font-size:10px; background:rgba(0,123,195,0.1); color:var(--color-ghn-blue); padding:2px 6px; border-radius:4px; font-weight:600; white-space:nowrap;">Transit Hub</span>
                                    </div>
                            `;
                        });
                        html += `
                                </div>
                            </div>
                        `;
                    }

                    // --- Sub Hubs section ---
                    if (provSubHubs.length > 0) {
                        html += `
                            <div class="tree-warehouse-group" style="margin-bottom: 8px; padding: 8px 10px; background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.15); border-radius: 8px; border-left: 3px solid #10b981; position: relative;">
                                <div style="font-size: 11px; font-weight: 700; color: #10b981; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.4px;">
                                    <i class="fa-solid fa-diamond" style="margin-right: 5px;"></i> Kho Chuyển Tiếp (${provSubHubs.length})
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 4px;">
                        `;
                        provSubHubs.forEach(wh => {
                            html += `
                                    <div style="display:flex; align-items:center; gap:8px; padding: 5px 8px; background:#fff; border-radius:6px; border:1px solid rgba(226,232,240,0.7);">
                                        <i class="fa-solid fa-diamond" style="color:#10b981; font-size:11px; flex-shrink:0;"></i>
                                        <span style="font-size:12px; color: var(--text-primary); font-weight:500; flex:1;">${escapeHTML(wh.name)} <span style="font-size:11px; color: var(--text-muted); font-weight:400; font-style:italic;">(AM: ${escapeHTML(wh.am)})</span></span>
                                        <span style="font-size:10px; background:rgba(16,185,129,0.1); color:#10b981; padding:2px 6px; border-radius:4px; font-weight:600; white-space:nowrap;">Chuyển Tiếp</span>
                                    </div>
                            `;
                        });
                        html += `
                                </div>
                            </div>
                        `;
                    }

                    // --- AM + Post Offices section ---
                    amNames.forEach(am => {
                        const allItems = ams[am];
                        const pos = allItems.filter(p => !isWarehouse(p.trim()));
                        if (pos.length === 0) return; // Skip AM if only has warehouses

                        html += `
                            <div class="am-node-item">
                                <div class="am-header" onclick="toggleTreeNode(this)">
                                    <span>
                                        <i class="fa-solid fa-user-tie" style="color: var(--color-ghn-blue); margin-right: 6px;"></i>
                                        ${escapeHTML(am)} <span style="font-size:11px; color:var(--text-muted); font-weight:400;">(${pos.length} bưu cục)</span>
                                    </span>
                                    <i class="fa-solid fa-chevron-right toggle-icon"></i>
                                </div>
                                <div class="am-children">
                        `;
                        pos.forEach(po => {
                            html += `
                                    <div class="po-leaf" data-po-name="${escapeHTML(po.trim())}">
                                        <span>${escapeHTML(po.trim())}</span>
                                    </div>
                            `;
                        });
                        html += `
                                </div>
                            </div>
                        `;
                    });

                    html += `
                        </div>
                    </div>
                    `;
                });

                // Close the tree-children container and the tree-root-leader-node container
                if (html) {
                    html += `
                        </div>
                    </div>
                    `;
                }

                root.innerHTML = html || `<div style="color: var(--text-muted); text-align: center; padding: 20px;">Không có dữ liệu cơ cấu NTB.</div>`;

                // Initialize Leaflet map with structure data
                initNTBLeafletMap(structure);

            } catch (err) {
                console.error("Lỗi khi tải cơ cấu NTB:", err);
                root.innerHTML = `<div style="color: var(--color-danger); text-align: center; padding: 20px;">
                    <i class="fa-solid fa-triangle-exclamation" style="margin-right: 8px;"></i> Lỗi tải dữ liệu. Vui lòng kiểm tra file co_cau_ntb.xlsx
                </div>`;
            }
        }

        function toggleTreeNode(element) {
            element.classList.toggle('expanded');
            const children = element.nextElementSibling;
            if (children) {
                children.classList.toggle('expanded');
            }
        }

        // =========================================================
        // LEAFLET MAP for NTB Introduction Tab
        // =========================================================
        let _ntbMap = null;
        let _ntbMapMarkers = [];

        function initNTBLeafletMap(structure) {
            const mapDiv = document.getElementById('ntb-leaflet-map');
            if (!mapDiv) return;

            // Initialize map only once
            if (!_ntbMap) {
                const bounds = L.latLngBounds([8.0, 100.0], [24.0, 112.0]);
                _ntbMap = L.map('ntb-leaflet-map', {
                    center: [12.2, 108.2],
                    zoom: 7,
                    minZoom: 6,
                    maxZoom: 12,
                    zoomControl: true,
                    attributionControl: false, // Turn off default Leaflet attribution text
                    scrollWheelZoom: false,
                    maxBounds: bounds,
                    maxBoundsViscosity: 1.0
                });

                // Draw simplified but geographically accurate Vietnam borders in the background
                if (typeof VIETNAM_BORDER_50 !== 'undefined') {
                    VIETNAM_BORDER_50.forEach(coords => {
                        L.polygon(coords, {
                            color: '#cbd5e1', // border color (slate-300)
                            weight: 1.5,
                            fillColor: '#ffffff', // clean white landmass
                            fillOpacity: 1.0,
                            interactive: false
                        }).addTo(_ntbMap);
                    });
                }

                // Draw all other provinces of Vietnam in the background as faint outlines (bản đồ thể hiện mờ mờ các tỉnh khác)
                if (typeof VIETNAM_PROVINCES_SIMPLIFIED !== 'undefined') {
                    const ntbNames = ["Đắk Nông", "Lâm Đồng", "Khánh Hòa", "Ninh Thuận", "Bình Thuận"];
                    
                    // Helper to generate a soft pastel color based on province name hash
                    function getPastelColor(str) {
                        const colors = [
                            '#ffe5d9', '#ffcad4', '#b3e5fc', '#c8e6c9', '#ffcc80',
                            '#d1c4e9', '#ffecb3', '#d7ccc8', '#cfd8dc', '#e0f2f1',
                            '#ffead2', '#ffe5ec', '#d8e2dc', '#ece4db', '#e8e8e4',
                            '#ffd7ba', '#fec5bb', '#e2e2e2', '#e0f2fe', '#e0e7ff',
                            '#fae8ff', '#f3e8ff', '#dcfce7', '#fef9c3', '#ffedd5',
                            '#fee2e2', '#ccfbf1'
                        ];
                        let hash = 0;
                        for (let i = 0; i < str.length; i++) {
                            hash = str.charCodeAt(i) + ((hash << 5) - hash);
                        }
                        const index = Math.abs(hash) % colors.length;
                        return colors[index];
                    }

                    VIETNAM_PROVINCES_SIMPLIFIED.forEach(prov => {
                        const normName = prov.name.replace('Khánh Hoà', 'Khánh Hòa').trim();
                        if (ntbNames.includes(normName)) {
                            return; // Skip drawing NTB provinces here, they are drawn in the colorful section
                        }
                        const pColor = getPastelColor(normName);
                        prov.rings.forEach(ring => {
                            L.polygon(ring, {
                                color: '#e2e8f0', // soft border (slate-200)
                                weight: 0.6,
                                fillColor: pColor, // faint pastel background
                                fillOpacity: 0.65,
                                interactive: false
                            }).addTo(_ntbMap);
                        });
                    });
                }

                // Draw simplified but geographically accurate province outlines
                const provincePolygons = {
                    "Đắk Nông": {
                        latlngs: [[12.68,107.15],[12.62,107.48],[12.50,107.72],[12.38,108.05],[12.18,108.18],[11.95,108.12],[11.72,107.90],[11.55,107.60],[11.60,107.30],[11.85,107.12],[12.18,107.10]],
                        color: '#b58a05',
                        fillColor: '#ffd166',
                        fillOpacity: 0.55
                    },
                    "Lâm Đồng": {
                        latlngs: [[12.38,107.70],[12.45,107.90],[12.42,108.15],[12.28,108.45],[12.08,108.75],[11.85,108.88],[11.62,108.82],[11.38,108.62],[11.18,108.30],[11.12,108.05],[11.35,107.80],[11.62,107.60],[11.92,107.52],[12.18,107.52]],
                        color: '#d9534f',
                        fillColor: '#ffadad',
                        fillOpacity: 0.55
                    },
                    "Khánh Hòa": {
                        latlngs: [[13.02,109.22],[12.88,109.40],[12.68,109.45],[12.50,109.35],[12.32,109.22],[12.12,109.05],[11.98,108.78],[11.88,108.55],[12.08,108.45],[12.28,108.45],[12.55,108.62],[12.78,108.80],[12.92,109.00]],
                        color: '#0288d1',
                        fillColor: '#90e0ef',
                        fillOpacity: 0.55
                    },
                    "Ninh Thuận": {
                        latlngs: [[12.08,108.45],[12.12,109.05],[12.32,109.22],[12.22,109.30],[12.02,109.28],[11.72,109.18],[11.45,109.00],[11.22,108.82],[11.25,108.58],[11.42,108.42],[11.65,108.40],[11.88,108.55],[11.98,108.78]],
                        color: '#388e3c',
                        fillColor: '#a7c957',
                        fillOpacity: 0.55
                    },
                    "Bình Thuận": {
                        latlngs: [[11.42,107.42],[11.62,107.60],[11.85,107.72],[12.05,107.95],[11.95,108.10],[11.72,108.22],[11.45,108.42],[11.22,108.58],[11.05,108.70],[10.88,108.50],[10.68,108.25],[10.52,108.05],[10.48,107.75],[10.55,107.50],[10.75,107.32],[11.05,107.25],[11.28,107.32]],
                        color: '#7b1fa2',
                        fillColor: '#e8dbfc',
                        fillOpacity: 0.55
                    }
                };

                // Coordinates for static text labels for the 5 provinces (offset to avoid overlapping with PO points)
                const labelCenters = {
                    "Đắk Nông": [12.30, 107.45],
                    "Lâm Đồng": [11.95, 108.05],
                    "Khánh Hòa": [12.65, 109.00],
                    "Ninh Thuận": [11.52, 108.75],
                    "Bình Thuận": [10.82, 107.70]
                };

                Object.entries(provincePolygons).forEach(([name, data]) => {
                    const poly = L.polygon(data.latlngs, {
                        color: data.color,
                        weight: 2,
                        fillColor: data.fillColor || data.color,
                        fillOpacity: data.fillOpacity || 0.55,
                        opacity: 0.8
                    }).addTo(_ntbMap);

                    poly.bindTooltip(`<strong>${name}</strong>`, {
                        permanent: false,
                        sticky: true,
                        className: 'leaflet-province-tooltip'
                    });

                    // Add dynamic hover effect to make regions interactive and friendly
                    poly.on('mouseover', () => {
                        poly.setStyle({
                            fillOpacity: 0.75,
                            weight: 3
                        });
                    });
                    poly.on('mouseout', () => {
                        poly.setStyle({
                            fillOpacity: data.fillOpacity || 0.55,
                            weight: 2
                        });
                    });

                    // Add a permanent, beautiful text label directly on the map for each province
                    if (labelCenters[name]) {
                        const labelHtml = `<div class="province-map-label" style="border-color: ${data.color}; color: ${data.color === '#7b1fa2' ? '#6b1f92' : data.color}; font-weight: 800;">${name}</div>`;
                        const labelIcon = L.divIcon({
                            className: 'leaflet-label-container',
                            html: labelHtml,
                            iconSize: [100, 24],
                            iconAnchor: [50, 12]
                        });
                        L.marker(labelCenters[name], {
                            icon: labelIcon,
                            interactive: true
                        }).addTo(_ntbMap).on('click', () => {
                            // Click label -> highlight province in tree
                            const treeHeaders = document.querySelectorAll('.tree-header');
                            treeHeaders.forEach(h => {
                                if (h.innerText.includes(name)) {
                                    if (!h.classList.contains('expanded')) h.click();
                                    h.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                    h.style.backgroundColor = 'rgba(255,95,0,0.08)';
                                    setTimeout(() => h.style.backgroundColor = '', 1500);
                                }
                            });
                        });
                    }

                    // Click province → highlight in org tree
                    poly.on('click', () => {
                        const treeHeaders = document.querySelectorAll('.tree-header');
                        treeHeaders.forEach(h => {
                            if (h.innerText.includes(name)) {
                                if (!h.classList.contains('expanded')) h.click();
                                h.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                h.style.backgroundColor = 'rgba(255,95,0,0.08)';
                                setTimeout(() => h.style.backgroundColor = '', 1500);
                            }
                        });
                    });
                });
            }

            // Clear old markers
            _ntbMapMarkers.forEach(m => _ntbMap.removeLayer(m));
            _ntbMapMarkers = [];

            // Province scatter centers for post offices
            const pCenters = {
                "Đắk Nông":   { lat: 12.05, lng: 107.72, lS: 0.32, gS: 0.28 },
                "Lâm Đồng":   { lat: 11.78, lng: 108.22, lS: 0.42, gS: 0.38 },
                "Khánh Hòa":  { lat: 12.35, lng: 109.00, lS: 0.32, gS: 0.14 },
                "Ninh Thuận": { lat: 11.68, lng: 108.88, lS: 0.22, gS: 0.18 },
                "Bình Thuận": { lat: 11.00, lng: 107.92, lS: 0.32, gS: 0.32 }
            };

            // Known warehouse lat/lng (approximate real coordinates)
            const whCoords = {
                "Kho Trung Chuyển Khánh Hòa": [12.245, 109.195],
                "Kho Chuyển Tiếp Bình Thuận":  [10.932, 108.100],
                "Kho Chuyển Tiếp Đắk Nông":    [12.002, 107.698],
                "Kho Chuyển Tiếp Lâm Đồng":    [11.940, 108.443],
                "Kho Chuyển Tiếp Bảo Lộc":     [11.548, 107.812]
            };

            const WAREHOUSE_KEYWORDS = ['kho trung chuy', 'kho chuy', 'kho tc', 'transit hub'];
            function isWH(name) {
                return WAREHOUSE_KEYWORDS.some(kw => name.toLowerCase().includes(kw));
            }

            for (const [prov, ams] of Object.entries(structure)) {
                const normProv = prov.replace('Khánh Hoà','Khánh Hòa').trim();
                const center = pCenters[normProv];
                if (!center) continue;

                const list = [];
                for (const [am, items] of Object.entries(ams)) {
                    items.forEach(name => list.push({ name: name.trim(), am, province: normProv }));
                }

                const warehouses  = list.filter(i => isWH(i.name));
                const postOffices = list.filter(i => !isWH(i.name));

                // Render warehouses
                warehouses.forEach(wh => {
                    const isTransit = wh.name.toLowerCase().includes('trung chuy');
                    const coords = whCoords[wh.name];
                    if (!coords) return;

                    const iconHtml = isTransit
                        ? `<div class="leaflet-wh-transit">★</div>`
                        : `<div class="leaflet-wh-sub">◆</div>`;

                    const icon = L.divIcon({
                        className: '',
                        html: iconHtml,
                        iconSize: isTransit ? [26,26] : [22,22],
                        iconAnchor: isTransit ? [13,13] : [11,11]
                    });

                    const marker = L.marker(coords, { icon, zIndexOffset: 1000 }).addTo(_ntbMap);
                    const typeLabel = isTransit ? 'Kho Trung Chuyển (Transit Hub)' : 'Kho Chuyển Tiếp (Sub-hub)';
                    marker.bindTooltip(
                        `<div style="font-weight:700;color:${isTransit ? '#007bc3' : '#10b981'};margin-bottom:4px;">${wh.name}</div>
                         <div>• Loại: <strong>${typeLabel}</strong></div>
                         <div>• Tỉnh: ${wh.province}</div>
                         <div>• AM: ${wh.am}</div>`,
                        { className: 'leaflet-marker-tooltip', sticky: true }
                    );
                    marker.on('click', () => highlightTreeNodeAndScroll(wh.name, wh.am, wh.province));
                    _ntbMapMarkers.push(marker);
                });

                // Render post office dots using golden spiral
                const N = postOffices.length;
                postOffices.forEach((po, i) => {
                    const angle = i * 137.5 * Math.PI / 180;
                    const r = Math.sqrt((i + 1) / (N + 1));
                    const lat = center.lat + r * center.lS * Math.sin(angle);
                    const lng = center.lng + r * center.gS * Math.cos(angle);

                    const icon = L.divIcon({
                        className: '',
                        html: `<div class="leaflet-po-dot"></div>`,
                        iconSize: [10,10],
                        iconAnchor: [5,5]
                    });

                    const marker = L.marker([lat, lng], { icon }).addTo(_ntbMap);
                    marker.bindTooltip(
                        `<div style="font-weight:700;color:var(--color-ghn-orange);margin-bottom:4px;">${po.name}</div>
                         <div>• Loại: <strong>Bưu cục GHN</strong></div>
                         <div>• Tỉnh: ${po.province}</div>
                         <div>• AM: ${po.am}</div>`,
                        { className: 'leaflet-marker-tooltip', sticky: true }
                    );
                    marker.on('click', () => highlightTreeNodeAndScroll(po.name, po.am, po.province));
                    _ntbMapMarkers.push(marker);
                });
            }

            // Ensure map renders correctly after tab switch
            setTimeout(() => _ntbMap.invalidateSize(), 200);
        }




        // Shared helper to highlight tree node, select province filter, and scroll to it
        function highlightTreeNodeAndScroll(poName, amName, provName) {
            // Select province in global filter and apply filter
            const filterProv = document.getElementById('filter-province');
            if (filterProv) {
                // Find matching option
                let matched = false;
                for (let i = 0; i < filterProv.options.length; i++) {
                    if (filterProv.options[i].text.includes(provName)) {
                        filterProv.selectedIndex = i;
                        matched = true;
                        break;
                    }
                }
                if (matched) {
                    applyFilters();
                }
            }

            // Expand province node in Org tree
            const treeHeaders = document.querySelectorAll('.tree-header');
            let matchedHeader = null;
            treeHeaders.forEach(header => {
                if (header.innerText.includes(provName)) {
                    matchedHeader = header;
                    if (!header.classList.contains('expanded')) {
                        header.click();
                    }
                }
            });

            // Expand AM node
            setTimeout(() => {
                const amHeaders = document.querySelectorAll('.am-header');
                let matchedAmHeader = null;
                amHeaders.forEach(amHeader => {
                    if (amHeader.innerText.includes(amName)) {
                        matchedAmHeader = amHeader;
                        if (!amHeader.classList.contains('expanded')) {
                            amHeader.click();
                        }
                    }
                });

                // Highlight leaf node
                setTimeout(() => {
                    const leaves = document.querySelectorAll('.po-leaf');
                    leaves.forEach(leaf => {
                        const lName = leaf.getAttribute('data-po-name') || leaf.innerText;
                        if (lName.includes(poName)) {
                            leaf.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            
                            // Highlight node
                            leaf.style.backgroundColor = 'rgba(255, 95, 0, 0.15)';
                            leaf.style.borderColor = 'var(--color-ghn-orange)';
                            leaf.style.fontWeight = 'bold';
                            
                            setTimeout(() => {
                                leaf.style.backgroundColor = '';
                                leaf.style.borderColor = '';
                                leaf.style.fontWeight = '';
                            }, 3000);
                        }
                    });
                }, 200);
            }, 200);
        }

        // Global province stats holding correct initial values (updated dynamically by loadNtbStructure)
        window.provinceStats = {
            "Lâm Đồng": { ams: 10, pos: 25, transitHubs: 0, subHubs: 2, region: "Tây Nguyên" },
            "Khánh Hòa": { ams: 7, pos: 21, transitHubs: 1, subHubs: 0, region: "Duyên hải" },
            "Đắk Nông": { ams: 5, pos: 16, transitHubs: 0, subHubs: 1, region: "Tây Nguyên" },
            "Bình Thuận": { ams: 4, pos: 17, transitHubs: 0, subHubs: 1, region: "Duyên hải" },
            "Ninh Thuận": { ams: 1, pos: 6, transitHubs: 0, subHubs: 0, region: "Duyên hải" }
        };

        // Interactive SVG Map hover, tooltip and click link logic
        document.addEventListener('DOMContentLoaded', () => {
            const mapPaths = document.querySelectorAll('.map-province');
            const tooltip = document.getElementById('map-tooltip');
            
            mapPaths.forEach(path => {
                const provName = path.getAttribute('data-province');
                
                path.addEventListener('mousemove', (e) => {
                    const stats = window.provinceStats[provName];
                    if (stats) {
                        tooltip.style.display = 'block';
                        tooltip.innerHTML = `
                            <div style="font-weight: 700; color: #ff5f00; margin-bottom: 4px;">${provName} (${stats.region})</div>
                            <div style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">
                                <strong>• AM quản lý:</strong> ${stats.ams}<br>
                                <strong>• Bưu cục:</strong> ${stats.pos}<br>
                                <strong>• Kho Chuyển Tiếp (CT):</strong> ${stats.subHubs || 0}<br>
                                <strong>• Kho Trung Chuyển (TC):</strong> ${stats.transitHubs || 0}
                            </div>
                        `;
                        const rect = e.target.ownerSVGElement.getBoundingClientRect();
                        const x = e.clientX - rect.left + 15;
                        const y = e.clientY - rect.top + 15;
                        tooltip.style.left = x + 'px';
                        tooltip.style.top = y + 'px';
                    }
                });

                path.addEventListener('mouseleave', () => {
                    tooltip.style.display = 'none';
                    document.querySelectorAll('.province-card').forEach(c => {
                        c.style.transform = 'none';
                        c.style.boxShadow = 'none';
                    });
                });

                path.addEventListener('mouseenter', () => {
                    const cards = document.querySelectorAll('.province-card');
                    cards.forEach(card => {
                        const title = card.querySelector('h4').innerText;
                        if (title.includes(provName)) {
                            card.style.transform = 'translateY(-4px)';
                            card.style.boxShadow = '0 10px 15px -3px rgba(0,0,0,0.1)';
                        }
                    });
                });

                path.addEventListener('click', () => {
                    // Filter by province globally
                    const filterProv = document.getElementById('filter-province');
                    if (filterProv) {
                        let matched = false;
                        for (let i = 0; i < filterProv.options.length; i++) {
                            if (filterProv.options[i].text.includes(provName)) {
                                filterProv.selectedIndex = i;
                                matched = true;
                                break;
                            }
                        }
                        if (matched) {
                            applyFilters();
                        }
                    }

                    // Highlight & Expand Org Tree Header
                    const treeHeaders = document.querySelectorAll('.tree-header');
                    treeHeaders.forEach(header => {
                        if (header.innerText.includes(provName)) {
                            if (!header.classList.contains('expanded')) {
                                header.click();
                            }
                            header.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            header.style.backgroundColor = 'rgba(255, 95, 0, 0.08)';
                            setTimeout(() => {
                                header.style.backgroundColor = '';
                            }, 1500);
                        }
                    });

                    // Scroll to card
                    const cards = document.querySelectorAll('.province-card');
                    cards.forEach(card => {
                        const title = card.querySelector('h4').innerText;
                        if (title.includes(provName)) {
                            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            card.style.borderColor = 'var(--color-ghn-orange)';
                            card.style.boxShadow = '0 10px 20px rgba(255,95,0,0.15)';
                            setTimeout(() => {
                                card.style.borderColor = '';
                                card.style.boxShadow = '';
                            }, 2000);
                        }
                    });
                });
            });
        });

        // ==========================================
        // RENDER: NHÂN SỰ & SCENARIO PLANNER (TAB)
        // ==========================================
        let nhanSuData = null;
        window.rowGrowthOverrides = window.rowGrowthOverrides || {};

        function formatNumber(val) {
            return (val || 0).toLocaleString();
        }

        async function loadNhanSuData() {
            const tbody = document.getElementById('table-nhan-su-body');
            try {
                const res = await fetch(getApiUrl('/api/nhan-su'), getFetchOptions());
                if (!res.ok) {
                    throw new Error("Lỗi tải API nhân sự");
                }
                const data = await res.json();
                nhanSuData = data;
                
                // Populate cards
                document.getElementById('ns-card-active').innerText = formatNumber(data.active_headcount || 0);
                document.getElementById('ns-card-resigned').innerText = formatNumber(data.resigned_headcount || 0);
                document.getElementById('ns-card-po').innerText = formatNumber(data.po_count || 0);

                // Render table
                renderNhanSuTable();
            } catch (err) {
                console.error("Lỗi khi load dữ liệu nhân sự: ", err);
                if (tbody) {
                    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--color-danger); padding: 32px;"><i class="fa-solid fa-circle-exclamation"></i> Không thể tải dữ liệu: ${err.message}</td></tr>`;
                }
            }
        }

        function renderNhanSuTable() {
            const tbody = document.getElementById('table-nhan-su-body');
            if (!tbody || !nhanSuData || !nhanSuData.pos) return;

            const query = document.getElementById('ns-search-input').value.toLowerCase().trim();
            const targetDaily = parseFloat(document.getElementById('ns-input-target-daily').value) || 70;
            const globalGrowth = parseFloat(document.getElementById('ns-input-global-growth').value) || 10;

            const filtered = nhanSuData.pos.filter(p => {
                return (p.name || '').toLowerCase().includes(query) ||
                       (p.province || '').toLowerCase().includes(query) ||
                       (p.am || '').toLowerCase().includes(query) ||
                       (p.warehouse_id || '').toLowerCase().includes(query);
            });

            let html = '';
            let totalHc = 0;
            let totalVol2025 = 0;
            let totalVol2026 = 0;
            let totalHcNeeded = 0;

            filtered.forEach(p => {
                const hc = p.hc_current || 0;
                const vol2025 = p.vol_2025 || 0;
                
                let growth = globalGrowth;
                if (window.rowGrowthOverrides[p.warehouse_id] !== undefined) {
                    growth = window.rowGrowthOverrides[p.warehouse_id];
                }

                const vol2026 = Math.round(vol2025 * (1 + growth / 100));
                const hcNeeded = Math.ceil(vol2026 / targetDaily);
                const diff = hcNeeded - hc;

                let diffBadge = '';
                if (diff > 0) {
                    diffBadge = `<span class="badge" style="background-color: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">+${diff} cần tuyển</span>`;
                } else {
                    diffBadge = `<span class="badge" style="background-color: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">Đủ định biên</span>`;
                }

                html += `
                    <tr>
                        <td style="font-weight: 600; color: var(--text-primary);">${p.name}</td>
                        <td>${p.province}</td>
                        <td>${p.am || '-'}</td>
                        <td>${formatNumber(hc)}</td>
                        <td>${formatNumber(vol2025)}</td>
                        <td>
                            <input type="number" value="${growth}" 
                                   style="width: 70px; padding: 4px 8px; border: 1px solid var(--border-color); border-radius: 4px; text-align: right;" 
                                   oninput="window.updateRowGrowth('${p.warehouse_id}', this.value)">
                        </td>
                        <td>${formatNumber(vol2026)}</td>
                        <td>${formatNumber(hcNeeded)}</td>
                        <td>${diffBadge}</td>
                    </tr>
                `;

                totalHc += hc;
                totalVol2025 += vol2025;
                totalVol2026 += vol2026;
                totalHcNeeded += hcNeeded;
            });

            tbody.innerHTML = html;

            // Update grand totals
            const totalDiff = totalHcNeeded - totalHc;
            let totalDiffBadge = '';
            if (totalDiff > 0) {
                totalDiffBadge = `<span class="badge" style="background-color: #fee2e2; color: #991b1b; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 700;">+${totalDiff} cần tuyển</span>`;
            } else {
                totalDiffBadge = `<span class="badge" style="background-color: #dcfce7; color: #166534; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 700;">Đủ định biên</span>`;
            }

            document.getElementById('ns-total-hc').innerText = formatNumber(totalHc);
            document.getElementById('ns-total-vol2025').innerText = formatNumber(totalVol2025);
            document.getElementById('ns-total-vol2026').innerText = formatNumber(totalVol2026);
            document.getElementById('ns-total-hc-needed').innerText = formatNumber(totalHcNeeded);
            document.getElementById('ns-total-growth').innerText = globalGrowth + '%';
            document.getElementById('ns-total-diff').innerHTML = totalDiffBadge;
        }

        window.updateRowGrowth = function(whId, val) {
            const parsedVal = parseFloat(val);
            window.rowGrowthOverrides[whId] = isNaN(parsedVal) ? 0 : parsedVal;
            renderNhanSuTable();
        }
    