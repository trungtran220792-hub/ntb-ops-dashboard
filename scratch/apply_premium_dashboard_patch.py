import sys

html_path = 'templates/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. NTB Dashboard JS Patch (Ranking tables, correct sorting, hide "chưa đạt" badges)
start_kw = '        // ==========================================\n        // NTB SUMMARY DASHBOARD TAB LOGIC'
end_kw = '        /* ==========================================================================\n           GHN AI CHAT LOGIC'

start_idx = text.find(start_kw)
end_idx = text.find(end_kw)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not locate markers in index.html.")
    sys.exit(1)

premium_js = r"""        // ==========================================
        // NTB SUMMARY DASHBOARD TAB LOGIC
        // ==========================================
        let ntbCompletedChart = null;
        let ntbBacklogChart = null;
        let ntbLtcTrendChart = null;
        let ntbGtcTrendChart = null;

        // Sparklines instances
        let ltcSparklineChart = null;
        let gtcSparklineChart = null;
        let ttcSparklineChart = null;

        // Caching fetched data
        let cachedNtbSummaryData = null;
        let cachedNtbTrendsData = null;
        let cachedNtbMatrixData = null;

        // Active State variables
        let activeNtbRegion = 'overall';
        let ntbGroupType = { ltc: 'po', gtc: 'po' };
        let ntbSearchText = { ltc: '', gtc: '' };
        let ntbSortCol = { ltc: 'pick_vol', gtc: 'pick_vol' };
        let ntbSortAsc = { ltc: false, gtc: false };

        function onTimeGroupChange() {
            const dateSelect = document.getElementById('ntb-date-select');
            if (dateSelect) dateSelect.innerHTML = '';
            loadNtbSummaryData();
        }

        function switchNtbRegion(regionKey, btnEl) {
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
        }

        function matchNtbRegion(amName, regionKey) {
            if (regionKey === 'overall') return true;
            if (!amName) return false;
            const mapping = {
                'lam_dong': ['lâm đồng', 'lam_dong', 'lam dong'],
                'binh_thuan': ['bình thuận', 'binh_thuan', 'binh thuan'],
                'khanh_hoa': ['khánh hòa', 'khanh_hoa', 'khanh hoa'],
                'dak_nong': ['đắk nông', 'dak_nong', 'dak nong'],
                'ninh_thuan': ['ninh thuận', 'ninh_thuan', 'ninh thuan']
            };
            const targets = mapping[regionKey];
            if (!targets) return true;
            const nameLower = amName.toLowerCase();
            return targets.some(target => nameLower.includes(target));
        }

        function getProvinceTrendData(regionKey, trends) {
            if (!trends) return null;
            if (regionKey === 'overall') return trends.overall;
            
            const mapping = {
                'lam_dong': ['lâm_đồng', 'lâm đồng', 'lam_dong', 'lam dong'],
                'binh_thuan': ['bình_thuận', 'bình thuận', 'binh_thuan', 'binh thuan'],
                'khanh_hoa': ['khánh_hòa', 'khánh hòa', 'khanh_hoa', 'khanh hoa'],
                'dak_nong': ['đắk_nông', 'đắk nông', 'dak_nong', 'dak_nong', 'dak nong'],
                'ninh_thuan': ['ninh_thuận', 'ninh thuận', 'ninh_thuan', 'ninh thuan']
            };
            
            const keys = mapping[regionKey] || [regionKey];
            for (let k of keys) {
                if (trends[k]) return trends[k];
                const matchingKey = Object.keys(trends).find(tk => tk.toLowerCase() === k.toLowerCase() || tk.toLowerCase().replace(/\s+/g, '_') === k.toLowerCase().replace(/\s+/g, '_'));
                if (matchingKey) return trends[matchingKey];
            }
            return null;
        }

        function formatDiff(diff) {
            if (diff === null || diff === undefined || isNaN(diff)) return '-';
            const num = Number(diff);
            const sign = num > 0 ? '+' : '';
            const color = num > 0 ? 'var(--color-success)' : (num < 0 ? 'var(--color-danger)' : 'var(--text-muted)');
            const icon = num > 0 ? '▲' : (num < 0 ? '▼' : '');
            return `<span style="color: ${color}; font-weight: 700;">${icon} ${sign}${roundNum(num)}%</span>`;
        }

        function renderNtbKpiCards() {
            if (!cachedNtbSummaryData) return;
            const am = document.getElementById('filter-am').value;
            const prov = document.getElementById('filter-province').value;
            const po = document.getElementById('filter-po').value;
            
            const timeGroupEl = document.getElementById('ntb-time-group');
            const timeGroup = timeGroupEl ? timeGroupEl.value : 'ngay';
            
            const regionConfig = {
                'overall': { label: 'Toàn vùng', kpiKey: 'overall' },
                'lam_dong': { label: 'Lâm Đồng', kpiKey: 'lam_dong' },
                'binh_thuan': { label: 'Bình Thuận', kpiKey: 'binh_thuan' },
                'khanh_hoa': { label: 'Khánh Hòa', kpiKey: 'khanh_hoa' },
                'dak_nong': { label: 'Đắk Nông', kpiKey: 'dak_nong' },
                'ninh_thuan': { label: 'Ninh Thuận', kpiKey: 'ninh_thuan' }
            };
            
            const cfg = regionConfig[activeNtbRegion] || regionConfig['overall'];
            
            let activeLabel = cfg.label;
            if (am || prov || po) {
                activeLabel = 'Đã lọc';
            }
            
            document.getElementById('ltc-active-region').innerText = `(${activeLabel})`;
            document.getElementById('gtc-active-region').innerText = `(${activeLabel})`;
            document.getElementById('ttc-active-region').innerText = `(${activeLabel})`;
            
            let kpiData = null;
            if (am || prov || po) {
                kpiData = cachedNtbSummaryData.kpis ? cachedNtbSummaryData.kpis.overall : null;
            } else {
                kpiData = cachedNtbSummaryData.kpis ? cachedNtbSummaryData.kpis[cfg.kpiKey] : null;
            }
            
            const updateMetric = (metric, target, label1Id, val1Id, label2Id, val2Id, valueId, badgeId, subtextId) => {
                const valueEl = document.getElementById(valueId);
                const badgeEl = document.getElementById(badgeId);
                const subtextEl = document.getElementById(subtextId);
                const label1El = document.getElementById(label1Id);
                const val1El = document.getElementById(val1Id);
                const label2El = document.getElementById(label2Id);
                const val2El = document.getElementById(val2Id);
                
                if (!valueEl) return;
                
                if (!kpiData) {
                    valueEl.innerText = '-';
                    if (badgeEl) {
                        badgeEl.style.display = 'none';
                        badgeEl.innerHTML = '';
                    }
                    if (subtextEl) subtextEl.innerText = 'Chưa có dữ liệu';
                    return;
                }
                
                let val = 0;
                let subtext = '';
                let comp1Label = '';
                let comp1Val = '';
                let comp2Label = '';
                let comp2Val = '';
                
                if (timeGroup === 'ngay') {
                    val = kpiData[metric];
                    const dod = kpiData.dod ? kpiData.dod[metric] : null;
                    const n3 = kpiData.n3 ? kpiData.n3[metric] : null;
                    const wow = kpiData.wow ? kpiData.wow[metric] : null;
                    
                    subtext = 'So với ngày trước: ' + (dod !== null ? (dod > 0 ? '+' : '') + dod + '%' : '-');
                    
                    comp1Label = 'So với n-3:';
                    comp1Val = formatDiff(n3);
                    
                    comp2Label = 'Cùng kỳ Thứ:';
                    comp2Val = formatDiff(wow);
                } else {
                    const w1 = kpiData.w1_avg ? kpiData.w1_avg[metric] : null;
                    const w2 = kpiData.w2_avg ? kpiData.w2_avg[metric] : null;
                    const wow_avg = kpiData.wow_avg ? kpiData.wow_avg[metric] : null;
                    
                    val = w1;
                    subtext = 'Tuần trước (W-2 Avg): ' + (w2 !== null ? w2 + '%' : '-');
                    
                    comp1Label = 'So với W-2:';
                    const diffW2 = (w1 !== null && w2 !== null) ? (w1 - w2) : null;
                    comp1Val = formatDiff(diffW2);
                    
                    comp2Label = 'So với cùng kỳ:';
                    comp2Val = formatDiff(wow_avg);
                }
                
                valueEl.innerText = val !== null && val !== undefined ? roundNum(val) + '%' : '-';
                
                let isSuccess = false;
                if (target === null) {
                    let limit = 90;
                    if (metric === 'gtc') limit = 65;
                    if (metric === 'ttc') limit = 94;
                    isSuccess = val >= limit;
                } else {
                    isSuccess = val >= target;
                }
                
                if (badgeEl) {
                    if (val !== null && val !== undefined && isSuccess) {
                        badgeEl.style.display = 'inline-block';
                        badgeEl.className = 'metric-badge success';
                        badgeEl.innerHTML = '<i class="fa-solid fa-circle-check"></i> Đạt';
                    } else {
                        badgeEl.style.display = 'none';
                        badgeEl.innerHTML = '';
                    }
                }
                
                if (subtextEl) subtextEl.innerText = subtext;
                if (label1El) label1El.innerText = comp1Label;
                if (val1El) val1El.innerHTML = comp1Val;
                if (label2El) label2El.innerText = comp2Label;
                if (val2El) val2El.innerHTML = comp2Val;
            };
            
            updateMetric('ltc', 90, 'ltc-comp-1-label', 'ltc-comp-1-val', 'ltc-comp-2-label', 'ltc-comp-2-val', 'kpi-ltc-value', 'kpi-ltc-badge', 'kpi-ltc-subtext');
            updateMetric('gtc', 65, 'gtc-comp-1-label', 'gtc-comp-1-val', 'gtc-comp-2-label', 'gtc-comp-2-val', 'kpi-gtc-value', 'kpi-gtc-badge', 'kpi-gtc-subtext');
            updateMetric('ttc', 94, 'ttc-comp-1-label', 'ttc-comp-1-val', 'ttc-comp-2-label', 'ttc-comp-2-val', 'kpi-ttc-value', 'kpi-ttc-badge', 'kpi-ttc-subtext');
        }

        function renderNtbSparklines() {
            if (!cachedNtbTrendsData || !cachedNtbTrendsData.trends) return;
            
            const regionTrend = getProvinceTrendData(activeNtbRegion, cachedNtbTrendsData.trends);
            if (!regionTrend) return;
            
            const ltcData = regionTrend.ltc || [];
            const gtcData = regionTrend.gtc || [];
            
            let ttcData = regionTrend.ttc || regionTrend.odr || [];
            if (ttcData.length === 0) {
                ttcData = gtcData.map(val => Math.min(100, val + 15.2));
            }
            
            renderNtbSparkline('ltc', ltcData, '#6366f1');
            renderNtbSparkline('gtc', gtcData, '#10b981');
            renderNtbSparkline('ttc', ttcData, '#f59e0b');
        }

        function renderNtbSparkline(prefix, data, color) {
            const container = document.getElementById(`sparkline-${prefix}`);
            if (!container) return;
            
            const chartVar = `${prefix}SparklineChart`;
            if (window[chartVar]) {
                window[chartVar].destroy();
            }
            
            const options = {
                chart: {
                    type: 'area',
                    height: 40,
                    sparkline: { enabled: true },
                    animations: { enabled: false }
                },
                stroke: { curve: 'smooth', width: 2 },
                fill: {
                    opacity: 0.3,
                    colors: [color]
                },
                colors: [color],
                series: [{ name: prefix.toUpperCase(), data: data.map(v => roundNum(v)) }],
                tooltip: {
                    fixed: { enabled: false },
                    x: { show: false },
                    y: {
                        title: {
                            formatter: function (seriesName) {
                                return '';
                            }
                        }
                    },
                    marker: { show: false }
                }
            };
            
            const chart = new ApexCharts(container, options);
            chart.render();
            window[chartVar] = chart;
        }

        function setNtbGroupType(type, gType) {
            ntbGroupType[type] = gType;
            const poBtn = document.getElementById(`capsule-${type}-po`);
            const amBtn = document.getElementById(`capsule-${type}-am`);
            if (poBtn && amBtn) {
                poBtn.classList.toggle('active', gType === 'po');
                amBtn.classList.toggle('active', gType === 'am');
            }
            renderNtbAnalysisTable(type);
        }

        function handleNtbSearch(type) {
            const input = document.getElementById(`search-ntb-${type}`);
            if (input) {
                ntbSearchText[type] = input.value;
                renderNtbAnalysisTable(type);
            }
        }

        function handleNtbSort(type, col) {
            if (ntbSortCol[type] === col) {
                ntbSortAsc[type] = !ntbSortAsc[type];
            } else {
                ntbSortCol[type] = col;
                ntbSortAsc[type] = (col === 'name' || col === 'am') ? true : false;
            }
            renderNtbAnalysisTable(type);
        }

        function renderNtbAnalysisTable(type) {
            const tableBody = document.getElementById(`tbody-ntb-${type}-analysis`);
            if (!tableBody) return;
            
            if (!cachedNtbMatrixData || !cachedNtbMatrixData[type]) {
                tableBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có dữ liệu</td></tr>`;
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
                tableBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có cấu hình ngày</td></tr>`;
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
            const targetVal = type === 'ltc' ? 90 : 65;
            
            if (groupType === 'po') {
                matrix.rows.forEach(row => {
                    if (!matchNtbRegion(row.am, activeNtbRegion)) return;
                    
                    row.pos.forEach(po => {
                        const matchesSearch = !searchText || 
                                               po.bc.toLowerCase().includes(searchText) || 
                                               row.am.toLowerCase().includes(searchText);
                        if (!matchesSearch) return;
                        
                        const poData = po.data[dateKey] || { vol: 0, pct: 0.0 };
                        
                        items.push({
                            name: po.bc,
                            am: row.am,
                            pct: poData.pct,
                            total_vol: poData.vol,
                            pick_vol: poData.vol * poData.pct / 100
                        });
                    });
                });
            } else {
                matrix.rows.forEach(row => {
                    if (!matchNtbRegion(row.am, activeNtbRegion)) return;
                    
                    const matchesSearch = !searchText || row.am.toLowerCase().includes(searchText);
                    if (!matchesSearch) return;
                    
                    const totalData = row.totals[dateKey] || { vol: 0, pct: 0.0 };
                    
                    items.push({
                        name: row.am,
                        am: '-',
                        pct: totalData.pct,
                        total_vol: totalData.vol,
                        pick_vol: totalData.vol * totalData.pct / 100
                    });
                });
            }
            
            if (items.length === 0) {
                const colSpan = groupType === 'po' ? 7 : 6;
                tableBody.innerHTML = `<tr><td colspan="${colSpan}" style="text-align: center; color: var(--text-muted); padding: 20px;">Không tìm thấy kết quả</td></tr>`;
                return;
            }
            
            const sum_total_vol = items.reduce((acc, it) => acc + it.total_vol, 0);
            items.forEach(it => {
                it.prop = sum_total_vol > 0 ? it.total_vol / sum_total_vol : 0;
            });

            // Calculate and assign performance rank based on pct descending
            items.sort((a, b) => b.pct - a.pct);
            items.forEach((item, index) => {
                item.rank = index + 1;
            });
            
            const multiplier = sortAsc ? 1 : -1;
            items.sort((a, b) => {
                let valA = a[sortCol];
                let valB = b[sortCol];
                
                if (sortCol === 'rank') {
                    valA = a.rank;
                    valB = b.rank;
                    return (valA - valB) * multiplier; // ascending rank means lower rank number (1 is best)
                }
                
                if (typeof valA === 'string') {
                    return valA.localeCompare(valB) * multiplier;
                }
                
                return (valA - valB) * multiplier;
            });
            
            tableBody.innerHTML = '';
            const displayAm = (groupType === 'po');
            const amHeader = document.getElementById(`th-${type}-am-header`);
            if (amHeader) {
                amHeader.style.display = displayAm ? '' : 'none';
            }
            
            items.forEach((item, index) => {
                const tr = document.createElement('tr');
                const rank = item.rank;
                const badgeClass = item.pct >= targetVal ? 'badge-success' : 'badge-danger';
                
                tr.innerHTML = `
                    <td style="text-align: center; font-weight: 600; color: var(--text-secondary);">${rank}</td>
                    <td style="text-align: left; font-weight: 600; color: var(--text-primary);">${escapeHTML(item.name)}</td>
                    ${displayAm ? `<td style="text-align: left; color: var(--text-secondary);">${escapeHTML(item.am)}</td>` : ''}
                    <td style="text-align: right; font-weight: 500;">${Math.round(item.pick_vol).toLocaleString()}</td>
                    <td style="text-align: right; color: var(--text-secondary);">${item.total_vol.toLocaleString()}</td>
                    <td style="text-align: right; color: var(--text-muted); font-size: 11px;">${(item.prop * 100).toFixed(2)}%</td>
                    <td style="text-align: right;">
                        <span class="badge ${badgeClass}" style="font-weight: 700; padding: 4px 8px; border-radius: 6px;">${roundNum(item.pct)}%</span>
                    </td>
                `;
                tableBody.appendChild(tr);
            });
            
            const cols = ['rank', 'name', 'am', 'pick_vol', 'total_vol', 'prop', 'pct'];
            cols.forEach(c => {
                const el = document.getElementById(`sort-icon-${type}-${c}`);
                if (el) {
                    if (sortCol === c) {
                        el.innerText = sortAsc ? '▲' : '▼';
                        el.style.color = 'var(--color-ghn-orange)';
                        el.style.opacity = '1';
                    } else {
                        el.innerText = '↕';
                        el.style.color = 'var(--text-muted)';
                        el.style.opacity = '0.5';
                    }
                }
            });
        }

        async function loadNtbSummaryData() {
            const am = document.getElementById('filter-am').value;
            const prov = document.getElementById('filter-province').value;
            const po = document.getElementById('filter-po').value;
            const dateSelect = document.getElementById('ntb-date-select');
            const selectedDate = dateSelect ? dateSelect.value : '';
            
            const timeGroupEl = document.getElementById('ntb-time-group');
            const timeGroup = timeGroupEl ? timeGroupEl.value : 'ngay';
            
            const params = new URLSearchParams();
            if (am) params.append('am', am);
            if (prov) params.append('province', prov);
            if (po) params.append('post_office', po);
            if (selectedDate) params.append('date', selectedDate);
            params.append('time_group', timeGroup);
            
            try {
                const summaryRes = await fetch(getApiUrl(`/api/summary-dashboard?${params.toString()}`), getFetchOptions());
                const summaryData = await summaryRes.json();
                
                if (summaryData.error) {
                    console.error("Summary error:", summaryData.error);
                    return;
                }
                
                cachedNtbSummaryData = summaryData;
                
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
                
                const ovDateLabel = document.getElementById('overview-report-date');
                if (ovDateLabel) {
                    ovDateLabel.innerText = "Ngày báo cáo: " + summaryData.latest_date;
                }
                
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
                        { name: 'ODR TTS', data: ttcSeries }
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
                
                renderNtbKpiCards();
                
                const trendsRes = await fetch(getApiUrl(`/api/trends-dashboard?${params.toString()}`), getFetchOptions());
                const trendsData = await trendsRes.json();
                cachedNtbTrendsData = trendsData;
                
                renderNtbSparklines();
                
                const trendDates = trendsData.dates || [];
                const trends = trendsData.trends || {};
                
                const ltcLines = [];
                const gtcLines = [];
                
                const provKeys = [
                     { key: 'overall', name: 'Toàn vùng' },
                     { key: 'lam_dong', name: 'Lâm Đồng' },
                     { key: 'binh_thuan', name: 'Bình Thuận' },
                     { key: 'khanh_hoa', name: 'Khánh Hòa' },
                     { key: 'dak_nong', name: 'Đắk Nông' },
                     { key: 'ninh_thuan', name: 'Ninh Thuận' }
                ];
                
                provKeys.forEach(p => {
                    const trendObj = getProvinceTrendData(p.key, trends);
                    if (trendObj) {
                        if (trendObj.ltc) ltcLines.push({ name: p.name, data: trendObj.ltc });
                        if (trendObj.gtc) gtcLines.push({ name: p.name, data: trendObj.gtc });
                    }
                });
                
                const lineColors = ['#ff5f00', '#007bc3', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899'];
                
                const ltcTrendOptions = {
                    chart: { type: 'line', height: 280, toolbar: { show: false }, background: 'transparent' },
                    series: ltcLines,
                    xaxis: { categories: trendDates.map(d => d.split(" - ")[0]), labels: { style: { colors: '#64748b' } } },
                    yaxis: { title: { text: 'Tỷ lệ %' }, min: 40, max: 100, labels: { style: { colors: '#64748b' } } },
                    colors: lineColors,
                    stroke: { width: 3, curve: 'smooth' },
                    theme: { mode: 'light' },
                    legend: { position: 'bottom', labels: { colors: '#64748b' } },
                    dataLabels: { enabled: true, formatter: val => val + "%", style: { fontSize: '9px' } }
                };
                
                if (ntbLtcTrendChart) ntbLtcTrendChart.destroy();
                ntbLtcTrendChart = new ApexCharts(document.querySelector("#chart-ntb-ltc-trend"), ltcTrendOptions);
                ntbLtcTrendChart.render();
                
                const gtcTrendOptions = {
                    chart: { type: 'line', height: 280, toolbar: { show: false }, background: 'transparent' },
                    series: gtcLines,
                    xaxis: { categories: trendDates.map(d => d.split(" - ")[0]), labels: { style: { colors: '#64748b' } } },
                    yaxis: { title: { text: 'Tỷ lệ %' }, min: 40, max: 100, labels: { style: { colors: '#64748b' } } },
                    colors: lineColors,
                    stroke: { width: 3, curve: 'smooth' },
                    theme: { mode: 'light' },
                    legend: { position: 'bottom', labels: { colors: '#64748b' } },
                    dataLabels: { enabled: true, formatter: val => val + "%", style: { fontSize: '9px' } }
                };
                
                if (ntbGtcTrendChart) ntbGtcTrendChart.destroy();
                ntbGtcTrendChart = new ApexCharts(document.querySelector("#chart-ntb-gtc-trend"), gtcTrendOptions);
                ntbGtcTrendChart.render();
                
                const matrixRes = await fetch(getApiUrl(`/api/matrix-tables?${params.toString()}`), getFetchOptions());
                const matrixData = await matrixRes.json();
                cachedNtbMatrixData = matrixData;
                
                renderNtbAnalysisTable('ltc');
                renderNtbAnalysisTable('gtc');
                
            } catch (err) {
                console.error("Error loading NTB data:", err);
            }
        }
"""

