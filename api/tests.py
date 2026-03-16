import os


ruta = "planificaciones/"

print("\nRuta: "+ruta)

usuario = input("\nInserte usuario: \n").lower()

print("\nUsuario: "+usuario)



ruta = ruta+usuario
print(ruta)

if os.path.exists(ruta):
    print("Carpera existente")
else:
    os.makedirs(ruta,exist_ok=True)
    print("Carpeta creada con exitos para: "+usuario)

