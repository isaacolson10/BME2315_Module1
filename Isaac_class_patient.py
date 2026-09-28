import csv
class Patient:
    all_patients = [] 
    def __init__(self, sex: str, age_at_diagnosis: float, highest_education: str, known_head_injury: str, cognitive_status: str, last_casi_score: float): 
        self.sex = sex
        self.age_at_diagnosis = age_at_diagnosis
        self.highest_education = highest_education
        self.known_head_injury = known_head_injury
        self.cognitive_status = cognitive_status
        self.last_casi_score = last_casi_score
        Patient.all_patients.append(self)
    def __repr__(self):  
        return f"{self.sex}: ({self.age_at_diagnosis} | {self.highest_education} | {self.known_head_injury} | {self.cognitive_status} | {self.last_casi_score})" 
    @classmethod
    def get_last_casi_score(cls, patient):
        return patient.last_casi_score
    
    @classmethod 
    def instantiate_from_csv(cls, filename: str):
        
        with open(filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)
        
            for row in rows_of_patients:
                if row['Age of Dementia diagnosis'] != '':
                    age_at_diagnosis = float(row['Age of Dementia diagnosis'])
                else:
                    age_at_diagnosis = None
                if row['Last CASI Score'] != '':
                    last_casi_score = float(row['Last CASI Score'])
                else:
                    last_casi_score = None

                cls(
                    sex=row['Sex'],
                    age_at_diagnosis=age_at_diagnosis,
                    highest_education=row['Highest level of education'],
                    known_head_injury=row['Known head injury'],
                    cognitive_status=row['Cognitive Status'],
                    last_casi_score=last_casi_score
                )

    @classmethod
    def get_patient(cls, sex):
        for patient in Patient.all_patients:
            if sex == patient.sex:
                return patient

    @classmethod
    def filter(cls, list, sex:str ="any", age_at_diagnosis:int ="any", highest_education:str ="any", known_head_injury:str ="any", cognitive_status:str ="any", last_casi_score:int ="any"):
            all_patients = list
            remove_list = []
            attr_list = (
                        sex,
                        age_at_diagnosis,
                        highest_education,
                        known_head_injury,
                        cognitive_status,
                        last_casi_score
                        )
            attr_name = (
                        "sex",
                        "age_at_diagnosis",
                        "highest_education",
                        "known_head_injury",
                        "cognitive_status",
                        "last_casi_score"
                        )
            for attr in range(len(attr_list)):
                if attr_list[attr] != "any":
                    for patient in all_patients:
                        if getattr(patient,attr_name[attr]) != attr_list[attr]:
                            remove_list.append(patient)
                    all_patients = [patient for patient in all_patients if patient not in remove_list]
                    remove_list.clear()

            return all_patients