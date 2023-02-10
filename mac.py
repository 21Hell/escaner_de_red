import os

def validar_mac(mac):
    
    # Validar que la MAC tenga 12 caracteres con o sin :
    
    mac_valida = False

    mac = mac.upper()
    
    mac = formato_mac(mac)
    
    for caracter in mac:
        if caracter in "0123456789ABCDEF":
            mac_valida = True
        else:
            mac_valida = False
            break
        
    return mac_valida


def obtener_vendor(mac):
    
    # https://standards-oui.ieee.org/oui/oui.txt
    
    # Descargar el archivo si no existe
    vendor = "Desconocido"
    
    if not os.path.exists("oui.txt"):
        print("Descargando el archivo de los proveedores...")
        os.system("wget -q -N https://standards-oui.ieee.org/oui/oui.txt")
    

    mac = formato_mac(mac)
    # Leer el archivo y buscar la MAC si se encuentra terminar el bucle


    with open("oui.txt") as archivo:
        for linea in archivo:
            if mac in linea:
                vendor = linea.split("\t")[2] 
                break
    
    
    
    return vendor



def formato_mac(mac):
    
    # 58:85:E9:11:3A:B7
    
    # 5885E9113AB7
    
    # 58-85-E9-11-3A-B7
    mac = mac.upper()
    # Quitar los : y -
    mac = mac.replace(":","")
    mac = mac.replace("-","")
    mac = mac[:6]
    
    return mac
