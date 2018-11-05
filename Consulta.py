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


	def t_espera_urgencias_ips(self, tiempo, fechain, fechaout, unidad):
		try:
			self.cur.execute('select nombre, avg('+tiempo+') '+\
					'from '+unidad+' as urg, dim_ips, dim_fecha as fecha '+\
					'where dim_ips.key_ips=urg.key_ips and fecha.key_date=urg.key_fecha_atencion '+\
					'and fecha."date">='+"'"+fechain+"'"+' '+\
					'and fecha."date"<='+"'"+fechaout+"'"+' '+\
					'group by nombre '+\
					'order by avg('+tiempo+') desc')
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

	def t_espera_urgencias_sexo(self, tiempo, fechain, fechaout, unidad):
		try:
			self.cur.execute('select per.sexo as sexo, avg('+tiempo+') '+\
					'from '+unidad+' as urg, dim_persona as per, dim_fecha as fecha '+\
					'where urg.key_persona=per.key_persona and fecha.key_date=urg.key_fecha_atencion '+\
					'and fecha."date">='+"'"+fechain+"'"+' '+\
					'and fecha."date"<='+"'"+fechaout+"'"+' '+\
					'group by sexo '+\
					'order by avg('+tiempo+') desc')
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


	def t_espera_urgencias_tipo_usuario(self, tiempo, fechain, fechaout, unidad):
		try:
			self.cur.execute('select per.tipo_usuario as tipo_usuario, avg('+tiempo+') '+\
					'from '+unidad+' as urg, dim_persona as per, dim_fecha as fecha '+\
					'where urg.key_persona=per.key_persona and fecha.key_date=urg.key_fecha_atencion '+\
					'and fecha."date">='+"'"+fechain+"'"+' '+\
					'and fecha."date"<='+"'"+fechaout+"'"+' '+\
					'group by tipo_usuario '+\
					'order by avg('+tiempo+') desc')
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


	def t_espera_urgencias_estado_civil(self, tiempo, fechain, fechaout, unidad):
		try:
			self.cur.execute('select per.estado_civil as estado_civil, avg('+tiempo+') '+\
					'from '+unidad+' as urg, dim_persona as per, dim_fecha as fecha '+\
					'where urg.key_persona=per.key_persona and fecha.key_date=urg.key_fecha_atencion '+\
					'and fecha."date">='+"'"+fechain+"'"+' '+\
					'and fecha."date"<='+"'"+fechaout+"'"+' '+\
					'group by estado_civil '+\
					'order by avg('+tiempo+') desc')
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

	def t_espera_urgencias_edad(self, tiempo, fechain, fechaout, unidad):
		try:
			self.cur.execute('with mat_age as '+\
					'(select ips.municipio as ciudad,date_part('+"'year'"+', age(per.fecha_nacimiento)) as mage, '+\
					'avg('+tiempo+') as tiempo_espera '+\
  					'from '+unidad+' as urg, dim_persona as per, dim_fecha as fecha,dim_ips as ips '+\
					'where per.key_persona=urg.key_persona and fecha.key_date=urg.key_fecha_atencion and urg.key_ips=ips.key_ips '+\
					'and fecha."date">='+"'"+fechain+"'"+' '+\
					'and fecha."date"<='+"'"+fechaout+"'"+' '+\
					'group by ciudad,mage '+\
					') '+\
					'select '+\
  					'ciudad, '+\
  					'avg(tiempo_espera) filter (where mage<20) as "edad<20", '+\
  					'avg(tiempo_espera) filter (where mage>=20 and mage<30) as "20<edad<30", '+\
 					'avg(tiempo_espera) filter (where mage>=30 and mage<50) as "30<edad<50", '+\
  					'avg(tiempo_espera) filter (where mage>=50) as "50<edad" '+\
					'from '+\
					'  mat_age '+\
					'  group by ciudad order by ciudad')
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