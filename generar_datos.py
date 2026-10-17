"""Genera 600 registros sintéticos reproducibles de activos TI (sin datos reales)."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)
empresas = ['CRESPO', 'MURUHUAY', 'ARUNTANI', 'ANABI', 'APUMAYO']
sedes = ['Lima', 'Arequipa', 'Cusco', 'Piura', 'Trujillo']
tipos = ['Laptop', 'Desktop', 'Monitor', 'Impresora', 'Servidor', 'Tablet']
marcas = {'Laptop':['Dell','HP','Lenovo'], 'Desktop':['Dell','HP','Lenovo'], 'Monitor':['Samsung','LG','Dell'], 'Impresora':['Epson','HP','Brother'], 'Servidor':['Dell','HPE','Lenovo'], 'Tablet':['Samsung','Lenovo','Apple']}
costos = {'Laptop':(1800,6500), 'Desktop':(1500,4500), 'Monitor':(450,1800), 'Impresora':(400,4200), 'Servidor':(7000,30000), 'Tablet':(650,3700)}
estados = ['Asignado','Disponible','Resguardo TI','En tránsito','De baja']
modalidades = ['Propio','Alquiler','Renting']
base = date(2026, 10, 1)
rows=[]
for i in range(1,601):
    tipo=random.choices(tipos,weights=[32,24,19,13,5,7],k=1)[0]
    estado=random.choices(estados,weights=[51,26,12,5,6],k=1)[0]
    modalidad=random.choices(modalidades,weights=[64,17,19],k=1)[0]
    fecha=base-timedelta(days=random.randint(20,2400))
    costo=round(random.uniform(*costos[tipo]),2)
    rows.append({'id_activo':f'ACT-{i:04d}','empresa':random.choice(empresas),'sede':random.choice(sedes),'tipo_activo':tipo,'marca':random.choice(marcas[tipo]),'estado':estado,'modalidad':modalidad,'fecha_adquisicion':fecha.isoformat(),'costo_soles':f'{costo:.2f}','responsable':f'COL-{random.randint(1,230):04d}' if estado=='Asignado' else 'SIN ASIGNAR'})
output=Path(__file__).with_name('activos_ti.csv')
with output.open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys())
    writer.writeheader();writer.writerows(rows)
print(f'Datos sintéticos creados: {len(rows)} registros en {output}')
