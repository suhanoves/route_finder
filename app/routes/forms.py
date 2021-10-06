from decimal import Decimal

from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Field, \
    Div
from django import forms
from django.core.exceptions import ValidationError

from cities.models import City

all_cities = City.objects.all()


class RouteSearchForm(forms.Form):
    origin = forms.ModelChoiceField(
        label='Откуда',
        queryset=all_cities,
    )
    destination = forms.ModelChoiceField(
        label='Куда',
        queryset=all_cities,
    )
    transfers = forms.ModelMultipleChoiceField(
        label='Через города',
        required=False,
        queryset=all_cities,
    )
    price_limit = forms.DecimalField(
        label='Бюджет',
        required=False,
        min_value=Decimal(0.01),
        max_digits=14,
        decimal_places=2,
    )
    duration_limit = forms.DurationField(
        label='Время в пути',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'route-search-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'routes:found_routes'

        self.helper.layout = Layout(
            Div(
                Field('origin',
                      css_class='js-single-choice',
                      wrapper_class='col-12'
                      ),
                Field('destination',
                      css_class='js-single-choice',
                      wrapper_class='col-12'
                      ),
                css_class='row'
            ),
            Field('transfers',
                  css_class='js-multiple-choice',
                  wrapper_class='col-12'
                  ),
            Div(
                AppendedText(
                    'price_limit',
                    '₽',
                    wrapper_class='col-xs-12 col-sm-6'
                ),
                Field('duration_limit',
                      wrapper_class='col-xs-12 col-sm-6'
                      ),
                css_class='row'
            ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Найти маршруты', )),
                css_class='row text-center'
            ),
        )

    def clean(self):
        if self.cleaned_data['origin'] == self.cleaned_data['destination']:
            raise ValidationError(
                'Город отправления и город назначения должны отличаться',
                code='origin_is_destination'
            )
