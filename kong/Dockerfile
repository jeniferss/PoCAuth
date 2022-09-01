FROM kong

USER root

RUN apk update && apk add git unzip luarocks 
RUN luarocks install kong-oidc
RUN luarocks install lua-resty-jwt

RUN git clone --branch feature/client-token https://github.com/jeniferss/kong-oidc.git && \
    cd kong-oidc && luarocks make
    
RUN git clone --branch 20200505-access-token-processing https://github.com/BGaunitz/kong-plugin-jwt-keycloak.git && \
    cd kong-plugin-jwt-keycloak && luarocks make