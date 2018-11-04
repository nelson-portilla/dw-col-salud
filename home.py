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
    logging.info("Ingresando en cargar, index")
    lista_ips=objconsulta.dim_ips()
    logging.info(lista_ips)
    return render_template('index.html', lista_ips=lista_ips)

@app.route('/', methods=['POST'])
def obtener():
    logging.info("Ingresando en obtener")
    texto=str(request.form['id_entrada'])
    print ("HOLA MUNDO!: ", texto)
    return render_template('queryuno.html', texto=texto, objetos=[1,2,3])

if __name__ == '__main__':
    # CONFIGURACION PARA LOG
    logging.basicConfig(filename=LOG_FILE,\
                        level=logging.INFO,\
                        format='%(levelname)s[%(asctime)s]: %(message)s',\
                        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w')  # Cambiar a "filemode=a"
    objconsulta = Consulta()
    app.run(host='0.0.0.0', debug=True, port=8081, use_reloader=True)
