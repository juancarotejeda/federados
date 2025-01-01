import os
from fpdf import FPDF
from pathlib import Path

def check_parada(cur,parada):
    cur.execute(f"SELECT autorizar FROM tabla_index WHERE nombre = '{parada}' ")
    check=cur.fetchall()
    for valor in check:
        if valor[0] == 'autorizada':
            return True
        else: 
            return False
    
def listado_paradas(cur):
    cur.execute("SELECT nombre FROM tabla_index")  
    db_paradas=cur.fetchall()     
    return db_paradas

def info_parada(cur,parada):
    cur.execute(f"SELECT codigo,nombre,direccion,municipio,provincia,zona,cuota,pago,banco,num_cuenta,federacion,geolocalizacion FROM  tabla_index  WHERE nombre='{parada}'" )
    infos=cur.fetchall()     
    return infos

def info_cabecera(cur,parada):          
    cur.execute(f'SELECT nombre FROM {parada}')
    seleccion=cur.fetchall()
    cant=len(seleccion)  
    presidente = []       
    cur.execute(f"SELECT nombre FROM {parada}  WHERE funcion = 'Presidente'")   
    press=cur.fetchone()
    if press != None:  
     for pres in press:   
        presidente=pres
    else:     
       presidente='No disponible'            
    return cant,presidente                
     
def lista_miembros(cur,parada):
    listas=[]
    cur.execute(f"SELECT id,nombre,cedula,telefono,funcion  FROM {parada}")
    miembros=cur.fetchall()
    for miembro in miembros:     
        listas+=miembro    
    lista=dividir_lista(listas,5)    
    return lista
    
def diario_general(cur,parada):
    if parada !=[]:
        prestamos=[]
        ingresos=[]
        gastos=[]
        aporte=[]
        pendiente=[]
        abonos=[]
        balance_bancario=[]
        cur.execute(f"SELECT  prestamos, ingresos, gastos, aporte, pendiente, abonos, balance_banco FROM tabla_index WHERE nombre='{parada}' " )  
        consult=cur.fetchall()
        for valor in consult:
            prestamos=valor[0]
            ingresos=valor[1]
            gastos=valor[2]
            aporte=valor[3]
            pendiente=valor[4]
            abonos=valor[5]
        balance_bancario=valor[6]
        balance=(aporte + ingresos + abonos )-(gastos+prestamos)
        data=(balance,prestamos,ingresos,gastos,aporte,pendiente,abonos,balance_bancario)   
        return data
    else:
        return []



def diario_general_pdf(cur,parada):
    if parada !=[]:
        prestamos=[]
        ingresos=[]
        gastos=[]
        aporte=[]
        pendiente=[]
        abonos=[]
        balance_bancario=[]
        cur.execute(f"SELECT  prestamos, ingresos, gastos, aporte, pendiente, abonos, balance_banco FROM tabla_index WHERE nombre='{parada}' " )  
        consult=cur.fetchall()
        for valor in consult:
            prestamos=valor[0]
            ingresos=valor[1]
            gastos=valor[2]
            aporte=valor[3]
            pendiente=valor[4]
            abonos=valor[5]
        balance_bancario=valor[6]
        balance=(aporte + ingresos + abonos )-(gastos+prestamos)
        var1='1','Balance Anterior','0.00 RD$'
        var2='2','Aporte por Cuotas',f'{aporte} RD$'
        var3='3','Ingresos Externos',f'{ingresos} RD$'
        var4='4','Abonos a Prestamos',f'{abonos} RD$'
        var5='5','Prestamos a Asociados',f'{prestamos} RD$'
        var6='6','Gastos  Incurridos',f'{gastos} RD$'
        var7='7','Cuotas no Pagadas',f'{pendiente} RD$'
        var8='8','Balance General',f'{balance} RD$'
        var9='9','Balance Bancario',f'{balance_bancario} RD$'
           
        return var1,var2,var3,var4,var5,var6,var7,var8,var9
    else:
        return []


