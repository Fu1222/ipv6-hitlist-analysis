import ipaddress
import pandas as pd
from collections import Counter

input_file = "responsive_sample_10000.txt"

prefix32_counter = Counter()
prefix48_counter = Counter()
prefix64_counter = Counter()

addresses = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        ip_str = line.strip()
        if not ip_str:
            continue

        try:
            ip = ipaddress.IPv6Address(ip_str)
        except ValueError:
            continue

        addresses.append(ip_str)

        p32 = ipaddress.IPv6Network((ip, 32), strict=False)
        p48 = ipaddress.IPv6Network((ip, 48), strict=False)
        p64 = ipaddress.IPv6Network((ip, 64), strict=False)

        prefix32_counter[str(p32)] += 1
        prefix48_counter[str(p48)] += 1
        prefix64_counter[str(p64)] += 1


def save_counter(counter, filename, topn=30):
    df = pd.DataFrame(counter.most_common(topn), columns=["prefix", "count"])
    df["percentage"] = df["count"] / len(addresses) * 100
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"已生成 {filename}")


save_counter(prefix32_counter, "top_prefix32.csv")
save_counter(prefix48_counter, "top_prefix48.csv")
save_counter(prefix64_counter, "top_prefix64.csv")

print("样本总数：", len(addresses))
print("不同 /32 前缀数量：", len(prefix32_counter))
print("不同 /48 前缀数量：", len(prefix48_counter))
print("不同 /64 前缀数量：", len(prefix64_counter))