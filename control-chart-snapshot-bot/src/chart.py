
import matplotlib
matplotlib.use('Agg')  # headless
import matplotlib.pyplot as plt

def plot_distribution(df, out_png):
    plt.figure()
    df["qa_cycle_days"].plot(kind="hist", bins=20, alpha=0.7)
    plt.title("QA Cycle Time Distribution (days)")
    plt.xlabel("Days")
    plt.ylabel("Count")
    plt.savefig(out_png, bbox_inches="tight")
    plt.close()
