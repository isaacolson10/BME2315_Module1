#import necessary libraries
import matplotlib
matplotlib.use('TkAgg')
from module_1_patient import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
from sklearn.linear_model import LinearRegression

Patient.instantiate_from_csv(r"C:\Users\ikedo\OneDrive\Desktop\Computational BME\Module 1\BME2315_Module1\Metadata and Protein Data for Module 1 (1).csv") #grabs the CSV file and creates Patient objects for each row in the file

def bar_by_status(attr, label): #defines a function that creates a bar graph comparing the mean protein levels (mean ± SD) for patients with "No dementia" vs "Dementia", with individual donors overlaid. The function also performs Welch's t-test and Mann-Whitney U test to analyze the differences between the two groups.
    """Bar graph of mean protein level (mean +/- SD) for No dementia vs Dementia,
    with individual donors overlaid, analyzed with Welch's t-test and Mann-Whitney U."""
    groups = ["No dementia", "Dementia"]

    values = [] 
    for status in groups: 
        values.append([getattr(p, attr) for p in Patient.filter(Patient.all_patients, cognitive_status=status) #creates a list of protein levels for patients with the specified cognitive status, filtering out any patients with missing values for the specified attribute
                       if getattr(p, attr) is not None])

    means = [statistics.mean(v) for v in values] #calculates the mean protein level for each group
    stdevs = [statistics.stdev(v) for v in values] #calculates the standard deviation of protein levels for each group

    t_stat, p_val = stats.ttest_ind(values[0], values[1], equal_var=False) #Welch's t-test
    u_stat, u_p = stats.mannwhitneyu(values[0], values[1]) #Mann-Whitney U test
    print(f'{label}: n = {len(values[0])} (No dementia), {len(values[1])} (Dementia)') #prints the number of patients in each group
    print(f'{label}: means = {means[0]:.3f}, {means[1]:.3f} | Welch t = {t_stat:.3f}, p = {p_val:.3e} | Mann-Whitney p = {u_p:.3e}') #prints the means of each group, Welch's t-test statistic and p-value, and Mann-Whitney U test p-value

    x_labels = [f"{groups[i]}\n(n={len(values[i])})" for i in range(2)]
    plt.bar(x_labels, means, yerr=stdevs, capsize=10, color=["blue", "orange"], alpha=0.6)

    for i in range(2): #iterates through each group and adds individual data points to the bar graph with a small random jitter to avoid overlap
        jitter = np.random.uniform(-0.15, 0.15, len(values[i]))
        plt.scatter(i + jitter, values[i], color="black", s=10, zorder=3)
    
    top = max(max(v) for v in values)
    plt.ylim(0, top * 1.25) #sets the y-axis limit to 1.25 times the maximum protein level across both groups to ensure that all data points and error bars are visible
    plt.text(0.5, top * 1.05, f"Welch t = {t_stat:.2f}\np = {p_val:.3e}", ha='center', va='bottom') #adds a text box to the bar graph displaying the Welch's t-test statistic and p-value
    plt.title(f"Average {label} by Cognitive Status (mean ± SD)") #adds a title to the bar graph indicating that it shows the average protein levels by cognitive status, along with the mean and standard deviation
    plt.xlabel("Cognitive Status") #adds a label to the x-axis indicating that it represents cognitive status
    plt.ylabel(f"{label} (pg/ug)") #adds a label to the y-axis indicating that it represents protein levels in pg/ug
    plt.show() #displays the bar graph

def scatter_vs_mmse(attr, label): #defines a function that creates a scatter plot of protein level vs MMSE score with a linear regression line, equation, R-squared and p-value. The function also prints the slope, R-squared and p-value of the linear regression.
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
    # Create scatter plot with regression line
    plt.scatter(X, y, color='blue')
    plt.plot(X, model.predict(X), color='red')
    plt.xlabel('MMSE Score')
    plt.ylabel(f'{label} (pg/ug)')
    plt.title(f'Scatter Plot of {label} vs MMSE Score')
    plt.show()

bar_by_status("abeta42", "ABeta42") #creates a bar graph comparing the mean ABeta42 protein levels (mean ± SD) for patients with "No dementia" vs "Dementia", with individual donors overlaid. The function also performs Welch's t-test and Mann-Whitney U test to analyze the differences between the two groups.
scatter_vs_mmse("abeta42", "ABeta42") #creates a scatter plot of ABeta42 protein level vs MMSE score with a linear regression line, equation, R-squared and p-value. The function also prints the slope, R-squared and p-value of the linear regression.
bar_by_status("ptau", "pTAU") #creates a bar graph comparing the mean pTAU protein levels (mean ± SD) for patients with "No dementia" vs "Dementia", with individual donors overlaid. The function also performs Welch's t-test and Mann-Whitney U test to analyze the differences between the two groups.
scatter_vs_mmse("ptau", "pTAU") #creates a scatter plot of pTAU protein level vs MMSE score with a linear regression line, equation, R-squared and p-value. The function also prints the slope, R-squared and p-value of the linear regression.
