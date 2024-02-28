from pyspark.sql import SparkSession

from src.MeliApi import MeliEngineSearch


def run():
    spark = SparkSession.builder.appName("MeliSearchPipeline").getOrCreate()

    meli_engine = MeliEngineSearch(spark)

    search_results_df = meli_engine.get_search_results('chromecast', 'id')
    
    list_items_id = [item_id[0] for item_id in search_results_df.select('id').collect()]

    item_columns = ['id','site_id','title','seller_id','date_created','last_updated']
    df_items = meli_engine.process_items_parallel(list_items_id, item_columns)

    df_items.show()

if __name__ == '__main__':
    run()
