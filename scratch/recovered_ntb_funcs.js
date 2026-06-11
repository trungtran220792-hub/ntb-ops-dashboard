function renderNtbAnalysisTable(type) {
L6512: const sortCol = ntbSortCol[type];
L6513: const sortAsc = ntbSortAsc[type];
L6581: items.sort((a, b) => {
L6583: if (sortCol === 'rank') {
L6586: if (v1 < v2) return sortAsc ? -1 : 1;
L6587: if (v1 > v2) return sortAsc ? 1 : -1;
L6589: } else if (sortCol === 'name') {
L6592: } else if (sortCol === 'am') {
L6595: } else if (sortCol === 'pick_vol') {
L6598: } else if (sortCol === 'total_vol') {
L6601: } else if (sortCol === 'prop') {
L6604: } else if (sortCol === 'pct') {
L6607: } else if (sortCol === 'status') {
L6612: if (v1 < v2) return sortAsc ? -1 : 1;
L6613: if (v1 > v2) return sortAsc ? 1 : -1;
L6653: const iconEl = document.getElementById(`sort-icon-${type}-${c}`);
L6655: if (sortCol === c) {
L6656: iconEl.innerText = sortAsc ? '▲' : '▼';
L6692: function handleNtbSort(type, col) {
L6693: if (ntbSortCol[type] === col) {
L6694: ntbSortAsc[type] = !ntbSortAsc[type];
L6696: ntbSortCol[type] = col;
L6697: ntbSortAsc[type] = true;
L6699: ntbSortAsc[type] = false;
L6895: const provinces = Object.keys(structure).sort();
L6904: const amNames = Object.keys(ams).sort();
