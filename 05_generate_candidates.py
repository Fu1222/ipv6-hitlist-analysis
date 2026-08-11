import ipaddress
from collections import Counter

input_file = "responsive_sample_10000.txt"
output_file = "generated_candidates.txt"

# 每个 /64 前缀下生成 ::1 到 ::255
MAX_IID = 255

prefix64_counter = Counter()
known_addresses = set()

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        ip_str = line.strip()
        if not ip_str:
            continue

        try:
            ip = ipaddress.IPv6Address(ip_str)
        except ValueError:
            continue

        known_addresses.add(str(ip))
        prefix64 = ipaddress.IPv6Network((ip, 64), strict=False)
        prefix64_counter[prefix64] += 1

# 选择出现次数最多的前 20 个 /64 前缀
top_prefixes = [p for p, c in prefix64_counter.most_common(20)]

generated = set()

for prefix in top_prefixes:
    base_int = int(prefix.network_address)

    for iid in range(1, MAX_IID + 1):
        candidate = ipaddress.IPv6Address(base_int + iid)
        generated.add(str(candidate))

with open(output_file, "w", encoding="utf-8") as f:
    for ip in sorted(generated):
        f.write(ip + "\n")

hit_count = len(generated & known_addresses)

print("选取的 /64 前缀数量：", len(top_prefixes))
print("生成候选地址数量：", len(generated))
print("候选地址与样本中已知 responsive 地址重合数量：", hit_count)
print("结果已保存到 generated_candidates.txt")