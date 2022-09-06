# Proof of Concept: Auth Environment

## Table of Contents
***
1. [Technologies](#technologies)
2. [Installation](#installation)
3. [Running Containers](#running-containers)
3. [Configuration](#configuration)
4. [Testing Endpoints](#testing-endpoints)
5. [Same Route for Different Clients](#same-route-for-different-clients)


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
* Prometheus Image: Latest Version
* [Grafana Image](https://hub.docker.com/r/grafana/grafana): Latest Version
* [Loki Image](https://hub.docker.com/r/grafana/loki): Latest Version
* [Promtail Image](https://hub.docker.com/r/grafana/promtail): Latest Version
* [Vault Image](https://hub.docker.com/_/vault): Latest Version
* [Rabbitmq Image](https://hub.docker.com/_/rabbitmqt): Version 3-management-alpine
* [Kong OIDC Plugin](https://github.com/nokia/kong-oidc)
* [Lua Resty JWT Plugin](https://github.com/SkyLothar/lua-resty-jwt)
* [Kong JWT Keycloak Plugin](https://github.com/BGaunitz/kong-plugin-jwt-keycloak)
* [Apple Social Identity Provider for Keycloak](https://github.com/BenjaminFavre/keycloak-apple-social-identity-provider)
* [Keycloak Event Listener Rabbitmq](https://github.com/aznamier/keycloak-event-listener-rabbitmq)


## Installation
***
 
```bash
$ git clone git@github.com:jeniferss/pocauth.git
```

## Running Containers
***

### Kong & Konga
```bash
# Konga admin panel will start at: http://localhost:1337
# Kong admin api will start at: http://localhost:8001
# Kong services api will start at: http://localhost:8000

$ cd kong
$ docker-compose --env-file .env up --build
```

### RabbitMQ
```bash
# Rabbit admin panel will start at: http://localhost:15672

$ cd rabbitmq
$ docker-compose up --build
```
### Keycloak
```bash
# Keycloak admin panel will start at: http://localhost:8180

$ cd keycloak
$ docker-compose --env-file .env up --build
```
### Vault
```bash
# Keycloak admin panel will start at: http://localhost:8200

$ cd vault
$ docker-compose --env-file .env up --build
```

### Grafana & Prometheus
```bash
# Grafana admin panel will start at: http://localhost:3030
# Loki api will start at: http://localhost:3100
# Prometheus api will start at: http://localhost:9090

$ cd monitoring
$ docker-compose --env-file .env up --build
```

### Auth API
```bash
# Auth api will start at: http://localhost:1000

$ cd auth-api
$ docker-compose --env-file .env up --build
```

### ServiceA & ServiceB $ Login Page
```bash
# ServiceA will start at: http://localhost:5000
$ cd serviceA
$ docker-compose up --build

# ServiceB will start at: http://localhost:7000
$ cd serviceB
$ docker-compose --env-file .env up --build

# Login Page will start at: http://localhost:7005
$ cd login
$ docker-compose --env-file .env up --build
```

## Configuration
***
### Konga & Kong 
1. Create connection:
* Register an admin user > Login with admin user credentials > Setup a connection to kong (for 'kong admin url' parameter use: http://kong:8001)

2. Register Services: Go to services page > Add new service 
* Auth-api: Set host and name to authapi and port to 1000 > Submit Service
* ServiceA: Set host and name to servicea and port to 5000 > Submit Service
* ServiceB: Set host and name to serviceb and port to 7000 > Submit Service

3. Register Routes:

* Auth-api (userToken): Click on authapi link > Go to routes > Add Route > Set name field to userToken > Set paths field to /api/v1/token/user > Set strip path to no and preserve host to yes > Submit Route

* Auth-api (serviceToken): Click on authapi link > Go to routes > Add Route > Set name field to serviceToken > Set paths field to /api/v1/token/service > Set strip path to no and preserve host to yes > Submit Route

* ServiceA (articles): Click on servicea link > Go to routes > Add Route > Set name field to articlesA > Set paths field to /api/v1/articles > Set strip path to no and preserve host to yes > Submit Route

* ServiceB (articles): Click on serviceb link > Go to routes > Add Route > Set name field to articlesB > Set paths field to /api/v1/articles > Set strip path to no and preserve host to yes > Submit Route

** Both services were configured to have the same routes to test clients routing (for example, ClientA will call ServiceA routes and ClientB will call ServiceB routes)

### Keycloak Configuration
1. Configure admin panel:
* Click on 'Administration Console' > Login with default credentials (username and password are 'admin') > Add a new Realm 

2. Register clients:
* Kong: Go to clients page > Create > set Client Id to kong and Root URL: http://localhost:8000 > Settings page, set Access Type to 'confidential' and save it > Go to Credentials page and copy the Secret value 

* ServiceB: Go to clients page > Create > set Client Id to serviceb and Root URL: http://localhost:7000 > Settings page, set Access Type to 'confidential', disable 'Standard Flow Enabled', enable 'Service Account Enabled' and save it > Go to Credentials page and copy the Secret value 

* Auth API: Go to clients page > Create > set Client Id to authapi and Root URL: http://localhost:1000  

3. Register users: Go to users page > Add user > Set email verified to on > Go to credentials > Set a new password, with temporary field off

### Vault configuration
1. Create Secrets: Login with root token > Enable new engine > Choose kv type > Set path to pocauth (this will be the mountpoint in the service code) > Create secret > Set path to credentials > Enable JSON > Copy and paste the following JSON object, make sure to change the values for the secrets (kong and serviceb) and save it

```
{
  "kongHost": "http://kong:8000",
  "keycloakHost": "http://keycloak:8080",

  "keycloakRealm": "pocauth",

  "servicebId": "serviceB",
  "kongServiceId": "kong",

  "kongServiceSecret": "",
  "servicebSecret": ""
}

```

### Kong Plugins Configuration 
1. Monitoring Plugin: Go to plugins > Add Global Plugins > Analytics & Monitoring > Prometheus > Add Plugin

2. Authentication Pluging:
* OIDC: Go to plugins > Add Global Plugins > Other > Oidc > Add Plugin > Set the client secret field with the value that was generated to kong on keycloak > Set Bearer Only field to yes > Set Client Id Field to kong > Set Introspection Endpoint field to 'http://keycloak:8080/realms/${REALM}/protocol/openid-connect/token/introspect' > Set Discovery field to 'http://keycloak:8080/auth/realms/${REALM}/.well-known/openid-configuration'

* JWT Keycloak: Go to Services page > the service or route that needs permission > plugins > add plugin > other > JWT Keycloak > Configure the roles for that route > Set allowed iss to 'http://keycloak:8080/realms/${REALM}'

3. Allow Frontend Apps: Go to plugins > Add Global Plugins > Security > Cors > Add the origins for your clients (usually http://localhost:3000) or * to allow all

4. VPN Configuration (Kong Inside VPN): Go to plugins > Add Global Plugins > Security > Ip Restriction > Set the CIDR notation that fits the ip range to allow field

## Testing Endpoints
***
1. Service Token:
```bash
$ curl --location --request POST 'http://localhost:8000/api/v1/token/service' \
--header 'Content-Type: application/json' \
--data-raw '{
    "client_id": "",
    "client_secret": ""
}'
```

2. User Token:
```bash
$ curl --location --request POST 'http://localhost:8000/api/v1/token/user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "",
    "password": ""
}'
```

2. Call articles API (won't work unless made with client app):
```bash
$ curl --location --request GET 'http://localhost:8000/api/v1/articles' \
--header 'Authorization: Bearer eyJhb...'
```

## Same Route for Different Clients
***

1. Create new domain locally (Windows): Go to C:\WINDOWS\system32/drivers/etc/hosts > add the following lines to the file and save it

```
192.168.15.37 server.one
192.168.15.37 server.two
```

2. Set hosts to routes: 
* ServiceA: Go to Routes > articlesA > set hosts to kong and server.one > Submit changes

* ServiceB: Go to Routes > articlesB > set hosts to server.two > Submit changes

* Auth API: Go to Routes > serviceToken and userToken > set hosts to kong, server.one and server.two > Submit changes
