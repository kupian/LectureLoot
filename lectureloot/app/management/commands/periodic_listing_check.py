import schedule
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Listing, Bid, Notification

def check_listings():
  current_time = timezone.now()

  print("checking listings now")

  #fetches only the listings that have ended
  listings = Listing.objects.filter(end_datetime__lt=current_time, highest_bid__isnull=False)
  
  for listing in listings:
    highest_bid = listing.highest_bid
    if highest_bid:
      winning_user = highest_bid.user
      winning_amount = highest_bid.amount
      seller_email = listing.seller.email

      #send a notification to the winner
      Notification.objects.create(
        user=winning_user,
        title="You won the auction!",
        message=f"Congratulations! You won the auction for '{listing.title}' with a bid of £{winning_amount}. "
                f"You can contact the seller at {seller_email} to arrange the transaction.",
        # listing=listing
      )


      #send a notification to the seller
      Notification.objects.create(
        user=listing.seller,
        title="Your listing has ended",
        message=f"The auction for your listing '{listing.title}' has ended. "
                f"The winner is {winning_user.username} with a bid of £{winning_amount}. "
                f"Their email is {winning_user.email}, so you can arrange the transaction.",
        # listing=listing
      )

      listing.delete()

      

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    print("Starting periodic checks")

    schedule.every(10).seconds.do(check_listings)

    while True:
      schedule.run_pending()
      time.sleep(1)  # sleep for 1 second to avoid high CPU usage

