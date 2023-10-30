import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import os
#Nhập các thư viện và module cần thiết. cv2 và numpy được sử dụng để xử lý hình ảnh. 
#Flask và các chức năng liên quan đến nó được nhập để tạo ứng dụng web. 
#os được sử dụng để tương tác với hệ thống tệp.

app = Flask(__name__)

UPLOAD_FOLDER = 'templates/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Khởi tạo ứng dụng Flask với tên app. 
#Đồng thời, thiết lập thư mục nơi các tệp tải lên sẽ được lưu trữ (UPLOAD_FOLDER).

def histogram_equalization(image_path):
    image = cv2.imread(image_path, 0)  # Đọc hình ảnh vào dạng grayscale (0)
    equ = cv2.equalizeHist(image)  # Áp dụng cân bằng histogram
    return equ  # Trả về hình ảnh đã cân bằng histogram

@app.route('/', methods=['GET', 'POST'])
def index():
    result_image = None  # Khởi tạo biến kết quả

    if request.method == 'POST':
        if 'image' in request.files:  # Kiểm tra nếu có tệp hình ảnh được tải lên
            image = request.files['image']  # Lấy tệp hình ảnh từ yêu cầu
            if image.filename != '':  # Kiểm tra nếu tệp không trống
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.jpg')  # Tạo đường dẫn lưu tệp
                image.save(image_path)  # Lưu tệp hình ảnh được tải lên
                result_image = histogram_equalization(image_path)  # Áp dụng cân bằng histogram và lưu kết quả
                cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'enhanced_image.jpg'), result_image)  # Lưu hình ảnh đã cân bằng histogram
                return redirect(url_for('result'))  # Chuyển hướng đến trang kết quả

    return render_template('index.html')  # Hiển thị trang giao diện chính

@app.route('/result')
def result():
    result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'enhanced_image.jpg')  # Đường dẫn đến tệp hình ảnh đã cân bằng histogram
    return render_template('result.html', result_image=result_image_path)  # Hiển thị trang kết quả với hình ảnh đã cân bằng histogram

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Tạo thư mục lưu trữ tệp tải lên (nếu chưa tồn tại)
    app.run(debug=True, port=5001)  # Chạy ứng dụng Flask với chế độ debug trên cổng 5001


#Dòng 13-21: Định nghĩa hàm histogram_equalization(image_path) để cân bằng histogram của một hình ảnh.
#Dòng 23-51: Định nghĩa tuyến đường chính / (trang chính). Nếu có một yêu cầu POST (tệp hình ảnh được tải lên), 
# nó sẽ xử lý tệp và áp dụng cân bằng histogram. Khi xử lý hoàn tất, nó sẽ chuyển hướng đến trang kết quả. Nếu không có yêu cầu POST, trang giao diện chính sẽ được hiển thị.
#Dòng 53-61: Định nghĩa tuyến đường /result để hiển thị trang kết quả với hình ảnh đã cân bằng histogram.
#Dòng 63-68: Kiểm tra xem mã chương trình có được chạy trực tiếp (không được nhập bởi một tệp khác) hay không. Nếu điều kiện đúng, 
# thư mục lưu trữ tệp tải lên sẽ được tạo (nếu chưa tồn tại), và ứng dụng Flask sẽ được chạy với chế độ debug trên cổng 5001.