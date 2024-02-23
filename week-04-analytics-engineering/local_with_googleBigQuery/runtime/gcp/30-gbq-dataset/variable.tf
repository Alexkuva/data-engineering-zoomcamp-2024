variable "credentials" {
  description = "GCP credentials"
}

variable "project" {
  description = "Project"
}

variable "region" {
  description = "Region"
}

variable "location" {
  description = "Project Location"
}

variable "gcs_bucket_name" {
  description = "Bucket Name"
  default     = "terraform-engineering-wk1"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "zoomcamp_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
}