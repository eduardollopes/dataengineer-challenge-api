"""
Meli Engine Search

Este módulo fornece uma classe para realizar pesquisas na API do Mercado Livre e processar dados de itens de forma assíncrona.
"""
import requests
from concurrent.futures import ThreadPoolExecutor
import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(current_dir, "..")  
sys.path.append(project_dir)

from utils.FlatJson import FlatJson


class MeliEngineSearch:
    """
    Classe para realizar pesquisas na API do Mercado Livre e processar dados de itens de forma assíncrona.

    Atributos:
    - spark: Uma instância do SparkSession para processamento de dados.
    - flat_json: Uma instância da classe FlatJson para aplanar dados JSON.

    Métodos Públicos:
    - get_search_results(query_filter, select_columns): Realiza uma pesquisa na API do Mercado Livre com base no filtro de consulta.
    - get_item_data(item_id): Obtém dados detalhados de um item específico usando seu ID.
    - process_items_parallel(list_items_id, select_columns, max_threads=3): Processa dados de vários itens de forma paralela.

    """
    def __init__(self, spark):
        """
        Inicializa a instância da classe MeliEngineSearch.

        Parâmetros:
        - spark: Uma instância do SparkSession.
        """
        self.spark = spark
        self.flat_json = FlatJson()

    def get_search_results(self, query_filter, select_columns):
        """
        Obtém resultados de pesquisa da API do Mercado Livre.

        Parâmetros:
        - query_filter: Termo de pesquisa.
        - select_columns: Colunas selecionadas para o resultado.

        Retorna:
        Um DataFrame contendo os resultados da pesquisa.
        """  
        offset = 0
        final_df = None

        while True:
            url = f'https://api.mercadolibre.com/sites/MLA/search?q={query_filter}&limit=50&offset={offset}'
            response = requests.get(url)
            data = response.text
            json_rdd = self.spark.sparkContext.parallelize([data])
            df_json = self.spark.read.json(json_rdd).select("results")

            if len(df_json.collect()[0][0]) == 0:
                break

            df = self.flat_json.flatten_structs_first_level(df_json).select(select_columns)

            if final_df is None:
                final_df = df
            else:
                final_df = final_df.union(df)

            offset += 50

        return final_df
    
    def get_item_data(self, item_id):
        """
        Obtém dados detalhados de um item específico usando seu ID.

        Parâmetros:
        - item_id: ID do item.

        Retorna:
        Dados detalhados do item em formato JSON.
        """
        url = f'https://api.mercadolibre.com/items/{item_id}'
        response = requests.get(url)
        data = response.text
        return data
    
    def process_items_parallel(self, list_items_id, select_columns, max_threads=3):
        """
        Processa dados de vários itens de forma paralela.

        Parâmetros:
        - list_items_id: Lista de IDs de itens a serem processados.
        - select_columns: Colunas selecionadas para o resultado.
        - max_threads: Número máximo de threads para execução paralela.

        Retorna:
        Um DataFrame contendo os dados processados dos itens.
        """
        results_list = []

        with ThreadPoolExecutor(max_threads) as executor:
            results = executor.map(self.get_item_data, list_items_id)
            results_list.extend(results)

        json_rdd = self.spark.sparkContext.parallelize(results_list)
        df_items = self.spark.read.json(json_rdd).select(select_columns)

        return df_items
