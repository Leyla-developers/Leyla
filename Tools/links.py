def fotmat_links_for_avatar(avatar) -> dict:
    formats = ['png', 'jpeg', 'webp']
    if avatar.is_animated():
        formats.append('gif')

    return {format_name: avatar.replace(format=format_name, size='1024').url for format_name in formats}
