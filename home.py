# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import os, sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
from config.config import *
from Consulta import *

global objconsulta

@app.route('/')
def cargar():
    logging.info("Ingresando en cargar")
    lista_ips=objconsulta.dim_ips()
    # logging.info(lista_ips)
    return render_template('index.html', lista_ips=lista_ips)

@app.route('/', methods=['POST'])
def obtener():
    logging.info("Ingresando en obtener")
    print(request.form)
    logging.error(request.form)
    #ips=str(request.form['comboips'])
    #tiempo=str(request.form['radtiempomin'])
    #logging.info(ips)
    #logging.info(tiempo)
    return render_template('index.html', lista_ips="")

if __name__ == '__main__':
    # CONFIGURACION PARA LOG
    logging.basicConfig(filename=LOG_FILE,\
                        level=logging.INFO,\
                        format='%(levelname)s[%(asctime)s]: %(message)s',\
                        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w')  # Cambiar a "filemode=a"
    objconsulta = Consulta()
    app.run(host='0.0.0.0', debug=True, port=8081, use_reloader=True)
