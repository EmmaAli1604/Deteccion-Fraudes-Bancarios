from kedro.pipeline import Node, Pipeline

from .nodes import (
    cargar_datos,
    minusculizar_columnas,
    eliminar_duplicados,
    eliminar_nulos,
    convertir_a_numerico
)

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=cargar_datos,
                inputs="transacciones_bancarias_raw",
                outputs="loaded_data",
                name="cargar_datos_node",
            ),
            Node(
                func=minusculizar_columnas,
                inputs="loaded_data",
                outputs="columnas_minusculas",
                name="minusculizar_columnas_node",
            ),
            Node(
                func=eliminar_duplicados,
                inputs="columnas_minusculas",
                outputs="sin_duplicados",
                name="eliminar_duplicados_node",
            ),
            Node(
                func=eliminar_nulos,
                inputs="sin_duplicados",
                outputs="sin_nulos",
                name="eliminar_nulos_node",
            ),
            Node(
                func=convertir_a_numerico,
                inputs="sin_nulos",
                outputs="convertidos_a_numerico",
                name="convertir_a_numerico_node",
            ),   
        ]
    )
