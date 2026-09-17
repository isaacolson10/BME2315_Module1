import csv #import the built-in csv module

class Donor: 
    #Tracking list for all created donor objects
    all_donors = []

    def __init__(self, donor_id: str, age_at_death: float, sex: str, brain_weight: float, cognitive_status: str): #CONSTRUCTOR METHOD: initializes instance variable for each donor profile and automatically appends the new object instance to the class-wide tracking list.
        self.donor_id = donor_id
        self.age_at_death = age_at_death
        self.sex = sex
        self.brain_weight = brain_weight
        self.cognitive_status = cognitive_status

        Donor.all_donors.append(self)

    def __repr__(self):
        return f"Donor {self.donor_id}: ({self.sex} | Age: {self.age_at_death} | Brain Weight: {self.brain_weight}g | {self.cognitive_status}))" #REPRESENTER METHOD: defines the visual text format when printing a donor oobject to the console.
    @classmethod
    def filter_and_print(cls, target_sex: str, target_cognitive_status: str): #FILTERING CLASS METHOD: filters and prints a subset of objects based on TWO specific atributes (Sex and Cognitive Status). Returns the filtered list of matches.
        print(f"\n--- Filtered Results Summary ({target_sex} & {target_cognitive_status}) ---")
        filtered_subset = []
        for individual in cls.all_donors:
            if individual.sex == target_sex and individual.cognitive_status == target_cognitive_status:
                filtered_subset.append(individual)
                print(individual)
        return filtered_subset
    
    @classmethod
    def instantiate_from_csv(cls, filename: str): #CSV IMPORT METHOD: opens the specified data file, reads rows as dictionaries, screens out missing or "Unavailable' data values, and dynamically creates Donor objects."
        with open(filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_of_donors = list(reader)   

            for row in rows_of_donors: 
                weight_raw = row.get('Fresh Brain Weight', '0')
                if weight_raw == 'Unavailable' or not weight_raw:
                    continue #Safely skip incimplete entries to prevent graph calculation crashes.

                cls(
                    donor_id = row['Donor ID'],
                    age_at_death = float(row['Age at Death']),
                    sex = row['Sex'],
                    brain_weight = float(weight_raw),
                    cognitive_status = row['Cognitive Status']
                )