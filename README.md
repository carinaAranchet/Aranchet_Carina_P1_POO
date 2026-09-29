# Primera Evaluación Parcial - Programación IV

**Alumna:** Carina Aranchet  
**Proyecto:** Catálogo Food Store  
**Lenguaje:** Python 3.12+

## Descripción

En este proyecto se desarrolla un catálogo de productos para Food Store aplicando
los conceptos vistos en la unidad: encapsulamiento, herencia, clases abstractas,
composición, agregación, asociación y uso de Protocol.

El catálogo permite trabajar con productos simples, productos vendidos por peso
y combos formados por otros productos.

## Estructura

```text
Aranchet_Carina_P1_POO/
├── README.md
├── catalogo.py
├── libreria_externa.py
├── main.py
├── link_video.txt
└── uml/
    └── modelo_final.md
```

Para ejecutar el proyecto:

```bash
python main.py
```

No se utilizaron librerías externas.

## Productos

`Producto` es una clase abstracta donde se define lo que tienen en común todos
los productos.

Cada tipo de producto implementa su propia forma de calcular el precio mediante:

```python
precio_final(cantidad: float) -> float
```

### ProductoSimple

Se utiliza para los productos que se venden por unidad.

La cantidad tiene que ser un número entero mayor o igual a 1. Por ejemplo,
`3` y `3.0` son válidos, pero `2.5` no.

El precio se calcula multiplicando el precio base por la cantidad.

### ProductoPorPeso

Se utiliza para productos que se venden por peso.

En este caso se permiten cantidades decimales mayores que cero y el resultado
se redondea a dos decimales.

### ProductoCombo

Un combo se forma con al menos dos productos que ya existen en el catálogo.

Los componentes se reciben desde afuera, por lo que no dependen del combo para
existir y también pueden utilizarse en otros combos.

El precio base lo calculé a partir de la suma del precio de una unidad de cada
componente. Después, para calcular el precio final, se aplica el descuento y se
multiplica por la cantidad solicitada.

También decidí que el combo tenga su propio stock. Ese stock representa la
cantidad de combos disponibles para vender y no modifica el stock individual
de los productos que lo forman.

## Relaciones entre las clases

### Composición

Entre `Producto` y `ProductoCategoria` utilicé composición.

Cuando se crea un producto se recibe su categoría principal, pero el
`ProductoCategoria` se crea internamente dentro de `Producto`.

También es `Producto` quien controla cuál de sus categorías es la principal.

### Agregación

Entre `ProductoCombo` y `Producto` utilicé agregación.

Los productos que forman un combo ya existen antes de crear el combo y pueden
seguir existiendo de forma independiente. También pueden formar parte de otro
combo.

### Asociación

Entre `Producto` y `UnidadMedida` utilicé asociación.

La unidad de medida existe de manera independiente y además es opcional para
el producto.

`UnidadMedida` está definida como `@dataclass(frozen=True)` para que no se pueda
modificar después de crearla.

## Categorías

Cada producto se crea con una categoría principal.

Después se pueden agregar otras categorías con `clasificar_en()`. Si una nueva
categoría pasa a ser principal, la anterior deja de serlo.

No se permite agregar dos veces la misma categoría.

El método `categorias()` devuelve una tupla para no permitir que desde afuera
se modifique directamente la lista interna del producto.

## ProductoDestacado

En el diagrama inicial `ProductoDestacado` aparecía heredando de `Producto`,
pero decidí cambiar esa relación.

Para mí, que un producto sea destacado no significa que sea un tipo distinto
de producto. Un producto simple, uno por peso o incluso un combo pueden estar
destacados.

Por eso `ProductoDestacado` tiene una referencia a un `Producto` y guarda el
`orden_vidriera`.

De esta forma no necesito crear otra regla de precio solamente por el hecho de
que un producto esté destacado y puedo aplicar el destacado a cualquiera de
los tipos de producto.

## Clase abstracta y polimorfismo

`Producto` hereda de `ABC` y tiene `precio_final()` como método abstracto.

Esto hace que cada subclase tenga que implementar su propia forma de calcular
el precio. Si se intenta crear una subclase que no implementa `precio_final()`,
Python no permite instanciarla.

Para calcular los precios no necesito preguntar qué tipo de producto es con
`if`, `elif` o `isinstance`. Cada objeto responde a `precio_final()` según su
propia implementación.

## Exportable

Para la exportación utilicé un `Protocol`.

```python
class Exportable(Protocol):
    def exportar(self) -> str:
        ...
```

Elegí este tipo de contrato porque no necesito que las clases hereden
directamente de `Exportable`. Si tienen el método `exportar()` con la firma
esperada, cumplen con el contrato.

Esto permite trabajar tanto con los productos del catálogo como con
`FichaPuntoDeVenta`, que viene de una librería externa que no se puede
modificar.

La función:

```python
exportar_catalogo(items: list[Exportable]) -> list[str]
```

puede recibir ambos tipos de objetos y exportarlos juntos.

## Encapsulamiento

Los atributos internos están definidos con `_` y se exponen solamente cuando
es necesario.

Por ejemplo, `_habilitado` no se modifica directamente. Para cambiar su estado
se utilizan:

```python
habilitar()
deshabilitar()
```

La propiedad `disponible` indica si el producto está habilitado y además tiene
stock mayor que cero.

También se utilizan tuplas en `categorias()` y `componentes()` para no devolver
las listas internas directamente.

## UML

El diagrama final está en:

```text
uml/modelo_final.md
```

El UML representa el modelo que finalmente implementé, incluyendo el cambio
realizado en `ProductoDestacado`.

## Librería externa

`libreria_externa.py` contiene la clase `FichaPuntoDeVenta` entregada en la
consigna y no fue modificada.

## Video

El enlace a la defensa se encuentra en:

```text
link_video.txt
```