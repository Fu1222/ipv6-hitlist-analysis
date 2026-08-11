from collections import Counter
import pandas as pd

input_file = "addr6_decode.txt"
output_file = "iid_type_count.csv"

counter = Counter()
total = 0

with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split("=")

        # addr6 输出格式一般为：
        # AddressType=AddressSubtype=Scope=IIDType=IIDSubtype
        if len(parts) >= 4:
            iid_type = parts[3].strip()
        else:
            iid_type = "unknown"

        counter[iid_type] += 1
        total += 1

df = pd.DataFrame(counter.most_common(), columns=["iid_type", "count"])
df["percentage"] = df["count"] / total * 100
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(df)
print(f"已生成 {output_file}")