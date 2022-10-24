import json


# Base function
def encode_json(not_json_obj):
    json_obj = json.dumps(not_json_obj, ensure_ascii=False)

    return json_obj


def decode_json(json_obj):
    not_json_obj = json.loads(json_obj)

    return not_json_obj


# Other
def encode_message(text):
    json_obj = {"title": "MESSAGE", "text": text}

    return encode_json(json_obj)


def encode_nickname(nickname):
    json_obj = {"title": "NICK", "text": nickname}

    return encode_json(json_obj)


def encode_system(text):
    json_obj = {"title": "SYSTEM", "text": text}

    return encode_json(json_obj)


def encode_command(text):
    json_obj = {"title": "COMMAND", "text": text}
    return encode_json(json_obj)




