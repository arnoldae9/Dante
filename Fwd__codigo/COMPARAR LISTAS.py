import numpy as np
import pandas as pd

hoja_excel = pd.read_excel("basecfdis.xlsx", sheet_name="Hoja1")

df = hoja_excel
valores = df [["RfcReceptor"]]


hoja_excel2 = pd.read_excel("69-b.xlsx", sheet_name="69-B")

df2 = hoja_excel2
#print(df2)

#df2['check']=valores.RfcReceptor.isin(df2.RFC)
df2['check']=df2.RFC.isin(valores.RfcReceptor)
print(df2)
#print(df2['check'].value_counts())

#print(df2.loc[df2.check == True,'RFC'])
filtrados = df2[(df2['check'] == True)]
#print(filtrados)
#filtrados.to_csv('coincidencias.csv')

definitivos =  filtrados[(filtrados['Situación del contribuyente'] == 'Definitivo')]
#print(definitivos)
#print(defin)

filtrado = hoja_excel[(hoja_excel['EfectoComprobante'] == 'Ingreso') & (hoja_excel['EstadoComprobante'] == "Vigente")]
grupos = filtrado.groupby(['RfcReceptor'])
total = grupos.apply(lambda x: x[(x['EfectoComprobante'] == 'Ingreso') & (x['EstadoComprobante'] == "Vigente")]['Total'].sum())
total_ordenado = sorted(total.items(), key=lambda x: x[1], reverse=True)

n = len(pd.unique(filtrado['RfcReceptor']))
#print(n)

TOP = n

rfcs_unicos = grupos.groups.keys()
registro_rfcs = {}

for rfc in rfcs_unicos:
    columna_razon = filtrado.groupby("RfcReceptor").get_group(rfc)["NombreRazonSocialReceptor"].tolist()
    razon = columna_razon[0]
    registro_rfcs[rfc] = razon
matriz = []
for i in range(TOP):
    RFC = total_ordenado[i][0]
    total = total_ordenado[i][1]
    #print(f"{i+1}. {RFC} = ${total} {registro_rfcs[RFC]} ")
    matriz.append({'rfc': RFC, 'TOTAL': total, 'razon social': registro_rfcs[RFC]})

listado = pd.DataFrame(matriz)
#listado.to_csv('totales.csv')
#print(listado)
#print(defin)


listado['check']=listado.rfc.isin(definitivos.RFC)
print(listado)
#print(listado['check'].value_counts())
coincidencias = listado.loc[(listado.check == False),'check']
print(coincidencias)

#print(coincidencias.columns)
#coincidencias.to_csv('definitivos.csv')