import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        contents = f.read()
        encoded = base64.b64encode(contents).decode()
    return encoded