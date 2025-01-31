from flask import Flask, request, render_template, url_for
import random
import string
import webbrowser


app = Flask(__name__)

def decrypt_url(encrypted_url):
    return ''.join(c for c in encrypted_url if ord(c) < 128)

def encrypt_url(url):
    encrypted_url = ""
    for c in url:
        if ord(c) < 128:
            encrypted_url += c + chr(random.randint(0x1F600, 0x1F64F))
        else:
            encrypted_url += c
    return encrypted_url

@app.route("/", methods=["GET", "POST"])
def index():
    decrypt_result = None
    encrypt_result = None
    if request.method == "POST":
        if 'url' in request.form:
            encrypted_url = request.form["url"]
            decrypt_result = decrypt_url(encrypted_url)
        if 'encrypt' in request.form:
            url = request.form["url"]
            encrypt_result = encrypt_url(url)
    return render_template('index.html', decrypt_result=decrypt_result, encrypt_result=encrypt_result)

@app.route("/encrypt", methods=["POST"])
def encrypt():
    url = request.form["url"]
    encrypt_result = encrypt_url(url)
    return render_template('index.html', encrypt_result=encrypt_result)

if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000')
    app.run(debug=False)

