'''
=================================================
Milestone 3

Name: Rivaldi Valensia
Batch: FTDS-007-HCK

Program ini dibuat untuk melakukan automatisasi transform dan load datamenggunakan PostgreSQL, Airflow dan Visualisasi menggunakan ElasticSearch& Kibana. 
Adapun dataset yang digunakan adalah dataset mengenai data restaurant.
=================================================
'''

import pandas as pd
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint

context = gx.get_context()
datasource = context.sources.add_pandas(name="my_pandas_datasource")
dataframe = pd.read_csv('/Users/valdi/Desktop/Milestone 3/p2-ftds007-hck-m3-rivaldivlns/data/P2M3_Valdi_data_clean.csv')

name = "restaurant"
data_asset = datasource.add_dataframe_asset(name=name)
my_batch_request = data_asset.build_batch_request(dataframe=dataframe)

expectation_suite_name = "Milestone3"
context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)
validator = context.get_validator(
    batch_request=data_asset.build_batch_request(dataframe=dataframe),
    expectation_suite_name=expectation_suite_name,)

# 1. Expect each value in the 'id' column to be unique
validator.expect_column_values_to_be_unique(column='id')

# 2. Expect 'area' and 'city' columns to not have any null values
validator.expect_column_values_to_not_be_null(column='area')
validator.expect_column_values_to_not_be_null(column='city')

# 3. Expect 'price' to be of integer type and greater than 0
validator.expect_column_values_to_be_of_type(column='price', type_='int')
validator.expect_column_values_to_be_between(column='price', min_value=0, max_value=2500)

# 4. Expect 'average_ratings' to be of integer type and between 1 and 5
validator.expect_column_values_to_be_of_type(column='average_ratings', type_='int')
validator.expect_column_values_to_be_between(column='average_ratings', min_value=1, max_value=5)

# 5. Expect 'total_ratings' to be non-negative
validator.expect_column_values_to_be_between(column='total_ratings', min_value=0)

# 6. Expect 'food_type' to not be empty
validator.expect_column_values_to_not_be_null(column='food_type')

# 7. Expect 'delivery_time' to be greater than 0
validator.expect_column_values_to_be_between(column='delivery_time', min_value=1)

# Validate the data and save the results
validator.save_expectation_suite(discard_failed_expectations=False)

my_checkpoint_name = "Milestone3_Rivaldi_Checkpoint"

checkpoint = Checkpoint(
    name=my_checkpoint_name,
    run_name_template="%Y%m%d-%H%M%S-Milestone3_Rivaldi_Checkpoint",
    data_context=context,
    batch_request=my_batch_request,
    expectation_suite_name=expectation_suite_name,
    action_list=[
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
    ],
)

context.add_or_update_checkpoint(checkpoint=checkpoint)
checkpoint_result = checkpoint.run()
context.run_data_docs()