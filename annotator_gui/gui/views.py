from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import regex as re
import functools
import datetime
from itertools import chain, cycle
from .models import PatientDemographic, PatientYear, Note
from accounts.forms import NoteForm, SignUpForm, RequestPatientsForm, KeywordForm, PatientForm, ScratchpadForm, ConsensusForm
from django.contrib import messages

#reading in headers
import pandas as pd

# log-in and sign-up forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


## INDEX VIEW
def index(request):

    # retrieve information of currently logged in user
    current_user = request.user

    # redirect to either annotator home or login page
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/login')


### ABOUT PAGE
def about(request):

     # get template from gui/profile.html
    template = loader.get_template('gui/about.html')

    email_form = "Name:%0D%0AFeature Request:"

    context = {'email_form': email_form}

    return HttpResponse(template.render(context, request))


## USER LOGIN VIEW
def user_login(request):

    # get template from gui/login.html
    template = loader.get_template('gui/login.html')

    # define sign up and log in forms
    signup_form = SignUpForm(request.POST)
    login_form = AuthenticationForm(data=request.POST)

    if request.method == 'POST':

        # check sign up form, log in user
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)

            # # upon sign-up, assign five patients
            # unassigned = PatientDemographic.objects.filter(Assigned = False)[0:5]

            # # get patient IDs, update Assigned of PatientDemographic database to True
            # patientIDs = []
            # for patient in unassigned:
            #     patientIDs.append(patient.PatientID)
            #     patient.Assigned = True
            #     patient.save()

            # # save patient IDs in AssignedPatients variable for each user upon login
            # user.AssignedPatients = ', '.join([str(x) for x in patientIDs])
            # print("Patients Assigned: " + user.AssignedPatients)
            user.save()

            return redirect('/home')
        else:
            signup_form = SignUpForm()

        # check log in form
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            print("Log-In Success Message")
            messages.success(request, 'You are now logged in as ' + user.username + '.')
            return redirect('/home')
        else:
            login_form = AuthenticationForm()

        
        print("Sign-Up or Log-In Error Message")
        messages.error(request, 'The credentials entered are invalid. Please try again.')

    context = {
        'signup_form': signup_form,
        'login_form': login_form
    }

    return HttpResponse(template.render(context, request))


### USER LOGOUT
@login_required(redirect_field_name = None)
def user_logout(request):
    # if request.method == 'POST':
    #     logout(request)
    logout(request)    
    return redirect('/login')


### USER PROFILE
@login_required(redirect_field_name = None)
def user_profile(request):

     # get template from gui/profile.html
    template = loader.get_template('gui/profile.html')

    current_user = request.user

    # retrieve and parse assigned IDs
    assignedIDs = current_user.AssignedPatients
    assignedIDs = [int(x) for x in assignedIDs.split(', ')] if assignedIDs != 'None' else [None] # if no patients are assigned (i.e. admin), show patient 1

    full_note_count = Note.objects.filter(PatientID__in = assignedIDs).count()
    full_patient_count = PatientDemographic.objects.filter(PatientID__in = assignedIDs).count()

    # get notes with completed annotations
    noteDB = Note.objects.filter(Annotator = current_user.username)
    annot_patients = []
    for annot_notes in noteDB:
        annot_patients.append(annot_notes.PatientID)
    annot_patients = list(set(annot_patients)) # convert to set to remove duplicate patient IDs

    note_patientDB = PatientDemographic.objects.filter(PatientID__in = annot_patients) # subset patients which have SOME completed notes, NOT ALL COMPLETED PATIENTS
    
    completed_note_count = noteDB.count()
    no_notes = completed_note_count == 0

    # get all completed patients
    patientDB = PatientDemographic.objects.filter(Annotator = current_user.username)

    completed_patient_count = patientDB.count()
    no_patients = completed_patient_count == 0


    # get account keywords
    keywords_raw = current_user.Keywords

    # form to update keywords
    keywords_form = KeywordForm(initial = {'keywords': keywords_raw})
    if request.method == 'POST':
        keywords_form  = KeywordForm(request.POST)
        if keywords_form.is_valid():
            keywords_raw = keywords_form['keywords'].value()
            print("Keywords: " + keywords_raw)
            current_user.Keywords = keywords_raw
            current_user.save()
            messages.success(request, 'Keywords updated for your account.')
            return redirect('/profile')

    context = {
        'current_user': current_user,
        
        'noteDB': noteDB,
        'note_patientDB': note_patientDB,
        'completed_note_count': completed_note_count,
        'full_note_count': full_note_count,
        'no_notes': no_notes,

        'patientDB': patientDB,
        'completed_patient_count': completed_patient_count,
        'full_patient_count': full_patient_count,
        'no_patients': no_patients,

        'keywords_form': keywords_form,
        'keywords_raw': keywords_raw,
    }

    return HttpResponse(template.render(context, request))


