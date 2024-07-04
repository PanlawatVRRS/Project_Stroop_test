อุปกรณ์ที่ต้องใช้ในการทดสอบโปรแกรม
1.Raspberry pi ที่มีระบบปฏิบัติการ Raspbian อยู่ข้างใน
2.จอ monitor ที่ใช้ต่อกับ Raspberry pi
3.arduinoพร้อมชุดprototype

ขั้นตอนการsetup

ส่วนของRaspberry pi
1.Download Folder Project_Raspberry pi จาก github ลงบน desktop ของ Raspberry pi
2.เปิดหน้า terminal บน Raspberry pi
3.download module ที่จำเป็นด้วยคำสั่งดังนี้่
3.1 pygame: ติดตั้ง pygame ด้วยคำสั่ง pip install pygame
3.2 bluetooth: ติดตั้ง PyBluez เพื่อใช้งาน bluetooth บน Raspberry Pi โดยใช้คำสั่ง pip install pybluez
4.เข้าไปยังfolderของโปรแกรมด้วยคำสั่ง cd Desktop/Project_Raspberry pi

ส่วนของArduino (ในส่วนนี้อาจารย์ไม่สามารถทำได้เนื่องจากอาจารย์ไม่มีตัว prototype)
1.ติดตั้ง arduino กับกล่อง prototype
2.Download Folder Project_Arduino ลงบนคอมของตัวเองแล้วเปิดไฟล์ project_test_arduino_send.ino
3.ทำการ upload code ลงบน arduino nano

ขั้นตอนการtest
1.ต่อarduinoเข้ากับแหล่งจ่ายไฟ
2.run โปรแกรมบนRaspberry piด้วยคำสั่ง sudo python on_process.py
3.ระบบจะทำการเชื่อมต่อกันเองด้วย bluetooth และสามารถใช้งานได้เลย
