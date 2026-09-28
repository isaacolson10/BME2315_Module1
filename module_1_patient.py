import csv
class Patient:
    all_patients = []

    def __init__(self, cognitive_status: str, abeta42: float, ptau: float, mmse: float):
        self.cognitive_status = cognitive_status
        self.abeta42 = abeta42
        self.ptau = ptau
        self.mmse = mmse
        Patient.all_patients.append(self)
    def __repr__(self):
        return f"({self.cognitive_status} | ABeta42 = {self.abeta42} | pTAU = {self.ptau} | MMSE = {self.mmse})"
        
    @classmethod
    def instantiate_from_csv(cls, filename: str):
        
        with open(filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)

            for row in rows_of_patients:
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