### USER PROFILE
@login_required(redirect_field_name = None)
def group_consensus(request):

    # get template from gui/consensus.html
    template = loader.get_template('gui/consensus.html')

    # get note and patient databases
    patientDB = PatientDemographic.objects.filter(Consensus = True) # subset patients which are assigned
    consensusIDs = [x.PatientID for x in patientDB]
    noteDB = Note.objects.filter(PatientID__in = consensusIDs) # subset notes of those patients

    # calculate statistics for notes
    noteTODO = noteDB.filter(Label = "Incomplete")
    total_notes = noteDB.count()
    todo_notes = noteTODO.count()
    completed_notes = total_notes - todo_notes
    notes_per = round(todo_notes / total_notes * 100) if total_notes != 0 else 0

    no_notes = total_notes == 0

    # calculate statistics for patient-year
    patientTODO = patientDB.filter(SyndromicDiagnosis = "Incomplete")
    total_patients = patientDB.count()
    todo_patients = patientTODO.count()
    completed_patients = total_patients - todo_patients
    patients_per = round(todo_patients / total_patients * 100) if total_patients != 0 else 0


    context = {
        'patientDB': patientDB,
        'noteDB': noteDB, 
        'noteTODO': noteTODO, 
        'total_notes': total_notes, 
        'todo_notes': todo_notes, 
        'completed_notes': completed_notes, 
        'notes_per': notes_per, 
        'no_notes': no_notes,
        'patientTODO': patientTODO, 
        'total_patients': total_patients, 
        'todo_patients': todo_patients, 
        'completed_patients': completed_patients, 
        'patients_per': patients_per,
    }

    return HttpResponse(template.render(context, request))
     

## ANNOTATOR HOME VIEW
@login_required(redirect_field_name = None)
def annotator_home(request):
    
    # get template from gui/home.html
    template = loader.get_template('gui/home.html')

    # retrieve information of currently logged in user
    current_user = request.user

    # retrieve and parse assigned IDs
    assignedIDs = current_user.AssignedPatients
    assignedIDs = [int(x) for x in assignedIDs.split(', ')] if assignedIDs != 'None' else [None] # if no patients are assigned (i.e. admin), show patient 1

    # get note and patient databases
    patientDB = PatientDemographic.objects.filter(PatientID__in = assignedIDs) # subset patients which are assigned
    noteDB = Note.objects.filter(PatientID__in = assignedIDs) # subset notes of those patients
    # patientyearDB = PatientYear.objects.filter(PatientID__in = assignedIDs)

    ### CALCULATE STATISTICS FOR DASHBOARD 

    # calculate statistics for notes
    noteTODO = noteDB.filter(Label = "Incomplete")
    total_notes = noteDB.count()
    todo_notes = noteTODO.count()
    completed_notes = total_notes - todo_notes
    notes_per = round(todo_notes / total_notes * 100) if total_notes != 0 else 0

    no_notes = total_notes == 0

    # calculate statistics for patient-year
    patientTODO = patientDB.filter(SyndromicDiagnosis = "Incomplete")
    total_patients = patientDB.count()
    todo_patients = patientTODO.count()
    completed_patients = total_patients - todo_patients
    patients_per = round(todo_patients / total_patients * 100) if total_patients != 0 else 0

    # form to assign additional patients
    form = RequestPatientsForm()
    if request.method == 'POST':
        
        value = RequestPatientsForm(request.POST)

        if value.is_valid():
            num_to_add = int(value['num_to_add'].value()) # get values from POST
            print("Assigning Additional Patients: " + str(num_to_add) + " patients to " + str(current_user))
            # num_to_add = num_to_add-1 if num_to_add > 1 else num_to_add  # remember this is zero-indexed

            # assign additional patients
            unassigned = PatientDemographic.objects.filter(Assigned = False)[0:num_to_add]

            # get patient IDs, update Assigned of PatientDemographic database to True
            patientIDs = []
            for patient in unassigned:
                patientIDs.append(patient.PatientID)
                patient.Assigned = True
                patient.save()

            print(patientIDs)
            # save patient IDs in AssignedPatients variable for each user upon login
            current_user.AssignedPatients = current_user.AssignedPatients + ', ' + ', '.join([str(x) for x in patientIDs]) if current_user.AssignedPatients != 'None' else ', '.join([str(x) for x in patientIDs])
            current_user.save()
            print("Patients Assigned: " + current_user.AssignedPatients)

            # after submission of a web form, have to return redirect, even if to the same view
            return redirect("/home")

        print("Patient Request Error Message")
        messages.error(request, 'Please request between 1-100 additional patient records to annotate at a time.')


    context = {
        'current_user': current_user,
        'patientDB': patientDB,
        'noteDB': noteDB, 
        'noteTODO': noteTODO, 
        'total_notes': total_notes, 
        'todo_notes': todo_notes, 
        'completed_notes': completed_notes, 
        'notes_per': notes_per, 
        'no_notes': no_notes,
        'patientTODO': patientTODO, 
        'total_patients': total_patients, 
        'todo_patients': todo_patients, 
        'completed_patients': completed_patients, 
        'patients_per': patients_per,
        'request_patients_form': form,
    }

    return HttpResponse(template.render(context, request))


