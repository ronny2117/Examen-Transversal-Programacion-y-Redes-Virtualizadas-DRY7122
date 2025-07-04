def verificar_as(numero_as):
    # Rango de AS públicos (1-64511) y privados (64512-65534)
    if 1 <= numero_as <= 64511:
        return "público"
    elif 64512 <= numero_as <= 65534:
        return "privado"
    else:
        return "inválido (fuera del rango conocido)"

def main():
    print("Verificador de AS de BGP")
    try:
        as_number = int(input("Ingrese el número de AS: "))
        tipo = verificar_as(as_number)
        print(f"El AS {as_number} es {tipo}")
    except ValueError:
        print("Error: Debe ingresar un número válido")

if __name__ == "__main__":
    main()
