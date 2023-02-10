import os
import mac as m

# Aplicacion que hace un nmap a una red y usa la funcion obtener_vendor para obtener el vendor de cada MAC encontrada

def main():
    
    
    os.system("ifconfig > ifconfig.txt")
    
    with open("ifconfig.txt") as archivo:
        for linea in archivo:
            if "inet " in linea:
                ip = linea.split()[1]
                mascara = linea.split()[3]
                break
            
    os.system("rm ifconfig.txt")
    
    print("La ip es: ", ip)
    print("La mascara es: ", mascara)
    
    red, broadcast = obtener_red(ip, mascara)
    
    print("La red es: ", red) 
    print("El broadcast es: ", broadcast)
    
    mascara_formmato_corto = "/"+str(formatoCorto(mascara))
    
    
    print("Escaneando la red...")

    os.system("sudo arp-scan --localnet > arp-scan.txt")
    
    
    print("Red escaneada")
    print("-"*60)
    Lineas = []
    
    with open("arp-scan.txt") as archivo:
        for linea in archivo:
            if "Starting" in linea:
                continue
            elif "Ending" in linea:
                continue
            elif "Interface" in linea:
                continue
            elif "packets" in linea:
                continue
            # linea sin caaracteres
            elif len(linea) <= 1:
                continue
            else:
                ip = linea.split()[0]
                mac = linea.split()[1]
                vendor = m.obtener_vendor(mac)
                Lineas.append([ip, mac, vendor])                    
    Lineas.sort()
    for linea in Lineas:
        print("IP: " + linea[0])
        print("MAC: " + linea[1])
        print("Vendor: " + linea[2])
        print("-"*60)
        
        
        
        
    guardar = input("Desea guardar el resultado en un archivo? (s/n): ")
    if guardar == "s":
        nombre_archivo = input("Nombre del archivo: ")
        with open(nombre_archivo, "w") as archivo:
            archivo.write("IP,MAC,Vendor" + "\n")
            for linea in Lineas:
                archivo.write(linea[0] + "," + linea[1] + "," + linea[2] + "\n")
                
    
    
        
    
def obtener_red(ip, mascara):
    binario_ip = ip_a_binario(ip).split(".")
    binario_mascara = ip_a_binario(mascara).split(".")
    red = ""
    broadcast = ""
    for i in range(len(binario_ip)):
        red += str(int(binario_ip[i], 2) & int(binario_mascara[i], 2)) + "."
        broadcast += str(int(binario_ip[i], 2) | (int(binario_mascara[i], 2) ^ 255)) + "."
    return red[:-1], broadcast[:-1]

    
    
def formatoCorto(mascara):
    # mascara = 255.255.255.240
    
    bits = ip_a_binario(mascara)
    suma = 0
    for i in range(len(bits)):
        if bits[i] == "1":
            suma += 1
        
        
    return suma
    
    
def binario_a_ip(binario):
    octetos = binario.split(".")
    ip = ""
    for octeto in octetos:
        ip += str(int(octeto, 2)) + "."
    return ip[:-1]
    
def ip_a_binario(ip):
    octetos = ip.split(".")
    binario = ""
    for octeto in octetos:
        binario += format(int(octeto), "08b") + "."
    return binario[:-1]

if __name__ == "__main__":
    main()