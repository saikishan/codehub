from codingcenter.serializers import UserListSerializer
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserListSerializer(user, context={'request': request}).data
    }