def pendiente_aport(cur,parada):
        var1=[]
        var2=[]
        cur.execute(f"SHOW TABLES LIKE '{parada}_cuota'")
        vericar=cur.fetchall()
        if vericar !=[]:
            vgral=[]
            cur.execute(f"SELECT nombre FROM {parada}")
            list_nomb=cur.fetchall()
            for nombre in list_nomb:
                cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' and nombre='{nombre[0]}'") 
                var_x = cur.fetchall()
                for var_p in var_x:
                    var1=var_p[0]
                cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' and nombre='{nombre[0]}'")
                var_z = cur.fetchall()
                for var_n in var_z:
                    var2=var_n[0]   
                sub_t=var1+var2
                if sub_t != 0 :    
                    avg=round((var1/sub_t)*100,2)
                else:
                    avg = 0.00               
                vgral+=(nombre[0],var1,var2,sub_t,avg) 
            list_1=dividir_lista(vgral,5)                    
            return list_1
        else:
           return [] 



def lista_prestamos(cur,parada):
        cur.execute(f"SHOW TABLES LIKE '{parada}_prestamos'")
        verificar=cur.fetchall()
        if verificar !=[]:
            cur.execute(f"SELECT prestamo_a FROM {parada}_prestamos")
            nombres=cur.fetchall()
            return nombres
        return []



def dividir_lista(lista,lon) : 
    return [lista[n:n+lon] for n in range(0,len(lista),lon)]     


def aportacion(cur,parada):           
    cur.execute(f"SELECT codigo, nombre, cedula, telefono, funcion FROM {parada}")
    data=cur.fetchall()
    return data
  
def verif_p(cur,parada,cedula):
    cur.execute(f"SELECT * FROM {parada} WHERE  cedula = '{cedula}'")                                       
    accounts =cur.fetchall()
    if accounts != []:
         return True
    else:
         return False 
     
def nombres_miembro(cur,parada):
        listado=[]
        cur.execute(f"SELECT nombre FROM {parada} ")
        nombres=cur.fetchall()
        for nombre in nombres:
            listado += nombre
        return listado 
    
def info_personal(cur,parada,cedula):
    if parada !=[] and cedula !=[] :
      nombre = []
      cur.execute(f"SELECT nombre FROM {parada} WHERE cedula='{cedula}'")   
      nombres=cur.fetchall()
      for nombre in nombres: 
       return nombre[0]
    else:
      return []  


    
def dat_miembros(cur,parada,miembro):
    cur.execute(f"SELECT nombre,cedula,telefono,funcion FROM {parada} WHERE nombre='{miembro}'")
    listado=cur.fetchall()
    return listado

def vef_cedula(cur,cedula):
  lista_paradas=[]  
  cur.execute("SELECT nombre FROM tabla_index")  
  db_paradas=cur.fetchall()    
  for parada in db_paradas:
      lista_paradas+=parada   
  for parada in lista_paradas:
      cur.execute(f"SELECT nombre FROM {parada} WHERE cedula='{cedula}'")
      nombre=cur.fetchall()
      if nombre !=[]:            
        return parada             
  return []  

def vef_cedula_federado(cur,password):
  lista_paradas=[]    
  cur.execute(f"SELECT funcion FROM administracion WHERE password='{password}'")
  funcion=cur.fetchall()
  if funcion !=[]:
      if password=="intrant":
         cur.execute(f"SELECT nombre FROM tabla_index")  
         db_paradas=cur.fetchall()    
         for parada in db_paradas:
            lista_paradas+=parada              
         return lista_paradas  
      else:     
         cur.execute(f"SELECT nombre FROM tabla_index WHERE municipio='{password}'")  
         db_paradas=cur.fetchall()    
         for parada in db_paradas:
            lista_paradas+=parada              
         return lista_paradas             
  return []   

   
       
