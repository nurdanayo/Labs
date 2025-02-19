import json


file_path = "data.json"
with open(file_path, "r") as file:
    data = json.load(file)


print("Interface Status")
print("=" * 80)
print(f"Total Count: {data.get('totalCount', 'Unknown')}")
print("{:<45} {:<15} {:<10} {:<10}".format("DN", "Description", "Speed", "MTU"))
print("-" * 80)


for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes.get("dn", "N/A")
    description = attributes.get("descr", "inherit") if attributes.get("descr") else "inherit"
    speed = attributes.get("speed", "N/A")
    mtu = attributes.get("mtu", "N/A")
    
    print("{:<45} {:<15} {:<10} {:<10}".format(dn, description, speed, mtu))
