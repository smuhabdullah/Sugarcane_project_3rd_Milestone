from django.db import models
from django.contrib.auth.models import User

class upload(models.Model):
    image = models.ImageField(upload_to='images')
    InfectedRegion = models.ImageField(upload_to='spot_on_org_images')
    
    def __str__(self):
        return str(self.id)

class Treatment(models.Model):
    disease_name = (
        ('Bacterial Blight', 'Bacterial Blight'),
        ('Leaf Rust', 'Leaf Rust'),
        ('Leaf Spot', 'Leaf Spot'),
        ('Mite Insect', 'Mite Insect'), 
        ('Red Rot', 'Red Rot'),
        ('Red Rust', 'Red Rust'), 
        ('White Fly', 'White Fly'),
        ('Yellow Leaf Virus', 'Yellow Leaf Virus')
        )
    disease = models.CharField(max_length=200, null=True, choices=disease_name)
    symptoms = models.CharField(max_length=1000, null=True)
    caused = models.CharField(max_length=1000, null=True)
    organic_control = models.CharField(max_length=1000, null=True)
    chemical_control = models.CharField(max_length=1000, null=True)
    preventive_measures = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.disease
    

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='/static/img/default.png', upload_to='avatar/')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
        
         
    