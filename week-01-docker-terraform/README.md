# run docker-compose.yaml
docker-compose up -d

# check available containers
docker-compose ps

# check all containers
docker-compose ps -a

# check log to a specific container (e.g. ingest_data)
docker-compose logs -f ingest_data

# stop, then delete a specific container (e.g. ingest_data)
docker-compose stop ingest_data 
docker-compose rm ingest_data

# rebuild ingest_data (if necessary)
docker-compose build ingest_data

# shell connect to a specific container (e.g. ingest_data)
docker-compose exec -it ingest_data sh