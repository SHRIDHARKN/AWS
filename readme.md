# Start Floci
floci start --persist ./data

# Create Lambda Function

## 01 Predictor

```
mkdir -p 01_aws_lambda/predictor
cd 01_aws_lambda/predictor/
```
```
cat > lambda_func.py <<'EOF'
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": '{"prediction": "class_b", "confidence": 0.87, "features_received": [5.1, 3.5, 1.4, 0.2]}'
    }
EOF
```
```
 zip function.zip lambda_func.py
```

```
aws lambda list-functions

aws lambda create-function \
  --function-name ml-predictor-v1 \
  --runtime python3.12 \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --handler lambda_func.lambda_handler \
  --zip-file fileb://function.zip
```

```
aws lambda invoke \
  --function-name ml-predictor-v1 \
  --payload '{"hello":"from-direct-lambda"}' \
  response.json

cat response.json
```

# Create REST API
aws apigateway create-rest-api \
  --name ml-predictor-api

# Delete REST API
aws apigateway delete-rest-api \
  --rest-api-id 3d4a2018ce


## Create REST API
`aws apigateway create-rest-api   --name ml-predictor-api-v1`
## List resources
`aws apigateway get-resources   --rest-api-id f9ece88a12`
## Create resource
`aws apigateway create-resource   --rest-api-id f9ece88a12   --parent-id d09a228b   --path-part predict`
## Create POST method
`aws apigateway put-method   --rest-api-id f9ece88a12   --resource-id abbde82d   --http-method POST   --authorization-type NONE`
## Integration
`
aws apigateway put-integration   --rest-api-id f9ece88a12   --resource-id abbde82d   --http-method POST   --type AWS_PROXY   --integration-http-method POST   --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:ml-predictor-v1/invocations
`
## Create deployment
`
aws apigateway create-deployment   --rest-api-id f9ece88a12
`
## Create staging
`
aws apigateway create-stage   --rest-api-id f9ece88a12   --stage-name dev   --deployment-id eda5a1e63a
`
## Use curl
`
curl -i -X POST   http://localhost:4566/restapis/f9ece88a12/dev/_user_request_/predict   -H "Content-Type: application/json"   -d '{"features":[5.1,3.5,1.4,0.2]}'
`