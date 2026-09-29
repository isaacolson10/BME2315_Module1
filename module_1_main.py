import matplotlib
matplotlib.use('TkAgg')
from module_1_patient import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
from sklearn.linear_model import LinearRegression

Patient.instantiate_from_csv(r"C:\Users\ikedo\OneDrive\Desktop\Computational BME\Module 1\BME2315_Module1\Metadata and Protein Data for Module 1 (1).csv")

def bar_by_status(attr, label):
    """Bar graph of mean protein level (mean +/- SD) for No dementia vs Dementia,
    with individual donors overlaid, analyzed with Welch's t-test and Mann-Whitney U."""
    groups = ["No dementia", "Dementia"]

    values = []
    for status in groups:
        values.append([getattr(p, attr) for p in Patient.filter(Patient.all_patients, cognitive_status=status)
                       if getattr(p, attr) is not None])

    means = [statistics.mean(v) for v in values]
    stdevs = [statistics.stdev(v) for v in values]

    t_stat, p_val = stats.ttest_ind(values[0], values[1], equal_var=False)
    u_stat, u_p = stats.mannwhitneyu(values[0], values[1])
    print(f'{label}: n = {len(values[0])} (No dementia), {len(values[1])} (Dementia)')
    print(f'{label}: means = {means[0]:.3f}, {means[1]:.3f} | Welch t = {t_stat:.3f}, p = {p_val:.3e} | Mann-Whitney p = {u_p:.3e}')

    x_labels = [f"{groups[i]}\n(n={len(values[i])})" for i in range(2)]
    plt.bar(x_labels, means, yerr=stdevs, capsize=10, color=["blue", "orange"], alpha=0.6)

    for i in range(2):
        jitter = np.random.uniform(-0.15, 0.15, len(values[i]))
        plt.scatter(i + jitter, values[i], color="black", s=10, zorder=3)

    top = max(max(v) for v in values)
    plt.ylim(0, top * 1.25)
    plt.text(0.5, top * 1.05, f"Welch t = {t_stat:.2f}\np = {p_val:.3e}", ha='center', va='bottom')
    plt.title(f"Average {label} by Cognitive Status (mean ± SD)")
    plt.xlabel("Cognitive Status")
    plt.ylabel(f"{label} (pg/ug)")
    plt.show()

def scatter_vs_mmse(attr, label):
    """Scatter plot of protein level vs MMSE score with a linear regression line,
    equation, R-squared and p-value."""
    mmse_list = []
    level_list = []
    for patient in Patient.all_patients:
        if patient.mmse is not None and getattr(patient, attr) is not None:
            mmse_list.append(patient.mmse)
            level_list.append(getattr(patient, attr))

    X = np.array(mmse_list).reshape(-1, 1)  # Reshape for sklearn
    y = np.array(level_list)
    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]
    intercept = model.intercept_
    r2 = model.score(X, y)

    p_value = stats.linregress(mmse_list, level_list).pvalue
    print(f'{label} vs MMSE: n = {len(mmse_list)}, slope = {slope:.3f}, R² = {r2:.3f}, p = {p_value:.3e}')

    equation = f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r2:.2f}, p = {p_value:.3f}\nn = {len(mmse_list)}"
    plt.text(0.05, 0.95, equation, color='red', fontsize=12, va='top', transform=plt.gca().transAxes)

    plt.scatter(X, y, color='blue')
    plt.plot(X, model.predict(X), color='red')
    plt.xlabel('MMSE Score')
    plt.ylabel(f'{label} (pg/ug)')
    plt.title(f'Scatter Plot of {label} vs MMSE Score')
    plt.show()

bar_by_status("abeta42", "ABeta42")
scatter_vs_mmse("abeta42", "ABeta42")
bar_by_status("ptau", "pTAU")
scatter_vs_mmse("ptau", "pTAU")
