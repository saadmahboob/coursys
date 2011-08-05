from models import *
from django.forms import ModelForm
from django import forms
from django.forms.models import BaseModelFormSet
from grades.models import FLAG_CHOICES, CalNumericActivity,LETTER_GRADE_CHOICES_IN
import json

class ActivityComponentMarkForm(ModelForm):
    
    class Meta:
        model = ActivityComponentMark            
        fields = ['comment', 'value']
    

activity_mark_fields = ['late_penalty', 'mark_adjustment', 'mark_adjustment_reason', 'overall_comment', \
                  'file_attachment']
           
class ActivityMarkForm(ModelForm):
    class Meta:
        model = ActivityMark
        fields = activity_mark_fields
    
    def clean_late_penalty(self):  
        late_penalty = self.cleaned_data['late_penalty']
        try:
            float(late_penalty)
        except TypeError:
            raise forms.ValidationError(u'The late penalty must be a number')
        if late_penalty:
            if late_penalty > 100:
                raise forms.ValidationError(u'The late penalty can not exceed 100 percent')
        return late_penalty

class StudentActivityMarkForm(ActivityMarkForm):
    class Meta:
        model = StudentActivityMark
        fields = activity_mark_fields

class GroupActivityMarkForm(ActivityMarkForm):
    class Meta:
        model = GroupActivityMark
        fields = activity_mark_fields

    
