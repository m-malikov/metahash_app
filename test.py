import subprocess
import requests


print("Retrieving torrent node IP...")
torrent_nodes_info = subprocess.check_output(['drill', 'tor.net-dev.metahashnetwork.com']).decode('utf-8').split('\n')
torrent_node_ip = None

for i in range(len(torrent_nodes_info) - 1):
    if 'ANSWER SECTION' in torrent_nodes_info[i]:
        torrent_node_ip = torrent_nodes_info[i+1].split('\t')[-1]

print("Generating address for the smart home...")
subprocess.call("openssl ecparam -genkey -name secp256k1 -out test.pem".split())
p1 = subprocess.Popen("openssl ec -in test.pem -pubout -outform DER".split(), stdout=subprocess.PIPE)
p2 = subprocess.Popen("tail -c 65".split(), stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen("xxd -p -c 65".split(), stdin=p2.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
pub_key = p3.communicate()[0]
print("Pubkey:\n{}".format(pub_key.decode('utf-8')))

p1 = subprocess.Popen("xxd -r -p".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p2 = subprocess.Popen("openssl dgst -sha256".split(), stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdin.write(pub_key)
p1.stdin.close()
p1.stdout.close()
sha256_hash = p2.communicate()[0].decode('utf-8').split()[-1]
print("1st sha256 hash:\n{}".format(sha256_hash))

p1 = subprocess.Popen("xxd -r -p".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p2 = subprocess.Popen("openssl dgst -rmd160".split(), stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdin.write(sha256_hash.encode("utf-8"))
p1.stdin.close()
p1.stdout.close()
rmd160_hash = "00" + p2.communicate()[0].decode('utf-8').split()[-1]
print("rmd160 hash:\n{}".format(rmd160_hash))


p1 = subprocess.Popen("xxd -r -p".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p2 = subprocess.Popen("openssl dgst -sha256".split(), stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdin.write(rmd160_hash.encode("utf-8"))
p1.stdin.close()
p1.stdout.close()
second_sha256_hash = p2.communicate()[0].decode('utf-8').split()[-1]
print("2nd sha256 hash:\n{}".format(second_sha256_hash))

p1 = subprocess.Popen("xxd -r -p".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p2 = subprocess.Popen("openssl dgst -sha256".split(), stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdin.write(second_sha256_hash.encode("utf-8"))
p1.stdin.close()
p1.stdout.close()
third_sha256_hash = p2.communicate()[0].decode('utf-8').split()[-1]
print("3rd sha256 hash:\n{}".format(third_sha256_hash))

address = "0x"+ rmd160_hash + third_sha256_hash[:8]
print("\nAddress:\n{}".format(address))
    
data = {
    "jsonrpc": "2.0",
    "method": "mhc_send",
    "params": {
        "to": "PLACEHOLDER",
        "value": "1000000",
        "fee": "",
        "nonce": "1",
        "data": "AAAAAA",
        "pubkey": "PUBKEY",
        "sign": "PLACEHOLDER"
    }
}

print("Sending request...")
r = requests.post("http://{}:5795".format(torrent_node_ip), data=data)
print(r.text)
