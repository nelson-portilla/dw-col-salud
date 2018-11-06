select ips.municipio as mun, fec."year" as anno, sum(form.precio_total) as total 
from fact_formula_medica as form, dim_fecha as fec, dim_medico as med,dim_ips as ips
where form.key_date=fec.key_date and form.key_medico=med.key_medico and med.id_ips=ips.id_ips
and (ips.municipio='Cali' or ips.municipio='Yumbo')
group by mun,anno
order by mun


select distinct(ips.municipio) as mun from fact_formula_medica as form, dim_fecha as fec, dim_medico as med,dim_ips as ips
where form.key_date=fec.key_date and form.key_medico=med.key_medico and med.id_ips=ips.id_ips

select distinct("year") from fact_formula_medica natural join dim_fecha

with mat_age as (
  select fec.month_short_label_eng as mes, fec."month" as mesn, date_part('year', age(per.fecha_nacimiento)) as mage, sum(form.precio_total) as total
  from fact_formula_medica as form, dim_fecha as fec, dim_persona as per, dim_medico as med,dim_ips as ips
where form.key_date=fec.key_date and form.key_persona=per.key_persona and form.key_medico=med.key_medico and med.id_ips=ips.id_ips
and fec."year"=2008
and ips.municipio='Medellin'
group by mesn, mes,mage
)
select
mesn,
  mes,
  sum(total) filter (where mage<20) as "age<20",
  sum(total) filter (where mage>=20 and mage<30) as "20<age<30",
  sum(total) filter (where mage>=30 and mage<50) as "30<age<50",
  sum(total) filter (where mage>=50) as "50<age"
from
  mat_age
  group by mesn,mes
  order by mesn