import lzma

input_file = "responsive-addresses.txt.xz"
output_file = "responsive_sample_10000.txt"
sample_size = 10000

count = 0

with lzma.open(input_file, "rt", encoding="utf-8", errors="ignore") as f, \
     open(output_file, "w", encoding="utf-8") as out:
    for line in f:
        ip = line.strip()
        if not ip or ip.startswith("#"):
            continue

        out.write(ip + "\n")
        count += 1

        if count >= sample_size:
            break

print(f"已抽取 {count} 条 IPv6 地址，保存到 {output_file}")