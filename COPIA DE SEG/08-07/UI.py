import os
import sys, os 
from tkinter import *
from tkinter import ttk
from importlib import reload
import sqlite3
from datetime import date
from datetime import datetime
from tkinter import messagebox
import threading

#Decoradoras---------------------------------------------------------------------------------------------------
def decorate(func):
	def connect_disconnect(*args,**kwargs):
		articlesX=sqlite3.connect("art001")
		cursorX=articlesX.cursor()
		func(cursorX,*args,**kwargs)	
		articlesX.commit()
		articlesX.close()
	return connect_disconnect
#Funciones------------------------------------------------------------------------------------------------------
def conexionBBDD():
	cursorX.execute('''
	CREATE TABLE IF NOT EXISTS VENTAS (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	FECHA VARCHAR(25),
	NUM_ART VARCHAR(7),
	COMENTARIO VARCHAR,
	PRECIO_UNIT INTEGER, 
	CANT_ART INTEGER,
	PRECIO_TOTAL INTEGER)
	''')
#SQLITE
@decorate
def guardarRegistroBBDD(cursorX,lista):
	cursorX.executemany("INSERT INTO VENTAS VALUES (NULL,?,?,?,?,?,?)",lista)
#SQLITE
def leerRegistroBBDD():
	articlesX=sqlite3.connect("art001")
	cursorX=articlesX.cursor()
	entrada=filtro.get()
	if filterState==False:
		cursorX.execute("SELECT * FROM VENTAS")
	else:
		if filtroType.get()=='ID':
			listaVentas=cursorX.execute("SELECT * FROM VENTAS WHERE ID=?",[entrada])
		if filtroType.get()=='FECHA':
			listaVentas=cursorX.execute("SELECT * FROM VENTAS WHERE FECHA=?",[entrada])
		if filtroType.get()=='NUM_ART':
			listaVentas=cursorX.execute("SELECT * FROM VENTAS WHERE NUM_ART=?",[entrada])
		if filtroType.get()=='COMENTARIO':
			listaVentas=cursorX.execute("SELECT * FROM VENTAS WHERE COMENTARIO LIKE ?",["%{}%".format(entrada)])
		if filtroType.get()=='PRECIO_UNIT':
			listaVentas=cursorX.execute("SELECT * FROM VENTAS WHERE PRECIO_UNIT=?",[entrada])
		if filtroType.get()=='CANT_ART':
			listaVentas=cursorX.execute("SELECT * FROM VENTAS WHERE CANT_ART=?",[entrada])
		if filtroType.get()=='PRECIO_TOTAL':
			listaVentas=cursorX.execute("SELECT * FROM VENTAS WHERE PRECIO_TOTAL=?",[entrada])
	listaVentas=cursorX.fetchall()
	articlesX.commit()
	articlesX.close()
	return listaVentas

#----------------------------------------------
def clear():
	global cantVentas
	cantVentas=0
	for widget in mainFrame.winfo_children():
			if "button" in str(widget):
				continue
			else:
				widget.destroy()
def center_window(width,height):
	#Obtengo ancho y alto de la pantalla actual
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	#Calculo las posiciones 
	x=(screen_width/2) - (width/2)
	y=(screen_height/2) - (height/2)

	root.geometry(('%dx%d+%d+%d') % (width,height,x,y))

def recibirDatos():
	global ids
	global cantVentas
	global filterState
	lista=leerRegistroBBDD()	
	if filterState==True and lista!=[]:
		clear()
	for tupla in lista:
		verif=tupla[0]
		if verif<=cantVentas:
			continue

		cantVentas+=1
		leng=len(tupla)
		for i in range(0,leng):
			crearVenta(tupla[i],i)

