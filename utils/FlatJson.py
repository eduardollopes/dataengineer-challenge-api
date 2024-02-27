""""
This module contains the FlatJson class. This is a Class that provides 
methods to flatten nested JSON structures in a PySpark DataFrame.
"""

from pyspark.sql.functions import col, explode_outer

class FlatJson:
    """
    A class that provides methods to flatten nested JSON structures in a PySpark DataFrame.

    The main functionality of this class revolves around flattening nested structures,
    converting array columns to string representation, and cleaning column names.
    """

    def __init__(self):
        """
        Initializes a new instance of the FlatJson class.
        """
        pass
    
    def flatten_structs_first_level(self, array_df):
        """
        Flattens the first level of structs within array columns in a PySpark DataFrame.

        This method flattens only the first level of structs within array columns by
        exploding the array columns and selecting the fields of the first level of structs.

        Parameters:
        - array_df (pyspark.sql.dataframe.DataFrame): The DataFrame with array columns containing structs.

        Returns:
        pyspark.sql.dataframe.DataFrame: The flattened DataFrame.
        """
        array_cols = [c[0] for c in array_df.dtypes if c[1][:5] == "array"]

        for array_col in array_cols:
            array_df = array_df.withColumn(array_col, explode_outer(col(array_col)))

            struct_fields = [
                f"{array_col}.{field.name}" for field in array_df.schema[array_col].dataType.fields
            ]

            array_df = array_df.select("*", *struct_fields).drop(array_col)

        return array_df