a = [["A1", "A2", "A3"], ["B1", "B2", "B3"]]

# 90°回転
b = list(zip(*a[::-1]))

# -90°回転
c = list(zip(*[r[::-1] for r in a]))

print("元のリスト:", a)
print("90°回転:", b)
print("-90°回転:", c)
