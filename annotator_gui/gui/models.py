from django.db import models

# to reset databsae:
    # run python manage.py reset_db (from django-extensions package)

# to delete all data from the table:
# python manage.py shell
# >> from gui.models import PatientDemographic, PatientYear, Note
# >> PatientDemographic.objects.all().delete()
# >> PatientYear.objects.all().delete()
# >> Note.objects.all().delete()

# to add data:
# update .csv files in load_data/data
# python manage.py shell
# >> %run load_data/load_data.py


SDChoices = (
('0', 'No Cognitive Concern'),
('1', 'Mild Cognitive Impairment'),
('2', 'Dementia')
)

DSChoices = (
('0', 'None'),
('1', 'Mild'),
('2', 'Moderate'),
('3', 'Severe'),
('9', 'Unknown')
)

LCChoices = (
('0', 'Not Confident'),
('1', 'Mildly Confident'),
('2', 'Moderately Confident'),
('3', 'Highly Confident')
)

LabelChoices = (
('0', 'No Relevant Information'),
('1', 'Relevant to Cognitive Concern')
)


class PatientDemographic(models.Model):
    PatientID = models.IntegerField(blank = True, null = True)
    MRN = models.IntegerField(blank = True, null = True)
    BirthDTS = models.DateField(blank = True, null = True)
    EthnicGroupDSC = models.TextField(blank = True, null = True)
    MaritalStatusDSC = models.TextField(blank = True, null = True)
    SexDSC = models.TextField(blank = True, null = True)
    EducationLevelDSC = models.TextField(blank = True, null = True)
    CoordinationNote = models.TextField(blank = True, null = True)
    PatientLabs = models.TextField(blank = True, null = True)
    PatientImaging = models.TextField(blank = True, null = True)
    Assigned = models.BooleanField(default = False)
    SyndromicDiagnosis = models.TextField(choices = SDChoices, default = 'Incomplete')
    DementiaSeverity = models.TextField(choices = DSChoices, default = 'Incomplete')
    LabelCertainty = models.TextField(choices = LCChoices, default = 'Incomplete')
    Annotator = models.TextField(blank = True, null = True)
    DateAnnotated = models.DateTimeField(blank = True, null = True)
    Scratchpad = models.TextField(blank = True, null = True, default='')
    Consensus = models.BooleanField(default = False)
    ConsensusActor = models.TextField(blank = True, null = True)
    
    def __str__(self):
        return(str(self.PatientID))


class PatientYear(models.Model):
    PatientID = models.IntegerField(blank = True, null = True)
    Year = models.CharField(max_length = 4, blank = True, null = True)
    CurrentMeds = models.TextField(blank = True, null = True)
    MedHistory = models.TextField(blank = True, null = True)
    NoShows = models.IntegerField(blank = True, null = True)
    Cancellations = models.IntegerField(blank = True, null = True)
    NumberNotes = models.IntegerField(blank = True, null = True)
    TotalEncounters = models.IntegerField(blank = True, null = True)
    ICDCodes = models.TextField(blank = True, null = True)
    
    def __str__(self):
        return(str(self.PatientID) + "/" + str(self.Year))


class Note(models.Model):
    PatientID = models.IntegerField(blank = True, null = True)
    PatientEncounterID = models.CharField(max_length = 100, blank = True, null = True)
    InpatientNoteTypeDSC = models.TextField(blank = True, null = True)
    ContactDTS = models.DateField(blank = True, null = True)
    EncounterTypeDSC = models.TextField(blank = True, null = True)
    NoteID = models.IntegerField(blank = True, null = True)
    LocalNoteID = models.IntegerField(blank = True, null = True)
    NoteTXT = models.TextField(blank = True, null = True)
    ProviderNM = models.TextField(blank = True, null = True)
    LicenseDisplayDSC = models.TextField(blank = True, null = True)
    PrimaryDepartmentDSC = models.TextField(blank = True, null = True)
    CurrentPCP = models.TextField(blank = True, null = True)
    Year = models.CharField(max_length = 4, blank = True, null = True)
    KeywordCount = models.IntegerField(blank = True, null = True)
    ImagingInInterval = models.BooleanField(default = False)
    LabsInInterval = models.BooleanField(default = False)
    Label = models.TextField(choices = LabelChoices, default = 'Incomplete')
    Annotator = models.TextField(blank = True, null = True)
    DateAnnotated = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return(str(self.PatientID) + "/" + str(self.LocalNoteID))
