from pyspark.sql import SparkSession

from src.MeliApi import MeliEngineSearch


def run(product_search):
    spark = SparkSession.builder.appName("MeliSearchPipeline").getOrCreate()

    meli_engine = MeliEngineSearch(spark)

    search_results_df = meli_engine.get_search_results(product_search, 'id')
    
    list_items_id = [item_id[0] for item_id in search_results_df.select('id').collect()]

    item_columns = ['id','site_id','title','seller_id','price','date_created','last_updated']
    df_items = meli_engine.process_items_parallel(list_items_id, item_columns)

    return df_items

if __name__ == '__main__':

    list_of_search = ['chromecast', 'fire tv', 'apple tv']
    df = None

    for product in list_of_search:
        if df is None:
            df = run(product_search= product)
        else: 
            df_items = run(product_search= product)
            df.union(df_items)

    df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .option("encoding", "UTF-8") \
        .csv("/app/data/files")



