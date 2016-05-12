from django.apps import apps
from django import forms

"""
    Application: HealthNet
    File: medicalHistory/forms.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the forms for the medical history
"""
medHistory = apps.get_model('base', 'MedicalHistory')


class MedicalHistoryForm(forms.ModelForm):
    histWeight = forms.IntegerField(label='Weight', required=True, help_text='lbs',
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    histHeight = forms.IntegerField(label='Height', required=True, help_text='Inches',
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    histAge = forms.IntegerField(label='Age', required=True, help_text='years',
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    histCancer = forms.BooleanField(label='Cancer', initial=False, required=False)
    histAlcoholism = forms.BooleanField(label='Alcoholism', initial=False, required=False)
    histUlcers = forms.BooleanField(label='Ulcers', initial=False, required=False)
    histCholesterol = forms.BooleanField(label='Cholesterol', initial=False, required=False)
    histAsthma = forms.BooleanField(label='Asthma', initial=False, required=False)
    histHeartTrouble = forms.BooleanField(label='Heart Trouble', initial=False, required=False)
    histKidneyDisease = forms.BooleanField(label='Kidney Disease', initial=False, required=False)
    histSickleCellAnemia = forms.BooleanField(label='Sickle Cell Anemia', initial=False, required=False)
    histTuberculosis = forms.BooleanField(label='Tuberculosis', initial=False, required=False)
    histHiv = forms.BooleanField(label='HIV/AIDS', initial=False, required=False)
    histEmphysema = forms.BooleanField(label='Emphysema', initial=False, required=False)
    histHighBloodPressure = forms.BooleanField(label='High Blood Pressure', initial=False, required=False)
    histBleedingDisorder = forms.BooleanField(label='Bleeding Disorder', initial=False, required=False)
    histLiverDisorder = forms.BooleanField(label='Liver Disorder', initial=False, required=False)
    histBirthDefects = forms.BooleanField(label='Birth Defects', initial=False, required=False)
    histStroke = forms.BooleanField(label='Stroke', initial=False, required=False)
    histArthritis = forms.BooleanField(label='Arthritis', initial=False, required=False)
    histDiabetes = forms.BooleanField(label='Diabetes', initial=False, required=False)
    histHeartAttack = forms.BooleanField(label='Heart Attack', initial=False, required=False)
    histGout = forms.BooleanField(label='Gout', initial=False, required=False)
    histSystems = forms.CharField(label='Please Explain', required=False)
    histSystemsOther = forms.CharField(label='Other', required=False, 
      widget=forms.TextInput(attrs={'class': 'form-control'}))

    histSurgeryTonsils = forms.BooleanField(label='Tonsils', initial=False, required=False)
    histSurgeryBreast = forms.BooleanField(label='Breast', initial=False, required=False)
    histSurgeryAppendix = forms.BooleanField(label='Appendix', initial=False, required=False)
    histSurgeryUterus = forms.BooleanField(label='Uterus', initial=False, required=False)
    histSurgeryGallBladder = forms.BooleanField(label='Gall Bladder', initial=False, required=False)
    histSurgeryOvaries = forms.BooleanField(label='Ovaries', initial=False, required=False)
    histSurgeryStomach = forms.BooleanField(label='Stomach', initial=False, required=False)
    histSurgerySmallIntestine = forms.BooleanField(label='Small Intestine', initial=False, required=False)
    histSurgeryProstate = forms.BooleanField(label='Prostate', initial=False, required=False)
    histSurgeryColon = forms.BooleanField(label='Colon', initial=False, required=False)
    histSurgeryThyroid = forms.BooleanField(label='Thyroid', initial=False, required=False)
    histSurgeryKidney = forms.BooleanField(label='Kidney', initial=False, required=False)
    histSurgeryHernia = forms.BooleanField(label='Hernia', initial=False, required=False)
    histSurgeryHeart = forms.BooleanField(label='Heart', initial=False, required=False)
    histSurgeryPacemaker = forms.BooleanField(label='Pacemaker', initial=False, required=False)
    histSurgeryJointReplace = forms.BooleanField(label='Joint Replacement', initial=False, required=False)
    histSurgeryExtremities = forms.BooleanField(label='Extremities', initial=False, required=False)
    histSurgeryOther = forms.CharField(label='Any other surgeries (What kind)', required=False, 
      widget=forms.TextInput(attrs={'class': 'form-control'}))

    histAllergyPenicillin = forms.BooleanField(label='Penicillin', initial=False, required=False)
    histAllergySulfa = forms.BooleanField(label='Sulfa', initial=False, required=False)
    histAllergyMetal = forms.BooleanField(label='Metal', initial=False, required=False)
    histAllergyNone = forms.BooleanField(label='None', initial=False, required=False)
    histAllergyOther = forms.CharField(label='Other', required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    histAllergyFoodOther = forms.CharField(label='Other Food Allergies', required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))

    histMedicationOther = forms.CharField(label='Other Medication Allergies', required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))

    histConditionShortBreath = forms.BooleanField(label='Short Breath', initial=False, required=False)
    histConditionChestPain = forms.BooleanField(label='Chest Pain', initial=False, required=False)
    histConditionWeightLoss = forms.BooleanField(label='Weight Loss', initial=False, required=False)
    histConditionConstipation = forms.BooleanField(label='Constipation', initial=False, required=False)
    histConditionFever = forms.BooleanField(label='Fever', initial=False, required=False)
    histConditionVision = forms.BooleanField(label='Vision', initial=False, required=False)
    histConditionHeadache = forms.BooleanField(label='Headache', initial=False, required=False)
    histConditionUrination = forms.BooleanField(label='Urination', initial=False, required=False)
    histConditionNumbness = forms.BooleanField(label='Numbness', initial=False, required=False)

    histTobaccoCigarettes = forms.BooleanField(label='Cigarettes', initial=False, required=False)
    histTobaccoFrequency = forms.IntegerField(label='Frequencies', help_text='Amount/Day', required=False, initial=0)
    histTobaccoDuration = forms.IntegerField(label='Duration', help_text='Time since starting', required=False,
                                             initial=0)
    histTobaccoOther = forms.CharField(label='Other Tobacco Use', required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))

    histAlcoholBeer = forms.IntegerField(label='Beer/Wine', help_text='x a week', required=False, initial=0)
    histAlcoholShots = forms.IntegerField(label='Shots/Liquor', help_text='x a week', required=False, initial=0)
    histDrugOther = forms.CharField(label='Other Drug use', required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))

    histFamilyCancer = forms.BooleanField(label='Cancer', initial=False, required=False)
    histFamilyDiabetes = forms.BooleanField(label='Diabetes', initial=False, required=False)
    histFamilyRheumatoidArthritis = forms.BooleanField(label='Rheumatoid Arthritis', initial=False, required=False)
    histFamilyArthritis = forms.BooleanField(label='Arthritis', initial=False, required=False)
    histFamilyGout = forms.BooleanField(label='Gout', initial=False, required=False)
    histFamilyBleeding = forms.BooleanField(label='Bleeding', initial=False, required=False)
    histFamilySickleCellAnemia = forms.BooleanField(label='Sickle Cell Anemia', initial=False, required=False)
    histFamilyHeartDisease = forms.BooleanField(label='Heart Disease', initial=False, required=False)
    histFamilyOther = forms.CharField(label='Other', required=False)

    relationshipChoices = [('Single', 'Single'),
                           ('Married', 'Married'),
                           ('Divorced', 'Divorced'),
                           ('Widowed', 'Widowed')]
    histRelationship = forms.ChoiceField(choices=relationshipChoices, label='Relationship')
    workChoices = [('Employed', 'Employed'),
                   ('Unemployed', 'Unemployed'),
                   ('Disabled', 'Disabled'),
                   ('Retired', 'Retired'),
                   ('Student', 'Student')]
    histWork = forms.ChoiceField(choices=workChoices, label='Work Status', required=True)
    histWorkExplain = forms.CharField(label='Employed - Doing what', required=False)

    histPrimaryName = forms.CharField(label='Primary care provider', required=True)
    histPrimaryNumber = forms.IntegerField(label='Physician Number', required=True)

    class Meta:
        model = medHistory
        fields = ('histWeight', 'histHeight', 'histAge',
                  'histCancer', 'histAlcoholism', 'histUlcers',
                  'histCholesterol', 'histAsthma', 'histHeartTrouble',
                  'histKidneyDisease', 'histSickleCellAnemia', 'histTuberculosis',
                  'histHiv', 'histEmphysema', 'histHighBloodPressure',
                  'histBleedingDisorder', 'histLiverDisorder', 'histBirthDefects',
                  'histStroke', 'histArthritis', 'histDiabetes',
                  'histHeartAttack', 'histGout', 'histSystems',
                  'histSystemsOther', 'histSurgeryTonsils', 'histSurgeryBreast',
                  'histSurgeryAppendix', 'histSurgeryUterus', 'histSurgeryGallBladder',
                  'histSurgeryOvaries', 'histSurgeryStomach', 'histSurgerySmallIntestine',
                  'histSurgeryProstate', 'histSurgeryColon', 'histSurgeryThyroid',
                  'histSurgeryKidney', 'histSurgeryHernia', 'histSurgeryHeart',
                  'histSurgeryPacemaker', 'histSurgeryJointReplace', 'histSurgeryExtremities',
                  'histSurgeryOther', 'histAllergyPenicillin', 'histAllergySulfa',
                  'histAllergyMetal', 'histAllergyNone', 'histAllergyOther',
                  'histAllergyFoodOther', 'histMedicationOther', 'histConditionShortBreath',
                  'histConditionChestPain', 'histConditionWeightLoss', 'histConditionConstipation',
                  'histConditionFever', 'histConditionVision', 'histConditionHeadache',
                  'histConditionUrination', 'histConditionNumbness', 'histTobaccoCigarettes',
                  'histTobaccoFrequency', 'histTobaccoDuration', 'histTobaccoOther',
                  'histAlcoholBeer', 'histAlcoholShots', 'histDrugOther',
                  'histFamilyCancer', 'histFamilyDiabetes', 'histFamilyRheumatoidArthritis',
                  'histFamilyArthritis', 'histFamilyGout', 'histFamilyBleeding',
                  'histFamilySickleCellAnemia', 'histFamilyHeartDisease', 'histFamilyOther',
                  'histRelationship', 'histWork', 'histWorkExplain',
                  'histPrimaryName', 'histPrimaryNumber'
                  )
