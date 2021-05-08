import yaml
import random

def twenty_percent_chance():
    nonce = random.randint(1, 5)
    return nonce == 1

invalid_dns_config = {'dnsPolicy': 'None', 'dnsConfig': {'nameservers': ['192.168.1.213']}}


with open('quickstart-ts-deployment-part2.yml') as file:
    docs = yaml.load_all(file, Loader=yaml.FullLoader)
    scrambled_docs = []
    for doc in docs:
        print(doc)
        if doc['kind'] == 'Deployment' and twenty_percent_chance():
            doc["spec"]["template"]["spec"].update(invalid_dns_config)

        scrambled_docs.append(doc)

    with open("scrambled-yaml.yaml", "w") as outfile:
        yaml.dump_all(scrambled_docs, outfile, default_flow_style=False)

