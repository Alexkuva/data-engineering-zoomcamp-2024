resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

resource "google_bigquery_table" "green_tripdata" {
  dataset_id  = google_bigquery_dataset.dataset.dataset_id
  table_id    = "green_tripdata"

  deletion_protection=false

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    ignore_unknown_values = true
    source_uris = [
      "gs://${var.gcs_bucket_name}/green__tripdata/*"
    ]
  }
}

resource "google_bigquery_table" "yellow_tripdata" {
  dataset_id  = google_bigquery_dataset.dataset.dataset_id
  table_id    = "yellow_tripdata"

  deletion_protection=false

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    ignore_unknown_values = true
    source_uris = [
      "gs://${var.gcs_bucket_name}/yellow__tripdata/*"
    ]
  }
}

resource "google_bigquery_table" "fhv_tripdata" {
  dataset_id  = google_bigquery_dataset.dataset.dataset_id
  table_id    = "fhv_tripdata"

  deletion_protection=false

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    ignore_unknown_values = true
    source_uris = [
      "gs://${var.gcs_bucket_name}/fhv__tripdata/*"
    ]
  }
}