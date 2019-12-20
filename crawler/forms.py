from django import forms


class code_search_form(forms.Form):
    user = forms.CharField()
    contest_code = forms.IntegerField()
    question_code = forms.CharField()


class analyse_rating_form(forms.Form):
    user_1 = forms.CharField()
    user_2 = forms.CharField()


class questions_and_attempts_form(forms.Form):
    user = forms.CharField()


class average_gap_form(forms.Form):
    user = forms.CharField()


class compare_contest_form(forms.Form):
    user_1 = forms.CharField()
    user_2 = forms.CharField()
    contest_code = forms.CharField()
