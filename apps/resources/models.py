from django.db import models

class Country(models.Model):
    country_id = models.IntegerField()
    name = models.CharField(max_length=100)
    iso3 = models.CharField(max_length=3)
    iso2 = models.CharField(max_length=2)
    numeric_code = models.CharField(max_length=3)
    phone_code = models.CharField(max_length=10)
    capital = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    currency_name = models.CharField(max_length=50)
    currency_symbol = models.CharField(max_length=5)
    tld = models.CharField(max_length=5)
    native = models.CharField(max_length=100)
    timezones = models.TextField() 
    emoji = models.CharField(max_length=5)
    emojiU = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.IntegerField()
    state_code = models.CharField(max_length=5)
    type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country.name}"
    
class City(models.Model):
    state_code = models.CharField(null=True, max_length=20)
    name = models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.name}"