class BaseActivityComponentFormSet(BaseModelFormSet):
    
    def __init__(self, activity, *args, **kwargs):
        self.activity =  activity
        super(BaseActivityComponentFormSet, self).__init__(*args, **kwargs)
        
    def clean(self):
        """Checks the following:
        1. no two component have the same title  
        2. max mark of each component is non-negative 
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
             return
        # check titles
        titles = []
        for form in self.forms:
            try: # since title is required, empty title triggers KeyError and don't consider this row
                form.cleaned_data['title']
            except KeyError:      
                continue
            else:  
                title = form.cleaned_data['title']
                if (not form.cleaned_data['deleted']) and title in titles:
                    raise forms.ValidationError(u"Each component must have a unique title")
                titles.append(title)  
        
        # check max marks
        for form in self.forms:
            try:
                form.cleaned_data['title']
            except KeyError:
                continue                        
            max_mark = form.cleaned_data['max_mark']
            if max_mark < 0:
                raise forms.ValidationError(u"Max mark of a component cannot be negative")
            
            
class BaseCommonProblemFormSet(BaseModelFormSet):
    
    def __init__(self, activity_components, *args, **kwargs):
        super(BaseCommonProblemFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['penalty'].widget.attrs['size'] = 5
            if activity_components:
                # limit the choices of activity components
                form.fields['activity_component'].queryset = activity_components
    
    def clean(self):
        """Checks the following:
        1. no two common problems in a same component have the same title  
        2. penalty of each common problem is non-negative
        3. penalty of each common problem does not exceed the max mark of its corresponding component
        """   
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
             return
        # check titles
        common_problems = {}
        for form in self.forms:
            try: # component is required, empty component triggers KeyError and don't consider this row
                component = form.cleaned_data['activity_component']
            except KeyError:
                continue
            
            title = form.cleaned_data['title']
            if (not form.cleaned_data['deleted']) and \
               component in common_problems.keys() and \
               common_problems[component].count(form.cleaned_data['title']) > 0:
               raise forms.ValidationError(u"Each common problem must have a unique title within one component")
           
            if not form.cleaned_data['deleted']:
                if not component in common_problems.keys():
                    common_problems[component] = [];
                common_problems[component].append(title)
                      
        # check penalty       
        for form in self.forms:
            try: 
                component = form.cleaned_data['activity_component']
            except KeyError:
                continue
            
            penalty = form.cleaned_data['penalty']          
            if penalty:
                if not (-component.max_mark <= penalty <= component.max_mark):
                    raise forms.ValidationError(u"Penalty of a common problem cannot not exceed its corresponding component")
                          

class MarkEntryForm(forms.Form):
    value = forms.DecimalField(max_digits=5, decimal_places=2, required=False, widget=forms.TextInput(attrs={'size':6}))

class UploadGradeFileForm(forms.Form):
    file = forms.FileField(required=True)
    
    def clean_file(self):        
        file = self.cleaned_data['file']
        if file != None and (not file.name.endswith('.csv')) and\
           (not file.name.endswith('.CSV')):
            raise forms.ValidationError(u"Only .csv files are permitted")
        return file    

class ImportFileForm(forms.Form):
    file = forms.FileField(required=True)
    def clean_file(self):        
        file = self.cleaned_data['file']

        if file != None and (not file.name.endswith('.json')) and\
           (not file.name.endswith('.JSON')):
            raise forms.ValidationError(u"Only .json files are permitted")
        return file

class ImportMarkFileForm(forms.Form):
    file = forms.FileField(required=True)

    def __init__(self, activity, userid, *args, **kwargs):
        super(ImportMarkFileForm, self).__init__(*args, **kwargs)
        self.activity = activity
        self.userid = userid
    
    def clean_file(self):        
        file = self.cleaned_data['file']

        if file != None and (not file.name.endswith('.json')) and\
           (not file.name.endswith('.JSON')):
            raise forms.ValidationError(u"Only .json files are permitted")
        
        try:
            data = file.read().decode('utf-8')
        except UnicodeDecodeError:
            raise forms.ValidationError(u"Bad UTF-8 data in file.")
        
        try:
            data = json.loads(data)
        except ValueError as e:
            raise forms.ValidationError(u'JSON decoding error.  Exception was: "' + str(e) + '"')

        return activity_marks_from_JSON(self.activity, self.userid, data)


from django.utils.safestring import mark_safe
from grades.forms import _required_star 
class ActivityRenameForm(forms.Form):
    name = forms.CharField(required=False, max_length=30, label=mark_safe('Name:'+_required_star),
                    widget=forms.TextInput(attrs={'size':'30'}))
    short_name = forms.CharField(required=False, max_length=15, label=mark_safe('Short name:' + _required_star),
                                widget=forms.TextInput(attrs={'size':'8'}))
    selected = forms.BooleanField(required=False, label='Rename?', initial = True, 
                    widget=forms.CheckboxInput(attrs={'class':'rename_check'}))


class GradeStatusForm(forms.ModelForm):
    def __init__(self, activity=None, *args, **kwargs):
    #    self.activity = activity
        super(GradeStatusForm, self).__init__(*args, **kwargs)
        self.fields['value'].label=mark_safe('Grade:' + _required_star)
        self.fields['flag'].label=mark_safe('Change Status to:' + _required_star)
        # exclude CALC status choice for non-calcualted activity
        isCalActivity = CalNumericActivity.objects.filter(id=self.instance.activity.id).count() != 0
        if not isCalActivity:
            self.fields['flag'].choices = [(v,l) for v,l in self.fields['flag'].choices if v!="CALC"]
        
    comment = forms.CharField(required=False, max_length=500,
                            label=mark_safe('Comment:'),
                            help_text='Please provide the reasons here',
                            widget=forms.Textarea(attrs={'rows':'6', 'cols':'40'}))
        
    class Meta:
        model = NumericGrade
        exclude = ('activity', 'member')

class GradeStatusForm_LetterGrade(forms.ModelForm):
    def __init__(self, activity=None, *args, **kwargs):
    #    self.activity = activity
        super(GradeStatusForm_LetterGrade, self).__init__(*args, **kwargs)
        self.fields['letter_grade'].label=mark_safe('Grade:' + _required_star)
        self.fields['flag'].label=mark_safe('Change Status to:' + _required_star)
        
    comment = forms.CharField(required=False, max_length=500,
                            label=mark_safe('Comment:'),
                            help_text='Please provide the reasons here',
                            widget=forms.Textarea(attrs={'rows':'6', 'cols':'40'}))

    def clean_flag(self):
        flag = self.cleaned_data['flag']
        
       
        if flag == 'CALC':
            isCalActivity = CalLetterActivity.objects.filter(id=self.instance.activity.id).count() != 0
            if not isCalActivity:
                raise forms.ValidationError(u'Option "calculated" is only for "calculated activity". Please use "graded".')            
        
        return flag
        
    class Meta:
        model = LetterGrade
        exclude = ('activity', 'member')


class MarkEntryForm_LetterGrade(forms.Form):
    value = forms.CharField(required=False,max_length=2, widget=forms.TextInput(attrs={'size':3}))
    
    def clean_value(self):
        grade = self.cleaned_data['value']
        if grade != '' and grade not in LETTER_GRADE_CHOICES_IN:
            raise forms.ValidationError(u'Invalid letter grade.')
        return grade

class UploadGradeFileForm_LetterGrade(forms.Form):
    file = forms.FileField(required=True)
    
    def clean_file(self):        
        file = self.cleaned_data['file']
        if file != None and (not file.name.endswith('.csv')) and\
           (not file.name.endswith('.CSV')):
            raise forms.ValidationError(u"Only .csv files are permitted")
        return file 