def imprimir_info(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,cuota,region,geolocalizacion):
        os.makedirs(f'static/pdf/pdf_{parada}', exist_ok=True)
        pdf = FPDF()
        pdf = FPDF(orientation='P',unit='mm',format='Letter')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('arial', '', 13.0)
        pdf.set_xy(50.0, 8.0)
        pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt=f'{titulo}', border=0)
        pdf.set_line_width(0.0)
        pdf.image('static/imagenes/logo-motoben.jpg', 20.0, 17.0, link='', type='', w=30.0, h=30.0)
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(50.0, 21.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
        pdf.set_font('arial', 'B', 12.0) 
        pdf.set_xy(115.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
        pdf.set_xy(135.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=f'{fecha}', border=0)
        pdf.set_font('arial', 'B', 14.0)
        pdf.set_xy(115.0, 31.0)
        pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='N\xba: ', border=0)
        pdf.set_xy(135.0, 31.0)
        pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
        pdf.set_font('arial', 'B', 12.0)
        pdf.set_xy(18.0, 48)
        pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt='GRUPO ACTEC', border=0)    
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(0.0, 53.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Tecnologia 4.0', border=0)
        pdf.set_font('arial', '', 12.0)        
        pdf.set_line_width(0.0)
        pdf.line(15.0, 57.0, 185.0, 57.0)
        pdf.set_font('arial', 'B', 10.0)
        pdf.set_xy(17.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='PARADA:', border=0)
        pdf.set_xy(45.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=f'{parada}', border=0)
        pdf.set_xy(17.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='PRESIDENTE:', border=0)
        pdf.set_xy(45.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=f'{pre_p}', border=0)
        pdf.set_xy(17.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='MUNICIPIO:', border=0)
        pdf.set_xy(45.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=f'{municipio}', border=0)
        pdf.set_xy(17.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='DIRECCION:', border=0)
        pdf.set_xy(45.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=f'{direccion}', border=0)    
        pdf.set_xy(17.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt='PROVINCIA:', border=0)
        pdf.set_xy(45.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt=f'{provincia}', border=0)
        pdf.set_xy(17.0, 85.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='fEDERACION:', border=0)
        pdf.set_xy(45.0, 85.0)
        pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt=f'{pre_f}', border=0)
        pdf.set_xy(17.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='MIEMBROS:', border=0)
        pdf.set_xy(45.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{miembros}', border=0)       
        pdf.set_xy(17.0, 95.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='CUOTAS:', border=0)
        pdf.set_xy(45.0, 95.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{cuota}', border=0)
        pdf.set_xy(17.0, 100.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='REGION:', border=0)
        pdf.set_xy(45.0, 100.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{region}', border=0)       
        pdf.set_xy(17.0, 105.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='GEOLUGAR:', border=0)
        pdf.set_xy(45.0, 105.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{geolocalizacion}', border=0)  
                  
        pdf.output(f"static/pdf/pdf_{parada}/informacion_{fecha}.pdf", 'F')    

    


def imprimir_finanzas(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,diario):
        os.makedirs(f'static/pdf/pdf_{parada}', exist_ok=True)
        pdf = FPDF()
        pdf = FPDF(orientation='P',unit='mm',format='Letter')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('arial', '', 13.0)
        pdf.set_xy(50.0, 8.0)
        pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt=f'{titulo}', border=0)
        pdf.set_line_width(0.0)
        pdf.image('static/imagenes/logo-motoben.jpg', 20.0, 17.0, link='', type='', w=30.0, h=30.0)
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(50.0, 21.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
        pdf.set_font('arial', 'B', 12.0) 
        pdf.set_xy(115.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
        pdf.set_xy(135.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=f'{fecha}', border=0)
        pdf.set_font('arial', 'B', 14.0)
        pdf.set_xy(115.0, 31.0)
        pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='N\xba: ', border=0)
        pdf.set_xy(135.0, 31.0)
        pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
        pdf.set_font('arial', 'B', 12.0)
        pdf.set_xy(18.0, 48)
        pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt='GRUPO ACTEC', border=0)    
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(0.0, 53.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Tecnologia 4.0', border=0)
        pdf.set_font('arial', '', 12.0)        
        pdf.set_line_width(0.0)
        pdf.line(15.0, 57.0, 185.0, 57.0)
        pdf.set_font('arial', 'B', 10.0)
        pdf.set_xy(17.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='PARADA:', border=0)
        pdf.set_xy(45.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=f'{parada}', border=0)
        pdf.set_xy(17.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='PRESIDENTE:', border=0)
        pdf.set_xy(45.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=f'{pre_p}', border=0)
        pdf.set_xy(17.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='MUNICIPIO:', border=0)
        pdf.set_xy(45.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=f'{municipio}', border=0)
        pdf.set_xy(17.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='DIRECCION:', border=0)
        pdf.set_xy(45.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=f'{direccion}', border=0)    
        pdf.set_xy(17.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt='Provincia:', border=0)
        pdf.set_xy(45.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt=f'{provincia}', border=0)
        pdf.set_xy(115.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='Federacion:', border=0)
        pdf.set_xy(135.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt=f'{pre_f}', border=0)
        pdf.set_line_width(0.0)
        pdf.line(15.0, 88.0, 185.0, 88.0)
        pdf.set_xy(17.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='Numero de miembros:', border=0)
        pdf.set_xy(65.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{miembros}', border=0)
        pdf.set_xy(92.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=43.0, txt='Per\xedodo Facturado', border=0)
        pdf.set_xy(125.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{fecha}', border=0)
        pdf.set_xy(150.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='', border=0)        
        pdf.set_line_width(0.0)
        pdf.line(15.0, 95.0, 185.0, 95.0)
        pdf.set_font('arial', '', 11.0)
        pdf.set_xy(15.0,95.0)
        pdf.cell(w=35.0, h=10.0, txt='ITEM',border=1,ln=0,align='C',fill=0)
        pdf.cell(w=90.0, h=10.0, txt='TIPO DE ACTIVIDAD',border=1,ln=0,align='C',fill=0)
        pdf.multi_cell(w=45.0, h=10.0, txt='TOTAL AL MOMENTO',border=1,align='C',fill=0)       
        for valor in diario :
                pdf.set_x(15)
                pdf.cell(w=35.0,h= 10.0, txt=(valor[0]),border=1,ln=0,align='C',fill=0)
                pdf.cell(w=90.0, h=10.0,txt=str(valor[1]),border=1,ln=0,align='L',fill=0)
                pdf.multi_cell(w=45.0, h=10.0,txt=str(valor[2]),border=1,align='C',fill=0)            
        pdf.output(f"static/pdf/pdf_{parada}/finanzas_{fecha}.pdf", 'F')    



def imprimir_lista(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,cuotas_hist):
    os.makedirs(f'static/pdf/pdf_{parada}', exist_ok=True)
    pdf = FPDF()
    pdf = FPDF(orientation='P',unit='mm',format='Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('arial', '', 13.0)
    pdf.set_xy(50.0, 8.0)
    pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt=f'{titulo}', border=0)
    pdf.set_line_width(0.0)
    pdf.image('static/imagenes/logo-motoben.jpg', 20.0, 17.0, link='', type='', w=30.0, h=30.0)
    pdf.set_font('arial', '', 8.0)
    pdf.set_xy(50.0, 21.0)
    pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
    pdf.set_font('arial', 'B', 12.0) 
    pdf.set_xy(115.0, 25.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
    pdf.set_xy(135.0, 25.0)
    pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=f'{fecha}', border=0)
    pdf.set_font('arial', 'B', 14.0)
    pdf.set_xy(115.0, 31.0)
    pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='N\xba: ', border=0)
    pdf.set_xy(135.0, 31.0)
    pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
    pdf.set_font('arial', 'B', 12.0)
    pdf.set_xy(18.0, 48)
    pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt='GRUPO ACTEC', border=0)    
    pdf.set_font('arial', '', 8.0)
    pdf.set_xy(0.0, 53.0)
    pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Tecnologia 4.0', border=0)
    pdf.set_font('arial', '', 12.0)        
    pdf.set_line_width(0.0)
    pdf.line(15.0, 57.0, 185.0, 57.0)
    pdf.set_font('arial', 'B', 10.0)
    pdf.set_xy(17.0, 59.0)
    pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='PARADA:', border=0)
    pdf.set_xy(45.0, 59.0)
    pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=f'{parada}', border=0)
    pdf.set_xy(17.0, 64.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='PRESIDENTE:', border=0)
    pdf.set_xy(45.0, 64.0)
    pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=f'{pre_p}', border=0)
    pdf.set_xy(17.0, 69.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='MUNICIPIO:', border=0)
    pdf.set_xy(45.0, 69.0)
    pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=f'{municipio}', border=0)
    pdf.set_xy(17.0, 74.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='DIRECCION:', border=0)
    pdf.set_xy(45.0, 74.0)
    pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=f'{direccion}', border=0)    
    pdf.set_xy(17.0, 80.0)
    pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt='Provincia:', border=0)
    pdf.set_xy(45.0, 80.0)
    pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt=f'{provincia}', border=0)
    pdf.set_xy(115.0, 80.0)
    pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='Federacion:', border=0)
    pdf.set_xy(135.0, 80.0)
    pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt=f'{pre_f}', border=0)
    pdf.set_line_width(0.0)
    pdf.line(15.0, 88.0, 185.0, 88.0)
    pdf.set_xy(17.0, 90.0)
    pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='Numero de miembros:', border=0)
    pdf.set_xy(65.0, 90.0)
    pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{miembros}', border=0)
    pdf.set_xy(92.0, 90.0)
    pdf.cell(ln=0, h=5.0, align='L', w=43.0, txt='Per\xedodo Facturado', border=0)
    pdf.set_xy(125.0, 90.0)
    pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{fecha}', border=0)
    pdf.set_xy(150.0, 90.0)
    pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='', border=0)        
    pdf.set_line_width(0.0)
    pdf.line(15.0, 95.0, 185.0, 95.0)
    pdf.set_font('arial', '', 11.0)
    pdf.set_xy(15.0,95.0)
    pdf.cell(w=70.0, h=10.0, txt='NOMBRE DEL ASOCIADO',border=1,ln=0,align='C',fill=0)
    pdf.cell(w=25.0, h=10.0, txt='APORTES',border=1,ln=0,align='C',fill=0)
    pdf.cell(w=25.0, h=10.0,txt= 'PEDIENTES',border=1,ln=0,align='C',fill=0)
    pdf.cell(w=25.0, h=10.0, txt='TOTAL',border=1,align='C',fill=0) 
    pdf.multi_cell(w=25.0, h=10.0, txt='%',border=1,align='C',fill=0)       
    for valor in cuotas_hist :
            pdf.set_x(15)
            pdf.cell(w=70.0,h= 10.0, txt=(valor[0]),border=1,ln=0,align='C',fill=0)
            pdf.cell(w=25.0, h=10.0,txt=str(valor[1]),border=1,ln=0,align='L',fill=0)
            pdf.cell(w=25.0, h=10.0,txt=str(valor[2]),border=1,ln=0,align='C',fill=0)
            pdf.cell(w=25.0, h=10.0,txt=str(valor[3]),border=1,ln=0,align='C',fill=0)
            pdf.multi_cell(w=25.0, h=10.0,txt=str(valor[4]),border=1,align='C',fill=0)            
    pdf.output(f"static/pdf/pdf_{parada}/historial_{fecha}.pdf", 'F')    
  


   