def crearVenta(tupla,i):
	global cantVentas
	fila=cantVentas+1
	if i==0:
		labelID=Label(mainFrame,text=tupla,relief='groove',font=('Arial',12),width=5,pady=4)
		labelID.grid(row=fila,column=1,pady=4)
	if i==1:
		labelFecha=Label(mainFrame,text=tupla,relief='groove',font=('Arial',12),width=15,pady=4)
		labelFecha.grid(row=fila,column=2)	
	if i==2:
		labelNArt=Label(mainFrame,text=tupla,relief='groove',font=('Arial',12),width=6,pady=4)
		labelNArt.grid(row=fila,column=3)	
	if i==3:
		labelCM=Label(mainFrame,text=tupla,relief='groove',font=('Arial',12),width=75,pady=4)
		labelCM.grid(row=fila,column=4)
	if i==4:
		conSigno="${}".format(tupla)
		labelPU=Label(mainFrame,text=conSigno,relief='groove',font=('Arial',12),width=5,pady=4)
		labelPU.grid(row=fila,column=5)	
	if i==5:
		labelCArt=Label(mainFrame,text=tupla,relief='groove',font=('Arial',12),width=5,pady=4)
		labelCArt.grid(row=fila,column=6)
	if i==6:
		conSigno="${}".format(tupla)
		labelPT=Label(mainFrame,text=conSigno,relief='groove',font=('Arial',12),width=5,pady=4,bg='#99EB99')
		labelPT.grid(row=fila,column=7)

def busquedaFunction():
	#Functions---------------------
	def verResultadosBusqueda(busqueda):
		#FUNCTIONS-----------------------------------------
		#Crear resultados
		def crearResultados(tupla,i,tuplaCant):
			fila=tuplaCant+1
			if i==0:
				labelID=Label(verResultadosTop,text=tupla,relief='groove',font=('Arial',12),width=5,pady=4)
				labelID.grid(row=fila,column=1,pady=4)
			if i==1:
				labelFecha=Label(verResultadosTop,text=tupla,relief='groove',font=('Arial',12),width=15,pady=4)
				labelFecha.grid(row=fila,column=2)	
			if i==2:
				labelNArt=Label(verResultadosTop,text=tupla,relief='groove',font=('Arial',12),width=6,pady=4)
				labelNArt.grid(row=fila,column=3)	
			if i==3:
				labelCM=Label(verResultadosTop,text=tupla,relief='groove',font=('Arial',12),width=40,pady=4)
				
				labelCM.grid(row=fila,column=4)
			if i==4:
				conSigno="${}".format(tupla)
				labelPU=Label(verResultadosTop,text=conSigno,relief='groove',font=('Arial',12),width=5,pady=4)
				
				labelPU.grid(row=fila,column=5)	
			if i==5:
				labelCArt=Label(verResultadosTop,text=tupla,relief='groove',font=('Arial',12),width=5,pady=4)
				labelCArt.grid(row=fila,column=6)
			if i==6:
				conSigno="${}".format(tupla)
				labelPT=Label(verResultadosTop,text=conSigno,relief='groove',font=('Arial',12),width=5,pady=4,bg='#99EB99')
				
				labelPT.grid(row=fila,column=7)
		def resultadosBusqueda(busqueda):
				tuplaCant=0
				for tupla in busqueda:
					tuplaCant+=1
					leng=len(tupla)
					for i in range(0,leng):
						crearResultados(tupla[i],i,tuplaCant)

		#TOPLEVEL--------------------------------------------------
		verResultadosTop=Toplevel()
		resultadosBusqueda(busqueda)
	def buscar():
		global filterState
		filterState=True
		tipoElegido=selectBox.get()
		filtroType.set(tipoElegido)
		filtro.set(searchEntry.get())
		leerRegistroBBDD()
		recibirDatos()
	def noBuscar():
		global filterState
		filterState=False
		clear()
		leerRegistroBBDD()
		recibirDatos()
	def ifDate(event):
		def setDate():
			searchEntry.delete(0,20)
			dateActual=date.today().strftime('%d/%m/%Y')
			searchEntry.insert(0,dateActual)

		if selectBox.get()=='FECHA':
			buttonDate.grid(column=3,row=1,columnspan=1)
			buttonDate.configure(command=setDate)
		else:
			buttonDate.grid_forget()
			searchEntry.delete(0,20)

	def enterSearch(event):
		buscar()
	#Variables
	findBy=StringVar()

	#Graphic content---------------
	searchTop=Toplevel(width=500,height=500)
	searchTop.iconbitmap("Img\search.ico")
	labelSelect=Label(searchTop,text='Buscar por: ')
	labelSelect.grid(column=1,row=0,columnspan=1)
											# 1      2       3          4     		   5			6			  7
	selectBox=ttk.Combobox(searchTop,values=['ID','FECHA','NUM_ART','COMENTARIO','PRECIO_UNIT','CANT_ART','PRECIO_TOTAL'],
						  state="readonly")
	selectBox.current(0)
	selectBox.grid(column=2,row=0,columnspan=1)

	buttonDate=Button(searchTop,text="Fecha actual")
	buttonDate.grid(column=3,row=1,columnspan=1)
	buttonDate.grid_forget()
	selectBox.bind("<<ComboboxSelected>>",ifDate)

	searchEntry=Entry(searchTop)
	searchEntry.grid(column=3,row=0,columnspan=1)
	searchEntry.bind('<Return>',enterSearch)

	
	buttonSelect=Button(searchTop,text="Filtrar",command=buscar)
	buttonSelect.grid(column=4,row=0,columnspan=1,padx=5)
	buttonUnSelect=Button(searchTop,text="Dejar de filtrar",command=noBuscar)
	buttonUnSelect.grid(column=5,row=0,columnspan=1)
    
