import requests
from concurrent.futures import ThreadPoolExecutor
import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(current_dir, "..")  
sys.path.append(project_dir)

from utils.FlatJson import FlatJson


class MeliEngineSearch:
    def __init__(self, spark):

        self.spark = spark
        self.flat_json = FlatJson()

    def get_search_results(self, query_filter, select_columns):
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
        url = f'https://api.mercadolibre.com/items/{item_id}'
        response = requests.get(url)
        data = response.text
        return data
    
    def process_items_parallel(self, list_items_id, select_columns, max_threads=5):
        results_list = []

        with ThreadPoolExecutor(max_threads) as executor:
            results = executor.map(self.get_item_data, list_items_id)
            results_list.extend(results)

        json_rdd = self.spark.sparkContext.parallelize(results_list)
        df_items = self.spark.read.json(json_rdd).select(select_columns)

        return df_items
