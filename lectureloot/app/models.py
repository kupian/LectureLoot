from django.db import models

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False)
    user = models.ForeignObject(User, on_delete=models.CASCADE, blank=False)
    amount = models.DecimalField(blank=False)
    time = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"Bid on {self.listing} for £{self.amount}"
    