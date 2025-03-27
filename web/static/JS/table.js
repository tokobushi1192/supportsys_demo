//テーブル(リストテーブル)のソート、フィルタリング、行選択などの機能

// テーブルのソート機能
function sortTable(columnIndex) {
    const table = document.getElementById("listTable");
    const rows = Array.from(table.rows).slice(1); // ヘッダーを除く
    const isAscending = table.getAttribute("data-sort-order") === "asc";
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].innerText;
        const bText = b.cells[columnIndex].innerText;
        return isAscending ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });
    table.setAttribute("data-sort-order", isAscending ? "desc" : "asc");
    rows.forEach(row => table.tBodies[0].appendChild(row));
}

// テーブルのフィルタリング機能
function filterTable() {
    const nameFilter = document.getElementById("nameFilter").value.toLowerCase();
    const addressFilter = document.getElementById("addressFilter").value.toLowerCase();
    const table = document.getElementById("listTable");
    const rows = Array.from(table.rows).slice(1); // ヘッダーを除く
    rows.forEach(row => {
        const name = row.cells[1].innerText.toLowerCase();
        const address = row.cells[2].innerText.toLowerCase();
        const matchesName = name.includes(nameFilter);
        const matchesAddress = address.includes(addressFilter);
        row.style.display = matchesName && matchesAddress ? "" : "none";
    });
}

// テーブルの行選択機能
document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById("listTable");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) { // ヘッダー行を除く
        rows[i].addEventListener("click", function () {
            // すべての行から選択クラスを削除
            for (let j = 1; j < rows.length; j++) {
                rows[j].classList.remove("selected-row");
            }
            // クリックされた行に選択クラスを追加
            this.classList.add("selected-row");
        });
    }
});