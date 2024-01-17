#Decodes Bytes and returns an string
def bytesToString(userString, encoding='utf-8'):
    try:
        if isinstance(userString, bytes):
            return userString.decode(encoding)
        else:
            return userString
    except UnicodeDecodeError as e:
        print(f"Error decoding bytes: {e}")
        return None 