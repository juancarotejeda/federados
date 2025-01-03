Nueva presentacion
def imprimible():
    pdf = FPDF()
    pdf.add_page()

    logo_path = 'logo.png'
    pdf.image(logo_path, x=160, y=8, w=40)

    pdf.set_xy(10, 10)
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, 'SySCursos Company', ln=True)
    pdf.cell(0, 10, 'Calle No existe N30 CP 21020', ln=True)
    pdf.cell(0, 10, 'B32312312', ln=True)
    pdf.cell(0, 10, f'Fecha: {fecha_factura}', ln=True)

    pdf.ln(20)


    pdf.set_font('Arial', size=16)
    pdf.cell(0,10, txt='FACTURA', ln=True, align='C')

    pdf.set_font('Arial', size=12)
    pdf.cell(0,10, f'Numero Factura: {identificador_factura}', ln=True, align='C')

    pdf.set_font('Arial', size=12)
    pdf.cell(0,10, '------------------------------------', ln=True, align='L')

    pdf.cell(0,10, 'Datos del Cliente', ln=True, align='L')
    pdf.cell(0,10, f'Nombre: {nombre_cliente}', ln=True, align='L')
    pdf.cell(0,10, f'Apellidos: {apellidos_cliente}', ln=True, align='L')
    pdf.cell(0,10, f'Teléfono: {telefono_cliente}', ln=True, align='L')
    pdf.cell(0,10, f'DNI: {dni_cliente}', ln=True, align='L')
    pdf.cell(0,10, f'Ciudad: {ciudad_cliente}', ln=True, align='L')

    pdf.cell(0,10, 'Detalles del Servicio', ln=True, align='L')

    pdf.cell(0,10, '---------------------------------', ln=True, align='L')
    pdf.cell(60,10, 'Nombre del servicio', border=1)
    pdf.cell(80,10, 'Descripción del servicio', border=1)
    pdf.cell(30,10, 'Total', border=1, ln=True)

    pdf.cell(60,10, nombre_servicio, border=1)
    pdf.cell(80,10, descripcion_servicio, border=1)
    pdf.cell(30,10, total_servicio, border=1, ln=True)

    pdf.cell(0,10, '================================================', ln=True, align='L')
    pdf.cell(0,10, 'Gracias por su compra!', ln=True, align='C')


    pdf_file = f'Factura_{nombre_cliente}_{apellidos_cliente}.pdf'
    pdf.output(pdf_file,'F')
    messagebox.showinfo('Factura Generada')