select per.sexo as sexo , avg(tiempo_espera_minutos)
from fact_urgencias as urg, dim_persona as per, dim_fecha as fecha
where urg.key_persona=per.key_persona and fecha.key_date=urg.key_fecha_atencion
and fecha."year">=2004
and fecha."year"<=2006
group by sexo
order by avg(tiempo_espera_minutos) desc

select per.estado_civil as estado_civil , avg(tiempo_espera_minutos)
from fact_urgencias as urg, dim_persona as per, dim_fecha as fecha
where urg.key_persona=per.key_persona and fecha.key_date=urg.key_fecha_atencion
and fecha."year">=2004
and fecha."year"<=2006
group by estado_civil
order by avg(tiempo_espera_minutos) desc

select per.tipo_usuario as estado_civil , avg(tiempo_espera_minutos)
from fact_urgencias as urg, dim_persona as per, dim_fecha as fecha
where urg.key_persona=per.key_persona and fecha.key_date=urg.key_fecha_atencion
and fecha."year">=2004
and fecha."year"<=2006
group by estado_civil
order by avg(tiempo_espera_minutos) desc