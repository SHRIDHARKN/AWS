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

