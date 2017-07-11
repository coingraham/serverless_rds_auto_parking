from rdsautoparking import RdsAutoParking


def handler(event, context):

    # These should match the settings in your serverless.yml
    region = "us-east-1"
    dynamodb_table = "rds_autoparking_config"

    rds = RdsAutoParking(dynamodb_table, region)

    rds.main()

# Main for local testing
if __name__ == '__main__':

    # These should match the settings in your serverless.yml
    region = "us-east-1"
    dynamodb_table = "rds_autoparking_config"

    rds = RdsAutoParking(dynamodb_table, region)

    rds.main()
