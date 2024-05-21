# Parse people's names to last name and first name and title. 

_prompt = """
You analyze patient medical records to export them into a JSON format. 
I will present you with a patient medical record and describe the individual JSON objects and properties with <<<. 
You then create a JSON object from another patient medical record. 
[..] indicates that there could be multiple entries of a similar format, example goals (keep goal number).
Parse addresses. 
Format phone with dashes and no parens. 
Format dates as YYYY-MM-DD. 
Parse Medications. 
Include Risk Assessment.
Include Lab Montoring.
Do NOT include Treatment plans.
Do NOT include Follow up under Treatent plans.
Do NOT include exam.
Do include the JSON object even if it does not appear in the document.



>>> Example patient medical record:

PATIENT NAME: <<< patient (object) 
Amorette Test <<< patient.first_name = Amorette, patient_last_name = Test
AGE: 27 years  SEX: Female
DOB: 12/26/1996
PHONE: (352) 678-8460
ADDRESS: 4800 Rowan Rd
 New Port Richey, FL 34653
CHART NUMBER: <<< date_of_service (object)
09876  <<< date_of_service.chart_num
DATE OF SERVICE: 05/15/2024 <<< date_of_service.date_of_service 
PROVIDER:  <<< provider (object)
Tanveer Chaudhry, MD
17222 HOSPITAL BLVD STE 120
BROOKSVILLE, FL 34601-8925
 Phone: (352) 678-5550 Fax: (352) 678-5551
Page 1 of 4
Visit Diagnosis: <<< visit_diagnosis (string[])
 F40.01 AGORAPHOBIA WITH PANIC
DISORDER
 F33.1 MAJOR DEPRESSIVE
DISORDER, RECURRENT,
MODERATE
 F90.0 ATTN-DEFCT HYPERACTIVITY
DISORDER, PREDOM INATTENTIVE
TYPE
 F31.30 BIPOLAR DISORD, CRNT EPSD
DEPRESS, MILD OR MOD SEVERT,
UNSP
 F33.0 MAJOR DEPRESSIVE
DISORDER, RECURRENT, MILD
 F20.0 PARANOID SCHIZOPHRENIA
 F25.0 SCHIZOAFFECTIVE DISORDER,
BIPOLAR TYPE
 F53.0 POSTPARTUM DEPRESSION
 F31.81 BIPOLAR II DISORDER
 F33.2 MAJOR DEPRESSV DISORDER,
RECURRENT SEVERE W/O PSYCH
FEATURES
 F41.1 GENERALIZED ANXIETY
DISORDER
 F43.10 POST-TRAUMATIC STRESS
DISORDER, UNSPECIFIED
 F43.12 POST-TRAUMATIC STRESS
DISORDER, CHRONIC
 Z79.899 OTHER LONG TERM
(CURRENT) DRUG THERAPY
 F91.1 CONDUCT DISORDER,
CHILDHOOD-ONSET TYPE
 F32.A DEPRESSION, UNSPECIFIED
 R45.4 IRRITABILITY AND ANGER
 V97.33XS SUCKED INTO JET ENGINE,
SEQUELA
 F90.0 ATTN-DEFCT HYPERACTIVITY
DISORDER, PREDOM INATTENTIVE
TYPEMED MANAGEMENT NOTE: 
E/M START & STOP TIMES: 
Start Time:  03:39 PM. Stop Time:  3:39 pm. Total E/M Time: 2 minutes. 
VISIT TYPE: <<< visit_type (string[])
The purpose of this visit was a medication check and follow-up. An in-person visit was
conducted. <<< visit_type.[*] = The purpose of this visit was a medication check and follow-up. An in-person visit was
conducted.
SUPERVISING PHYSICIAN: <<< supervising_physician(string[])
Office visit rendered today under the credentialed supervision of: N/A: Rendering as
self. <<< supervising_physician.[*]
CHIEF COMPLAINT: <<< chief_complaint(string[])
Depression, PTSD <<< chief_complaint.[*]
HISTORY OF PRESENT ILLNESS: <<< history_present_illness(string[])
2 
INTERVAL SENTIANAL EVENTS: 2 <<< history_present_illness.[*]
TARGET SYMPTOMS: <<< target_symptoms(string[])
Maintenance: Will focus on maintaining stability with medication compliance and
monitoring for signs and symptoms of mental illness during medication management
follow-up appointments. <<< target_symptoms.[*]
EXAM: 
RATING SCALES:
MENTAL STATUS EXAM: General appearance notes: 2 Hygiene notes: 2 
Attitude/Behavior notes: 2 Mood notes: 2 Affect notes: 2 Motor exam notes: 2 Suicidal
ideation notes: None reported at this time. Homicidal ideation notes: None reported at
this time. Hallucination notes: None reported at this time. Illusion/Misperception notes:
None reported at this time. Delusion notes: None reported at this time. Ideas of
reference notes: None reported at this time. Thought process notes: Linear, logical and
goal oriented. Sensorium: Clear. Executive functioning notes: Intact. Abstract thinking
notes: Suboptimal. Insight into illness notes: Limited.  Judgement notes: Mildly
impaired. Reliability notes: Questionable. Cognition notes: No gross deficits observed.
MMSE SCORE: 2/30. 
Notes: 2
TREATMENT PLAN: 
HEALTH AND SAFETY GOALS: Goal 1: N/A: Domain not applicable at this time. Provider 
to reevaluate next session.
PATIENT NAME: Amorette Test
AGE: 27 years  SEX: Female
DOB: 12/26/1996
17222 HOSPITAL BLVD STE 120
BROOKSVILLE, FL 34601-8925
 Phone: (352) 678-5550 Fax: (352) 678-5551
Page 2 of 4 F31.30 BIPOLAR DISORD, CRNT EPSD
DEPRESS, MILD OR MOD SEVERT,
UNSP
 F33.0 MAJOR DEPRESSIVE
DISORDER, RECURRENT, MILD
 F20.0 PARANOID SCHIZOPHRENIA
 F25.0 SCHIZOAFFECTIVE DISORDER,
BIPOLAR TYPE
 F53.0 POSTPARTUM DEPRESSION
 F31.81 BIPOLAR II DISORDER
 F33.2 MAJOR DEPRESSV DISORDER,
RECURRENT SEVERE W/O PSYCH
FEATURES
 F41.1 GENERALIZED ANXIETY
DISORDER
 F43.10 POST-TRAUMATIC STRESS
DISORDER, UNSPECIFIED
 F43.12 POST-TRAUMATIC STRESS
DISORDER, CHRONIC
Solace Vital Signs: <<< solace_vital_signs(string[])
Happiness: 1/10. <<< solace_vital_signs.[*]
Anxiety; Stress: 5/10. <<< solace_vital_signs.[*]
Suicidal Thoughts: 4/10. <<< solace_vital_signs.[*]
Depression: 7/10. <<< solace_vital_signs.[*]
Energy Level: 4/10. <<< solace_vital_signs.[*]
Sleep quality: 3/10. <<< solace_vital_signs.[*]
Impulsivity: 5/10. <<< solace_vital_signs.[*]
Mania: 2/10. <<< solace_vital_signs.[*]
Psychotic symptoms: 4/10. <<< psychotic_symptoms(string[*]), psychotic_symptoms.[*] = 4/10
Hours of Sleep at Night: 5. <<< solace_vital_signs.[*]
MEASUREMENTS: Height: 55.00 in.<<< solace_vital_signs.[*]
Weight: 145 lbs. BMI: 33.7. The
patient's waist circumference is: 35
inches. <<< solace_vital_signs.[*]
Current Medications: <<< current_medications(string[])
Seroquel, 100 mg, HS
Paxil, 10 mg, QD
Wellbutrin XL, 300 mg, QAM
trazodone, 50 mg, BID
sertraline, 100 mg, QD
Xanax, 1 mg, TID
Zoloft, 100 mg, QAM
Klonopin, 0.5 mg, QD 
Important reactions to old meds: 2
Side Effect(s) / concerns with 
current meds: Denies SE. <<< current_medications.[*]
BEHAVIORAL / RELATIONSHIP GOALS: Goal 1: N/A: Domain not applicable at this time. 
Provider to reevaluate next session.
EMOTIONAL GOALS: Goal 1: FEAR/ANXIETY: Client will reduce overall frequency, 
intensity, and duration of anxiety symptoms to improve daily functioning. Date Created:
11/2/2022. Severity: Mild. Would like patient to be improved by 25%. Time to
Resolution: 6 months. Objective: Learn/demonstrate understanding of
Fight/Flight/Freeze distress.
Learn/demonstrate 2-3 mindfulness techniques to manage symptoms. Interventions:
Client to attend regular medication management appointments and take prescriptions
as prescribed.
Client to attend therapy sessions as prescribed.
INTELLECTUAL / MENTAL GOALS: Goal 1: N/A: Domain not applicable at this time. 
Provider to reevaluate next session.
PERSONAL GOALS: Goal 1: N/A: Domain not applicable at this time. Provider to 
reevaluate next session.
COMPLETED GOALS / ACHIEVEMENT: <<< null
RISK ASSESSMENT THIS VISIT: <<< risk_assessment(string[*])
2 Continues to have risks inherent to disease state.
Co-morbid substance use and abuse increases risk.
Prior history of suicide attempts.
Poor adherence to treatment recommendations.
Co-morbid substance use and abuse increases risk. 
OBJECTIVE TESTING RESULTS: 2 <<< risk_assessment.[*] 

LAB MONITORING: N/A <<< lab_monitoring(string[*])
PCP monitors and client will notify Solace of any abnormal results. <<< lab_monitoring.[*] = PCP monitors and client will notify Solace of any abnormal results.

REFERRALS: 
Psychotherapy. 
THERAPY: 
No therapy 
FOLLOW-UP / TREATMENT PLAN REVIEW:  
Appt made for 4 weeks.
Continue current prescribed treatment with current NP.
Medication management and psychotherapeutic interventions as needed (PRN).
Prescribed Treatment: Continue current prescribed therapy.
Electronically Signed: CHAUDHRY TANVEERon 05/15/2024License: ME85148
PATIENT NAME: Amorette Test
AGE: 27 years  SEX: Female
DOB: 12/26/1996
17222 HOSPITAL BLVD STE 120
BROOKSVILLE, FL 34601-8925
 Phone: (352) 678-5550 Fax: (352) 678-5551
Page 3 of 4Client has been educated on risks
associated with long term
benzodiazepine use, increased risks
in the elderly, and risks associated
with abrupt discontinuation.
Encouraged client to decrease
reliance on medication and use
other coping skills when possible.
Client was educated on effects
stimulants can have on anxiety and
quality of sleep.
Psychiatric Medication History: <<< psychiatric_med_history(string[])
Prozac, Celexa, Lexapro, Zoloft,
Viibryd, Paxil, Luvox, Effexor,
Prestiq, Cymbalta, Fetzima,
Remeron, Wellbutrin, Norpramine
(Disip), Pamelor (Nortrip), Vivactil
(Protryp), Trazodone, Emsam,
Nardil, Parnate, Trintellix, Lyrica,
Lithium, Depakote, Lamictal,
Tegretol/Trileptal, Neurontin,
Topomax, Keppra, Enlavil (Amitrip),
Anafranil (Clomipr), Doxepin
(Sinequan), Tofranil (Imipr),
Clozaril, Risperdal, Zyprexa,
Seroquel, Geodon, Abilify, Invega,
Saphris, Latuda, Fanapt, Rexulti,
Vraylar, Naplazid, Ingrezza,
Austedo, Trilafon, Haldol,
Thorazine, Prolixin, Orap
(Pimozide), Prazosin, Restoril,
Lunesta, Ambien, Propranolol,
Clonidine, Chantix, Naltrexone,
Campral, Antabuse, Suboxone,
Methadone, Vistaril, Buspar, Xanax,
Ativan, Klonopin, Librium, Valium,
Strattera, Ritalin, Adderall,
Vyvanse, Focalin, Provigil, Nuvigil,
Aricept, Namenda, Exelon,
Galantamine, Prolixin, Haldol,
Risperdal, Invega, Abilify, Aristada,
Vivitrol, Ketamine, Spravato,
Vitamin E, Melatonin, Diplin, NAC,
Nerve Tonic, Calm Forte, <<< psychiatric_med_history.[*]
Other Treatments: 2 <<< other_treatments(string[*]), other_treatments.[*]
PATIENT NAME: Amorette Test
AGE: 27 years  SEX: Female
DOB: 12/26/1996
17222 HOSPITAL BLVD STE 120
BROOKSVILLE, FL 34601-8925
 Phone: (352) 678-5550 Fax: (352) 678-5551
Page 4 of 4Patient has a history of substance
use.
Patient has a history of substance
use. <<< history_substance_use(string[]), history_substance_use.[*] 
Historical Drug Use (if any): <<< historical_drug_use(string[])
Caffeine, Nicotine, Alcohol, THC,
Prescription, Cocaine, Opioids,
Amphetamine, Meth, Ecstasy,
Ketamine, PCP, Mushrooms,
Inhalants, Steroids, LSD, GHB, DXM,
Current Drug Use (if any): Caffeine,
Nicotine, Alcohol, THC,
Prescription, Cocaine, Opioids,
Amphetamine, Meth, Ecstasy,
Ketamine, PCP, Mushrooms,
Inhalants, Steroids, LSD, LSD, DXM,  <<< historical_drug_use.[*]
Past IVDA: Yes <<< past_idva(string[]), past_idva.[*]
Present: Yes  <<< present_idva(string[]), present_idva.[*]
The patient has a history of
withdrawal. <<< withdrawal_history(string[]), <<< withdrawal_history.[*] 
Patient has a history of seizures. <<< seizure_history(string[]), <<< seizure_history.[*]
Patient has a history of OD.<<< od_history(string[]), <<< od_history.[*]
UDS Results History: 2.
Pattern of use: 2.
Consequences: 2.
Treatment: 2.
Comments: 2.
Stage of Change: 2.
New Medication Recommendations: <<< new_med_recommendation(string[*])
Continue meds as prescribed. <<< new_med_recommendation.[*]
Client has been educated on
treatment options, medications,
target symptoms, risks, benefits,
SE, what to monitor for, and
interactions. Client verbalized
understanding of education
provided. 
Current Allergies: <<< current_allergies(string[])
No allergies on file <<< current_allergies[*]

Signed By: Tanveer Chaudhry, MD 05/15/2024 03:41 PM 

"""