# KEYWORD COUNT FUNCTION
def keyword_count(output, keywords_raw, is_note = False):

    # parse keywords into regex alternation expressions
    keywords = keywords_raw.split(", ") # don't force alternation

    regex_raw = open("gui/static/regex_default.txt", mode = "r", encoding = 'utf-8').read().split("\n") # get regex expressions from file in static folder
        
    regex_raw = regex_raw + keywords
    regex_list = [re.compile(regex,flags=re.IGNORECASE) for regex in regex_raw] # compile regex list

    pattern_list = [re.findall(pattern, output) for pattern in regex_list]
    pattern_list = set(list((chain.from_iterable(pattern_list)))) # flatten list, remove duplicates

    if is_note:
        tups = [(itm, r'<span class = "note-keyword">' + itm + r'</span>') for itm in pattern_list]
    else:
         tups = [(itm, r'<span class = "keyword">' + itm + r'</span>') for itm in pattern_list]

    # make the substitution to add highlight tag
    for old, new in tups:
        output = re.sub(old, new, output)

    # center on first keyword but suffixing URL with /#keyword
    # output = re.sub(r'(<mark>.+?</mark>)',r'<span id = "first-keyword">\1</span>', output, count=1)

    return output


# SPLIT BY HEADERS FUNCTION
def format_note(output):

    # split by sentences
    # output = re.sub(r"(?<![A-Z][a-z])([!?.])(?=\s*[A-Z])\s*", r"\1\n<br>", output)

    headers = open("gui/static/regex_headers.txt", mode = "r", encoding = 'utf-8').read().split("\n")
    header_list = [re.compile(regex, flags=re.IGNORECASE) for regex in headers]
    # print(header_list)

    # check if the first word in the sentence is a word from the headers file
    # if it is, then add an extra breakpoint before it

    pattern_list = [re.findall(pattern, output) for pattern in header_list]
    pattern_list = set(list((chain.from_iterable(pattern_list)))) # flatten list, remove duplicates

    tups = [(itm, r'<br><br><span style="text-decoration: underline;">' + itm + r'</span>') for itm in pattern_list]

    for old, new in tups:
        output = re.sub(old, new, output)

    return output


# SPLIT BY BULLETS FUNCTION
def format_bullet(output):

    bullets = open("gui/static/regex_bullets.txt", mode = "r", encoding = 'utf-8').read().split("\n")
    bullet_list = [re.compile(regex, flags=re.IGNORECASE) for regex in bullets]

    pattern_list = [re.findall(pattern, output) for pattern in bullet_list]
    pattern_list = set(list((chain.from_iterable(pattern_list)))) # flatten list, remove duplicates

    tups = [(itm, r'<br>' + itm) for itm in pattern_list]

    for old, new in tups:
        output = re.sub(old, new, output)

    return output


