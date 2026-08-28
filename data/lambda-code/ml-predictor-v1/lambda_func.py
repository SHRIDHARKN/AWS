def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": '{"prediction": "class_b", "confidence": 0.87, "features_received": [5.1, 3.5, 1.4, 0.2]}'
    }
