import os
from flask import Flask, render_template, request, redirect, url_for
from pyqrcode import create as qr_create
from io import BytesIO
from reportlab.pdfgen import canvas
from dropbox import Dropbox, files

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sl.Bs5vvUnIC7phkQc71sFLlbHU75l6-Mc4BgMChrZC0mzwnYy2uXL0nLiGcrZStKXWZn8oJo40qXjRj0WXT5w2f43zdxdRTQ3lpQ0dBror-Def_SMGdZJmFDAVB2sVCOxs3xAuE55JwxX7vUI'  # Change this to a secure secret key

# Dropbox setup
dbx = Dropbox('sl.Bs5vvUnIC7phkQc71sFLlbHU75l6-Mc4BgMChrZC0mzwnYy2uXL0nLiGcrZStKXWZn8oJo40qXjRj0WXT5w2f43zdxdRTQ3lpQ0dBror-Def_SMGdZJmFDAVB2sVCOxs3xAuE55JwxX7vUI')  # Replace with your Dropbox access token

dropbox_link_username = 'cyberboys'
dropbox_link_password = 'fw89m2f5a9'  # Change this to your desired password


@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = ''

    if request.method == 'POST':
        data = request.form['data']
        username = request.form['username']
        password = request.form['password']

        if ((password != dropbox_link_password) and (username!=dropbox_link_username)):
            error_message = 'Incorrect password. Please try again.'
            return render_template('index.html', error_message=error_message)

        # Create a PDF with the provided data
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer)
        pdf.drawString(100, 750, "Data: " + data)
        
        pdf.save()
        pdf_buffer.seek(0)

        folder_path = '/secured'  # Replace 'YourFolder' with the desired folder name
        file_path = folder_path + '/password_protected_data.pdf'

        try:
            dbx.files_upload(pdf_buffer.read(), file_path, mode=files.WriteMode.overwrite)
        except Exception as e:
            error_message = f'Error uploading to Dropbox: {str(e)}'
            return render_template('index.html', error_message=error_message)


        # Generate QR code
        qr_url = dbx.sharing_create_shared_link(file_path).url
        qr = qr_create(qr_url)
        qr.png('static/password_protected_qr.png', scale=6)

        return render_template('result.html', qr_image='password_protected_qr.png')

    return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)