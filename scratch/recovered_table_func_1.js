function renderNtbAnalysisTable(type) {
            const tableBody = document.getElementById(`tbody-ntb-${type}-analysis`);
            if (!tableBody) return;
            
            if (!cachedNtbMatrixData || !cachedNtbMatrixData[type]) {
                tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có dữ liệu</td></tr>`;
                return;
            }
            
            const matrix = cachedNtbMatrixData[type];
            const timeGroupEl = document.getElementById('ntb-time-group');
            const timeGroup = timeGroupEl ? timeGroupEl.value : 'ngay';
            
            let targetDate = cachedNtbSummaryData ? cachedNtbSummaryData.latest_date : null;
            let targetDateKey = targetDate;
            if (targetDateKey && timeGroup === 'tuan') {
                targetDateKey = targetDateKey.split(' ')[0];
            }
            
            if (!matrix.dates || matrix.dates.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có cấu hình ngày</td></tr>`;
                return;
            }
            
            let dateKey = targetDateKey;
            if (!matrix.dates.includes(dateKey)) {
                dateKey = matrix.dates[0];
            }
            
            const groupType = ntbGroupType[type];
        
<truncated 8647 bytes>

================================================================================



=========================================
FILE: 92726133-7314-4954-9f94-c885d0c26df2_1171.txt
=========================================
--- STEP 1171 | Tool: replace_file_content ---
Description: "Modify switchNtbRegion to trigger re-rendering of LTC and GTC analysis tables on region capsule change"
Instruction: "Call renderNtbAnalysisTable for both ltc and gtc inside switchNtbRegion"
--- TARGET CONTENT ---
"        function switchNtbRegion(regionKey, btnEl) {
            activeNtbRegion = regionKey;
            
            // Toggle active state in UI
            document.querySelectorAll('#ntb-region-capsules .capsule-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            if (btnEl) {
                btnEl.classList.add('active');
            }
            
            // Re-render KPI cards instantly from cache
            renderNtbKpiCards();
        }"
--- REPLACEMENT CONTENT ---
"        function switchNtbRegion(regionKey, btnEl) {
            activeNtbRegion = regionKey;
            
            // Toggle active state in UI
            document.querySelectorAll('#ntb-region-capsules .capsule-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            if (btnEl) {
                btnEl.classList.add('active');
            }
            
            // Re-render KPI cards instantly from cache
            renderNtbKpiCards();
            
            // Re-render analysis tables instantly from cache
            renderNtbAnalysisTable('ltc');
            renderNtbAnalysisTable('gtc');
        }"

================================================================================



=========================================
FILE: 92726133-7314-4954-9f94-c885d0c26df2_1177.txt
=========================================
--- STEP 1177 | Tool: replace_file_content ---
Description: "Add matchNtbRegion helper and filter rows by activeNtbRegion capsule in renderNtbAnalysisTable"
Instruction: "Define matchNtbRegion function and insert filter checks in both po and am groups in renderNtbAnalysisTable"
--- TARGET CONTENT ---
"        function renderNtbAnalysisTable(type) {
            const tableBody = document.getElementById(`tbody-ntb-${type}-analysis`);
            if (!tableBody) return;
            
            if (!cachedNtbMatrixData || !cachedNtbMatrixData[type]) {
                tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có dữ liệu</td></tr>`;
                return;
            }
            
            const matrix = cachedNtbMatrixData[type];
            const timeGroupEl = document.getElementById('ntb-time-group');
            const timeGroup = timeGroupEl ? timeGroupEl.value : 'ngay';
            
            let targetDate = cachedNtbSummaryData ? cachedNtbSummaryData.latest_date : null;
            let targetDateKey = targetDate;
            if (targetDateKey && timeGroup === 'tuan') {
                targetDateKey = targetDateKey.split(' ')[0];
            }
            
            if (!matrix.dates || matrix.dates.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có cấu hình ngày</td></tr>`;
                return;
            }
            
            let dateKey = targetDateKey;
            if (!matrix.dates.includes(dateKey)) {
                dateKey = matrix.dates[0];
            }
            
            const groupType = ntbGroupType[type];
            const searchText = (ntbSearchText[type] || '').toLowerCase().trim();
            const sortCol = ntbSortCol[type];
            const sortAsc = ntbSortAsc[type];
            
            let items = [];
            const target = type === 'ltc' ? 80 : 60;
            
            if (groupType === 'po') {
                const amTh = document.getElementById(`th-${type}-am-header`);
                if (amTh) amTh.style.display = '';
                
                matrix.rows.forEach(row => {
                    row.pos.forE
<truncated 2097 bytes>
--- REPLACEMENT CONTENT ---
"        function matchNtbRegion(amName, regionKey) {
            if (regionKey === 'overall') return true;
            const mapping = {
                'lam_dong': ['lâm đồng', 'lam dong'],
                'binh_thuan': ['bình thuận', 'binh thuan'],
                'khanh_hoa': ['khánh hòa', 'khanh hoa'],
                'dak_nong': ['đắk nông', 'dak nong'],
                'ninh_thuan': ['ninh thuận', 'ninh thuan']
            };
            const targets = mapping[regionKey];
            if (!targets) return true;
            const nameLower = amName.toLowerCase();
            return targets.some(target => nameLower.includes(target));
        }

        function renderNtbAnalysisTable(type) {
            const tableBody = document.getElementById(`tbody-ntb-${type}-analysis`);
            if (!tableBody) return;
            
            if (!cachedNtbMatrixData || !cachedNtbMatrixData[type]) {
                tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có dữ liệu</td></tr>`;
                return;
            }
            
            const matrix = cachedNtbMatrixData[type];
            const timeGroupEl = document.getElementById('ntb-time-group');
            const timeGroup = timeGroupEl ? timeGroupEl.value : 'ngay';
            
            let targetDate = cachedNtbSummaryData ? cachedNtbSummaryData.latest_date : null;
            let targetDateKey = targetDate;
            if (targetDateKey && timeGroup === 'tuan') {
                targetDateKey = targetDateKey.split(' ')[0];
            }
            
            if (!matrix.dates || matrix.dates.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có cấu hình ngày</td></tr>`;
                return;
            }
            
            let dateKey = targetDateKey;
            if (!matrix.dates.includes(dat
<truncated 2978 bytes>

================================================================================



=========================================
FILE: 92726133-7314-4954-9f94-c885d0c26df2_133.txt
=========================================
--- STEP 133 | Tool: replace_file_content ---
Description: "R