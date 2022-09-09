response=$(curl \
    -H "X-Vault-Token: root" \
    -X GET \
    $VAULT_HOST/v1/$ENV/data/$SERVICE
) 

AUTH_HOST=$(echo $response | jq '.data.data.auth_host' | sed -e 's/"//g')
CLIENT_ID=$(echo $response | jq '.data.data.client_id' | sed -e 's/"//g')
CLIENT_SECRET=$(echo $response | jq '.data.data.client_secret' | sed -e 's/"//g')

resp=$(curl \
    -X POST \
    $AUTH_HOST/auth/v1/service/login \
    -H "Content-Type: application/json" \
    -d "{\"clientId\": \"$CLIENT_ID\", \"clientSecret\": \"$CLIENT_SECRET\"}"
)

token=$(echo $resp | jq '.accessToken' | sed -e 's/"//g')
token_type=$(echo $resp | jq '.tokenType' | sed -e 's/"//g')

export TOKEN=$token
export TOKEN_TYPE=$token_type

uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 5000