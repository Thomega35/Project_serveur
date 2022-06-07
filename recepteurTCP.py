import socket
import calendar
import codecs
from datetime import datetime

#Création variables
TCP_IP = '0.0.0.0'
TCP_PORT = 80
BUFFER_SIZE = 20 #Faster than 1024

#Préparation connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#Envoi en continu de Pages HTML
while True :
    
    #Acception requete
    conn, addr = s.accept()
    print ("Connection address :", addr)

    #Différentes valeurs affichés dans des versions précédentes sur les pages html
    hostname = socket.gethostname()
    local_ip = socket.getfqdn()
    heure = datetime.now()
    current_time = heure.strftime("%H:%M:%S")
    IP = str(addr[0])
    
    #Fabrication de la reponse/ contenu du serveur
    base = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length: "
    
    #Reception et Etude de la requete
    data = conn.recv(BUFFER_SIZE)
    decdata = data.decode()
    spldata = decdata.split(" ")
    
    # print ("Received data", data.decode())
    #renvoi de la page HTML adapté selon l'URL
    if spldata[0] == "GET" :
        try :
            #Si pas d'arguments, page de base envoyée
            print(spldata[1])
            if spldata[1] == "/" :
                file = codecs.open("Pages_HTML/Main.html", "r", encoding='utf-8')
                print("Page par defaut envoyée")
            #Si page admin 403, interdit
            elif spldata[1].casefold() == "/admin.html" :
                file = codecs.open("Pages_HTML/Error403.html", "r", encoding='utf-8')
                print("Vous n'avez pas les droits pour cette page")
            #Si un fichier html avec le nom existe on le renvoi
            else :
                file = codecs.open("Pages_HTML/" + spldata[1], "r", encoding='utf-8')
                print("Page envoyée")
            #Si le fichier est introuvable 404
        except Exception:
            file = codecs.open("Pages_HTML/Error404.html", "r", encoding='utf-8')
            print("Page non trouvée") 
        #Envoi de la reponse
        fileaff = file.read()
        conn.send(bytes(base + str(len(fileaff)) + "\r\n\r\n" + fileaff + "\r\n", 'utf-8'))
    conn.close()