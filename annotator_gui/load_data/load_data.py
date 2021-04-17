# %run load_data/load_data.py

# import libraries
import csv, os
import numpy as np
import pandas as pd
import django.shortcuts
from gui.models import PatientDemographic, PatientYear, Note

# define directories, note that CSV files must be contained within data folder in the same directory as load_data.py
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print("Root Directory: " + ROOT_DIR)
path = os.path.join(ROOT_DIR, 'data')
print("Data Directory: " + path)


########################################
##### PATIENT DEMOGRAPHICS IMPORT
########################################

tmp_patient_demo = pd.read_csv(os.path.join(path,'patient_demographics.csv'), sep = ',', encoding = 'utf8')
tmp_patient_demo = tmp_patient_demo.replace({np.nan: None})

patient_demo = [
    PatientDemographic(
        PatientID = tmp_patient_demo.iloc[row]['PatientID'],
        MRN = tmp_patient_demo.iloc[row]['MRN'],
        BirthDTS = tmp_patient_demo.iloc[row]['BirthDTS'],
        EthnicGroupDSC = tmp_patient_demo.iloc[row]['EthnicGroupDSC'],
        MaritalStatusDSC = tmp_patient_demo.iloc[row]['MaritalStatusDSC'],
        SexDSC = tmp_patient_demo.iloc[row]['SexDSC'],
        EducationLevelDSC = tmp_patient_demo.iloc[row]['EducationLevelDSC'],
        CoordinationNote = tmp_patient_demo.iloc[row]['CoordinationNote'],
        PatientLabs = tmp_patient_demo.iloc[row]['PatientLabs'],
        PatientImaging = tmp_patient_demo.iloc[row]['PatientImaging']
    )
    for row in range(0, len(tmp_patient_demo.index)) if not PatientDemographic.objects.filter(PatientID = int(tmp_patient_demo.iloc[row]['PatientID']))
]

PatientDemographic.objects.bulk_create(patient_demo, ignore_conflicts = False)
print("---- Patient Demographics Import Complete -----")


########################################
##### PATIENT YEARS IMPORT
########################################

tmp_patient_year = pd.read_csv(os.path.join(path,'patient_year.csv'), sep = ',', encoding = 'utf8')
tmp_patient_year = tmp_patient_year.replace({np.nan: None})

patient_year = [
    PatientYear(
        PatientID = tmp_patient_year.iloc[row]['PatientID'],
        Year = tmp_patient_year.iloc[row]['Year'],
        CurrentMeds = tmp_patient_year.iloc[row]['CurrentMeds'],
        MedHistory = tmp_patient_year.iloc[row]['MedHistory'],
        NoShows = tmp_patient_year.iloc[row]['NoShows'],
        Cancellations = tmp_patient_year.iloc[row]['Cancellations'],
        NumberNotes = tmp_patient_year.iloc[row]['NumberNotes'],
        TotalEncounters = tmp_patient_year.iloc[row]['TotalEncounters'],
        ICDCodes = tmp_patient_year.iloc[row]['ICDCodes']
    )
    for row in range(0, len(tmp_patient_year.index)) if not PatientYear.objects.filter(PatientID = int(tmp_patient_year.iloc[row]['PatientID']))
]

PatientYear.objects.bulk_create(patient_year, ignore_conflicts = False)
print("-------- Patient Year Import Complete ---------")


########################################
##### NOTES IMPORT
########################################

tmp_note = pd.read_csv(os.path.join(path,'notes.csv'), sep = ',', encoding = 'utf8')
tmp_note = tmp_note.replace({np.nan: None})

notes = [
    Note(
        PatientID = tmp_note.iloc[row]['PatientID'],
        PatientEncounterID = tmp_note.iloc[row]['PatientEncounterID'],
        InpatientNoteTypeDSC = tmp_note.iloc[row]['InpatientNoteTypeDSC'],
        ContactDTS = tmp_note.iloc[row]['ContactDTS'],
        EncounterTypeDSC = tmp_note.iloc[row]['EncounterTypeDSC'],
        NoteID = tmp_note.iloc[row]['NoteID'],
        LocalNoteID = tmp_note.iloc[row]['LocalNoteID'],
        NoteTXT = tmp_note.iloc[row]['NoteTXT'],
        ProviderNM = tmp_note.iloc[row]['ProviderNM'],
        LicenseDisplayDSC = tmp_note.iloc[row]['LicenseDisplayDSC'],
        PrimaryDepartmentDSC = tmp_note.iloc[row]['PrimaryDepartmentDSC'],
        CurrentPCP = tmp_note.iloc[row]['CurrentPCP'],
        Year = tmp_note.iloc[row]['Year'],
        KeywordCount = tmp_note.iloc[row]['KeywordCount'],
        ImagingInInterval = tmp_note.iloc[row]['ImagingInInterval'],
        LabsInInterval = tmp_note.iloc[row]['LabsInInterval']
    )
    for row in range(0, len(tmp_note.index)) if not Note.objects.filter(PatientID = int(tmp_note.iloc[row]['PatientID']))
]

Note.objects.bulk_create(notes, ignore_conflicts = False)
print("------------ Notes Import Complete ------------")