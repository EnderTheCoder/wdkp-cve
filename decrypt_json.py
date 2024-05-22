import base64
import json

from secret import secret_util

json_str = json.loads(input('ciphertext: '))
for k, v in dict(json_str).items():
    r = secret_util.decrypt(v)
    if k == 'UserTxContent':
        print(base64.b64decode(r.replace('\n', '').replace('"', '')))
    print(r)
