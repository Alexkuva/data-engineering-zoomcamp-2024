# Module 2 Homework

## Workflow Orchestration
The goal will be to construct an ETL pipeline that loads the data, performs some transformations, and writes the data to a database (and Google Cloud!).

## Question 1. Data Loading
### Once the dataset is loaded, what's the shape of the data?
- 266,855 rows x 20 columns

## Question 2. Data Transformation
### Upon filtering the dataset where the passenger count is greater than 0 and the trip distance is greater than zero, how many rows are left?
- 139,370 rows

## Question 3. Data Transformation
### Which of the following creates a new column lpep_pickup_date by converting lpep_pickup_datetime to a date?
- data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

## Question 4. Data Transformation
### What are the existing values of VendorID in the dataset?
- 1 or 2
```
print(data['vendor_id'].unique())
```

## Question 5. Data Transformation
### How many columns need to be renamed to snake case?
- 4
```
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
```

## Question 6. Data Exporting
### Once exported, how many partitions (folders) are present in Google Cloud?
- 96

```
@data_exporter
def export_data(data, *args, **kwargs):

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
```