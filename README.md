# Proof of Concept: Auth Environment

## Table of Contents
***
1. [Technologies](#technologies)
2. [Installation](#installation)
3. [Setting up Kong, Konga and Keycloak](#auth-services-set-up)
4. [Setting up Local Microservices](#microservices-set-up)


## Technologies
***
A list of technologies used within the project:
* [Docker](https://www.docker.com) 
* [Python](https://www.python.org): Version 3.10
* [FastApi](https://fastapi.tiangolo.com): Version 0.79.0
* [Postgres Image](https://hub.docker.com/_/postgres): Version 9.6
* [Kong Image](https://hub.docker.com/_/kong): Latest Version 
* [Konga Image](https://hub.docker.com/r/pantsel/konga): Latest Version
* [Keycloak Image](quay.io/repository/keycloak/keycloak): Version 17.0.0
* [Kong OIDC Plugin](https://github.com/nokia/kong-oidc)
* [Lua Resty JWT Plugin](https://github.com/SkyLothar/lua-resty-jwt)
* [Kong JWT Keycloak Plugin](https://github.com/BGaunitz/kong-plugin-jwt-keycloak)


## Installation
***
A little intro about the installation. 
```bash
$ git clone https://example.com
```

## Auth Services Set Up
***
Run this repo from your command line.
```bash
$ cd kong
$ docker compose up --build

# Konga admin panel will start at: http://localhost:1337
# Keycloak admin panel will start at: http://localhost:8180
# Kong admin api will start at: http://localhost:8001
# Kong services api will start at: http://localhost:8000
```

### Konga Configuration
1. Create an Admin user
2. Login with admin user credentials
3. Create a connection with kong (for 'kong admin url' parameter use: http://kong:8001)

### Microservices Set Up
Run this repo from your command line.
```bash
$ docker compose up --build

# ServiceA will start at: http://localhost:5000
# ServiceB will start at: http://localhost:7000
# auth-api will start at: http://localhost:1000
```

4. Go to Services Page > Add new Service 
5. Set host and name to servicea and port to 5000 > Submit Service
6. Click on servicea link > Go to routes > Add Route
7. Set name field to articles
8. Set paths field to /api/v1/articles
9. Set strip path to no and preserve host to yes > Submit Route

### Keycloak Configuration
1. Click on 'Administration Console'
2. Login with default credentials (username and password are 'admin')
3. Create a new Realm 
4. Go to 'Clients' > 'Create'
5. Create a client with Client Id: kong and Root URL: http://localhost:8000
6. In Settings page, set Access Type to 'confidential' and save it
7. Go to Credentials page and copy the Secret value (set secrete to client_secret value on main.py for servicea)
8. Create a new client, but with Access Type 'public'
9. Go to Users page > Add User > Set email verified to On
10. Go to Credentials > Create a new password, with temporary field off
11. Go to Roles page > Add Role > Set a role name (we used 'reader')
12. Go to Users page > iew All Users > Edit > Role Mappings > Add reader role to user
13. Go to Konga panel

### Plugins Configuration (Konga)
1. Go to plugins > Add Global Plugins > Other > Oidc > Add Plugin
2. Set the client secret field with the value that was copied 
3. Set Bearer Only field to yes
4. Set Client Id Field to kong
5. Set Introspection Endpoint field to 'http://keycloak:8080/realms/${REALM}/protocol/openid-connect/token/introspect'
6. Set Discovery field to 'http://keycloak:8080/auth/realms/${REALM}/.well-known/openid-configuration'
7. Go to Services page > servicea > plugins > add plugin > other > JWT Keycloak
8. Set realm roles to reader and allowed iss to 'http://keycloak:8080/realms/${REALM}'

### Test
1. Generate a JWT:
```bash
$ curl --location --request POST 'http://localhost:1000/api/v1/token' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "username": "username",
            "password": "password"
        }'
```
2. Call articles API:
```bash
$ curl --location --request GET 'http://localhost:8000/api/v1/articles' \
--header 'Authorization: Bearer JWTVALUE'
```

### Front Integration
1. Add http://localhost:3000 to CORS plugin