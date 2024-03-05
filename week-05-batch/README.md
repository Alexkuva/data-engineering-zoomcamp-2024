# Docker compose configuration

## run docker-compose.yaml
```dockerfile
docker-compose up -d
```

## check available containers
```dockerfile
docker-compose ps
```

## check all containers
```dockerfile
docker-compose ps -a
```

## check log to a specific container (e.g. ingest_data)
```dockerfile
docker-compose logs -f jupyter-notebook
```

## stop, then delete a specific container (e.g. ingest_data)
```dockerfile
docker-compose stop jupyter-notebook
docker-compose rm ingejupyter-notebookst_data
```

## shell connect to a specific container (e.g. ingest_data)
```dockerfile
docker-compose exec -it jupyter-notebook sh
```

# Download files
## Give permission to execute file
```sh
chmod u+x scripts/download_data.sh
```
## Download 2019 fhv files
```sh
./scripts/download_data.sh fhv 2019
```


# Using Jupyter's spark docker image
Documentation [here](https://hub.docker.com/r/jupyter/pyspark-notebook/)

You can also use Bitnami's spark docker image - Documentation [here](https://github.com/bitnami/containers/tree/main/bitnami/spark)

## Accessing Jupyter Notebook
After running the container, Jupyter Notebook will be accessible in your web browser. Look for a URL in the terminal output similar to:
```sh
http://127.0.0.1:8888/?token=your_token_here
```
Click on the link or copy-paste it into your browser. You'll be prompted to enter the token provided in the terminal.

You can find a full setup on my medium article [here](https://medium.com/@alexandre.bergere/running-pyspark-on-jupyter-notebook-with-docker-on-mac-a-step-by-step-guide-0b2e3bad1930)