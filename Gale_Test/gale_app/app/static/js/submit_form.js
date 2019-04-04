$("#SubmitButton").click(function() {
      var csrftoken = $("[name=csrfmiddlewaretoken]").val();
      var url = $("input#url").val();
      var depth_level = $("input#depth_level").val();
      var name = $("input#name").val();
      var email = $("input#email").val();
      var phone = $("input#phone").val();
      var message = $("textarea#message").val();
      var firstName = name; // For Success/Failure Message
      // Check for white space in name for Success/Fail message
      $this = $("#SubmitButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: "/gale_mini_app/",
        type: "POST",
	headers:{
        "X-CSRFToken": csrftoken
    	},
        data: {
	  url: url,
          depth_level: depth_level,
	  csrfmiddlewaretoken: csrftoken
        },
        cache: false,
        success: function() {
          // Success message
		  $('#success').html("<div class='alert alert-success'>");
		  $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
		    .append("</button>");
		  $('#success > .alert-success')
		    .append("<strong>Your request has been processed to Scraper. </strong>");
		  $('#success > .alert-success')
		    .append('</div>');
		  //clear all fields
		  $('#contactForm').trigger("reset");
        },
        error: function() {
          // Fail message
          $('#success').html("<div class='alert alert-danger'>");
          $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-danger').append($("<strong>").text("Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!"));
          $('#success > .alert-danger').append('</div>');
          //clear all fields
          $('#contactForm').trigger("reset");
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
          }, 1000);
        }
      })
  });
/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success').html('');
});
