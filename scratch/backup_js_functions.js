=== sendTelegramAiBriefing ===
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

        

=== sendTelegramWarning ===
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

        

=== NHAN SU JS ===
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
    

