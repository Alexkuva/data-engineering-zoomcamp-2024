# Cloud Infrastructure - Terraform

## Setup GCP service account credentials
```
- Add service account json key file in "runtime" -> "gcp" -> "key"
or
- Export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
```

## Initialize the directory
```
terraform init
```

## Format and validate the configuration
```
terraform fmt
```

## Validate your configuration
```
terraform validate
```

## Create infrastructure
```
terraform apply
```

In order to help you, the file titanic_clean.csv is load automatically on GCS through terraform.

# GBQ
Run SQL file in src/script_GBQ.sql