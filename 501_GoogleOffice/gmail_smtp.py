import smtplib, json, os
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate


ROOT_DIR = os.getcwd()
FILEJSON = 'google_account.json'
SMTPURL = 'smtp.gmail.com'
SMTPPORT = '465'  # SSL port

with open(os.path.join(ROOT_DIR, FILEJSON),'r') as f:
    jsonfile=json.load(f)

class GMAILSend:
    def __init__(self) -> None:
        self.mailServer = smtplib.SMTP_SSL(SMTPURL, SMTPPORT)
        self.mailServer.login(jsonfile['id'], jsonfile['password'])
        self.msg = MIMEMultipart()

    def add_adrress(self, From: str, To: str):
        self.msg['From'] = From
        self.msg['To'] = To

    def add_subject(self, Subject: str = ''):
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = Header(s=Subject, charset='utf-8')

    def add_body(self, Body: list):
        Body = ''.join(Body)
        htmltext = f'''<html><head></head><body>
            {Body}
            </body></html>'''
        htmltext = MIMEText(htmltext, 'html')
        self.msg.attach(htmltext)

    def add_img(self, Image: str = '', cidname: str = ''):
        with open(Image, 'rb') as img:
            _img = MIMEImage(img.read())
            _img.add_header('Content-Disposition',
                            f'attachment; filename={Image}')
            _img.add_header('Content-ID', f'<{cidname}>')
            self.msg.attach(_img)

    def add_file(self, FileList: list = []):
        for f in FileList:
            _file = MIMEBase('application', "octet-stream")
            _file.set_payload(open(f, 'rb').read())
            encode_base64(_file)
            _file.add_header('Content-Disposition',
                             f'attachment; filename="{f}"')
            self.msg.attach(_file)

    def mail_send(self):
        self.mailServer.send_message(self.msg)

    def quit(self):
        self.mailServer.quit()


if __name__ == '__main__':
    _from: str = 'yoosc89@gmail.com'
    _to: str = 'yoosc89@gmail.com'
    subject: str = 'image test'
    cidname = 'image'
    image = '1.jpg'
    body = f'<img src="cid:{cidname}">'
    bodytext=f'<h1>dfdfsdfsfsdf</h1>'
    filelist: list = []

    email = GMAILSend()
    email.add_adrress(From=_from, To=_to)
    email.add_subject(Subject=subject)
    email.add_body(Body=bodytext)
    email.add_img(Image=image, cidname=cidname)
    email.add_file(FileList=filelist)
    email.mail_send()
    email.quit()
