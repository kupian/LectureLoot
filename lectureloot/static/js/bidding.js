// these variables will be defined in the template before this script is loaded
// const userID
// const endDateTime
// const listingID

let finalMinute = false;
let highestBidTimer;

function getRemainingTime() {
  const endTime = new Date(endDateTime).getTime();
  const now = new Date().getTime();
  const timeLeft = endTime - now;
  return timeLeft;
}

function updateCountdown() {
  const countdownElement = $("#countdown")[0];
  
  function calculateTime() {
    const timeLeft = getRemainingTime();
    
    if (timeLeft > 0) {
      const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
      const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
      
      countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    } else {
      countdownElement.innerHTML = "Listing Ended";
      clearInterval(timer);
    }
  }
  
  calculateTime();
  const timer = setInterval(calculateTime, 1000);
}

function getHighestBid() {
  $.ajax({
    type: "POST",
    url: "/highest-bid/" + listingID,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: function(res) {
      $("#highestBid").text(`£${res.amount}`);
      
      if(res.user_id == userID) {
        $("#winning").text("You are the highest bidder!");
      } else {
        $("#winning").text(""); // Clear the text if user is not highest bidder
      }
    }
  });
  
  if (getRemainingTime() < 60000 && !finalMinute) {
    finalMinute = true;
    const interval = 1000;
    clearInterval(highestBidTimer);
    highestBidTimer = setInterval(getHighestBid, interval);
  }
}

function getHighestBidPeriodic() {
  const interval = 60000;
  
  getHighestBid();
  highestBidTimer = setInterval(getHighestBid, interval);
}

$(document).ready(function() {
  updateCountdown();
  getHighestBidPeriodic();

  $("#bidForm").submit(function(e) {
    e.preventDefault();

    $.ajax({
      type: "POST",
      url: "/bid/" + listingID,
      data: {
        amount: $("#amount").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function() {
        getHighestBid();
      },
      error: function(e) {
        $("#message").text($.parseJSON(e.responseText).message);
        const myModal = new bootstrap.Modal($("#errorModal"));
        myModal.show();
      }
    });
  });
});