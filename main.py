import mac as m
import escaneo as escaneo

def main():
    print("Bienvenido al programa de Identificacion de MAC y MACs en la red")
    
    while True:
        opcion = int(input("1. Identificar MAC\n2. Escanear red\n3. Salir\nOpcion: "))
        
        if opcion == 1:
            mac = input("Ingrese la MAC: ")
            if m.validar_mac(mac):
                print("La MAC es valida")
                print("El vendor es: " + m.obtener_vendor(mac))
                wait = input("Presione enter para continuar")
                if wait == "":
                    print("-"*60)
                else:
                    print("-"*60)
            else:
                print("La MAC es invalida")
                # Que se repita el programa
                print("Vuelva a intentarlo")
                print("-"*60)
        elif opcion == 2:
            escaneo.main()
        
        elif opcion == 3:
            exit()
            
        else:
            print("Opcion invalida")
            print("Vuelva a intentarlo")
            print("-"*60)



if __name__ == '__main__':
    main()