# REPLACE XXXXX WITH GRAY BOX FOR PRIVATE INFO
def redact(privateinfo):
    private_flag = re.compile("XXXXX") # replace regex
    pattern_list = re.findall(private_flag, privateinfo)
    pattern_list = set(list((chain.from_iterable(pattern_list)))) # flatten list, remove duplicates
    tups = [(itm, r'<span class="redact">' + itm + r'</span>') for itm in pattern_list]
    # make the substitution to add highlight tag
    for old, new in tups:
        privateinfo = re.sub(old, new, privateinfo)
    return privateinfo


# PARSE LABS/IMAGING BY REPLACING | WITH NEW LINE
def parse_labs(labs):
    return r'<tr><td>' + labs.replace('%^%', r'</td></tr><tr><td>') + r'</td></tr>'

def parse_labs_cell(labs):
    return labs.replace('%&%', r'</td><td>')



## ANNOTATOR PANEL VIEW
@login_required(redirect_field_name = None)
def show_note(request, patient_id, local_note_id):
    
    # get template from gui/note.html
    template = loader.get_template('gui/note.html')

    # retrieve information of currently logged in user
    current_user = request.user

    # use the parameters from URl slug to get all notes for specified patient, then select correct note from Note database
    notes_patient = Note.objects.filter(PatientID = patient_id)
    note = notes_patient.get(LocalNoteID = local_note_id)

    # get index for note in year
    notes_patient_year = notes_patient.filter(Year = note.Year)
    year_idx = []
    for my_note in notes_patient_year:
        year_idx.append(my_note.LocalNoteID)
    patient_year_idx = str(year_idx.index(local_note_id) + 1) # zero indexed

    # select correct patient corresponding to specified note from PatientDemographic databse
    patient = PatientDemographic.objects.get(PatientID = patient_id)

    # get correct the patient year record from PatientYear database
    patient_year_all = PatientYear.objects.filter(PatientID = patient_id)
    patient_year = patient_year_all.get(Year = note.Year) # get appropriate patient year record

    # get all years for this patient, remove None values    
    all_years = []
    for year in patient_year_all:
        if year.Year is not None: all_years.append(year.Year)
    all_years.sort()

    # find next patient ID
    current_year_idx = all_years.index(note.Year) if note.Year is not None else len(all_years)
    previous_year_idx = notes_patient.filter(Year = all_years[current_year_idx - 1])[0].LocalNoteID if current_year_idx > 0 else local_note_id
    next_year_idx = notes_patient.filter(Year = all_years[current_year_idx + 1])[0].LocalNoteID if current_year_idx < len(all_years) - 1 else local_note_id

    # get note year, note count
    note_year = str(note.Year)[0:4]
    note_count = notes_patient.count()

    # calculate current age
    show_age = True
    if note.ContactDTS is not None and patient.BirthDTS is not None: 
        age_at_encounter = note.ContactDTS - patient.BirthDTS
        years_rem = divmod(age_at_encounter.days, 365)
        years_at_encounter = years_rem[0]
        months_at_encounter = divmod(years_rem[1], 30)[0]
    else:
        years_at_encounter = "NA"
        months_at_encounter = "NA"
        show_age = False

    output = str(note.NoteTXT) # note text
    current_meds = str(patient_year.CurrentMeds) # current medications
    med_hist = str(patient_year.MedHistory) # medication history
    
    pcc_note = str(patient.CoordinationNote) # patient care coordination note
    icd_codes = str(patient_year.ICDCodes)
    labs = str(patient.PatientLabs) # patient labs
    imaging = str(patient.PatientImaging) # patient imaging

    #format note
    output = format_bullet(output)
    output = format_note(output)
    output = redact(output)

    keywords_raw = current_user.Keywords
    output = keyword_count(output, keywords_raw) # apply keyword_count function above for note text
    current_meds = keyword_count(current_meds, keywords_raw) # for current medications
    med_hist = keyword_count(med_hist, keywords_raw) # for medication history

    pcc_note = keyword_count(pcc_note, keywords_raw) # apply keyword highlighting above for coordination note
    icd_codes = keyword_count(icd_codes, keywords_raw)
    labs = keyword_count(labs, keywords_raw) # for labs
    imaging = keyword_count(imaging, keywords_raw) # for imaging

    labs = parse_labs_cell(parse_labs(labs))
    imaging = parse_labs_cell(parse_labs(imaging))

    # get scratchpad text
    scratchpad_raw = patient.Scratchpad

    # get current consensus label
    patient_consensus = patient.Consensus

    # for previous and next buttons
    current_link = '/annotate/' + str(patient_id) + '/' + str(local_note_id)
    previous_link = '/annotate/' + str(patient_id) + '/' + str(local_note_id - 1) if local_note_id > 1 else current_link
    next_link = '/annotate/' + str(patient_id) + '/' + str(local_note_id + 1) if local_note_id < note_count  else current_link

    previous_year_link = '/annotate/' + str(patient_id) + '/' + str(previous_year_idx)
    next_year_link = '/annotate/' + str(patient_id) + '/' + str(next_year_idx)


    # POST user input using NoteForm to save annotation labels
    note_form = NoteForm(instance = note)
    if request.method == 'POST':
        note_form = NoteForm(request.POST, instance = note)
        if note_form.is_valid():
            note_form.save()
            note.Annotator = current_user.username
            note.DateAnnotated = datetime.datetime.now()
            note.save()
            messages.success(request, 'You have sucessfully annotated Note #' + str(local_note_id) + ' for Patient #' + str(patient_id) + '.')
            return redirect(current_link) # go to same note
    

    # POST user input using PatientForm to save annotation labels
    patient_form = PatientForm(instance = patient)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance = patient)
        if patient_form.is_valid():
            patient_form.save()
            patient.Annotator = current_user.username
            patient.DateAnnotated = datetime.datetime.now()
            patient.save()
            # go to first note for the next year, unless this is the max. available year, in which case stay put
            messages.success(request, 'You have sucessfully annotated Patient #' + str(patient_id) + '.')
            return redirect(current_link)


    # form to dynamically update keywords
    keywords_form = KeywordForm(initial = {'keywords': keywords_raw})
    if request.method == 'POST':
        keywords_form  = KeywordForm(request.POST)
        if keywords_form.is_valid():
            keywords_raw = keywords_form['keywords'].value()
            print("Keywords: " + keywords_raw)
            output = keyword_count(output, keywords_raw) # note text regex highlighting
            current_meds = keyword_count(current_meds, keywords_raw) # current medications regex highlighting
            med_hist = keyword_count(med_hist, keywords_raw) # medication history regex highlighting
            current_user.Keywords = keywords_raw
            current_user.save()
            messages.success(request, 'Keywords updated.')
            return redirect(current_link)


    # form for scratchpad
    scratchpad_form = ScratchpadForm(initial = {'scratchpad': scratchpad_raw})
    if request.method == 'POST':
        scratchpad_form = ScratchpadForm(request.POST)
        if scratchpad_form.is_valid():
            scratchpad_raw = scratchpad_form['scratchpad'].value()
            patient.Scratchpad = scratchpad_raw
            patient.save()
            messages.success(request, 'Scratchpad successfully updated.')
            return redirect(current_link)


        # TOGGLE patient consensus message
    consensus_form = ConsensusForm()
    if request.method == 'POST':
        consensus_form = ConsensusForm(request.POST)
        if consensus_form.is_valid():
            patient.Consensus = not patient.Consensus
            patient.ConsensusActor = str("Dr. " + current_user.first_name + " " + current_user.last_name + " (" + current_user.username + ")")
            patient.save()
            if (patient.Consensus):
                messages.success(request, 'You have sucessfully sent Patient #' + str(patient_id) + ' to consensus conference.')
            else:
                messages.success(request, 'You have sucessfully removed Patient #' + str(patient_id) + ' from consensus conference.')
            return redirect(current_link)

    context = {
        'current_user': current_user,
        'patient': patient,
        'note': note,
        'patient_year': patient_year,
        'patient_ID': patient_id,
        'note_year': note_year,
        'patient_year_idx': patient_year_idx,
        'note_count': note_count,
        'years_at_encounter': years_at_encounter,
        'months_at_encounter': months_at_encounter,
        'show_age': show_age,
        'note_text': output,
        'med_hist': med_hist,
        'current_meds': current_meds,
        'pcc_note': pcc_note,
        'icd_codes': icd_codes,
        'labs': labs,
        'imaging': imaging,
        'note_form': note_form,
        'patient_form': patient_form,
        'consensus_form': consensus_form,
        'patient_consensus': patient_consensus,
        'keywords_form': keywords_form,
        'keywords_raw': keywords_raw,
        'scratchpad_form': scratchpad_form,
        'previous_link': previous_link,
        'next_link': next_link,
        'previous_year_link': previous_year_link,
        'next_year_link': next_year_link,
        'notes_patient': notes_patient,
    }

    return HttpResponse(template.render(context, request))
