from flask import Flask, render_template, request, redirect, url_for
import qrcode
import base64
from io import BytesIO  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'strongsecretkey'  


def generate_qr_code(data):
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, 'PNG')
    buffered.seek(0)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        if data:
            qr_code = generate_qr_code(data)
            return render_template('index.html', qr_code=qr_code)
    return render_template('index.html', qr_code=None)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        qr_data = request.form['qr_data']
        password = request.form['password']

    
        if password != 'your_password': 
            return render_template('scan.html', error="Incorrect password!")


        decoded_qr_data = base64.b64decode(qr_data).decode('utf-8')
        return f"Scanned data: {decoded_qr_data} (Password used: {password})"

    return render_template('scan.html', error=None)


if __name__ == '__main__': 
    app.run(debug=True)
