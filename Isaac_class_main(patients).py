from Isaac_class_patient import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics 
import pandas as pd
from sklearn.linear_model import LinearRegression

with open(r"C:\Users\ikedo\OneDrive\Desktop\Computational BME\Module 1\BME2315_Module1\Metadata and Protein Data for Module 1 (1).csv") as f:
        reader = csv.reader(f)
        headers = next(reader) # Get the first row
        for h in headers:
            print(h)
Patient.instantiate_from_csv(r"C:\Users\ikedo\OneDrive\Desktop\Computational BME\Module 1\BME2315_Module1\Metadata and Protein Data for Module 1 (1).csv")

print(Patient.get_patient("Male"))

patients_with_casi = [p for p in Patient.all_patients if p.last_casi_score is not None]
patients_with_casi.sort(key=Patient.get_last_casi_score, reverse=False)

male_patients = range(len(Patient.filter(Patient.all_patients, sex = "Male")))

print(f'Number of Male Patients = {len(male_patients)}')

female_patients = range(len(Patient.filter(Patient.all_patients, sex = "Female")))

print(f'Number of Female Patients = {len(female_patients)}')

male_scores = []
female_scores = []
for patients in Patient.filter(Patient.all_patients, sex = "Male"):
    if patients.last_casi_score is not None:
        male_scores.append(patients.last_casi_score)

for patients in Patient.filter(Patient.all_patients, sex = "Female"):
    if patients.last_casi_score is not None:
        female_scores.append(patients.last_casi_score)
x_male_bar = (statistics.mean(male_scores))
x_female_bar = (statistics.mean(female_scores))

male_scores_stdev = (statistics.stdev(male_scores))
female_scores_stdev = (statistics.stdev(female_scores))

print(f'x_male_bar = {x_male_bar}, male_scores_stdev {male_scores_stdev}')
print(f'x_female_bar = {x_female_bar}, female_scores_stdev {female_scores_stdev}')

sex_cols = ['male', 'female']
mean_casi_by_sex = [x_male_bar, x_female_bar]
stdev_casi_by_sex = [male_scores_stdev, female_scores_stdev]
yerr = [np.zeros(len(mean_casi_by_sex)), stdev_casi_by_sex]

f_stat, p_value = stats.f_oneway(male_scores, female_scores)

print("F-statistic:", f_stat)
print("P-value:", p_value)
plt.text(1.5, 380, f"One-Way-ANOVA: p = {p_value:.3f}", ha='right', va='top', fontsize=12)

t_stat, p_val = stats.ttest_ind(male_scores, female_scores)
print(f't_stat: {t_stat}, p_val: {p_val}')
plt.bar(sex_cols, mean_casi_by_sex, yerr=yerr, capsize=10, color=["blue", "orange"])
plt.title("Average CASI Score by Sex")
plt.xlabel("Sex")
plt.ylabel("Average CASI Score")
y_max = max(mean_casi_by_sex) + max(stdev_casi_by_sex) * .4
plt.text(
     0.5, y_max,
     f"t = {t_stat:.2f}\np= {p_val:.3e}",
     ha = 'center',
     va = 'bottom'
)
plt.show()

age_list = []
casi_list = []

for patient in Patient.all_patients:
    if patient.age_at_diagnosis is not None and patient.last_casi_score is not None:
        age_list.append(patient.age_at_diagnosis)
        casi_list.append(patient.last_casi_score)

X = [age_list]  # Independent variable
y = [casi_list] # Dependent variable

X = np.array(age_list).reshape(-1, 1)  # Reshape for sklearn
y = np.array(casi_list)  # Reshape for sklearn
model = LinearRegression()
model.fit(X, y)

slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)

equation = f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r2:.2f}"
plt.text(X.max(), y.max(), equation, color='red', fontsize=12, verticalalignment='top')

plt.scatter(X, y, color='blue')
plt.plot(X, model.predict(X), color='red')
plt.xlabel('Age at Diagnosis')
plt.ylabel('Average CASI Score')
plt.title('Scatter Plot of Age at Diagnosis vs Average CASI Score')
plt.show()
