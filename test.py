from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()

file_out = open("private.bin", "wb")
file_out.write(private_key)
file_out.close()

print()
print(key)
print()
print(private_key)
print()
print(private_key.decode('utf8'))
#print(pkcs1_15.can_sign(private_key))
#print(key.publickey().export_key())

#print(RSA.import_key(private_key.encode())

message = 'To be signed'
# key = RSA.import_key(open('private_key.der').read())
try:
    h = SHA256.new()
    h.update(b'To be signed')
    print(h.hexdigest())
except:
    print('Could not create message')
try:
    signing_object = pkcs1_15.new(key)
except:
    print('Could not create signing object')
try:
    signature = signing_object.sign(h)
    print(signature)
except Exception as e:
    print('Could not sign')
    print(e)

print(signature)