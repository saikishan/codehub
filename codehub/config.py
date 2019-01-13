config_data = {
    "email_sender" : "codehub.sender@gmail.com",
    "email_sender_password" : "pythoncjs",
    "default" : None,
}
def get_config(key="default"):
    return config_data.get(key,None)