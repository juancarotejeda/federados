import os
from fpdf import FPDF

              
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
      
def imprimir_info(cur,parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,cuota,region,geolocalizacion,id_factura):
      return 
    
def imprimir_finanzas(cur,parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,diario,id_factura):
    return 

def imprimir_lista(cur,parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,cuotas_hist,id_factura):
   
    return  
     
def imprimir_miembros(cur,parada,fecha,direccion,provincia,municipio,pre_p,pre_f,cantidad,titulo,miembros,id_factura):
      
        return 
    
    

