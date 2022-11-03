from django import forms

from .models import (
    Order,
    DeliveryMethod,
    Country,
    Region,
    City,
    PaymentMethod,
)


class OrderCreateForm(forms.ModelForm):

    first_name = forms.CharField(
        required=True,
        label="First name",
        widget=forms.TextInput(attrs={"class": "form-input", "style": "!important"}),
    )
    last_name = forms.CharField(
        label="Last name", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    phone_number = forms.CharField(
        label="Phone number",
        widget=forms.NumberInput(
            attrs={"type": "tel", "data-tel-input": "", "max-length": 18}
        ),
        required=True,
    )
    post_office_number = forms.CharField(
        required=False,
        label="Post Office Number",
    )
    delivery_method = forms.ModelChoiceField(
        queryset=DeliveryMethod.objects, label="Delivery method"
    )
    delivery_country = forms.ModelChoiceField(
        queryset=Country.objects, label="Delivery country", required=False
    )
    delivery_region = forms.ModelChoiceField(
        queryset=Region.objects, label="Delivery region", required=False
    )
    delivery_city = forms.ModelChoiceField(
        queryset=City.objects, label="Delivery city", required=False
    )

    class Meta:
        model = Order

        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "delivery_method",
            "delivery_country",
            "delivery_region",
            "delivery_city",
            "post_office_number",
            "payment_method",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["delivery_method"].queryset = DeliveryMethod.objects.all()
        self.fields["delivery_country"].queryset = Country.objects.none()
        self.fields["delivery_region"].queryset = Region.objects.none()
        self.fields["delivery_city"].queryset = City.objects.none()
        self.fields["payment_method"].queryset = PaymentMethod.objects.none()

        if "method" in self.data:
            try:
                method_id = int(self.data.get("method"))
                self.fields["countries"].queryset = Country.objects.filter(
                    method__id=method_id
                )
                self.fields["pay_methods"].queryset = PaymentMethod.objects.filter(
                    method__id=method_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields[
                "countries"
            ].queryset = self.instance.method.country_set.order_by("countries")
            self.fields[
                "pay_methods"
            ].queryset = self.instance.method.method_set.order_by("pay_methods")

        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["regions"].queryset = Region.objects.filter(
                    country__id=country_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["regions"].queryset = self.instance.method.country_set.order_by(
                "regions"
            )

        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["cities"].queryset = Region.objects.filter(
                    region__id=region_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["cities"].queryset = self.instance.method.country_set.order_by(
                "cities"
            )

    def clean(self):
        super(OrderCreateForm, self).clean()
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        phone_number = self.cleaned_data["phone_number"]
        delivery_method = self.cleaned_data["delivery_method"]
        delivery_country = Country.objects.get(
            pk=self.cleaned_data.get("delivery_country", 1)
        )
        delivery_region = Region.objects.get(
            pk=self.cleaned_data.get("delivery_region", 26)
        )
        delivery_city = City.objects.get(pk=self.cleaned_data.get("delivery_city", 17))
        post_office_number = self.cleaned_data.get(
            "post_office_number", "Самовивіз із магазину"
        )
        payment_method = PaymentMethod.objects.filter(
            pk=self.data["payment_method"]
        ).first()

        self.cleaned_data["first_name"] = first_name
        self.cleaned_data["last_name"] = last_name
        self.cleaned_data["phone_number"] = phone_number
        self.cleaned_data["delivery_method"] = delivery_method
        self.cleaned_data["delivery_country"] = delivery_country
        self.cleaned_data["delivery_region"] = delivery_region
        self.cleaned_data["delivery_city"] = delivery_city
        self.cleaned_data["post_office_number"] = post_office_number
        self.cleaned_data["payment_method"] = payment_method

        if self._errors:
            print("errors")
            print(self._errors)
            self._errors.pop("delivery_country")
            self._errors.pop("delivery_region")
            self._errors.pop("delivery_city")
            self._errors.pop("payment_method")
            print("errors deleted")
            print(self._errors)
        return self.cleaned_data
