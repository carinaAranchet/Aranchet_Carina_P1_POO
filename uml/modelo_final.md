# Modelo UML Final

```mermaid
classDia4gram
    direction TB

    class Exportable {
        <<Protocol>>
        +exportar() str
    }

    class UnidadMedida {
        <<frozen dataclass>>
        +nombre: str
        +simbolo: str
        +tipo: str
    }

    class Categoria {
        -_nombre: str
        -_descripcion: str
        +nombre str
        +descripcion str
    }

    class ProductoCategoria {
        -_categoria: Categoria
        -_es_principal: bool
        +categoria Categoria
        +es_principal bool
        #_marcar_principal(valor: bool) None
    }

    class Producto {
        <<abstract>>
        -_nombre: str
        -_precio_base: float
        -_stock_cantidad: float
        -_habilitado: bool
        -_unidad_venta: UnidadMedida
        -_clasificaciones: list
        +nombre str
        +precio_base float
        +unidad_venta UnidadMedida
        +disponible bool
        +precio_publicado str
        +habilitar() None
        +deshabilitar() None
        +clasificar_en(categoria, es_principal) None
        +categorias() tuple
        +categoria_principal() Categoria
        +exportar() str
        +precio_final(cantidad: float) float*
    }

    class ProductoSimple {
        +precio_final(cantidad: float) float
    }

    class ProductoPorPeso {
        +precio_final(cantidad: float) float
    }

    class ProductoCombo {
        -_componentes: list
        -_descuento: float
        +componentes() tuple
        +precio_final(cantidad: float) float
    }

    class ProductoDestacado {
        -_producto: Producto
        -_orden_vidriera: int
        +producto Producto
        +orden_vidriera int
    }

    class FichaPuntoDeVenta {
        -_codigo: str
        -_detalle: str
        +exportar() str
    }

    Producto <|-- ProductoSimple
    Producto <|-- ProductoPorPeso
    Producto <|-- ProductoCombo

    Producto "1" *-- "1..*" ProductoCategoria : clasificaciones
    ProductoCategoria "0..*" --> "1" Categoria : categoria

    ProductoCombo "1" o-- "2..*" Producto : componentes

    Producto "0..*" --> "0..1" UnidadMedida : unidad_venta

    ProductoDestacado "0..*" --> "1" Producto : producto destacado

    Producto ..|> Exportable : estructural
    FichaPuntoDeVenta ..|> Exportable : estructural
```

## Decisiones de diseño

`Producto` se modela como una clase abstracta porque representa el concepto
general de producto y delega el cálculo de `precio_final()` a sus subclases.

La relación entre `Producto` y `ProductoCategoria` es de composición.
Cada producto crea internamente sus clasificaciones y mantiene siempre una
categoría principal. Los vínculos no son creados directamente por el cliente.

La relación entre `ProductoCombo` y sus componentes es de agregación.
Los productos que forman el combo existen previamente, son recibidos por el
constructor y pueden seguir existiendo o utilizarse en otros combos.

La relación entre `Producto` y `UnidadMedida` es una asociación. La unidad
puede existir independientemente del producto y un producto puede no tener
una unidad de venta asignada.

`ProductoDestacado` fue eliminado de la jerarquía de herencia de `Producto`.
Se decidió modelarlo mediante una asociación con `Producto`, ya que ser
destacado es una condición que puede aplicarse a cualquier tipo de producto:
simple, por peso o combo. El atributo `_orden_vidriera` pertenece a
`ProductoDestacado`.

`Exportable` se modela como un `Protocol`. Tanto `Producto` como
`FichaPuntoDeVenta` cumplen estructuralmente el contrato porque implementan
`exportar()` sin necesidad de heredar de `Exportable`.