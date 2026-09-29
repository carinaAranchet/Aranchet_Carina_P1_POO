from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Exportable(Protocol):
    def exportar(self) -> str:
        ...


@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                "El nombre de la categoría no puede estar vacío"
            )

        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion


class ProductoCategoria:
    def __init__(
        self,
        categoria: Categoria,
        es_principal: bool = False,
    ) -> None:
        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal

    def _marcar_principal(self, valor: bool) -> None:
        self._es_principal = valor


class Producto(ABC):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        categoria_principal: Categoria,
        unidad_venta: UnidadMedida | None = None,
    ) -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                "El nombre del producto no puede estar vacío"
            )

        if precio_base < 0:
            raise ValueError(
                "El precio base no puede ser negativo"
            )

        if stock_cantidad < 0:
            raise ValueError(
                "El stock no puede ser negativo"
            )

        if not isinstance(categoria_principal, Categoria):
            raise ValueError(
                "La categoría principal debe ser una Categoria"
            )

        if (
            unidad_venta is not None
            and not isinstance(unidad_venta, UnidadMedida)
        ):
            raise ValueError(
                "La unidad de venta debe ser una UnidadMedida"
            )

        self._nombre = nombre
        self._precio_base = precio_base
        self._stock_cantidad = stock_cantidad
        self._habilitado = True
        self._unidad_venta = unidad_venta

        # Composición:
        # Producto crea internamente su ProductoCategoria principal.
        self._clasificaciones: list[ProductoCategoria] = [
            ProductoCategoria(categoria_principal, True)
        ]

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> UnidadMedida | None:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        precio = f"$ {self._precio_base:.2f}"

        if self._unidad_venta is not None:
            precio += f" / {self._unidad_venta.simbolo}"

        return precio

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def clasificar_en(
        self,
        categoria: Categoria,
        es_principal: bool = False,
    ) -> None:
        if not isinstance(categoria, Categoria):
            raise ValueError(
                "La categoría debe ser una Categoria"
            )

        if any(
            vinculo.categoria is categoria
            for vinculo in self._clasificaciones
        ):
            raise ValueError(
                "El producto ya está clasificado en esa categoría"
            )

        if es_principal:
            for vinculo in self._clasificaciones:
                if vinculo.es_principal:
                    vinculo._marcar_principal(False)

        self._clasificaciones.append(
            ProductoCategoria(categoria, es_principal)
        )

    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        for vinculo in self._clasificaciones:
            if vinculo.es_principal:
                return vinculo.categoria

        raise ValueError(
            "El producto no tiene una categoría principal"
        )

    def exportar(self) -> str:
        return (
            f"{self._nombre} | "
            f"{self.precio_publicado} | "
            f"Categoría: {self.categoria_principal().nombre}"
        )

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        pass


class ProductoSimple(Producto):
    def precio_final(self, cantidad: float) -> float:
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
            or cantidad < 1
            or not float(cantidad).is_integer()
        ):
            raise ValueError(
                "La cantidad debe ser un valor entero "
                "mayor o igual a 1"
            )

        return self._precio_base * cantidad


class ProductoPorPeso(Producto):
    def precio_final(self, cantidad: float) -> float:
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad debe ser mayor que 0"
            )

        return round(
            self._precio_base * cantidad,
            2,
        )


class ProductoCombo(Producto):
    def __init__(
        self,
        nombre: str,
        componentes: list[Producto],
        descuento: float,
        categoria_principal: Categoria,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None = None,
    ) -> None:
        if len(componentes) < 2:
            raise ValueError(
                "Un combo debe tener al menos 2 componentes"
            )

        if not all(
            isinstance(componente, Producto)
            for componente in componentes
        ):
            raise ValueError(
                "Todos los componentes deben ser productos"
            )

        if descuento < 0 or descuento >= 1:
            raise ValueError(
                "El descuento debe estar entre 0 y 1"
            )

        # Agregación:
        # los productos ya existen y son recibidos por el combo.
        self._componentes = list(componentes)
        self._descuento = descuento

        # El precio base del combo se deriva de sus componentes.
        precio_base = sum(
            componente.precio_final(1)
            for componente in self._componentes
        )

        super().__init__(
            nombre,
            precio_base,
            stock_cantidad,
            categoria_principal,
            unidad_venta,
        )

    def componentes(self) -> tuple[Producto, ...]:
        return tuple(self._componentes)

    def precio_final(self, cantidad: float) -> float:
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
            or cantidad < 1
            or not float(cantidad).is_integer()
        ):
            raise ValueError(
                "La cantidad debe ser un valor entero "
                "mayor o igual a 1"
            )

        suma_componentes = sum(
            componente.precio_final(1)
            for componente in self._componentes
        )

        return (
            suma_componentes
            * (1 - self._descuento)
            * cantidad
        )


class ProductoDestacado:
    """
    Representa la condición de destacado de un producto.

    No hereda de Producto porque "destacado" no define
    un tipo de producto. Cualquier Producto puede ser
    destacado independientemente de su forma de venta.
    """

    def __init__(
        self,
        producto: Producto,
        orden_vidriera: int,
    ) -> None:
        if not isinstance(producto, Producto):
            raise ValueError(
                "Solo se puede destacar un Producto"
            )

        if (
            not isinstance(orden_vidriera, int)
            or isinstance(orden_vidriera, bool)
            or orden_vidriera < 1
        ):
            raise ValueError(
                "El orden de vidriera debe ser un entero "
                "mayor o igual a 1"
            )

        self._producto = producto
        self._orden_vidriera = orden_vidriera

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def orden_vidriera(self) -> int:
        return self._orden_vidriera


def exportar_catalogo(
    items: list[Exportable],
) -> list[str]:
    return [item.exportar() for item in items]