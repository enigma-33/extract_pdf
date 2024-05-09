# Parse people's names to last name and first name and title. 

_prompt = """
You analyze patient medical records to export them into a JSON format. 
I will present you with a patient medical record and describe the individual JSON objects and properties with <<<. 
You then create a JSON object from another product data sheet. 
[..] indicates that there could be multiple entries of a similar format, example goals (keep goal number).
Parse addresses. 
Format phone with dashes and no parens. 
Format dates as YYYY-MM-DD. 
Parse medications.
Parse all medical treatment plans, do not summarize or abbreviate.
Parse follow up.

>>> Example patient medical record:

PATIENT NAME: <<< patient (object) 
Mark Ayala <<< patient.first_name = Marl, patient_last_name = Ayala
AGE: 
45 years
SEX:
Male
DOB:
01/16/1979
PHONE:
(352) 737-2217 
ADDRESS:
17736 MEDLY AVE
 SPRING HILL, FL 34610-6757
CHART NUMBER: <<< date_of_service (object)
30523 <<< date_of_service.chart_num
DATE OF SERVICE: 
03/14/2024 <<< date_of_service.date_of_service
PROVIDER: <<< provider (object)
 Sylvia Leaman, APRN 
17222 HOSPITAL BLVD STE 120 
BROOKSVILLE, FL 34601-8925 
 Phone: (352) 678-5550 Fax: (352) 678-5551

Visit Diagnosis: <<< visit_diagnosis (object)
F33.2 Major Depressive Disorder 

Recurrent: Severe 
F43.12 Post-traumatic Stress  

Disorder Chronic 
99214 - Established Patient Office 
Visit - 30-39 minutes 

Page
1
 of
3

[..]

Solace Vital Signs:
Happiness: 4/10. 
Anxiety; Stress: 4-6/10.
Suicidal Thoughts: 0/10.
Depression: 4-8/10. 
Energy Level: 8/10. 
Sleep quality: 8/10. 
Impulsivity: 0/10. 
Mania: 0/10. 
Psychotic symptoms: 0/10. 
Hours of Sleep at Night: 4-6. 
MEASUREMENTS: Height: 73 in.  
Weight: 188 lbs.   
BMI: 24.8. 


Current Medications: <<< current_meds (object)
Spravato, 84 mg (28 mg x 3),

QWeekly
lithium carbonate, 300 mg, QHS
lamotrigine, 200 mg, QHS
clonazepam, 0.5 mg, ASDIR
aripiprazole, 1 mg/mL, QD

Side Effect(s) / concerns with
current meds: None at this time. 

[..]

Psychiatric Medication History: <<< psych_med_history (object)
Lexapro, Lithium, Lamictal, Abilify,
Klonopin,  <<< psych_med_history.history
Other Treatments: Spravato 
treatment reported. <<< psych_med_history.other = Spravato
Historical Drug Use (if any): <<< psych_med_history.hist_drug_use = N/A
Current Drug Use (if any): <<< psych_med_history.curr_drug_use = N/A


New Medication Recommendations: <<< new_med_rec (object)
Increase Abilify 1 mg/mL - take 10

oral mL at bedtime.
Continue Lamictal 200 mg

disintegrating tab QHS.
Continue Klonopin 0.5 mg, 1/2 tab

TID (only using PRN, has supply).
Continue Lithium 300 mg ii QHS.

[..]

MED MANAGEMENT NOTE: <<< med_management_notes (object)
E/M START & STOP TIMES:
Start Time: 03:20 PM. Stop Time: 03:36 PM. Total E/M Time: 16 minutes.
VISIT TYPE:
The purpose of this visit was a medication check and follow-up. An in-person visit was

conducted.
SUPERVISING PHYSICIAN:
Office visit rendered today under the credentialed supervision of: Dr. Chaudhry.
CHIEF COMPLAINT:
Pt reports depression.
HISTORY OF PRESENT ILLNESS
:
Patient seen for medication management appointment. Patient reports that he's feeling

tired today, has been busy pouring concrete.  Patient reports that he and his wife are

still separated, she has an injunction in place that is up the second week of April.

Patient states he's currently living in a camper.  Patient states he hates to see what this

is doing to the kids.  Patient states it's hard for anything to change because his wife

doesn't see that she's doing anything wrong
and won't get treated for her mental illness.  Patient states his medications are

beneficial and he wants to go back up to the previous dose of Abilify he was taking.

Patient has been coming in for Sapravato once a week.
[..]

TARGET SYMPTOMS 
: <<< target_symptoms (object)
Anxiety: pt reports generalized anxiety, ongoing worry and insomnia. Most of the

preoccupations are about things that are out of their control. There is clear activation of

the sympathetic nervous system and the fight, flight and freeze mechanisms. Also:

emotional reactivity, fatigue, problems concentrating and completing tasks. Depression:

pt reports depressed mood, periods of sadness and lack of an ability to feel joy.

[..]

EXAM: <<< exam (object)
RATING SCALES:
MENTAL STATUS EXAM: General appearance notes: Casually dressed. Hygiene notes:

Adequate attention to ADL's observed. Attitude/Behavior notes: Concerned.  Mood

notes: Depressed.   Affect notes: Fluid and modulated  Motor exam notes: Normal gait,

strength and stature. Suicidal ideation notes: None reported at this time. Homicidal
PATIENT NAME:
Mark Ayala
AGE:
45 years
SEX:
Male
DOB:
01/16/1979
17222 HOSPITAL BLVD STE 120
BROOKSVILLE, FL 34601-8925
 Phone: (352) 678-5550 Fax: (352) 678-5551
Page
2
 of
3





ideation notes: None reported at this time. Hallucination notes: None reported at this

time. Illusion/Misperception notes: None reported at this time. Delusion notes: None

reported at this time. Ideas of reference notes: None reported at this time. Thought

process notes: Linear, logical and goal oriented. Sensorium: Clear. Executive functioning

notes: Intact. Abstract thinking notes: Suboptimal. Insight into illness notes: Some

denial. Judgement notes: Mildly impaired. Reliability notes: Questionable. Cognition

notes: No gross deficits observed.

Current Allergies: 
NKDA <<< current_allergies (object)

TREATMENT PLAN: <<< treatment_plan (object)
HEALTH AND SAFETY GOALS: <<< treatment_plan.health_safety_goals
Goal 1: Client will reduce overall frequency, intensity, and
duration of reported symptoms related to physical trauma. Date Created: 8/13/2022.
Severity: Moderate. Would like patient to be improved by 25%. Time to Resolution: 6
months. Objective: Learn/demonstrate understanding of Fight/Flight/Freeze distress.
Learn/demonstrate 2-3 CBT skills to manage reported symptoms. Interventions: Client
to attend regular medication management appointments and take prescriptions as
prescribed.
Client to attend therapy sessions as prescribed.

[..]

BEHAVIORAL / RELATIONSHIP GOALS: <<< treatment_plan.behavioral_rel_goals
 Goal 1: N/A: Domain not applicable at this time.

Provider to reevaluate next session.
EMOTIONAL GOALS: <<< treatment_plan.emotional_goals
Goal 1: DEPRESSION: Client will reduce overall frequency, intensity,

and duration of depression symptoms to improve daily functioning. Date Created:

10/21/2022. The goal was addressed during today's visit. Severity: Moderate. Would like

patient to be improved by 50%. Time to Resolution: 6 months. Objective:

Learn/demonstrate 2-3 CBT skills to manage reported symptoms.
Learn/implement 2-3 skills to maintain discipline.
Learn/demonstrate 2-3 mindfulness techniques to manage symptoms. Interventions:

Client to attend regular medication management appointments and take prescriptions

as prescribed.
Client to attend therapy sessions as prescribed.
Engage in Spravato treatment as prescribed. Comments: Patient with ongoing

depression and anxiety, coming in for Spravato, increased Abilify.  SL

[..]

INTELLECTUAL / MENTAL GOALS: <<< treatment_plan.int_mental_goals
Goal 1: N/A: Domain not applicable at this time.

Provider to reevaluate next session. 
PERSONAL GOALS: 
Goal 1: N/A: Domain not applicable at this time. Provider to

reevaluate next session. <<< treatment_plan.personal_goals

COMPLETED GOALS / ACHIEVEMENT: <<< treatment_plan.completed_goals


RISK ASSESSMENT THIS VISIT: <<< risk_assessment (object)

No safety issues determined at this time. Continues to have risks inherent to disease

state.

LAB MONITORING: <<< lab_monitoring (object)
Monitor Lithium level, TSH and Lamotrigine level.
Patient having yearly bloodwork done for PCP and will bring in those results.
REFERRALS:
None.
THERAPY:
No therapy
FOLLOW-UP / TREATMENT PLAN REVIEW: <<< follow_up (object)
Continue current treatment plan.
FOLLOW UP WITH ARNP: Next appointment - 3 month(s).
Continue current prescribed treatment with current NP.
Medication management and psychotherapeutic interventions as needed (PRN).
Prescribed Treatment: Continue current prescribed therapy.

[..]

Electronically Signed: LEAMAN SYLVIAon 03/14/2024License: APRN2191702 <<< signature_info (object)
Signed By: Sylvia Leaman, APRN 03/14/2024 03:46 PM <<< signature_info.signed_by = Sylvia Leaman,signature_info.title = APRN, signature_info.date_time = 03/14/2024 03:46 PM,
signature_info.license = APRN2191702

"""