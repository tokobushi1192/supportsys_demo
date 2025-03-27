from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
import bcrypt #パスワードのハッシュ化

load_dotenv()

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY")  # セッション管理用の秘密鍵

# MySQL接続関数
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"), # MySQLサーバーのホスト
            user=os.getenv("DB_USER"), # MySQLのユーザー名
            password=os.getenv("DB_PASSWORD"), # MySQLのパスワード
            database=os.getenv("DB_NAME") # 接続するデータベース名
        )
        return conn
    except mysql.connector.Error as err:
        return str(err)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.get_json()  # 修正: JSON 形式のデータを受け取る
        
        username = data.get("username")
        password = data.get("password")
        # if not username or not password:
        #     return render_template("index.html", error="ユーザー名とパスワードを入力してください。")

        conn = connect_to_mysql()
        if isinstance(conn, str):
            return jsonify({"status": "error", "message": f"データベース接続エラー: {conn}"})  # 修正: JSON でエラーメッセージを返す

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, TRIM(CAST(password_hash AS CHAR(60))) as password_hash FROM support_users WHERE username = %s", (username,))
            # cursor.execute("SELECT username, CONVERT(password_hash USING utf8)  as password_hash FROM support_users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                stored_hashed_password = user["password_hash"].rstrip('\x00')
                if password == stored_hashed_password:
                    session["username"] = username  # セッションに保存
                    return jsonify({"status": "success"})  # 修正: 成功時に JSON でレスポンス
                else:
                    return jsonify({"status": "error", "message": "パスワードが間違っています。"})  # 修正: JSON でエラーメッセージを返す
            else:
                return jsonify({"status": "error", "message": "ユーザーが存在しません。"})  # 修正: JSON でエラーメッセージを返す

        except mysql.connector.Error as err:
            print(f"データベースエラー: {err}")  # ログにエラー内容を出力
            return jsonify({"status": "error", "message": f"データベースエラー: {err}"})  # 修正: データベースエラーの対応
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")  # フォームを表示
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({"status": "error", "message": "ユーザー名とパスワードを入力してください。"})

        conn = connect_to_mysql()
        if isinstance(conn, str):
            return jsonify({"status": "error", "message": conn})

        try:
            cursor = conn.cursor()           
            # ユーザー名が既に存在するかチェック
            cursor.execute("SELECT COUNT(*) FROM support_users WHERE username = %s", (username,))
            user_exists = cursor.fetchone()[0]
            
            if user_exists > 0:
                return jsonify({"status": "error", "message": "このユーザー名は既に使用されています。"})

            # ユーザー登録
            cursor.execute("INSERT INTO support_users (username, password_hash) VALUES (%s, %s)", (username, password))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"status": "success", "message": "ユーザー登録が完了しました！"})

        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": str(err)})

    #return render_template("register.html")
@app.route("/main_menu")
def main_menu():
    if "username" not in session:
        return redirect(url_for("home"))  # 未ログインならトップページへ
    
    conn = connect_to_mysql()
    cursor = conn.cursor()
    
    #リストビュー取得
    cursor.execute("SELECT NO_id, Name, Group_Kbn FROM tbl_infopeople_z")
    rows = cursor.fetchall()

    #住宅区分を取得
    cursor.execute("SELECT residence_No, residence_Name FROM mst_residence ORDER BY residence_No")
    residence_data = cursor.fetchall()

    #支払区分を取得
    cursor.execute("SELECT kbn_no, PayName FROM mst_paykbn ORDER BY kbn_no")
    pay_data = cursor.fetchall()

    #集金者区分を取得
    cursor.execute("SELECT CM_No, CM_Name FROM mst_cmkbn ORDER BY CM_No")
    CM_data = cursor.fetchall()

    #保留区分を取得
    cursor.execute("SELECT hold_No, hold_Name FROM mst_memverhold ORDER BY hold_No")
    hold_data = cursor.fetchall()

    conn.close()
    return render_template(
        "main_menu.html", 
        rows=rows,
        residence_data=residence_data,
        pay_data=pay_data,
        CM_data=CM_data,
        hold_data=hold_data
        )

#20250325追加S
@app.route('/main_menu/get_details', methods=['POST'])
def get_details():
    no_id = request.json.get('NO_id')  # フロントエンドから送信されたNO_idを取得

    # データベース接続
    conn = connect_to_mysql()
    cursor = conn.cursor()

    no_id = str(no_id)
    cursor.execute("""
        SELECT t1.NO_id AS NO_id, t1.Name AS Name, t1.Group_Kbn AS Group_Kbn, t1.Address1 AS Address1,
            t1.Address2 AS Address2, t1.RN AS RN, t1.PN AS PN, t1.Remarks AS Remarks, t1.Num_Detache AS Num_Detache,
            t1.Num_Total AS Num_Total, t1.Num_75old AS Num_75old, t1.Num_PS AS Num_PS, t1.Num_build AS Num_build,
            t1.Num_Apart AS Num_Apart, t1.Month_price AS Month_price, t3.kbn_no AS Pay_Kbn,
            t1.Move_Out AS Move_Out, t1.Year_Price AS Year_Price, t1.Transfer_Flg AS Transfer_Flg,
            t2.CM_No AS Collector_Kbn, t1.HoldPrice_Kbn AS HoldPrice_Kbn,
            t5.residence_No AS residence_No
        FROM tbl_infopeople_z AS t1
        LEFT OUTER JOIN mst_cmkbn AS t2 ON t1.Collector_Kbn = t2.CM_No 
        LEFT OUTER JOIN mst_paykbn AS t3 ON t1.Pay_kbn = t3.kbn_no
        LEFT OUTER JOIN mst_residence AS t5 ON t1.residence_No = t5.residence_No
        LEFT OUTER JOIN mst_memverhold AS t6 ON t1.HoldPrice_Kbn = t6.hold_No   
        WHERE NO_id = %s
    """, (no_id,))
    result = cursor.fetchone()  # 1件のデータを取得
    # データベース接続を閉じる
    conn.close()

    # 結果をJSONで返す
    if result:
        keys = ["NO_id", "Name", "Group_Kbn", "Address1", "Address2", "RN", "PN", "Remarks",
                "Num_Detache", "Num_Total", "Num_75old", "Num_PS", "Num_build", "Num_Apart",
                "Month_price", "Pay_Kbn", "Move_Out", "Year_Price",
                "Transfer_Flg", "Collector_Kbn", "HoldPrice_Kbn", "residence_No"]
        return jsonify(dict(zip(keys, result)))
    else:
        return jsonify({"error": "No data found"}), 404
#20250325追加E

if __name__ == "__main__":
    app.run(debug=True)