from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

import smtplib
import base64
import pickle
import datefinder
import string
import re

#-----------------------------------------Metodos----------------------------------------------
#                       "%Y-%m-%d T %H:%M:%S"
def accesocalendario():
        #Accedemos al calendario creado en google api mediante el link el metodo de lectura y escritura
        permiso = ['https://www.googleapis.com/auth/calendar']
        #accemos uso del id de cliente  OAuth 2.0 asignado de google
        IDOAuth = InstalledAppFlow.from_client_secrets_file("secreto_cliente.json", scopes=permiso)
        Credencial = IDOAuth.run_console()
        #convertimos las credenciales a excritura binaria y las almacenamos en un archivo
        pickle.dump(Credencial, open("Credencial.pkl", "wb"))
        #leemos las credenciales y las y las aguardamos en su respectiva variable
        Credencial = pickle.load(open("Credencial.pkl", "rb"))
        return build("calendar", "v3", credentials=Credencial)

def accesoGmail():
        permisoG = ['https://www.googleapis.com/auth/gmail.readonly']
        IDOAuth = InstalledAppFlow.from_client_secrets_file("secreto_cliente_Gmail.json", scopes=permisoG)
        CredencialG = IDOAuth.run_local_server(port=0)
        pickle.dump(CredencialG, open("CredencialG.pkl", "wb"))
        CredencialG = pickle.load(open("CredencialG.pkl", "rb"))
        return build('gmail', 'v1', credentials=CredencialG)
           
def CrearEvento(Nombre, Ubicacion, Describcion, year, mes, dia, hora, minu, Servicio):
        result = Servicio.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        timezone =result['items'][0]['timeZone']
        #obtenemos el calendario mediante
        result = Servicio.events().list(calendarId=calendar_id, timeZone=timezone)
        #print(result)#lo imprimimos
        Hora_inicio = datetime(year, mes, dia, hora, minu, 0)
        Hora_final = Hora_inicio + timedelta(hours=4)
        event = {
          'summary': Nombre,
          'location': Ubicacion,
          'description': Describcion,
          'start': {
            'dateTime': Hora_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'end': {
            'dateTime': Hora_final.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
           ],
          },
        }
        return Servicio.events().insert(calendarId=calendar_id, body=event).execute()

def EnvioGmail(ServicioG, Usuario, Hacia, Asunto, Mensaje):
        results = ServicioG.users().labels().list(userId='me').execute()
        labels = results.get('labels', ['SENT'])
        print(labels)
        return 0
        
        
#--------------------------------------Main-----------------------------------------------

ServicioG = accesoGmail()
Usuario ='L'#input("Escriba el Usuario: ")
Hacia ='L'#input("Escrba el destino: ")
Asunto ='L'#input("Escriba el asunto: ")
Mensaje ='L'#input("Escriba el Mensaje: ")
EnvioGmail(ServicioG, Usuario, Hacia, Asunto, Mensaje)
Servicio =accesocalendario()
Nombre =input("Ecriba el nombre del Evento: ")
Ubicacion =input("Escribe la ubicacion del Evento: ")
Describcion =input("Escribe una Describcion: ")
year =int(input("Escribe un año: "))
mes =int(input("Escribe un mes: "))
dia =int(input("Escribe un dia: "))
hora =int(input("Escribe una hora: "))
minu =int(input("Escribe un minutos: "))
CrearEvento(Nombre, Ubicacion, Describcion, year, mes, dia, hora, minu, Servicio)


  
        