def salir():
	root.destroy()	
#ADDTOPS----------------------------------------------------------------------------------------------------
#ADD TOP INSERT--------------------------------------------------------------------------------
def addTopIFunction():
	#SUB FUNCIONES-----------------------------------------
	def center_windowADDTOP(width=300,height=400):
		#Obtengo ancho y alto de la pantalla actual 			 														
		screen_width = addTopI.winfo_screenwidth()
		screen_height = addTopI.winfo_screenheight()

		#Calculo las posiciones 
		x=(screen_width/2) - (width*1.7)
		y=(screen_height/2) - (height/8)

		addTopI.geometry(('+%d+%d') % (x,y))
	
	
	def fechaActual():
		fechaEntry.delete(0,'end')
		dateS=date.today()
		fechaEntry.insert(0,dateS.strftime('%d/%m/%Y'))
		return

	def total():
		try:
			cant=int(cantArtEntry.get())
			precio=int(precioUnitEntry.get())
		except ValueError:
			error.set("Cantidad y/o precio incorrecto")
			return
		total=cant*precio
		return total

	def guardarRegistro(fecha,numArt,comentario,precioU,cantArt,precioT):
		tupla=(fecha,numArt,comentario,precioU,cantArt,precioT)
		lista=[tupla]
		guardarRegistroBBDD(lista)
	def func(enterHitted):
			obtenerValores()
	def obtenerValores():
		fecha=fechaEntry.get()
		formato="%d/%m/%Y"
		try:
			datetime.strptime(fecha,formato) 
		except ValueError:
			error.set("Fecha incorrecta")
			return
		numArt=numArtEntry.get()
		comentario=comentEntry.get()
		precioU=precioUnitEntry.get()
		cantArt=cantArtEntry.get()
		if fecha=='' or numArt=='' or precioU=='' or cantArt=='':
			error.set("Complete los campos")
			return
		precioT=total() 
		if precioT==None:
			return
		error.set('')
		guardarRegistro(fecha,numArt,comentario,precioU,cantArt,precioT)
		recibirDatos()
	@decorate
	def buscarArt(cursorX):
		#BUSCAR MISMO ARTICULO CARAC.
		art=numArtEntry.get()
		art=str(art)
		comment=cursorX.execute("SELECT comentario,precio_unit FROM ventas WHERE num_art=? LIMIT 1",(art,))
		comentEntry.delete(0,40)
		precioUnitEntry.delete(0,10)
		for i in comment:
			comentEntry.insert(0,i[0])
			precioUnitEntry.insert(0,i[1])
	#--------------------------------------------------------------------------------------------
	addTopI=Toplevel();
	addTopI.title("Agregar venta")
	addTopI.iconbitmap('Img\insert.ico')
	error=StringVar()
	center_windowADDTOP()

	vacio=Label(addTopI,width=3)
	vacio.grid(column=1,row=2,sticky=N)

	fecha=Label(addTopI, text='Fecha',font=('Helvetica','10'))
	fecha.grid(column=2,row=1,sticky=N)
	
	num_Art=Label(addTopI, text='Art N°',font=('Helvetica','10'))
	num_Art.grid(column=3,row=1,sticky=N)
	
	comentLabel=Label(addTopI, text='Comentario',font=('Helvetica','10'))
	comentLabel.grid(column=4,row=1,sticky=N)
	
	precio_Unit=Label(addTopI, text='$C/U',font=('Helvetica','10'))
	precio_Unit.grid(column=5,row=1,sticky=N)
	
	cant_Art=Label(addTopI, text='Cant',font=('Helvetica','10'))
	cant_Art.grid(column=6,row=1,sticky=N)
	

	#Entry:
	fechaEntry=Entry(addTopI,bd=3,width=10,font=("Arial",12))
	fechaEntry.grid(column=2,row=2)

	fechaActual() #Set fecha actual
	numArtEntry=Entry(addTopI,bd=3,width=6,font=("Arial",12))
	numArtEntry.grid(column=3,row=2)
	
	comentEntry=Entry(addTopI,bd=3,width=50,font=("Arial",12))
	comentEntry.grid(column=4,row=2)
	
	precioUnitEntry=Entry(addTopI,bd=3,width=5,font=("Arial",12))
	precioUnitEntry.grid(column=5,row=2)
	
	cantArtEntry=Entry(addTopI,bd=3,width=5,font=("Arial",12))
	cantArtEntry.grid(column=6,row=2)
	cantArtEntry.insert(0,1)
	
	#BOTON SEND
	sendButton=Button(addTopI,text="Ingresar datos",width=20,command=obtenerValores)
	sendButton.grid(row=2,column=7,padx=10)
	#Error label
	errorLabel=Label(addTopI,textvariable=error,width=30)
	errorLabel.grid(row=3,column=7)
	#BOTON FECHA
	dateButton=Button(addTopI,text="Fecha actual",width=10,command=fechaActual)
	dateButton.grid(row=3,column=2)

	#BOTON COMPLETAR COMMENT
	completeComment=Button(addTopI,text="Buscar articulo",width=10,command=buscarArt)

	completeComment.grid(row=3,column=4)
	numArtEntry.bind('<Return>',func)
	fechaEntry.bind('<Return>',func)
	comentEntry.bind('<Return>',func)
	precioUnitEntry.bind('<Return>',func)
	cantArtEntry.bind('<Return>',func)
