select nombre, avg(tiempo_espera_minutos)
from fact_urgencias as urg join dim_ips
on dim_ips.key_ips=urg.key_ips
group by nombre
order by avg(tiempo_espera_minutos) desc