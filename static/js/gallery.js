$(".btn-counter").on("click", function (event) {
  event.preventDefault();

  var $this = $(this),
    count = parseInt($this.attr("data-count")),
    active = $this.hasClass("active"),
    multiple = $this.hasClass("multiple-count");

  // Get the gallerylogId from the hidden span tag
  var gallerylogId = $(this).find(".gallerylog-id").text(); // Modify this line

  $.ajax({
    type: "POST",
    url: "like_toggle/",
    data: {
      gallerylog_id: gallerylogId,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
  })
    .done(function (response) {
      if (response["status"]) {
        // 서버로부터 성공적인 응답이 왔을 때의 처리
        if (active) {
          count--;
          $this.removeClass("active");
        } else {
          count++;
          $this.addClass("active");
        }
        $this.attr("data-count", count);
      } else {
        // If active is true but server returned false,
        // decrease the count and remove 'active' class.
        if (active) {
          count--;
          $this.removeClass("active");
          $this.attr("data-count", count);
        }
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.log("AJAX call failed.");
      console.log("Status: " + textStatus);
      console.log("Error: " + errorThrown);
    });
});
