"""
Este módulo contém a classe FlatJson. Esta é uma classe que fornece
métodos para reazliar um flat em estruturas JSON e realizar a normalização em um DataFrame PySpark.
"""

from pyspark.sql.functions import col, explode_outer

class FlatJson:
    """
    Uma classe que fornece métodos para realizar o flat estruturas JSON em um DataFrame PySpark.

    A funcionalidade principal desta classe gira em torno de realizar o flat de estruturas JSON,
    e converter colunas de array.
    """

    def __init__(self):
        """
        Inicializa uma nova instância da classe FlatJson.
        """
        pass
    
    def flatten_structs_first_level(self, array_df):
        """
        Realiza o flat do objeto no primeiro nível de estruturas dentro de colunas de array em um DataFrame PySpark.

        Este método realiza o flat apenas no primeiro nível de estruturas dentro de colunas do tipo array,
        explodindo as colunas de array sem a necessidade de fornecer um schema, ao mesmo tempo 
        selecionando os campos do primeiro nível de estruturas.

        Parâmetros:
        - array_df (pyspark.sql.dataframe.DataFrame): O DataFrame com colunas de array contendo estruturas.

        Retorna:
        pyspark.sql.dataframe.DataFrame: O DataFrame normalizado no primeiro nivel de forma automatica.
        """
        array_cols = [c[0] for c in array_df.dtypes if c[1][:5] == "array"]

        for array_col in array_cols:
            array_df = array_df.withColumn(array_col, explode_outer(col(array_col)))

            struct_fields = [
                f"{array_col}.{field.name}" for field in array_df.schema[array_col].dataType.fields
            ]

            array_df = array_df.select("*", *struct_fields).drop(array_col)

        return array_df
    
