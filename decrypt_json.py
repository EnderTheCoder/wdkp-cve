import json

from secret import secret_util

json_str = json.loads(input('ciphertext: '))
for k, v in dict(json_str).items():
    print(secret_util.decrypt(v))
