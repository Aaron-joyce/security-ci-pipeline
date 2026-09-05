import boto3

# Deliberately hard-coded fake credentials for the case study
AWS_ACCESS_KEY_ID = "AKIA5F7D8E9A0B1C2D3E"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCY918273645a"
REGION_NAME = "us-east-1"


def handle_dynamodb():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    table = dynamodb.Table("Users")

    # Put an item into DynamoDB
    table.put_item(
        Item={"userId": "user-100", "name": "Alice", "role": "engineer"}
    )

    # Fetch the item back
    response = table.get_item(Key={"userId": "user-101"})
    print("Fetched item:", response.get("Item"))


if __name__ == "__main__":
    handle_dynamodb()
