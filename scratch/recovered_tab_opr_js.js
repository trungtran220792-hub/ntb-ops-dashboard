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
        // RENDER: BACKLOG