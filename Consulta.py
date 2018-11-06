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

	def costos_x_ciudad(self):
		try:
			self.cur.execute('select ips.municipio as mun, fec."year" as año, sum(form.precio_total) as total from fact_formula_medica as form, dim_fecha as fec, dim_medico as med,dim_ips as ips '+\
								'where form.key_date=fec.key_date and form.key_medico=med.key_medico and med.id_ips=ips.id_ips '+\
								'group by mun,año '+\
								'order by mun')
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

	def costos_get_ciudad(self):
		try:
			self.cur.execute('select distinct(ips.municipio) as mun from fact_formula_medica as form, dim_fecha as fec, dim_medico as med,dim_ips as ips '+\
								'where form.key_date=fec.key_date and form.key_medico=med.key_medico and med.id_ips=ips.id_ips order by mun')
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

	def costos_x_ciudades(self, ciudad1, ciudad2):
		try:
			self.cur.execute(
				'select ips.municipio as mun, fec."year" as año, sum(form.precio_total) as total from fact_formula_medica as form, dim_fecha as fec, dim_medico as med,dim_ips as ips ' + \
				'where form.key_date=fec.key_date and form.key_medico=med.key_medico and med.id_ips=ips.id_ips ' + \
				'and (ips.municipio=' + "'" + ciudad1 + "'" + " or ips.municipio='" + ciudad2 + "'" + ') ' + \
				'group by mun,año ' + \
				'order by mun')
			rows = self.cur.fetchall()
			return rows
		except psycopg2.DatabaseError, e:
			logging.error("Fallo en la consulta")
			logging.error("Error: " + str(e))
			sys.exit(1)
		except psycopg2.InterfaceError, ie:
			logging.error("Fallo en la consulta, se ha cerrado la conexion")
			logging.error("Error: " + str(ie))
			sys.exit(1)

	def costos_mes(self, periodo, ciudad):
		try:
			self.cur.execute('with mat_age as ( '+\
					'select fec.month_short_label_eng as mes, fec."month" as mesn, date_part('+"'year'"+', age(per.fecha_nacimiento)) as mage, sum(form.precio_total) as total '+\
					'from fact_formula_medica as form, dim_fecha as fec, dim_persona as per, dim_medico as med,dim_ips as ips '+\
					'where form.key_date=fec.key_date and form.key_persona=per.key_persona and form.key_medico=med.key_medico and med.id_ips=ips.id_ips '+\
					'and fec."year"='+periodo+' '+\
					'and ips.municipio='+"'"+ciudad+"' "+\
					'group by mesn, mes,mage) '+\
					'select '+\
					  'mesn, mes, '+\
					  'sum(total) filter (where mage<20) as "age<20", '+\
					  'sum(total) filter (where mage>=20 and mage<30) as "20<age<30", '+\
					  'sum(total) filter (where mage>=30 and mage<50) as "30<age<50", '+\
					  'sum(total) filter (where mage>=50) as "50<age" '+\
					'from '+\
					  'mat_age '+\
					  'group by mesn, mes '+\
					  'order by mesn')
			rows = self.cur.fetchall()
			return rows
		except psycopg2.DatabaseError, e:
			logging.error("Fallo en la consulta")
			logging.error("Error: " + str(e))
			sys.exit(1)
		except psycopg2.InterfaceError, ie:
			logging.error("Fallo en la consulta, se ha cerrado la conexion")
			logging.error("Error: " + str(ie))
			sys.exit(1)

