# Server - Checkomo
A REST API server for Checkomo - a QR Code Check-In Application

## Related Projects
- [Checkomo Check-In Application](https://github.com/cameronhh/checkomo-check-in)
- [Checkomo Client Dashboard](https://github.com/cameronhh/checkomo-dashboard)


## Setting up the development environment
### Database

Checkomo is built on top of Postgres.
You can locally run a development database with docker using the following command:

```
docker run -d -p 5432:5432 \
--name checkomo-postgres \
-e POSTGRES_USER=dev \
-e POSTGRES_PASSWORD=mysecretpassword \
-e POSTGRES_DB=checkomo-dev-db \
postgres
```

### Running the server locally
0. Create and source a virtual environment with Python >= 3.6
1. Run `pip install -r requirements.txt` to install dependencies
2. Set your PostgreSQL connection string as an environment variable named `CKMO_DATABASE_URI`
3. Run the server with `python main.py`


## Deployment
A docker image for this server can built by running:
```
docker built -t checkomo-server .
```

Then the server can be run with (Note the server runs on port 8002 inside the container):
```
docker run -d -p 8080:8002 \
--name checkomo-server-container \
-e CKMO_DATABASE_URI='postgresql://postgres:mysecretpassword@127.0.0.1:5432/checkomo-test-db' \
checkomo-flask-server
```
