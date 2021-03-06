# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import os, sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
import json
from dateutil import parser
from config.config import *
from Consulta import *

global objconsulta

@app.route('/')
def cargar():
    logging.info("Ingresando en cargar")
    lista_ips=[]
    results = []
    columns=("institucion","t_espera")
    for row in lista_ips:
        results.append(dict(zip(columns, row)))
    t_espera_data=json.dumps(results, ensure_ascii=False)
    logging.info(t_espera_data)
    return render_template('index.html', lista_ips=lista_ips, t_espera_data=t_espera_data)

@app.route('/', methods=['POST'])
def obtener():
    logging.info("Ingresando en obtener")
    print(request.form)

    tiempo=request.form["radiotiempo"]
    fechain = parser.parse(request.form["datepicker"]).strftime('%Y-%m-%d')
    fechaout= parser.parse(request.form["datepicker2"]).strftime('%Y-%m-%d')
    criterio=request.form['criterio']
    combounidad="fact_urgencias" if request.form['combounidad']=="Tiempos de espera en urgencias" else "fact_citas_medicas"
    print combounidad

    if criterio=="institucion":
        lista_resultado=objconsulta.t_espera_urgencias_ips(tiempo,fechain,fechaout,combounidad)
        logging.info(lista_resultado)
        results = []
        columns = ("institucion", "t_espera")
        for row in lista_resultado:
            results.append(dict(zip(columns, row)))
        t_espera_data = json.dumps(results, ensure_ascii=False)
        return render_template('index.html', lista_ips=lista_resultado, t_espera_data=t_espera_data, criterio=criterio)

    if criterio=="sexo":
        lista_resultado=objconsulta.t_espera_urgencias_sexo(tiempo,fechain,fechaout,combounidad)
        logging.info(lista_resultado)
        results = []
        columns = ("sexo", "t_espera")
        for row in lista_resultado:
            results.append(dict(zip(columns, row)))
        t_espera_data = json.dumps(results, ensure_ascii=False)
        return render_template('index.html', lista_ips=lista_resultado, t_espera_data=t_espera_data, criterio=criterio)

    if criterio=="tipo_usuario":
        lista_resultado=objconsulta.t_espera_urgencias_tipo_usuario(tiempo,fechain,fechaout,combounidad)
        logging.info(lista_resultado)
        results = []
        columns = ("tipo_usuario", "t_espera")
        for row in lista_resultado:
            results.append(dict(zip(columns, row)))
        t_espera_data = json.dumps(results, ensure_ascii=False)
        return render_template('index.html', lista_ips=lista_resultado, t_espera_data=t_espera_data, criterio=criterio)

    if criterio=="estado_civil":
        lista_resultado=objconsulta.t_espera_urgencias_estado_civil(tiempo,fechain,fechaout,combounidad)
        logging.info(lista_resultado)
        results = []
        columns = ("estado_civil", "t_espera")
        for row in lista_resultado:
            results.append(dict(zip(columns, row)))
        t_espera_data = json.dumps(results, ensure_ascii=False)
        return render_template('index.html', lista_ips=lista_resultado, t_espera_data=t_espera_data, criterio=criterio)

    if criterio=="edad":
        lista_resultado=objconsulta.t_espera_urgencias_edad(tiempo,fechain,fechaout,combounidad)
        logging.info(lista_resultado)
        results = []
        columns = ("estado_civil", "t_espera")
        for row in lista_resultado:
            results.append(dict(zip(columns, row)))
        t_espera_data = json.dumps(results, ensure_ascii=False)
        return render_template('tiempo_edad.html', lista_ips=lista_resultado, t_espera_data=t_espera_data, criterio=criterio)

    else:
        return render_template('index.html', lista_ips="", t_espera_data="")

@app.route('/costos')
def cargar_costos():
    print "Entro en costos"
    lista_resultado = objconsulta.costos_x_ciudad()
    lista_ciudades = objconsulta.costos_get_ciudad()
    logging.info(lista_resultado)
    return render_template('costos.html', lista_ips="", t_espera_data=lista_resultado, lista_ciudades=lista_ciudades)

@app.route('/costos', methods=['POST'])
def get_costos():
    print "Entro en get costos"
    print request.form["city1"]
    print request.form["city2"]
    if request.form['radiotipo']=="dos_ciudades":
        lista_resultado = objconsulta.costos_x_ciudades(request.form["city1"], request.form["city2"])
    else:
        lista_resultado = objconsulta.costos_x_ciudad()

    lista_ciudades = objconsulta.costos_get_ciudad()
    logging.info(lista_resultado)
    return render_template('costos.html', t_espera_data=lista_resultado, lista_ciudades=lista_ciudades)

@app.route('/costosmes')
def cargar_costos_mes():
    print "Entro en costos mes"
    lista_resultado = objconsulta.costos_mes("2006", "Cali")
    lista_ciudades = objconsulta.costos_get_ciudad()
    logging.info(lista_resultado)
    return render_template('costos_mes.html', t_espera_data=lista_resultado, lista_ciudades=lista_ciudades)

@app.route('/costosmes', methods=['POST'])
def get_costos_mes():
    print "Entro en get costos mes"
    lista_resultado = objconsulta.costos_mes(request.form["periodo"], request.form["city1"])
    lista_ciudades = objconsulta.costos_get_ciudad()
    logging.info(lista_resultado)
    return render_template('costos_mes.html', t_espera_data=lista_resultado, lista_ciudades=lista_ciudades)

if __name__ == '__main__':
    # CONFIGURACION PARA LOG
    logging.basicConfig(filename=LOG_FILE,\
                        level=logging.INFO,\
                        format='%(levelname)s[%(asctime)s]: %(message)s',\
                        datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w')  # Cambiar a "filemode=a"
    objconsulta = Consulta()
    app.run(host='0.0.0.0', debug=True, port=8081, use_reloader=True)
