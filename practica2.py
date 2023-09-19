# =============================================================================
# Taller 2 ---> Programación Avanzada
# Equipo: 
#     - Alberth Londoño Rodriguez
#     - Grachi Pulgarin Gonzalez
#     - Esteban Vásquez Cano
# =============================================================================

import pickle

#%% Función para cargar la base de datos desde un archivo
def cargar_base_de_datos():
    try:    # el try,except es un condicional el cualse encarga de ser un metodo de "escape"
        with open("estudiantes.pkl", "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:   #el bloque except se ejecutara cuando el bloque try falle debido a un error y retornara
        return []

#%% Función para guardar la base de datos 
def guardar_base_de_datos(base_de_datos):
    try:
        with open("estudiantes.pkl", "wb") as archivo:
            pickle.dump(base_de_datos, archivo)  #pickle.dump() toma el objeto que desea serializar(base_de_datos) y un objeto de archivo(archivo) donde se guardará la información serializada
    except Exception as e:
        print(f"Error al guardar la base de datos: {e}")
        
#%% Función para resetear la base de datos
def resetear_base_de_datos():
    base_de_datos.clear()  #limpiara todo lo que se encuentre en "base_datos"
    guardar_base_de_datos(base_de_datos)
    print("\nBase de datos reseteada con éxito.")

#%% Función para seleccionar una carrera
def seleccionar_carrera():
    print("\nSeleccione la carrera:")
    carreras = ["Ingeniería en automatización y control", "Ingeniería de sistemas", "Ingeniería industrial", "Ingeniería mecánica"]
    for i, carrera in enumerate(carreras, 1):
        print(f"{i}. {carrera}")
    while True:
        try:
            opcion_carrera = int(input("Seleccione la carrera (1-4): ")) - 1

            if 0 <= opcion_carrera < len(carreras):  # Verifica si el valor de "opcion_carrera" esta dentro del rango válido de opciones de la lista "carreras"
                return carreras[opcion_carrera]
            else:
                print("Opción de carrera no válida")
        except ValueError:
            print("Por favor, ingrese un valor numérico válido.")

#%% Función para registrar un estudiante
def registrar_estudiante():
    try:
        nombre = input("Ingrese el nombre completo del estudiante: ")
        if not nombre.replace(" ", "").isalpha():
            raise ValueError("El nombre debe contener solo letras y espacios.")  #es una clase de excepción que indica que se hay un error relacionado con el tipo o el valor de un objeto
        # carnet = input("Ingrese el número de carnet del estudiante: ")
        # if not carnet.isdigit():  #identifica si la string tiene solo números (dígitos)
        #     raise ValueError("El número de carnet debe contener solo dígitos.")
        while True:
            try:
                carnet = int(input("Ingrese el número de carnet del estudiante: "))
                carnet_no_existe = list(filter(lambda estudiante: estudiante["carnet"] == carnet, base_de_datos))
                # print(carnet_no_existe)
                if (carnet > 0) and len(carnet_no_existe) == 0:
                    break
                else:
                    print("Número de carnet ya existente.")
                    headers = ["Nombre", "Edad", "Carrera", "Promedio", "Carnet"]
                    data = []
                    nombre = carnet_no_existe[0]['nombre']
                    edad = carnet_no_existe[0]['edad']
                    carrera = carnet_no_existe[0]['carrera']
                    promedio = carnet_no_existe[0]['promedio']
                    carnet = carnet_no_existe[0]['carnet']
                    data.append({"Nombre": nombre, "Edad": edad, "Carrera": carrera, "Promedio": promedio, "Carnet": carnet})

                    imprimir_tabla(data, headers)  # Llamar a la función para imprimir la tabla

            except ValueError:
                print("Por favor, ingrese un valor numérico válido.")
        carrera = seleccionar_carrera()
        while True:
            try:
                edad = int(input("Ingrese la edad del estudiante: "))
                if 100 > edad >= 9:
                    break
                else:
                    print("La edad debe ser un valor positivo.")
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

        estudiante = {
            "nombre": nombre,
            "carnet": carnet,
            "edad": edad,
            "carrera": carrera,
            "promedio": promedio
        }
        base_de_datos.append(estudiante)
        print("\nEstudiante registrado con éxito!")
    except ValueError as e:
        print(f"Error: {e}")
        
#%% Función para imprimir una tabla ordenada
def imprimir_tabla(data, headers):
    if not data:
        print("No hay datos para mostrar.")
        return

    print("*" * 100)  # Línea de separación superior
    header_format = "{:<20}" * len(headers)  # Formato para los encabezados
    print(header_format.format(*headers))  # Imprimir encabezados
    print("*" * 100)  # Línea de separación inferior

    for row in data:
        row_format = "{:<20}" * len(headers)  # Formato para las filas de datos
        print(row_format.format(*[row[header] for header in headers]))

    print("*" * 100)  # Línea de separación final

#%% Función para consultar estudiantes de una carrera
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
                data.append({"Nombre": nombre, "Edad": edad, "Promedio": promedio, "Carnet": carnet})

            imprimir_tabla(data, headers)  # Llamar a la función para imprimir la tabla
    except ValueError as e:
        print(f"Error: {e}")
#%% Función para consultar estudiante por carnet
def consultar_estudiantes_por_carnet():
    try:
        carnet_buscado = int(input("\nIngrese el número de carnet a buscar: "))
        # Itera estudiantes para buscar donde la posición carnet es igual al buscado y retornar todo el disccionario
        estudiantes_encontrados = [estudiante for estudiante in base_de_datos if estudiante["carnet"] == carnet_buscado] 

        if not estudiantes_encontrados:
            print(f"\nNo se encontraron estudiantes con el número de carnet {carnet_buscado}.")
        else:
            print(f"Estudiantes con el número de carnet {carnet_buscado}:")
            headers = ["Nombre", "Edad", "Carrera", "Promedio", "Carnet"]
            data = []

            for estudiante in estudiantes_encontrados:
                nombre = estudiante['nombre']
                edad = estudiante['edad']
                carrera = estudiante['carrera']
                promedio = estudiante['promedio']
                carnet = estudiante['carnet']
                data.append({"Nombre": nombre, "Edad": edad, "Carrera": carrera, "Promedio": promedio, "Carnet": carnet})

            imprimir_tabla(data, headers)  # Llamar a la función para imprimir la tabla
    except ValueError as e:
        print(f"Error: {e}")

#%% Función para calcular el promedio general de todos los estudiantes
def calcular_promedio_general():
    if not base_de_datos:
        print("No hay estudiantes registrados.")
        return
    promedios = map(lambda estudiante: estudiante["promedio"], base_de_datos)
    promedio_general = sum(promedios) / len(base_de_datos)
    print(f"El promedio general de todos los estudiantes es: {promedio_general:.2f}")

#%% Función para ver los estudiantes destacados (con los dos mayores promedios)
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
    
# Base de datos de estudiantes (cargada al inicio del programa)
base_de_datos = cargar_base_de_datos()
    
#%% Función principal
def main():    
    
    if base_de_datos:
        print(f"\nBase de datos cargada con éxito. Total de estudiantes: {len(base_de_datos)}")
    else:
        print("\nAún no hay estudiantes registrados.")
    
    while True:
        print("\nMenú Principal:")
        print("1. Registrar estudiante")
        print("2. Consultar estudiantes por número de carnet")  
        print("3. Consultar estudiantes de una carrera")
        print("4. Calcular promedio general")
        print("5. Ver estudiantes destacados")
        print("6. Salir y guardar")
        print("7. Salir y reset")
        opcion = input("\nSeleccione una opción (1-7): ")
        try:
            if opcion == "1":
                registrar_estudiante()
            elif opcion == "2":
                consultar_estudiantes_por_carnet()  
            elif opcion == "3":
                consultar_estudiantes_carrera()
            elif opcion == "4":
                calcular_promedio_general()
            elif opcion == "5":
                ver_estudiantes_destacados()
            elif opcion == "6":
                guardar_base_de_datos(base_de_datos)
                print("Base de datos guardada en 'estudiantes.pkl'. ¡Adiós!")
                break
            elif opcion == "7":
                resetear_base_de_datos()
            else:
                raise ValueError("Opción no válida. Por favor, seleccione una opción válida (1-7).")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
