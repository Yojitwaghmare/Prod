from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("Users")


@app.route("/users/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        response = table.scan()
        return jsonify(response.get("Items", [])), 200

    if request.method == "POST":
        data = request.get_json()
        if not data or "userId" not in data or "name" not in data:
            return {"error": "userId and name required"}, 400

        table.put_item(Item=data)
        return {"message": "User created"}, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)