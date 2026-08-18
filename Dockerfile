# ใช้ Python version 3.9 แบบ slim เพื่อให้ขนาด image เล็กและโหลดไว
FROM python:3.9-slim

# กำหนดโฟลเดอร์ทำงานภายใน Container ให้อยู่ที่ /app
WORKDIR /app

# คัดลอกไฟล์ requirements.txt จากเครื่องเราเข้าไปใน Container
# (เหตุผลที่คัดลอกมาก่อน เพื่อใช้ประโยชน์จาก Layer Caching หากโค้ดเปลี่ยนแต่ library เท่าเดิม)
COPY requirements.txt .

# รันคำสั่งติดตั้ง library ต่างๆ ตามที่ระบุไว้ใน requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โค้ดทั้งหมด (เช่น app.py) เข้าไปใน Container
COPY . .

# ระบุให้ Container นี้เปิดพอร์ต 5000 สำหรับให้ภายนอกเรียกใช้งาน
EXPOSE 5000

# กำหนดคำสั่งเริ่มต้นเมื่อ Container ทำงาน ให้รันไฟล์ app.py
CMD ["python", "app.py"]