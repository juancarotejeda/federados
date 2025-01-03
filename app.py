import funciones,os,mysql.connector,random
from flask import Flask, render_template,flash, request,  redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key=os.getenv("APP_KEY")

DB_HOST =os.getenv('DB_HOST')
DB_USERNAME =os.getenv("DB_USERNAME")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_NAME =os.getenv("DB_NAME")

# Connect to the database
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME,
    autocommit=True
)

id_factura="MB"+str(random.randint(1000000,9999999))

@app.route("/")
def login():                     
    return render_template('login.html')

@app.route("/verificador", methods=["GUET","POST"])
def verificador(): 
   msg = ''   
   if request.method == 'POST':        
    password = request.form['password'] 
    cur =connection.cursor()
    paradas=funciones.vef_cedula_federado(cur,password) 
    if paradas!= []: 
            parada=[] 
            limites=[]                                                                     
            fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H")            
            informacion = funciones.info_parada(cur,parada)               
            diario = funciones.diario_general(cur,parada)  
            cuotas_hist = funciones.pendiente_aport(cur,parada)
            cur.close()  
            if password=='intrant' :
                limites='Tiene Acceso a todas las paradas del pais' 
            else:
                limites=f'Tiene Acceso a todas las paradas del municipio de {password}'             
            return render_template('index.html',informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas ,password=password,limites=limites)   
          
    else:
        msg = 'su password no esta registrado!'        
        flash(msg)           
        return redirect(url_for('login'))    
       
@app.route("/seleccion", methods=["GUET","POST"])
def seleccion(): 
   msg = ''   
   if request.method == 'POST': 
        global limites,password,paradas,fecha,informacion,miembros,diario,cuotas_hist,cabecera  
        parada = request.form['selector']
        password = request.form['password'] 
        limites = request.form['acceso']  
        fecha = datetime.strftime(datetime.now(),"%Y_%m_%d_%H") 
        cur =connection.cursor() 
        if parada!= []:
            if password == 'intrant': 
                paradas=funciones.vef_cedula_federado(cur,password)                                                                                      
                informacion = funciones.info_parada(cur,parada) 
                miembros=funciones.lista_miembros(cur,parada)              
                diario = funciones.diario_general(cur,parada)
                cuotas_hist = funciones.pendiente_aport(cur,parada)
                cabecera=funciones.info_cabecera(cur,parada)            
                cur.close()  
                #os.makedirs(f'pdfs/pdf_{parada}', exist_ok=True)         
                return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas,password=password,limites=limites)  
            else:
                paradas=funciones.vef_cedula_federado(cur,password)                                                                                      
                informacion = funciones.info_parada(cur,parada)  
                miembros=funciones.lista_miembros(cur,parada)             
                diario = funciones.diario_general(cur,parada)
                cuotas_hist = funciones.pendiente_aport(cur,parada)
                cabecera=funciones.info_cabecera(cur,parada)
                cur.close()
                #os.makedir(f'pdfs/pdf_{parada}', exist_ok=True)            
                return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas,password=password,limites=limites)                
        else:
            msg = 'su password no esta registrado!'        
            flash(msg)           
            return redirect(url_for('login'))      
        
@app.route('/informacion_pdf',methods=['GUEST','POST']) 
def informacion_pdf() :
       if request.method == 'POST': 
          titulo = request.form['titu']        
          parada = request.form['para']
          direccion=request.form['dirr']
          municipio=request.form['muni']
          provincia=request.form['prov']
          region=request.form['zona']
          cuota=request.form['apor']
          pre_p=request.form['prep']
          pre_f=request.form['pref'] 
          miembros=request.form['miem'] 
          geolocalizacion=request.form['geol']        
          funciones.imprimir_info(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,cuota,region,geolocalizacion,id_factura )
          return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas,password=password,limites=limites)    
                       
@app.route("/miembros_pdf",methods=['GUEST','POST'])
def miembros_pdf():  
    if request.method == 'POST': 
        titulo = request.form['titu']        
        parada = request.form['para']
        direccion=request.form['dirr']
        municipio=request.form['muni']
        provincia=request.form['prov']
        region=request.form['zona']
        aporte=request.form['apor']
        pre_p=request.form['prep']
        pre_f=request.form['pref'] 
        miembros=request.form['miem'] 
        geolocalizacion=request.form['geol']    
        cur =connection.cursor()  
        cuotas_hist = funciones.pendiente_aport(cur,parada) 
        cur.close()     
        funciones.imprimir_lista(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,cuotas_hist,id_factura )
        return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas,password=password,limites=limites)   

@app.route("/finanzas_pdf",methods=['GUEST','POST'])
def finanzas_pdf():  
    if request.method == 'POST': 
        titulo = request.form['titu']        
        parada = request.form['para']
        direccion=request.form['dirr']
        municipio=request.form['muni']
        provincia=request.form['prov']
        region=request.form['zona']
        aporte=request.form['apor']
        pre_p=request.form['prep']
        pre_f=request.form['pref'] 
        miembros=request.form['miem'] 
        geolocalizacion=request.form['geol']   
        cur =connection.cursor()
        diario = funciones.diario_general_pdf(cur,parada)
        cur.close()
        funciones.imprimir_finanzas(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,miembros,titulo,diario,id_factura )
        return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas,password=password,limites=limites) 

@app.route("/listado_pdf",methods=['GUEST','POST'])
def listado_pdf():  
    if request.method == 'POST': 
        titulo = request.form['titu']        
        parada = request.form['para']
        direccion=request.form['dirr']
        municipio=request.form['muni']
        provincia=request.form['prov']
        region=request.form['zona']
        aporte=request.form['apor']
        pre_p=request.form['prep']
        pre_f=request.form['pref'] 
        cantidad=request.form['miem'] 
        geolocalizacion=request.form['geol']   
        cur =connection.cursor()  
        miembros=funciones.lista_miembros(cur,parada)         
        funciones.imprimir_miembros(parada,fecha,direccion,provincia,municipio,pre_p,pre_f,cantidad,titulo,miembros,id_factura )
        return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas,password=password,limites=limites)    



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=7800)
