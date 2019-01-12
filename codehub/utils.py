from codingcenter.serializers import UserDetailSerializer

def jwt_payload_handler(user):
    return UserDetailSerializer(user).data

def jwt_payload_get_username(payload):
    return payload["email"]