def updated_username(user) -> str:
    return user.name if user.discriminator == "0" else user
