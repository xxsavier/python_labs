import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/lab07/bench_for_plot.csv")
df = df[df["Task"] == "sort"]

for method in df["Method"].unique():
    if 'binary' in method: continue
    df_work = df[(df["Method"] == method) & (df["Length"] < 15001)]
    plt.plot(df_work["Length"], df_work["Time"], label=method.strip(), marker="o")
    
plt.yscale("log")
plt.xlabel("Количество элементов в списке")
plt.ylabel("Время выполнения (секунды)")
plt.title("Сравнение алгоритмов сортировки")
plt.legend()
plt.grid(True, which="major")
plt.show()