#ADD TOP DELETE--------------------------------------------------------------------------------
def addTopDFunction():
	global cantVentas
	#SUBFUNCIONES------------------------------------
	def autoDel(event):
		borrarVenta()
	def center_windowADDTOP(width=300,height=400):
		screen_width = addTopD.winfo_screenwidth()
		screen_height = addTopD.winfo_screenheight()

		x=(screen_width/2) - (width*0.3)
		y=(screen_height/2) - (height/8)

		addTopD.geometry(('+%d+%d') % (x,y))

	def borrarVenta():
		def alerta(error):
			resumen=StringVar()
			resumen.set(error)
			labelAlerta=Label(addTopD,textvariable=resumen)
			labelAlerta.grid(row=3)
		articlesX=sqlite3.connect("art001")
		cursorX=articlesX.cursor()
		numID=questEntry.get()
		contador=0
		rango=BooleanVar()
		if '-' in numID:
			rango.set(True)
			aux=numID.split('-')
			first=int(aux[0])
			last=int(aux[1])+1
			numID=''
			for num in range(first,last):
				numID+=str(num)+','
			numID=list(numID)
			numID.pop(-1)
			numID=''.join(numID)
		for i in numID.split(','):
			try:
				i=int(i)
			except ValueError:
				alerta("Caracter inválido")
				return
			if i>cantVentas and rango.get()==True:
				continue
			i-=contador
			i=str(i)
			try:
				cursorX.execute("SELECT ID FROM VENTAS WHERE ID=?",(i))
			except sqlite3.ProgrammingError:
				print("Programming error")
				return
			existe=cursorX.fetchone()
			if existe==None:
				messagebox.showwarning("No encontrado","El ID ingresado no fue encontrado")
	
			else:
				cursorX.execute(("DELETE FROM VENTAS WHERE ID=?"),(i))
				cursorX.execute("UPDATE SQLITE_SEQUENCE SET SEQ=SEQ-1 WHERE NAME='VENTAS'")
				cursorX.execute(("UPDATE VENTAS SET ID=ID-1 WHERE ID>?"),(i))
				articlesX.commit()
		
			contador+=1
		rango.set(False)
		clear()
		recibirDatos()
		addTopD.destroy()
		articlesX.close()
	#-------------------------------------------------------------------------------
	addTopD=Toplevel()
	addTopD.title("Borrar venta")
	addTopD.iconbitmap('Img\delete.ico')
	center_windowADDTOP()
	labelQuest=Label(addTopD,text="Ingrese el ID de la venta a borrar: ",width=10)
	labelQuest.grid()
	questEntry=Entry(addTopD)
	questEntry.grid()
	deleteButton=Button(addTopD,text="Borrar",width=15,relief='groove',command=borrarVenta)
	deleteButton.grid()
	questEntry.bind('<Return>',autoDel)

	addTopD.mainloop()

