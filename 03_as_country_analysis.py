import socket
import pandas as pd
from collections import Counter

input_file = "responsive_sample_10000.txt"
output_file = "asn_country_result.csv"

# 为了避免查询太慢，先查前 2000 条即可
MAX_QUERY = 2000

with open(input_file, "r", encoding="utf-8") as f:
    ips = [line.strip() for line in f if line.strip()]

ips = ips[:MAX_QUERY]


def query_team_cymru(ip_list):
    query = "begin\nverbose\n" + "\n".join(ip_list) + "\nend\n"

    s = socket.create_connection(("whois.cymru.com", 43), timeout=60)
    s.sendall(query.encode("utf-8"))

    data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk

    s.close()
    return data.decode("utf-8", errors="ignore")


print(f"开始查询 {len(ips)} 条 IPv6 地址的 ASN 和国家信息...")
result = query_team_cymru(ips)

rows = []
for line in result.splitlines():
    if not line.strip():
        continue
    if line.startswith("AS"):
        continue

    parts = [p.strip() for p in line.split("|")]

    # 格式一般为：AS | IP | BGP Prefix | CC | Registry | Allocated | AS Name
    if len(parts) >= 7:
        rows.append({
            "asn": parts[0],
            "ip": parts[1],
            "bgp_prefix": parts[2],
            "country": parts[3],
            "registry": parts[4],
            "allocated": parts[5],
            "as_name": parts[6]
        })

df = pd.DataFrame(rows)
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"已生成 {output_file}")

print("\nAS Top 10：")
print(df["asn"].value_counts().head(10))

print("\n国家 Top 10：")
print(df["country"].value_counts().head(10))

print("\nBGP Prefix Top 10：")
print(df["bgp_prefix"].value_counts().head(10))