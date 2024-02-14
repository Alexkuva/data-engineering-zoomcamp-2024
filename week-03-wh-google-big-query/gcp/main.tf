resource "google_storage_bucket" "bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
locals {
  file_prefix = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
}
# Upload a text file as an object to the storage bucket
resource "google_storage_bucket_object" "green_tripdata" {
 for_each =  toset(local.file_prefix)
 name         = "green_tripdata/tripdata_2022-${each.value}.parquet"
 source       = "./samples/green_tripdata_2022-${each.value}.parquet"
 content_type = "text/plain"
 bucket       = google_storage_bucket.bucket.id
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

resource "google_bigquery_table" "green_tripdata" {
  dataset_id  = google_bigquery_dataset.dataset.dataset_id
  table_id    = "green_dataset"

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    ignore_unknown_values = true
    source_uris = [
      "gs://${var.gcs_bucket_name}/green_tripdata/*"
    ]
  }
}


