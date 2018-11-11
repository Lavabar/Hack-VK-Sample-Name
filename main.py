import sys
#import pymysql
import re
import requests
import dlib
import vk
import telegra
import clever
from flask import Flask,request
from flask import Response
import foto_verification
import script
from urllib.request import urlopen
from urllib.parse import quote_plus
from urllib.error import HTTPError
from bs4 import BeautifulSoup

app = Flask(__name__)

token = "c24617ec8afa43845a5cf91b68c70c3c607dd0bfd79e1c3106c63f69142fea78956a14dc57a11f10d20b2"
confirmation_token= "33b00e7d"
@app.route('/', methods=['POST'])
def processing():
    data = request.get_json()
    #print(data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    if data['type'] == 'lead_forms_new':
        name = str(data['object']['answers'][0]['answer'])
        phone = str(data['object']['answers'][1]['answer'])
        #conn = pymysql.connect(host='185.117.152.219', user='hack', password='Wzfuv175', database='hack')
       # cursor = conn.cursor()
        # data = (str(None), str(nam), str(phon))
        #sql = '''insert into users1 (nam, phone) values ('test', '123');'''
       # cursor.execute(sql)
        # cursor.execute("""insert into users1 (id, name, phone) values (NULL, {0}, {1}""".format(str("\'" + nam + "\'" ), str("\'" + phon + "\'" )))
        #print(cursor.execute("select * from users1"))
       # conn.close()
        print(nam)
        print(phon)
        return "true"
       # t = clever.start(name, phone)
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v=5.0)
        user_id = data['object']['user_id']
        text = data['object']['attachments'][0]
        im = text['photo']['photo_807']
        resp = foto_verification.get_name(im)
        if resp != 'noname':
            link = script.findConcert(resp).encode("utf-8").decode("utf-8")
            fin = telegra.createArt(resp, link, im)
            api.messages.send(access_token=token, user_id=str(user_id), message = fin)
        elif resp == 'noname':
            api.messages.send(access_token=token, user_id=str(user_id), message="Извините, мы не смогли найти данного композитора, попробуйте еще раз")
    return 'ok'

@app.route('/serv')
def first():
    return "true"

@app.route('/mobile', methods=['POST'])
def mobil():
    data1 = request.get_json()
    print(data1)
    return data1

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug = True)
