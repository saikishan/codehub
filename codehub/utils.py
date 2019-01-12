from codingcenter.serializers import UserListSerializer

def jwt_payload_handler(user):
    return UserListSerializer(user).data