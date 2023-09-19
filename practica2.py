import pickle

# Función para cargar la base de datos desde un archivo
def cargar_base_de_datos():
    try:                                       #El try, except es un condicional el cual se encarga de ser un metodo de "escape"
        with open("estudiantes.pkl", "rb") as archivo:  
            return pickle.load(archivo)
    except FileNotFoundError:          #El bloque except se ejecutará cuando el bloque try falle debido a un error y retornara 
        return []

# Función para guardar la base de datos 
def guardar_base_de_datos(base_de_datos):
    try:
        with open("estudiantes.pkl", "wb") as archivo:
            pickle.dump(base_de_datos, archivo)
    except Exception as e:
        print(f"Error al guardar la base de datos: {e}")
        
# Función para resetear la base de datos
def resetear_base_de_datos():
    base_de_datos.clear()
    guardar_base_de_datos(base_de_datos)
    print("\nBase de datos reseteada con éxito.")

# Base de datos de estudiantes (cargada al inicio del programa)
base_de_datos = cargar_base_de_datos()

# Función para seleccionar una carrera
def seleccionar_carrera():
    print("\nSeleccione la carrera:")
    carreras = ["Ingeniería en automatización y control", 
                "Ingeniería de sistemas",
                "Ingeniería industrial",
                "Ingeniería mecánica\n"]
    
    for i, carrera in enumerate(carreras, 1):
        print(f"{i}. {carrera}")
    while True:
        try:
            opcion_carrera = int(input("Seleccione la carrera (1-4): ")) - 1
            if 0 <= opcion_carrera < len(carreras):  #verifica si el valor de "opcion_carrera" esta dentro del rango válido de opciones de la lista "carreras"
                return carreras[opcion_carrera]
            else:
                print("Opción de carrera no válida")
        except ValueError:
            print("Por favor, ingrese un valor numérico válido.")

# Función para registrar un estudiante
def registrar_estudiante():
    estudiante = {
        "nombre": None ,
        "edad": None,
        "carrera": None,
        "promedio": None,
        "carnet": None 
    }
    try:
        nombre = input("Ingrese el nombre del estudiante: ")
        if not nombre.isalpha and nombre.isspace(): #Permite solo letras y espacios
           raise ValueError("El nombre debe contener solo letras.") #se le avisa al usuario que lo digitado fue un error
        carrera = seleccionar_carrera()
        while True:
            try:
                edad = int(input("Ingrese la edad del estudiante: "))
                if 100 > edad > 0:
                    break
                else:
                    print("Edad no valida.")
            except ValueError:
                print("Por favor, ingrese un valor numérico válido para la edad.")
        while True:
            try:
                promedio = float(input("Ingrese el promedio del estudiante (0.0 - 5.0): "))
                if 0.0 <= promedio <= 5.0:
                    break
                else:
                    print("El promedio debe estar en el rango de 0.0 a 5.0")
            except ValueError:
                print("Por favor, ingrese un valor numérico válido.")
                
        while True:
            try:
                carnet = int(input("Ingrese el número de carnet del estudiante: "))
                carnet_no_existe = list(filter(lambda estudiante: estudiante["carnet"] == carnet, base_de_datos))
                if (carnet > 0) and len(carnet_no_existe) == 0:
                    break
                else:
                    print("Número de carnet ya existente.")
            except ValueError:
                print("Por favor, ingrese un valor numérico válido.")
        
        estudiante = {
            "nombre": nombre,
            "edad": edad,
            "carrera": carrera,
            "promedio": promedio,
            "carnet": carnet 
        }
        base_de_datos.append(estudiante)
        print("\nEstudiante registrado con éxito!")
    except ValueError as e:
        print(f"Error: {e}")
        
# Función para imprimir una tabla ordenada
def imprimir_tabla(data, headers):
    if not data:
        print("No hay datos para mostrar.")
        return

    print("*" * 75)  # Línea de separación superior
    header_format = "{:<20}" * len(headers)  # Formato para los encabezados
    print(header_format.format(*headers))  # Imprimir encabezados
    print("*" * 75)  # Línea de separación inferior

    for row in data:
        row_format = "{:<20}" * len(headers)  # Formato para las filas de datos
        print(row_format.format(*[row[header] for header in headers]))

    print("*" * 75)  # Línea de separación final

