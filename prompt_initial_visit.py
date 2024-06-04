# Parse people's names to last name and first name and title. 

_prompt = """
You analyze patient medical records to export them into a JSON format. 
I will present you with a patient medical record and describe the individual JSON objects and properties with <<<. 
You then create a JSON object from another patient medical record. 
Parse addresses. 
Format phone with dashes and no parens. 
Format dates as YYYY-MM-DD. 
Parse Medications. 
Include Risk Assessment.
Include Lab Monitoring.
Do NOT include Treatment plans.
Do NOT include Follow up under Treatment plans.
Do NOT include exam.

Apply the following schema to all JSON results.  Enforce the schema strictly, only keys found in the schema:

{
  "type": "object",
  "properties": {
    "patient": {
      "type": "object",
      "properties": {
        "first_name": {
          "type": "string"
        },
        "last_name": {
          "type": "string"
        },
        "age": {
          "type": "number"
        },
        "sex": {
          "type": "string"
        },
        "dob": {
          "type": "string"
        },
        "phone": {
          "type": "string"
        },
        "address": {
          "type": "object",
          "properties": {
            "street": {
              "type": "string"
            },
            "city": {
              "type": "string"
            },
            "state": {
              "type": "string"
            },
            "zip": {
              "type": "string"
            }
          },
          "required": [
            "street",
            "city",
            "state",
            "zip"
          ]
        }
      },
      "required": [
        "first_name",
        "last_name",
        "age",
        "sex",
        "dob",
        "phone",
        "address"
      ]
    },
    "date_of_service": {
      "type": "object",
      "properties": {
        "chart_num": {
          "type": "string"
        },
        "date_of_service": {
          "type": "string"
        }
      },
      "required": [
        "chart_num",
        "date_of_service"
      ]
    },
    "provider": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "address": {
          "type": "object",
          "properties": {
            "street": {
              "type": "string"
            },
            "city": {
              "type": "string"
            },
            "state": {
              "type": "string"
            },
            "zip": {
              "type": "string"
            }
          },
          "required": [
            "street",
            "city",
            "state",
            "zip"
          ]
        },
        "phone": {
          "type": "string"
        },
        "fax": {
          "type": "string"
        }
      },
      "required": [
        "name",
        "address",
        "phone",
        "fax"
      ]
    },
    "visit_diagnosis": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "solace_vital_signs": {
      "type": "object",
      "properties": {
        "Happiness": {
          "type": "string"
        },
        "Anxiety_Stress": {
          "type": "string"
        },
        "Suicidal_Thoughts": {
          "type": "string"
        },
        "Depression": {
          "type": "string"
        },
        "Energy_Level": {
          "type": "string"
        },
        "Sleep_quality": {
          "type": "string"
        },
        "Impulsivity": {
          "type": "string"
        },
        "Mania": {
          "type": "string"
        },
        "Psychotic_Symptoms": {
          "type": "string"
        },
        "Hours_of_Sleep_at_Night": {
          "type": "string"
        },
        "Height": {
          "type": "string"
        },
        "Weight": {
          "type": "string"
        },
        "BMI": {
          "type": "string"
        },
        "Waist_Circumference": {
          "type": "string"
        }
      },
      "required": [
        "Happiness",
        "Anxiety_Stress",
        "Suicidal_Thoughts",
        "Depression",
        "Energy_Level",
        "Sleep_quality",
        "Impulsivity",
        "Mania",
        "Psychotic_Symptoms",
        "Hours_of_Sleep_at_Night",
        "Height",
        "Weight",
        "BMI",
        "Waist_Circumference"
      ]
    },
    "visit_type": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "supervising_physician": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "chief_complaint": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "history_present_illness": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "target_symptoms": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "social_history": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "disability": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "current_medications": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "psychiatric_med_history": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "sexuality": {
      "type": "object",
      "properties": {
        "instances_of_sexual_abuse_rape": {
          "type": "boolean"
        },
        "sexually_active": {
          "type": "boolean"
        },
        "sexual_dysfunction_pain": {
          "type": "boolean"
        },
        "no_sexuality_issues_reported": {
          "type": "boolean"
        },
        "details": {
          "type": "number"
        },
        "sexual_orientation": {
          "type": "string"
        },
        "previous_sexual_partners": {
          "type": "number"
        },
        "contraceptive_types_used": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "comments": {
          "type": "number"
        }
      },
      "required": [
        "instances_of_sexual_abuse_rape",
        "sexually_active",
        "sexual_dysfunction_pain",
        "no_sexuality_issues_reported",
        "details",
        "sexual_orientation",
        "previous_sexual_partners",
        "contraceptive_types_used",
        "comments"
      ]
    },
    "military_service": {
      "type": "object",
      "properties": {
        "served": {
          "type": "boolean"
        },
        "branch": {
          "type": "string"
        },
        "rank": {
          "type": "string"
        },
        "years_served": {
          "type": "string"
        },
        "status": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "comments": {
          "type": "number"
        }
      },
      "required": [
        "served",
        "branch",
        "rank",
        "years_served",
        "status",
        "comments"
      ]
    },
    "education": {
      "type": "object",
      "properties": {
        "highest_level": {
          "type": "string"
        },
        "grades": {
          "type": "string"
        },
        "experienced_difficulties": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "received_special_education": {
          "type": "boolean"
        },
        "comments": {
          "type": "number"
        }
      },
      "required": [
        "highest_level",
        "grades",
        "experienced_difficulties",
        "received_special_education",
        "comments"
      ]
    },
    "legal_history": {
      "type": "object",
      "properties": {
        "juvenile_legal_history": {
          "type": "boolean"
        },
        "juvenile_arrests_age": {
          "type": "number"
        },
        "juvenile_time_incarcerated": {
          "type": "number"
        },
        "arrested_as_adult": {
          "type": "boolean"
        },
        "pending_cases": {
          "type": "boolean"
        },
        "pending_cases_info": {
          "type": "number"
        },
        "history": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "past_probations": {
          "type": "boolean"
        },
        "on_probation": {
          "type": "boolean"
        }
      },
      "required": [
        "juvenile_legal_history",
        "juvenile_arrests_age",
        "juvenile_time_incarcerated",
        "arrested_as_adult",
        "pending_cases",
        "pending_cases_info",
        "history",
        "past_probations",
        "on_probation"
      ]
    },
    "religion": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "housing_status": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "firearms": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "prev_psych_history": {
      "type": "object",
      "properties": {
        "age_symptoms_began": {
          "type": "number"
        },
        "attempt_to_receive_care_age": {
          "type": "number"
        },
        "age_reason_feel_afraid_anxious": {
          "type": "number"
        },
        "symptoms_resulted": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "growing_up_experience": {
          "type": "number"
        },
        "witnessed_events": {
          "type": "number"
        },
        "age_first_death_experience": {
          "type": "number"
        },
        "last_time_felt_normal": {
          "type": "number"
        },
        "psychiatric_diagnosis": {
          "type": "array",
          "items": [
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "number"
            }
          ],
          "additionalItems": false
        },
        "treatment_modalities": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "suicide_history": {
          "type": "object",
          "properties": {
            "lifetime_attempts": {
              "type": "number"
            },
            "last_attempt_date": {
              "type": "string"
            },
            "method_used": {
              "type": "string"
            },
            "triggers": {
              "type": "number"
            },
            "lifetime_hospitalizations": {
              "type": "number"
            },
            "last_hospitalization_date": {
              "type": "string"
            },
            "outcomes": {
              "type": "string"
            },
            "comments": {
              "type": "number"
            }
          },
          "required": [
            "lifetime_attempts",
            "last_attempt_date",
            "method_used",
            "triggers",
            "lifetime_hospitalizations",
            "last_hospitalization_date",
            "outcomes",
            "comments"
          ]
        }
      },
      "required": [
        "age_symptoms_began",
        "attempt_to_receive_care_age",
        "age_reason_feel_afraid_anxious",
        "symptoms_resulted",
        "growing_up_experience",
        "witnessed_events",
        "age_first_death_experience",
        "last_time_felt_normal",
        "psychiatric_diagnosis",
        "treatment_modalities",
        "suicide_history"
      ]
    },
    "family_psych_history": {
      "type": "object",
      "properties": {
        "psychiatric_problems": {
          "type": "boolean"
        },
        "history": {
          "type": "object",
          "properties": {
            "Alcohol_Abuse": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "Anger": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "Anxiety": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "Bipolar_Disorder": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "Depression": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "Post-traumatic_Stress": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "Schizophrenia": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "Substance_Abuse": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          "required": [
            "Alcohol_Abuse",
            "Anger",
            "Anxiety",
            "Bipolar_Disorder",
            "Depression",
            "Post-traumatic_Stress",
            "Schizophrenia",
            "Substance_Abuse"
          ]
        }
      },
      "required": [
        "psychiatric_problems",
        "history"
      ]
    },
    "medical_history": {
      "type": "object",
      "properties": {
        "pertinent_history": {
          "type": "boolean"
        },
        "history": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "required": [
        "pertinent_history",
        "history"
      ]
    },
    "surgical_history": {
      "type": "object",
      "properties": {
        "previous_surgeries": {
          "type": "boolean"
        },
        "surgeries": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "required": [
        "previous_surgeries",
        "surgeries"
      ]
    },
    "risk_assessment": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "lab_monitoring": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "patient",
    "date_of_service",
    "provider",
    "visit_diagnosis",
    "solace_vital_signs",
    "visit_type",
    "supervising_physician",
    "chief_complaint",
    "history_present_illness",
    "target_symptoms",
    "social_history",
    "disability",
    "current_medications",
    "psychiatric_med_history",
    "sexuality",
    "military_service",
    "education",
    "legal_history",
    "religion",
    "housing_status",
    "firearms",
    "prev_psych_history",
    "family_psych_history",
    "medical_history",
    "surgical_history",
    "risk_assessment",
    "lab_monitoring"
  ]
}

>>> Example patient medical record:

PATIENT NAME: <<< patient (object)
Amorette Test <<< patient.first_name = Amorette, patient_last_name = Test
AGE: 27 years  SEX: Female
DOB: 12/26/1996
PHONE: (352) 678-8460
ADDRESS: 4800 Rowan Rd
 New Port Richey, FL 34653
CHART NUMBER: <<< date_of_service (object)
09876 <<< date_of_service.chart_num
DATE OF SERVICE: 05/15/2024 <<< date_of_service.date_of_service
PROVIDER:   <<< provider (object)
Tanveer Chaudhry, MD
17222 HOSPITAL BLVD STE 120
BROOKSVILLE, FL 34601-8925
 Phone: (352) 678-5550 Fax: (352) 678-5551

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
Solace Vital Signs: <<< solace_vital_signs(string[])
Happiness: 1/10. <<< solace_vital_signs.[*]
Anxiety; Stress: 5/10. <<< solace_vital_signs.[*]
Suicidal Thoughts: 4/10. <<< solace_vital_signs.[*]
Depression: 7/10. <<< solace_vital_signs.[*]
Energy Level: 4/10. <<< solace_vital_signs.[*]
Sleep quality: 3/10. <<< solace_vital_signs.[*]
Impulsivity: 5/10. <<< solace_vital_signs.[*]
Mania: 2/10. <<< solace_vital_signs.[*]
Psychotic Symptoms: 4/10. <<< psychotic_symptoms(string[*]), psychotic_symptoms.[*] = 4/10
Hours of Sleep at Night: 5. INITIAL VISIT NOTE: <<< solace_vital_signs.[*]
MEASUREMENTS: Height: 55.00 in.<<< solace_vital_signs.[*]
Weight: 145 lbs. BMI: 33.7. The
patient's waist circumference is: 35
inches. <<< solace_vital_signs.[*]

VISIT TYPE: <<< visit_type (string[])
An in-person visit was conducted. <<< visit_type.[*] = An in-person visit was conducted.
SUPERVISING PHYSICIAN: <<< supervising_physician(string[])
Office visit rendered today under the credentialed supervision of: N/A: Rendering as
self.. <<< supervising_physician.[*]
CHIEF COMPLAINT: <<< chief_complaint(string[])
Depression, PTSD  <<< chief_complaint.[*]

HISTORY OF PRESENT ILLNESS: <<< history_present_illness(string[])
2
INTERVAL SENTIANAL EVENTS: 2 <<< history_present_illness.[*]

TARGET SYMPTOMS: <<< target_symptoms(string[])
Maintenance: Will focus on maintaining stability with medication compliance and
monitoring for signs and symptoms of mental illness during medication management
follow-up appointments. <<< target_symptoms.[*]

SOCIAL HISTORY: <<< social_history(string[])
MARITAL STATUS:
Current Marital Status: Married.
Number of pervious marriages: 2
Name of spouse/significant other: 2.
Additional comments about marriage: 2 
CHILDREN:
Biological Children: 2.
Stepchildren: 2.
Adopted Children: 2.
Foster Children: 2. Special Needs Children: 2.
Ages of Children: 2.
Children Comments: 2
OCCUPATION:
The patient is employed.
Current Employer: 2.
Current Occupation: 2.
Current School: 2.
Occupation Comments: 2 <<< social_history.[*]

DISABILITY: <<< disability(string[])
Disability status: No Yes
Are you planning on filing for disability? No Yes
Have you filed for disability? No Yes
Type of disability? Medical Psychiatric
Do you receive SSID (Social Security Disability? No Yes
Do you receive private disability insurance? No Yes
How many years have you been disabled? 2 years.
What is the nature of your disability? 2
Additional comments about disability: 2 <<< disability.[*]

Current Medications: <<< current_medications(string[])
Seroquel, 100 mg, HS
Paxil, 10 mg, QD
Wellbutrin XL, 300 mg, QAM
trazodone, 50 mg, BID
sertraline, 100 mg, QD
Xanax, 1 mg, TID
Zoloft, 100 mg, QAM
Klonopin, 0.5 mg, QD
Important reactions to old meds: 2 <<< current_medications.[*] = Important reactions to old meds: 2
Side Effect(s) / concerns with
current meds: Denies SE. <<< current_medications.[*] = Side Effect(s) / concerns with
current meds: Denies SE

Client has been educated on risks
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
Viibryd, Paxil, Buspar, Xanax, <<< psychiatric_med_history.[*]
Other Treatments: 2 <<< psychiatric_med_history.[*]
Patient has a history of substance
use.
Patient has a history of substance
use. <<< psychiatric_med_history.[*]
Historical Drug Use (if any):
Caffeine, Nicotine, Alcohol, THC,
Prescription, Cocaine, Opioids,
Amphetamine, Meth, Ecstasy,
Ketamine, PCP, Mushrooms,
Inhalants, Steroids, LSD, GHB, DXM, <<< psychiatric_med_history.[*] = Historical Drug Use (if any):
Current Drug Use (if any): Caffeine,
Nicotine, Alcohol, THC,
Prescription, Cocaine, Opioids, 
Ketamine, PCP, Mushrooms,
Inhalants, Steroids, LSD, LSD, DXM, <<< psychiatric_med_history.[*] = Current Drug Use (if any):
Past IVDA: Yes <<< psychiatric_med_history.[*] = Past IVDA: Yes
Present: Yes <<< psychiatric_med_history.[*] = Present: Yes
The patient has a history of
withdrawal. <<< psychiatric_med_history.[*]
Patient has a history of seizures. <<< psychiatric_med_history.[*]
Patient has a history of OD. <<< psychiatric_med_history.[*]
UDS Results History: 2. <<< psychiatric_med_history.[*]
Pattern of use: 2. <<< psychiatric_med_history.[*]
Consequences: 2. <<< psychiatric_med_history.[*]
Treatment: 2. <<< psychiatric_med_history.[*]
Comments: 2. <<< psychiatric_med_history.[*]
Stage of Change: 2. <<< psychiatric_med_history.[*]

SEXUALITY: <<< sexuality(string[])
Patient reports instances of sexual abuse / rape.
Patient is sexually active.
Patient has sexual dysfunction or pain.
No sexuality issues reported.
Details: 2
Patient's sexual orientation: Heterosexual.
Number of previous sexual partners: 2.
Contraceptive type used: Oral.
Contraceptive type used: Barrier.
Contraceptive type used: IUD.
Contraceptive type used: Natural Methods.
Contraceptive type used: Implants.
Contraceptive type used: Condoms.
Contraceptive type used: Diaphragm.
Patient states they do not use contraceptives.
Additional comments about sexuality: 2 <<< sexuality(string[])

MILITARY SERVICE: <<< military_service(string[*])
Have you ever served in the armed forces? No Yes
Branch of Service: Army.
Patient obtained the rank of: 2.
Patient served for: 2 years.
Military Status: Active.
Military Status: Medical Discharge.
Military Status: Disciplinary Action.
Additional comments about military status: 2 <<< military_service.[*]

EDUCATION: <<< education(string[*])
The patient's highest level of education obtained is: Completed elementary school.
The patient states their grades in school were A's. The patient experienced attention
difficulties. The patient experienced behavioral difficulties. The patient received special
education services.
Additional Schooling Comments: 2 <<< education.[*]

LEGAL HISTORY: <<< legal_history(string[])
The patient does not have juvenile legal history. Patients age of juvenile arrest(s): 2.
Juvenile Time Incarcerated: 2. Patient has been arrested as an adult. The state the
The patient does not have any pending cases.
The patient has pending cases.
Pending Cases Info: 2
The patient has had a DUI/DWI.
Patient has been charged with Public Intoxication.
The patient has had past probation(s).
The patient is currently on probation. <<< legal_history.[*]

New Medication Recommendations: <<< IGNORE
Continue meds as prescribed. <<< IGNORE

Client has been educated on
treatment options, medications,
target symptoms, risks, benefits,
SE, what to monitor for, and
interactions. Client verbalized
understanding of education
provided. <<< IGNORE

Current Allergies: <<< current_allergies(string[])
No allergies on file <<< current_allergies[*]

Visit CPT: <<< IGNORE
 DISORDER, UNSPECIFIED
 F43.12 POST-TRAUMATIC STRESS
DISORDER, CHRONIC 


RELIGION: <<< religion(string[])
Religious preference: Catholic. <<< religion.[*] = Religious preference: Catholic
Religious Preference: 2. <<< religion.[*] = Religious Preference: 2
Religion is not important to the patient. <<< religion.[*]
Religion is somewhat important to the patient. <<< religion.[*]
Religion is very important to the patient. <<< religion.[*]
Addition comments pertaining to religion: 2 <<< religion.[*] = Addition comments pertaining to religion: 2

HOUSING STATUS: <<< housing_status(string[])
Current Housing Status: Independent. <<< housing_status.[*] = Current Housing Status: Independent
Current Housing Status: Immediate Family. <<< housing_status.[*] = Current Housing Status: Immediate Family
Current Housing Status: Extended Family. <<< housing_status.[*] = Current Housing Status: Extended Family
Current Housing Status: Homeless. <<< housing_status.[*] = Current Housing Status: Homeless
Housing Type: House. <<< housing_status.[*] = Housing Type: House
Housing Type: Apartment. <<< housing_status.[*] = Housing Type: Apartment
Housing Type: Trailer. <<< housing_status.[*] = Housing Type: Trailer
Housing Type: Section 8. <<< housing_status.[*]
Patient states there are 2 people living in the same house. <<< housing_status.[*]
Additional housing comments: 2 <<< housing_status.[*]

FIREARMS: <<< firearms(string[])
Do you possess any kind of firearms? The patient does not possess any firearms. The
patient possesses firearms. Patient refuses to answer if they posses firearms or not.<<< firearms.[*]
Kind of firearms in the patient's possession: 2<<< firearms.[*]
Additional comments about their firearms: 2 <<< firearms.[*]

PREVIOUS PSYCHIATRIC HISTORY: <<< prev_psych_history(string[])
Age mental health symptoms first began: 2. <<< prev_psych_history.[*]
Age the patient first made an attempt to receive psychiatric care: 2. <<< prev_psych_history.[*]
Age/reason for first feel afraid, anxious or unsafe.  2. Symptoms that resulted from the
above experience: Addiction, Anxiety, Depression, Post-Traumatic Stress Disorder,
Personality Disorder(s), Suicidal Behavior, Self Injurious Behavior, Severe mental health
symptoms left untreated, Impulsive Behavior, Rebellious Behavior, Self Esteem Issues,
Introversion, Extroversion, Promiscuity, None Reported <<< prev_psych_history.[*]
What was it like growing up: 2 <<< prev_psych_history.[*]
Did you witness any anger, poverty, trauma, abuse, or bullying? 2 <<< prev_psych_history.[*]
How old were you when you first experienced death? 2 <<< prev_psych_history.[*]
Looking back, when was the last time you felt normal and have you ever gone back to
feeling normal? 2 <<< prev_psych_history.[*]
Prior Psychiatric Diagnosis: Unknown, None Reported, Depression, Anxiety, Bipolar,
Bipolar, PTSD, Addiction, Dementia, Head Injury, Personality Disorder(s),
Developmental Disorder(s), 2
Previous Treatment Modalities: Outpatient, Only Inpatient, Partial Hospitalization,
Counseling, Intensive Outpatient, Drug Rehabilitation, Residential, None, <<< prev_psych_history.[*]
Suicide History:
Number of lifetime suicide attempts: 2.
Unknown number of suicide attempts.
No reported number of suicide attempts.
Date of last suicide attempt: 02/01/2001
Method used during suicide attempt: 2.
Triggers that caused suicide attempt(s): 2. <<< prev_psych_history.[*]
Number of lifetime psychiatric hospitalizations: 2. <<< prev_psych_history.[*]
Date of last psychiatric hospitalization: 02/01/2001 <<< prev_psych_history.[*]
Outcomes of past psychiatric care: Unknown - None Reported. Symptom
resolution/stabilization failure to stabilize reconstitution of functional capacity.
Significant  threat to self/others. Continued incapacity treatment resistance. <<< prev_psych_history.[*]
Comments: 2 <<< prev_psych_history.[*]


FAMILY PSYCHIATRIC HISTORY: <<< family_psych_history(string[*])
Patient denies any history of psychiatric family problems. Alcohol Abuse - Child, Alcohol
Abuse - Child, Alcohol Abuse - Parent, Alcohol Abuse - Sibling, Alcohol Abuse -
Grandparent, Anger - Child, Anger - Parent, Anger - Sibling, Anger - Grandparent,
Anxiety - Child, Anxiety - Parent, Anxiety - Sibling, Anxiety - Grandparent, Bipolar
Disorder - Child, Bipolar Disorder - Parent, Bipolar Disorder - Sibling, Bipolar Disorder -
Grandparent, Depression - Child, Depression - Parent, Depression - Sibling, Depression -
Grandparent, Post-traumatic Stress - Child, Post-traumatic Stress - Parent, Post-
traumatic Stress - Sibling, Post-traumatic Stress - Sibling, Schizophrenia - Child,
Schizophrenia - Parent, Schizophrenia - Sibling, Schizophrenia - Grandparent, Substance
Abuse - Child, Substance Abuse - Parent, Substance Abuse - Sibling, Substance Abuse -
Grandparent,
2  <<< family_psych_history.[*]

MEDICAL HISTORY: <<< medical_history(string[])
Patient denies any pertinent medical history. Alcohol Abuse - Child, AIDS / Related
Complex, Alcoholism, Anemia, Osteoarthritis, Rheumatoid Arthritis, Asthma,
Autoimmune Disorder, Back Pain, Bariatric Surgery Status, Cancer Type: 2, Chronic
Fatigue, Chronic Pain, Congenital Abnormality Type: 2, Congestive Heart Failure,
Contraceptives, COPD, Coronary Heart Disease, Cushings Syndrome, Diabetes Type I,
Diabetes Type II, Emphysema, Epilepsy, Fibromyalgia, Head Injury, Headaches
(frequent), Heart Attack, Hepatitis, Hypercholesterolemia, Hyperlipidemia,
Hypertension (Essential Primary), IBD (Inflammatory Bowel), IBS (Irritable Bowell
Syndrome), Kidney Disease, Liver Disease, Lupus, Lyme Disease, Menopause, Metabolic
Syndrome, Migraines, Multiple Sclerosis, Morbid Obesity, Obesity (30+ BMI),
Parkinson's, PCOS, Premenstrual Syndrome, Restless Leg Syndrome, RSD, Seizure
Disorder, Sleep Apnea, Stroke / Paralysis, Hyperthyroidism, Hypothyroidism,
Thyroidectomy,
22  <<< medical_history.[*]

SURGICAL HISTORY: <<< surgical_history(string[])
Patient denies any previous surgical history. Appendectomy, C-Section, Carpel Tunnel
Surgery, Cholesytectomy, Gastric Bypass, Heart Bypass, Hysterectomy, Joint
Replacement, Lap Band System, Tonsillectomy, Vasectomy,
2  <<< surgical_history.[*]

EXAM: <<< IGNORE
TREATMENT PLAN: <<< IGNORE

RISK ASSESSMENT THIS VISIT:  <<< risk_assessment(string[*])
2 Continues to have risks inherent to disease state.
Co-morbid substance use and abuse increases risk.
Prior history of suicide attempts.
Poor adherence to treatment recommendations.
Co-morbid substance use and abuse increases risk. <<< risk_assessment.[*]
OBJECTIVE TESTING RESULTS: 2 <<< risk_assessment.[*] = OBJECTIVE TESTING RESULTS: 2

LAB MONITORING: <<< lab_monitoring(string[*])
PCP monitors and client will notify Solace of any abnormal results. <<< lab_monitoring.[*] = PCP monitors and client will notify Solace of any abnormal results.

REFERRALS: <<< IGNORE
Psychotherapy.
THERAPY: <<< IGNORE
No therapy
FOLLOW-UP / TREATMENT PLAN REVIEW: <<< IGNORE

"""