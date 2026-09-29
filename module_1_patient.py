import csv #import csv module to read CSV files
class Patient: #class to represent a patient with cognitive status, protein levels, and MMSE score
    all_patients = [] 

    def __init__(self, cognitive_status: str, abeta42: float, ptau: float, mmse: float): #defines the constructor for the Patient class, which takes in cognitive status, abeta42 level, ptau level, and MMSE score as arguments
        self.cognitive_status = cognitive_status
        self.abeta42 = abeta42
        self.ptau = ptau
        self.mmse = mmse
        Patient.all_patients.append(self)
    def __repr__(self): #defines the string representation of the Patient object, which returns a string with the cognitive status, abeta42 level, ptau level, and MMSE score of the patient
        return f"({self.cognitive_status} | ABeta42 = {self.abeta42} | pTAU = {self.ptau} | MMSE = {self.mmse})"
        
    @classmethod
    def instantiate_from_csv(cls, filename: str): #class method that reads patient data from a CSV file and creates Patient objects for each row in the file
        
        with open(filename, encoding="utf8") as f: #opens the CSV file with UTF-8 encoding
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)

            for row in rows_of_patients: #iterates through each row in the CSV file and extracts the cognitive status, abeta42 level, ptau level, and MMSE score for each patient. If any of these values are missing, they are set to None. A new Patient object is then created for each row using the extracted values.
                if row['ABeta42 pg/ug'] != '':
                    abeta42 = float(row['ABeta42 pg/ug'])
                else:
                    abeta42 = None
                if row['pTAU pg/ug'] != '':
                    ptau = float(row['pTAU pg/ug'])
                else:
                    ptau = None
                if row['Last MMSE Score'] != '':
                    mmse = float(row['Last MMSE Score'])
                else:
                    mmse = None

                cls(
                    cognitive_status=row['Cognitive Status'],
                    abeta42=abeta42,
                    ptau=ptau,
                    mmse=mmse
                )
    @classmethod
    def filter(cls, patient_list, cognitive_status: str = "any"): #class method that filters a list of Patient objects based on their cognitive status. If the cognitive status is set to "any", all patients are returned. Otherwise, only patients with the specified cognitive status are returned.
        remaining_patients = patient_list
        if cognitive_status != "any":
            remaining_patients = [patient for patient in remaining_patients
                                  if patient.cognitive_status == cognitive_status]
        return remaining_patients