# Función para consultar estudiantes de una carrera

def consultar_estudiantes_carrera():
    try:
        carrera = seleccionar_carrera()
        estudiantes_carrera = list(filter(lambda estudiante: estudiante["carrera"] == carrera, base_de_datos))
        if len(estudiantes_carrera) == 0:
            print(f"No hay estudiantes registrados en la carrera {carrera}")

        else:
            print(f"Estudiantes en la carrera {carrera}:")
            headers = ["Nombre", "Edad", "Promedio", "Carnet"]
            data = []

            for estudiante in estudiantes_carrera:
                nombre = estudiante['nombre']
                edad = estudiante['edad']
                promedio = estudiante['promedio']
                carnet = estudiante['carnet']
                data.append({"Nombre": nombre,"Edad": edad, "Promedio": promedio, "Carnet": carnet})
                
            imprimir_tabla(data, headers)  # Llamar a la función para imprimir la tabla
    except ValueError as e:
        print(f"Error: {e}")

# Función para calcular el promedio general de todos los estudiantes
def calcular_promedio_general():
    if not base_de_datos:
        print("No hay estudiantes registrados.")
        return
    promedios = map(lambda estudiante: estudiante["promedio"], base_de_datos)
    promedio_general = sum(promedios) / len(base_de_datos)
    print(f"El promedio general de todos los estudiantes es: {promedio_general:.2f}")

# Función para ver los estudiantes destacados  (promedio > 4.0)
def ver_estudiantes_destacados():
    if not base_de_datos:
        print("No hay estudiantes registrados.")
        return
    
    estudiantes_destacados = [estudiante for estudiante in base_de_datos if estudiante["promedio"] > 4.0]

    if not estudiantes_destacados:
        print("No hay estudiantes destacados que cumplan con el requisito (promedio > 4.0).")
        return
        
    estudiantes_ordenados = sorted(estudiantes_destacados, key=lambda estudiante: estudiante["promedio"], reverse=True)
    
    print("Estudiantes destacados (Promedio > 4.0):")
    headers = ["Nombre", "Edad", "Carrera", "Promedio", "Carnet"]
    data = []

    for estudiante in estudiantes_ordenados[:2]:
        nombre = estudiante['nombre']
        edad = estudiante ['edad']
        carrera = estudiante['carrera']
        promedio = estudiante['promedio']
        carnet = estudiante['carnet']
        data.append({"Nombre": nombre, "Edad": edad, "Carrera": carrera, "Promedio": promedio, "Carnet": carnet})

    imprimir_tabla(data, headers)  # Llamar a la función para imprimir la tabla
    
# Función principal
def main():
    
    
    if base_de_datos:
        print(f"\nBase de datos cargada con éxito. Total de estudiantes: {len(base_de_datos)}")
    else:
        print("\nAún no hay estudiantes registrados.")
    
    while True:
        print("\nMenú Principal:\n")
        print("1. Registrar estudiante")
        print("2. Consultar estudiantes de una carrera")
        print("3. Calcular promedio general")
        print("4. Ver estudiantes destacados")
        print("5. Salir y guardar")
        print("6. Salir y reset")
        opcion = input("\nSeleccione una opción (1-6): ")
        try:
            if opcion == "1":
                registrar_estudiante()
            elif opcion == "2":
                consultar_estudiantes_carrera()
            elif opcion == "3":
                calcular_promedio_general()
            elif opcion == "4":
                ver_estudiantes_destacados()
            elif opcion == "5":
                guardar_base_de_datos(base_de_datos)
                print("Base de datos guardada en 'estudiantes.pkl'. ¡Adiós!")
                break
            elif opcion =="6":
                resetear_base_de_datos()
                break
            else:
                raise ValueError("Opción no válida. Por favor, seleccione una opción válida (1-6).")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
