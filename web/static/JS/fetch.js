//fetch サーバーからデータを取得し、フォームに反映する機能を含む。


function fetchDetails(noId) {
    // サーバーに選択したNO_idを送信
    fetch('/main_menu/get_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ NO_id: noId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // テキストボックスにデータを反映
            document.getElementById('Name').value = data.Name;
            document.getElementById('Group_Kbn').value = data.Group_Kbn;
            document.getElementById('Address1').value = data.Address1;
            document.getElementById('Address2').value = data.Address2;
            document.getElementById('RN').value = data.RN;
            document.getElementById('PN').value = data.PN;
            document.getElementById('Remarks').value = data.Remarks;
            document.getElementById('Num_Detache').value = data.Num_Detache;
            document.getElementById('Num_Total').value = data.Num_Total;
            document.getElementById('Num_75old').value = data.Num_75old;
            document.getElementById('Num_PS').value = data.Num_PS;
            document.getElementById('Num_build').value = data.Num_build;
            document.getElementById('Num_Apart').value = data.Num_Apart;
            document.getElementById('Month_price').value = data.Month_price;
            document.getElementById('Pay_Kbn').value = data.Pay_Kbn;
            document.getElementById('Move_Out').value = data.Move_Out;
            document.getElementById('Year_Price').value = data.Year_Price;
            document.getElementById('Transfer_Flg').checked = data.Transfer_Flg === "振込";
            document.getElementById('Collector_Kbn').value = data.Collector_Kbn;
            document.getElementById('HoldPrice_Kbn').value = data.HoldPrice_Kbn;
            document.getElementById('residence_No').value = data.residence_No;
        }
    })
    //.catch(error => console.error('Error:', error));
}  