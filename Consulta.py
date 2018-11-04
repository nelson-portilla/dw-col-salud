#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import logging
import psycopg2
from datetime import datetime
from config.config import *
##CLASE PRINCIPAL
class Consulta(object):
	con = None
	cur = None
	"""docstring for Consulta"""
	def __init__(self):
		logging.info("Creando nuevo objeto Consulta")
		try:
			self.con = psycopg2.connect(host=HOST, database=DATABASE, user=USER)
			self.cur = self.con.cursor()
			self.cur.execute('SELECT version()')
			ver = self.cur.fetchone()
			logging.info("Conexion a base de datos exitosa "+str(HOST)+": "+str(ver))

		except psycopg2.DatabaseError, e:
			logging.error("Fallo en la conexion a base de datos, revise parametros de configuracion en config/config")
			logging.error("Error: "+str(e))
			sys.exit(1)


	##METODO PARA VERIFICAR SI UNA CEDULA EXISTE EN LA TABLA PACIENTES
	def dim_ips(self):
		try:
			self.cur.execute('select nombre,nivel from dim_ips limit 10')
			rows = self.cur.fetchall()
			return rows
		except psycopg2.DatabaseError, e:
			logging.error("Fallo en la consulta")
			logging.error("Error: "+str(e))
			sys.exit(1)
		except psycopg2.InterfaceError, ie:
			logging.error("Fallo en la consulta, se ha cerrado la conexion")
			logging.error("Error: "+str(ie))
			sys.exit(1)
