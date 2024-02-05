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
# Upload a text file as an object to the storage bucket
resource "google_storage_bucket_object" "titanic" {
 name         = "titanic_clean.csv"
 source       = "./samples/titanic_clean.csv"
 content_type = "text/csv"
 bucket       = google_storage_bucket.bucket.id
}



resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}