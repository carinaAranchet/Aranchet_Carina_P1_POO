from dataclasses import FrozenInstanceError

from catalogo import (
    Categoria,
    Producto,
    ProductoCombo,
    ProductoDestacado,
    ProductoPorPeso,
    ProductoSimple,
    UnidadMedida,
    exportar_catalogo,
)
from libreria_externa import FichaPuntoDeVenta


def main() -> None:
    # Unidades de medida
    unidad = UnidadMedida("Unidad", "u", "unidad")
    kilogramo = UnidadMedida("Kilogramo", "kg", "masa")

    # Categorías
    bebidas = Categoria("Bebidas", "Productos para beber")
    gaseosas = Categoria("Gaseosas")
    fiambreria = Categoria("Fiambrería")
    promociones = Categoria("Promociones")
    ofertas = Categoria("Ofertas")

    # Productos
    coca = ProductoSimple(
        "Coca Cola",
        2500.0,
        10,
        bebidas,
        unidad,
    )

    agua = ProductoSimple(
        "Agua mineral",
        1200.0,
        15,
        bebidas,
        unidad,
    )

    queso = ProductoPorPeso(
        "Queso",
        8500.0,
        5,
        fiambreria,
        kilogramo,
    )

    salame = ProductoPorPeso(
        "Salame",
        12000.0,
        4,
        fiambreria,
        kilogramo,
    )

    coca.clasificar_en(gaseosas, es_principal=True)

    combo = ProductoCombo(
        "Combo picada",
        [queso, salame],
        0.10,
        promociones,
        6,
        unidad,
    )

    print("=== CATÁLOGO ===")

    productos: list[Producto] = [
        coca,
        agua,
        queso,
        salame,
        combo,
    ]

    for producto in productos:
        print(
            f"{producto.nombre} | "
            f"{producto.precio_publicado} | "
            f"{producto.categoria_principal().nombre} | "
            f"Disponible: {producto.disponible}"
        )

    print("\n=== PRECIOS ===")

    print(f"3 Coca Cola: $ {coca.precio_final(3):.2f}")
    print(f"2 Agua: $ {agua.precio_final(2):.2f}")
    print(f"250 g de queso: $ {queso.precio_final(0.250):.2f}")
    print(f"500 g de salame: $ {salame.precio_final(0.500):.2f}")
    print(f"2 combos: $ {combo.precio_final(2):.2f}")

    print("\n=== CANTIDADES INVÁLIDAS ===")

    try:
        coca.precio_final(2.5)
    except ValueError as error:
        print(f"Coca con cantidad 2.5: {error}")

    try:
        queso.precio_final(0)
    except ValueError as error:
        print(f"Queso con cantidad 0: {error}")

    try:
        combo.precio_final(1.5)
    except ValueError as error:
        print(f"Combo con cantidad 1.5: {error}")

    print("\n=== DISPONIBILIDAD ===")

    print(f"Coca: {coca.disponible}")

    coca.deshabilitar()
    print(f"Coca deshabilitada: {coca.disponible}")

    coca.habilitar()
    print(f"Coca habilitada: {coca.disponible}")

    print("\n=== CATEGORÍAS ===")

    print(
        "Categoría principal de Coca:",
        coca.categoria_principal().nombre,
    )

    resultado = coca.clasificar_en(ofertas)
    print("Resultado de clasificar_en:", resultado)

    print(
        "Cantidad de categorías:",
        len(coca.categorias()),
    )

    try:
        coca.clasificar_en(ofertas)
    except ValueError as error:
        print(f"Categoría repetida: {error}")

    categorias_coca = coca.categorias()

    print(
        "Tipo de dato de categorias():",
        type(categorias_coca).__name__,
    )

    try:
        categorias_coca.append(ofertas)
    except AttributeError:
        print("No se puede hacer append porque es una tupla")

    print("\n=== UNIDAD DE MEDIDA ===")

    print(
        f"Unidad: {kilogramo.nombre} "
        f"({kilogramo.simbolo})"
    )

    try:
        kilogramo.simbolo = "g"
    except FrozenInstanceError:
        print("No se puede modificar porque es frozen")

    print("\n=== COMBO ===")

    print(
        "Componentes:",
        [producto.nombre for producto in combo.componentes()],
    )

    otro_combo = ProductoCombo(
        "Combo alternativo",
        [queso, salame],
        0.05,
        promociones,
        3,
        unidad,
    )

    print(
        "Otro combo con los mismos productos:",
        [
            producto.nombre
            for producto in otro_combo.componentes()
        ],
    )

    print(
        "Tipo de dato de componentes():",
        type(combo.componentes()).__name__,
    )

    print("\n=== DESTACADOS ===")

    destacado_simple = ProductoDestacado(coca, 1)
    destacado_peso = ProductoDestacado(queso, 2)
    destacado_combo = ProductoDestacado(combo, 3)

    print(
        destacado_simple.producto.nombre,
        "- orden:",
        destacado_simple.orden_vidriera,
    )

    print(
        destacado_peso.producto.nombre,
        "- orden:",
        destacado_peso.orden_vidriera,
    )

    print(
        destacado_combo.producto.nombre,
        "- orden:",
        destacado_combo.orden_vidriera,
    )

    print("\n=== EXPORTACIÓN ===")

    ficha = FichaPuntoDeVenta(
        "POS-001",
        "Ficha externa de Food Store",
    )

    items_exportables = [
        coca,
        agua,
        queso,
        salame,
        combo,
        ficha,
    ]

    for item in exportar_catalogo(items_exportables):
        print(item)

    print("\n=== CLASE ABSTRACTA ===")

    class ProductoIncompleto(Producto):
        pass

    try:
        ProductoIncompleto(
            "Producto incompleto",
            1000.0,
            1,
            bebidas,
            unidad,
        )
    except TypeError as error:
        print(f"No se puede crear ProductoIncompleto: {error}")


if __name__ == "__main__":
    main()