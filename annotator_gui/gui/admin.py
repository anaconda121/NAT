from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import PatientDemographic, PatientYear, Note

class PatientDemographicResource(resources.ModelResource):
    class Meta:
        model = PatientDemographic
class PatientDemographicAdmin(ImportExportModelAdmin):
    resource_class = PatientDemographicResource

    list_display = ('PatientID', 'MRN', 'BirthDTS', 'EthnicGroupDSC', 'MaritalStatusDSC',
    'SexDSC', 'EducationLevelDSC', 'CoordinationNote', 'PatientLabs', 'PatientImaging', 'Assigned', 'SyndromicDiagnosis',
    'DementiaSeverity', 'LabelCertainty', 'Annotator', 'DateAnnotated', 'Scratchpad', 'Consensus', 'ConsensusActor') 

# register patient model
admin.site.register(PatientDemographic, PatientDemographicAdmin)


class PatientYearResource(resources.ModelResource):
    class Meta:
        model = PatientYear
class PatientYearAdmin(ImportExportModelAdmin):
    resource_class = PatientYearResource

    list_display = ('PatientID', 'Year', 'CurrentMeds', 'MedHistory', 'NoShows',
    'Cancellations', 'NumberNotes', 'TotalEncounters', 'ICDCodes') 

# register patient model
admin.site.register(PatientYear, PatientYearAdmin)


class NoteResource(resources.ModelResource):
    class Meta:
        model = Note
class NoteAdmin(ImportExportModelAdmin):
    resource_class = NoteResource

    list_display = ('PatientID', 'InpatientNoteTypeDSC', 'ContactDTS', 'EncounterTypeDSC',
    'NoteID', 'LocalNoteID', 'NoteTXT', 'ProviderNM', 'LicenseDisplayDSC', 'PrimaryDepartmentDSC', 'CurrentPCP',
    'Year', 'KeywordCount', 'ImagingInInterval', 'LabsInInterval', 'Label', 'Annotator', 'DateAnnotated')

# register note model
admin.site.register(Note, NoteAdmin)