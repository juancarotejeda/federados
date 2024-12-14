import mysql.connector,funciones,os
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

@app.route("/")
def login():                     
    return render_template('login.html')

@app.route("/verificador", methods=["GUET","POST"])
def verificador(): 
   msg = ''   
   if request.method == 'POST':        
    password = request.form['password'] 
    print(password) 
    cur = connection.cursor() 
    paradas=funciones.vef_cedula_federado(cur,password) 
    print(paradas) 
    if paradas!= []: 
            parada=[]                                                                      
            fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H")            
            informacion = funciones.info_parada(cur,parada)               
            diario = funciones.diario_general(cur,parada)  
            cuotas_hist = funciones.pendiente_aport(cur,parada)
            cur.close()            
            return render_template('index.html',informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas ,password=password)   
          
    else:
        msg = 'su password no esta registrado!'        
        flash(msg)           
        return redirect(url_for('login'))    
    
    
@app.route("/seleccion", methods=["GUET","POST"])
def seleccion(): 
   msg = ''   
   if request.method == 'POST':        
        parada = request.form['selector']
        password = request.form['password']   
        cur = connection.cursor() 
        if parada!= []:
            if password == 'intrant': 
                paradas=funciones.vef_cedula_federado(cur,password)                                                                           
                fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H")            
                informacion = funciones.info_parada(cur,parada) 
                miembros=funciones.lista_miembros(cur,parada)              
                diario = funciones.diario_general(cur,parada)
                cuotas_hist = funciones.pendiente_aport(cur,parada)
                cabecera=funciones.info_cabecera(cur,parada)
                cur.close()            
                return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas)  
            else:
                paradas=funciones.vef_cedula_federado(cur,password)                                                                           
                fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H")            
                informacion = funciones.info_parada(cur,parada)  
                miembros=funciones.lista_miembros(cur,parada)             
                diario = funciones.diario_general(cur,parada)
                cuotas_hist = funciones.pendiente_aport(cur,parada)
                cabecera=funciones.info_cabecera(cur,parada)
                cur.close()            
                return render_template('index.html',miembros=miembros,cabecera=cabecera,informacion=informacion,fecha=fecha,diario=diario,cuotas_hist=cuotas_hist,paradas=paradas)                
        else:
            msg = 'su password no esta registrado!'        
            flash(msg)           
            return redirect(url_for('login'))      
         

    
            
@app.route("/canal")
def canal():
    return render_template('canal_motoben.html')








if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=6800)