#ESTADÍSTICAS----------------------------------------------------------------------------------
@decorate
def estadisticasFunction(cursorX):
	#----------------------------------
	def center_windowEstd(width=300,height=400):
		#Obtengo ancho y alto de la pantalla actual 			 														
		screen_width = estadTop.winfo_screenwidth()
		screen_height = estadTop.winfo_screenheight()

		#Calculo las posiciones 
		x=(screen_width/2) - (width*0.2)
		y=(screen_height/2) - (height/4)

		estadTop.geometry(('+%d+%d') % (x,y))

	def ganancia_total():
		ganancias=cursorX.execute("SELECT PRECIO_TOTAL FROM VENTAS")
		gananciaTotal=0
		for tupla in ganancias:
			for numero in tupla:
				gananciaTotal+=numero
		ganancias_totalesVar.set("Ganancia total: $"+str(gananciaTotal))
		return gananciaTotal
	def ganancia_del_dia():
		gananciaDia=0
		ganancias=cursorX.execute("SELECT PRECIO_TOTAL FROM VENTAS WHERE FECHA=STRFTIME('%d/%m/%Y','now')")
		for tupla in ganancias:
			for numero in tupla:
				gananciaDia+=numero
		ganancias_del_diaVar.set("Ganancias del día: $"+str(gananciaDia))
		return gananciaDia
	@decorate
	def ganancia_del_mes(cursorX):
		gananciaMes=0
		mesInsertado='%/{}/{}'.format(mes.get(),anio.get())
		ganancias=cursorX.execute("SELECT PRECIO_TOTAL FROM VENTAS WHERE FECHA LIKE (?)",(mesInsertado,))
		for tupla in ganancias:
			for numero in tupla:
				gananciaMes+=numero

		ganancia_del_mesVar.set("Ganancia del mes: $"+str(gananciaMes))
	def selectMonth(event):
		monthSelected=monthSelect.current()+1
		if monthSelected<10:
			monthSelected="0{}".format(monthSelected)
		mes.set(monthSelected)
		ganancia_del_mes()
	def selectYear(event):
		mes=''
		selectedYear=yearSelect.current()
		anio.set(selectedYear+2018)
		ganancia_del_mes()

	anio=StringVar()
	mes=StringVar()
	#Obtener estadisticas
	ganancia_total()
	ganancia_del_dia()
	#MES
	mes_actual=date.today().strftime('%m') #Junio
	anio_actual=date.today().strftime('%Y')
	anio.set(anio_actual)
	mes.set(mes_actual)
	ganancia_del_mes()

	#TOPLEVEL----------------------------------
	estadTop=Toplevel(width=300,height=400)
	estadTop.title("Estadisticas")

	center_windowEstd(width=300,height=400)

	labelTotal=Label(estadTop,textvariable=ganancias_totalesVar,width=20)
	labelDia=Label(estadTop,textvariable=ganancias_del_diaVar,width=20)
	labelMes=Label(estadTop,textvariable=ganancia_del_mesVar,width=20)
	#SELECCION MES
	monthSelect=ttk.Combobox(estadTop,values=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre",
		"Noviembre","Diciembre",],state="readonly")
	yearSelect=ttk.Combobox(estadTop,values=['2018','2019','2020','2021'],state="readonly")
	mes_actual=int(mes_actual)-1
	monthSelect.current(mes_actual)
	monthSelect.bind("<<ComboboxSelected>>",selectMonth)

	yearSelect.current(int(anio_actual)-2018)
	yearSelect.bind("<<ComboboxSelected>>",selectYear)
	
	labelTotal.grid(row=1,column=1)
	labelDia.grid(row=1,column=2)
	labelMes.grid(row=1,column=3)
	monthSelect.grid(row=2,column=3)
	yearSelect.grid(row=3,column=3)
	#----------------------------------

