from flask import Flask, request, render_template_string, url_for
import random
import string

app = Flask(__name__)

def decrypt_url(encrypted_url):
    """解密被表情符号干扰的URL链接"""
    return ''.join(c for c in encrypted_url if ord(c) < 128)

def encrypt_url(url):
    """加密URL链接，通过在ASCII字符之间添加表情符号"""
    encrypted_url = ""
    for c in url:
        if ord(c) < 128:
            # 随机添加一些非ASCII字符
            encrypted_url += c + chr(random.randint(0x1F600, 0x1F64F))  # 使用emoji范围
        else:
            encrypted_url += c
    return encrypted_url

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>链接解密/加密工具</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        h1 { color: #333; }
        input[type="text"] { width: 400px; padding: 10px; font-size: 16px; }
        input[type="submit"] { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f9f9f9; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>链接解密工具</h1>
    <form method="POST" action="{{ url_for('index') }}">
        <input type="text" name="url" placeholder="请输入加密的链接" required>
        <input type="submit" value="解密">
    </form>
    {% if decrypt_result %}
    <div class="result">
        <strong>解密结果：</strong><br>
        <code>{{ decrypt_result }}</code>
    </div>
    {% endif %}
    
    <h1>链接加密工具</h1>
    <form method="POST" action="{{ url_for('encrypt') }}">
        <input type="text" name="url" placeholder="请输入正常的链接" required>
        <input type="submit" value="加密">
    </form>
    {% if encrypt_result %}
    <div class="result">
        <strong>加密结果：</strong><br>
        <code>{{ encrypt_result }}</code>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    decrypt_result = None
    if request.method == "POST":
        encrypted_url = request.form["url"]
        decrypt_result = decrypt_url(encrypted_url)
    return render_template_string(HTML_TEMPLATE, decrypt_result=decrypt_result)