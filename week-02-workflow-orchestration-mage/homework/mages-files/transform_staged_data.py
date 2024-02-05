import pandas as pd
import numpy as np
import re
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Check camel_to_snake transformation
    def check_camel_to_snake(name):
        check_transformation=0
        result = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        if name != result:
            print (f"Transformed column from {name} to {result}")
            check_transformation=1
        return check_transformation

    counter=0
    for col in data.columns:
        counter+=check_camel_to_snake(col)
    print("Preprocessing: number of columns transformed from camel to snake : ", counter)

    # Rename columns in Camel Case to Snake Case
    data.columns = (data.columns
                    .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                    .str.lower()
    )

    # Print disctinct values for vendor_id
    print(data['vendor_id'].unique())

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date
    data['lpep_pickup_date'] = pd.to_datetime(data['lpep_pickup_datetime'].dt.date)

    print("Preprocessing: rows with zero passengers : ", data['passenger_count'].isin([0]).sum())

    # Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero
    return data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]



@test
def test_passenger_count(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with 0 passengers'

@test
def test_trip_distance_count(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with no trip_distance'


@test
def test_output_none(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
