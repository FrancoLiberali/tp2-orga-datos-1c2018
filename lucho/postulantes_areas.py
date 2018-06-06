import csv
posts = {}
cols = []
with open('/home/luciano/orga-datos/tmp/postulantes_v2.csv') as e:
    rdr = csv.reader(e)
    cols = next(rdr)
    for fila in rdr:
        posts[fila[0]] = list(map(float, fila[1:]))
    
avisos = {}
with open('/home/luciano/orga-datos/datos_preprocesados/fiuba_6_avisos_detalle.csv') as e:
    rdr = csv.DictReader(e)
    for fila in rdr:
        avisos[fila['idaviso']] = fila['nombre_area']

cols = {k:v for v,k in enumerate(cols)}


with open('/home/luciano/orga-datos/datos_preprocesados/fiuba_4_postulaciones.csv') as e:
    rdr = csv.DictReader(e)
    for fila in rdr:
        idaviso, idpostulante = fila['idaviso'], fila['idpostulante']
        if not idaviso in avisos or not idpostulante in posts:
            continue
        area = avisos[idaviso]
        posts[idpostulante][cols['nombre_area_' + area] - 1] += 2 # Una postulación pesa 2

        
with open('/home/luciano/orga-datos/datos_preprocesados/fiuba_3_vistas.csv') as e:
    rdr = csv.DictReader(e)
    for fila in rdr:
        idaviso, idpostulante = fila['idAviso'], fila['idpostulante']
        if not idaviso in avisos or not idpostulante in posts:
            continue
        area = avisos[idaviso]
        posts[idpostulante][cols['nombre_area_' + area] - 1] += 1 # Una vista pesa 1

        
columns = ['idpostulante'] + ['' for c in cols]
for c in cols:
    columns[cols[c]] = c
    
with open('/home/luciano/orga-datos/tmp/postulantes_v2.csv', 'w') as salida:
    wrt = csv.writer(salida)
    wrt.writerow(columns[:-1])
    for idpostulante in posts:
        row = [idpostulante] + posts[idpostulante]
        wrt.writerow(row)