def scrollFunc(event):
    relleno.configure(scrollregion=relleno.bbox("all"),width=200,height=200)
#Root
root=Tk()
root.title("Lista de articulos");root.configure();root.resizable(0,0);root.iconbitmap('Img\main.ico')

#FRAMES Y CANVAS------------------------------------------------------------
borde=Frame(root,relief=GROOVE)
borde.pack(fill='both',expand=True)

relleno=Canvas(borde)

mainFrame=Frame(relleno)

myscrollbar=Scrollbar(borde,orient="vertical",command=relleno.yview)

relleno.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill='y')
relleno.pack(fill='both',expand=True)
relleno.create_window((0,0),window=mainFrame,anchor='nw')
mainFrame.bind("<Configure>",scrollFunc)

#MENÚ---------------------------------------------------------------
mainMenuBar=Menu(root)

root.config(menu=mainMenuBar)


#SUBMENUES
archivoMenu=Menu(mainMenuBar,tearoff=0)
edicionMenu=Menu(mainMenuBar,tearoff=0)
herramientasMenu=Menu(mainMenuBar,tearoff=0)
busquedaMenu=Menu(mainMenuBar,tearoff=0)

mainMenuBar.add_cascade(label="Archivo",menu=archivoMenu)
mainMenuBar.add_cascade(label="Editar",menu=edicionMenu)
mainMenuBar.add_cascade(label="Herramientas",menu=herramientasMenu)
mainMenuBar.add_cascade(label="Búsqueda",menu=busquedaMenu)

edicionMenu.add_command(label="Insertar venta",command=addTopIFunction)
edicionMenu.add_command(label="Borrar venta",command=addTopDFunction)
archivoMenu.add_command(label="Salir",command=salir)
herramientasMenu.add_command(label="Estadísticas",command=estadisticasFunction)
herramientasMenu.add_command(label="Gráficos")

busquedaMenu.add_command(label="Buscar venta",command=busquedaFunction)
#---------------------------------------------------------------------
#Programa principal
idButton=Button(mainFrame,text="ID",font=('Helvetica',13),width=5)
idButton.grid(column=1,row=1,pady=6,padx=2)
dateButton=Button(mainFrame,text="FECHA",font=('Helvetica',13),width=15)
dateButton.grid(column=2,row=1,pady=6,padx=2)
numArtButton=Button(mainFrame,text="ART N°",font=('Helvetica',13),width=6)
numArtButton.grid(column=3,row=1,pady=6,padx=2)
comentButton=Button(mainFrame,text="COMENTARIO",font=('Helvetica',13),width=75)
comentButton.grid(column=4,row=1,pady=6,padx=2)
precioUButton=Button(mainFrame,text="$/U",font=('Helvetica',13),width=5)
precioUButton.grid(column=5,row=1,pady=6,padx=2)
cantArtButton=Button(mainFrame,text="CANT",font=('Helvetica',13),width=7)
cantArtButton.grid(column=6,row=1,pady=6,padx=2)
precioTButton=Button(mainFrame,text="TOTAL $",font=('Helvetica',13),width=8)
precioTButton.grid(column=7,row=1,pady=6,padx=2)
#--------------------------------------------------------------------------
#SQLITE CONNECT
try:
	articlesX=sqlite3.connect("art001")
	cursorX=articlesX.cursor()
except:
	messagebox.showerror("Error","Error al conectar con la base de datos")

#Variables--------
borrar=IntVar()
ganancias_totalesVar=StringVar()
ganancias_del_diaVar=StringVar()
ganancia_del_mesVar=StringVar()
ganancia_del_año=StringVar()#### HACER GANANCIAS ANUALES

filtroType=StringVar()
filtro=StringVar()
filterState=False

try:
	conexionBBDD()
except:
	messagebox.showerror("Error","Error al crear la base de datos")
cantVentas=0
tuplaCant=0
ids=[]
try:
	recibirDatos()
except:
	messagebox.showerror("Error","Ha ocurrido un error al intentar mostrar los datos en pantalla")
#Centrar ventana
try:
	center_window(1194,400)
except:
	messagebox.showerror("Error","Se detectó un problema al intentar establecer el tamaño de la ventana")

#----------------------
root.mainloop()