def imprimir_miembros(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,cantidad,titulo,miembros):
        os.makedirs(f'static/pdf/pdf_{parada}', exist_ok=True)
        pdf = FPDF()
        pdf = FPDF(orientation='P',unit='mm',format='Letter')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('arial', '', 13.0)
        pdf.set_xy(50.0, 8.0)
        pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt=f'{titulo}', border=0)
        pdf.set_line_width(0.0)
        pdf.image('static/imagenes/logo-motoben.jpg', 20.0, 17.0, link='', type='', w=30.0, h=30.0)
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(50.0, 21.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
        pdf.set_font('arial', 'B', 12.0) 
        pdf.set_xy(115.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
        pdf.set_xy(135.0, 25.0)
        pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=f'{fecha}', border=0)
        pdf.set_font('arial', 'B', 14.0)
        pdf.set_xy(115.0, 31.0)
        pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='N\xba: ', border=0)
        pdf.set_xy(135.0, 31.0)
        pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
        pdf.set_font('arial', 'B', 12.0)
        pdf.set_xy(18.0, 48)
        pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt='GRUPO ACTEC', border=0)    
        pdf.set_font('arial', '', 8.0)
        pdf.set_xy(0.0, 53.0)
        pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Tecnologia 4.0', border=0)
        pdf.set_font('arial', '', 12.0)        
        pdf.set_line_width(0.0)
        pdf.line(15.0, 57.0, 185.0, 57.0)
        pdf.set_font('arial', 'B', 10.0)
        pdf.set_xy(17.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='PARADA:', border=0)
        pdf.set_xy(45.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=f'{parada}', border=0)
        pdf.set_xy(17.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='PRESIDENTE:', border=0)
        pdf.set_xy(45.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=f'{pre_p}', border=0)
        pdf.set_xy(17.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='MUNICIPIO:', border=0)
        pdf.set_xy(45.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=f'{municipio}', border=0)
        pdf.set_xy(17.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='DIRECCION:', border=0)
        pdf.set_xy(45.0, 74.0)
        pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=f'{direccion}', border=0)    
        pdf.set_xy(17.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt='Provincia:', border=0)
        pdf.set_xy(45.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt=f'{provincia}', border=0)
        pdf.set_xy(115.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='Federacion:', border=0)
        pdf.set_xy(135.0, 80.0)
        pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt=f'{pre_f}', border=0)
        pdf.set_line_width(0.0)
        pdf.line(15.0, 88.0, 185.0, 88.0)
        pdf.set_xy(17.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='Numero de miembros:', border=0)
        pdf.set_xy(65.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{cantidad}', border=0)
        pdf.set_xy(92.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=43.0, txt='Per\xedodo Facturado', border=0)
        pdf.set_xy(125.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=f'{fecha}', border=0)
        pdf.set_xy(150.0, 90.0)
        pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='', border=0)        
        pdf.set_line_width(0.0)
        pdf.line(15.0, 95.0, 185.0, 95.0)
        pdf.set_font('arial', '', 11.0)
        pdf.set_xy(15.0,95.0)
        pdf.cell(w=15.0, h=10.0,txt= 'ITEM',border=1,ln=0,align='C',fill=0)
        pdf.cell(w=70.0, h=10.0, txt='NOMBRE DEL ASOCIADO',border=1,ln=0,align='C',fill=0)
        pdf.cell(w=30.0, h=10.0, txt='CEDULA',border=1,ln=0,align='C',fill=0)
        pdf.cell(w=30.0, h=10.0, txt='TELEFONO',border=1,align='C',fill=0) 
        pdf.multi_cell(w=30.0, h=10.0, txt='FUNCION',border=1,align='C',fill=0)       
        for valor in miembros:
                pdf.set_x(15)
                pdf.cell(w=15.0,h= 10.0, txt=str(valor[0]),border=1,ln=0,align='C',fill=0)
                pdf.cell(w=70.0, h=10.0,txt=str(valor[1]),border=1,ln=0,align='L',fill=0)
                pdf.cell(w=30.0, h=10.0,txt=str(valor[2]),border=1,ln=0,align='C',fill=0)
                pdf.cell(w=30.0, h=10.0,txt=str(valor[3]),border=1,ln=0,align='C',fill=0)
                pdf.multi_cell(w=30.0, h=10.0,txt=str(valor[4]),border=1,align='C',fill=0)                  
        pdf.output(f"static/pdf/pdf_{parada}/listado_{fecha}.pdf",'F')   
        return