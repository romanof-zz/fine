# build s3 bucket
APP_BUILDS = "fine.builds"
# lambda pkg file name. product of bin/lambda.sh
APP_PKG_NAME = "lambda.zip"
# name of all prod lambda functions
APP_LAMBDA_NAMES = [
    # dev ops
    "deployment",

    # sync apis
    "get_bets",

    # async jobs
    "update_twitter",
    "update_options",
    "update_5m_tickers",
    "update_1d_tickers",
    "update_1h_tickers",
    "update_1m_tickers"
]

# lambda file deployment post handler.
def lambda_finalize_deployment(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    if bucket == APP_BUILDS and key == APP_PKG_NAME:
        print(f"triggeed deplyment for {bucket}:{key}")
        client = boto3.client('lambda')
        for fname in APP_LAMBDA_NAMES:
            client.update_function_code(FunctionName=fname, S3Bucket=bucket, S3Key=key)
            print(f"finished deplyment for {fname}")

    print("finished all deplyments.")
    return {'resultCode': 200}