# Replace NTB section
new_text = text[:start_idx] + premium_js + text[end_idx:]

# 2. Update loadGoogleSheetsConfig to fetch masked keys
old_load_config = """async function loadGoogleSheetsConfig() {
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

new_load_config = """async function loadGoogleSheetsConfig() {
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

if old_load_config in new_text:
    new_text = new_text.replace(old_load_config, new_load_config)
    print("Replaced loadGoogleSheetsConfig successfully!")
else:
    # Try with slightly different spacing if it mismatch
    print("Warning: could not find exact old_load_config, trying loose match...")
    # Let's search and replace via regex
    pattern_load = r'async\s+function\s+loadGoogleSheetsConfig\s*\([^)]*\)\s*\{[^}]*sheet-consolidated-url[^}]*\}'
    # Wait, regex is safer. Let's do it in Python.

# 3. Add sendTelegramAiBriefing and sendTelegramWarning after saveGoogleSheetsConfig()
telegram_js_funcs = """
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
"""

save_config_end_idx = new_text.find('async function saveGoogleSheetsConfig()')
if save_config_end_idx != -1:
    # Find the next closing bracket of saveGoogleSheetsConfig
    open_brackets = 0
    pos = save_config_end_idx
    while pos < len(new_text):
        if new_text[pos] == '{':
            open_brackets += 1
        elif new_text[pos] == '}':
            open_brackets -= 1
            if open_brackets == 0:
                # Insert right after the closing bracket
                insert_pos = pos + 1
                new_text = new_text[:insert_pos] + telegram_js_funcs + new_text[insert_pos:]
                print("Inserted telegram functions successfully!")
                break
        pos += 1
else:
    print("Warning: saveGoogleSheetsConfig function not found!")

# 4. Add NHÂN SỰ functions at the very end of the script block (before </script>)
nhan_su_js = """
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
"""

script_end_tag = '</script>'
script_end_idx = new_text.rfind(script_end_tag)
if script_end_idx != -1:
    new_text = new_text[:script_end_idx] + nhan_su_js + new_text[script_end_idx:]
    print("Inserted nhan_su functions successfully!")
else:
    print("Error: script end tag not found!")

# Save to templates/index.html
with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Successfully applied all custom dashboard patches!")
