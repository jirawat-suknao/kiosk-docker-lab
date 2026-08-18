import time
import redis
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
# เชื่อมต่อกับ Database
cache = redis.Redis(host='kiosk-db', port=6379)

# โค้ดส่วนหน้าตาเว็บ (HTML & CSS)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Kiosk Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f7f6; }
        .container { background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
        .btn { padding: 15px 30px; font-size: 20px; margin: 20px; cursor: pointer; border: none; border-radius: 8px; color: white; transition: 0.3s; }
        .btn-borrow { background-color: #e74c3c; }
        .btn-borrow:hover { background-color: #c0392b; }
        .btn-return { background-color: #2ecc71; }
        .btn-return:hover { background-color: #27ae60; }
        .stats { font-size: 22px; margin: 20px 0; color: #333; }
        .count { font-size: 28px; font-weight: bold; color: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🛠️ Kiosk Administrative Dashboard</h2>
        <div class="stats">
            <p>จำนวนอุปกรณ์ที่ถูก <b>ยืม</b> ไปแล้ว: <span class="count">{{ borrow_count }}</span> ครั้ง</p>
            <p>จำนวนอุปกรณ์ที่นำมา <b>คืน</b> แล้ว: <span class="count">{{ return_count }}</span> ครั้ง</p>
        </div>
        
        <form method="POST" action="/borrow" style="display: inline;">
            <button type="submit" class="btn btn-borrow">📤 กดเพื่อ "ยืม" อุปกรณ์</button>
        </form>
        
        <form method="POST" action="/return" style="display: inline;">
            <button type="submit" class="btn btn-return">📥 กดเพื่อ "คืน" อุปกรณ์</button>
        </form>
    </div>
</body>
</html>
'''

# หน้าจอหลัก
@app.route('/')
def dashboard():
    # ดึงข้อมูลจาก Redis (ถ้าไม่มีค่าให้เป็น 0)
    borrow_count = int(cache.get('borrow_count') or 0)
    return_count = int(cache.get('return_count') or 0)
    return render_template_string(HTML_TEMPLATE, borrow_count=borrow_count, return_count=return_count)

# เวลากดปุ่มยืม ให้รันฟังก์ชันนี้
@app.route('/borrow', methods=['POST'])
def borrow_item():
    cache.incr('borrow_count')
    return redirect(url_for('dashboard'))

# เวลากดปุ่มคืน ให้รันฟังก์ชันนี้
@app.route('/return', methods=['POST'])
def return_item():
    cache.incr('return_count')
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)