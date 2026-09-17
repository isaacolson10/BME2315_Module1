import matplotlib.pyplot as plt
import statistics
from ashlee_donor import *

csv_filename = "donor_data_set.csv"

#SECTION 1: DATA INGESTION
#Attempts to load files from local directory workplace.
#Exits program safely with an error description if the file loaction is incorrect.


try:
    Donor.instantiate_from_csv(csv_filename)
    print(f"Sucessfully loaded {len(Donor.all_donors)} donor profiles.")
except FileNotFoundError:
    print(f"Error: Missing data target '{csv_filename}'. Check folder placement.")
    exit()

#SECTION 2: SORTING SYSTEM
#Sorts the full list of collected donor objects based on age values.
#Outputs a diagnostic print statement of the top 5 youngest entries to the console.
sorted_by_age = sorted(Donor.all_donors, key=lambda d: d.age_at_death)
print("\n--- Top 5 Youngest Donors (Sorted by Age) ---")
for individual in sorted_by_age[:5]:
    print(individual)

#SECTION 3: CLASS FILTERING CALL
#Triggers our custom class method to filter the data.
#Intended Output: Prints a localized list of matching entries (Female & Dementia).

Donor.filter_and_print("Female", "Dementia")

#SECTION 4: SCATTER PLOT CREATION
#Compiles ages and brain weights into parallel array lists for graphing.
#Intended Output: Prints a localized list of matching entries (Female & Dementia).

donor_ages = [individual.age_at_death for individual in Donor.all_donors]
donor_brain_weights = [individual.brain_weight for individual in Donor.all_donors]

X = donor_ages
Y = donor_brain_weights

plt.figure(figsize = (7,5))
plt.scatter(X, Y, color = 'crimson', alpha = 0.7, edgecolor = 'k')
plt.xlabel("Age at Death (Years)")
plt.ylabel("Fresh Brain Weight (g)")
plt.title("Scatter Plot of Donor Age at Death vs Fresh Brain Weight")
plt.grid(True, linestyle='--', alpha=0.5)
plt.show() #Script will pause here until the scatter plot window is closed.

#SECTION 5: BAR GRAPH WITH STANDARD DEVIATION
#Groups brain weights by biological sex and calculates means and standard deviations.
#Intended Output: Renders a bar graph comparing the two sex averages, fully customized with error caps (+/- standard deviation) to indicate analytical variance bounds.
male_weights = [d.brain_weight for d in Donor.all_donors if d.sex == "Male"]
female_weights = [d.brain_weight for d in Donor.all_donors if d.sex == "Female"]

male_mean = sum(male_weights) / len(male_weights) if male_weights else 0
female_mean = sum(female_weights) / len(female_weights) if female_weights else 0

stdev_male = statistics.stdev(male_weights) if len(male_weights) > 1 else 0
stdev_female = statistics.stdev(female_weights) if len(female_weights) > 1 else 0

categories = ['Male Donors', 'Female Donors']
means = [male_mean, female_mean]
std_errors = [stdev_male, stdev_female]

plt.figure(figsize = (6,5))
plt.bar(categories, means, yerr=std_errors, capsize=8, color=['lightblue', 'lightcoral'])
plt.xlabel("Biological Sex")
plt.ylabel("Average Fresh Brain Weight (g)")
plt.title("Mean Brain Weight (+/- Standard Deviation) by Sex")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
