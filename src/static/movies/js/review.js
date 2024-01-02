$("#replyBtn{{ review.id }}").click(function () {
  $("#replyForm{{review.id}}").show();
  var repliesContainer = $(`#replies-container{{review.id}}`);
  if (repliesContainer.children().length > 0) {
    repliesContainer.empty();
    repliesContainer.hide();
  } else {
    repliesContainer.show();
    $.ajax({
      url: "/review/load_replies/",
      type: "GET",
      data: {
        review_id: "{{ review.id }}",
      },
      success: function (data) {
        var repliesHtml = data.reply_reviews_html;
        repliesContainer.append(repliesHtml);
      },
      error: function (error) {
        console.log(error);
      },
    });
  }
});
$("#saveReplyBtn{{ review.id }}").click(function () {
  var replyContent = $("#replyContent{{review.id}}").val();
  $.ajax({
    url: "/review/reply/",
    type: "POST",
    data: {
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
      review_id: "{{ review.id }}",
      content: replyContent,
    },
    success: function (data) {
      if (data.status == "success") {
        $.toast({
          heading: "Success",
          text: data.message,
          showHideTransition: "slide",
          icon: "success",
          position: "top-right",
          loaderBg: "#05BD11",
        });
        var replyHtml = data.review;
        var repliesContainer = $(`#replies-container{{review.id}}`);
        repliesContainer.append(replyHtml);
        $("#replyContent{{review.id}}").val("");
      } else {
        $.toast({
          heading: "Error",
          text: data.message,
          showHideTransition: "slide",
          icon: "error",
          position: "top-right",
          loaderBg: "#FF5B5E",
        });
      }
    },
    error: function (error) {
      $.toast({
        heading: "Error",
        text: "An error occurred while processing your request.",
        showHideTransition: "slide",
        icon: "error",
        position: "top-right",
        loaderBg: "#FF5B5E",
      });
    },
  });
});
$("#cancelReplyBtn{{ review.id }}").click(function () {
  $("#replyForm{{review.id}}").hide();
});
$("#deleteBtn{{ review.id }}").click(function () {
  $("#confirmModal{{ review.id }}").show();
});
$("#confirmDeleteBtn{{ review.id }}").click(function () {
  var reviewId = "{{ review.id }}";
  $.ajax({
    url: "/review/delete/",
    type: "POST",
    data: {
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
      review_id: reviewId,
    },
    success: function (data) {
      if (data.status == "error") {
        $.toast({
          heading: "Error",
          text: data.message,
          showHideTransition: "slide",
          icon: "error",
          position: "top-right",
          loaderBg: "#FF0000",
        });
      } else {
        $.toast({
          heading: "Success",
          text: data.message,
          showHideTransition: "slide",
          icon: "success",
          position: "top-right",
          loaderBg: "#05BD11",
        });
        $("#review-container").html(data.reviews);
        $("#confirmModal{{ review.id }}").hide();
        $(`#card-review-item{{ review.id }}`).remove();
      }
    },
  });
});
$("#cancelDeleteBtn{{ review.id }}").click(function () {
  $("#confirmModal{{ review.id }}").hide();
});
$("#review-list-container").on("click", "#editBtn{{ review.id }}", function () {
  var reviewId = "{{ review.id }}";
  $(`#card-review-item{{ review.id }} .card-review-item__content-text`).hide();
  $(`#card-review-item{{ review.id }} .card-review-item__timestamp`).hide();
  $(`#card-review-item{{ review.id }} .card-review-item__actions`).hide();
  $(`#card-review-item{{ review.id }} .editReviewForm`).show();
});
$("#cancelEditBtn{{ review.id }}").click(function () {
  var reviewId = "{{ review.id }}";
  $(`#card-review-item{{ review.id }} .card-review-item__content-text`).show();
  $(`#card-review-item{{ review.id }} .card-review-item__timestamp`).show();
  $(`#card-review-item{{ review.id }} .card-review-item__actions`).show();
  $(`#card-review-item{{ review.id }} .editReviewForm`).hide();
});
$("#saveBtn{{ review.id }}").click(function () {
  var reviewId = "{{ review.id }}";
  var content = $(
    `#card-review-item{{ review.id }} textarea[name=content]`
  ).val();
  $.ajax({
    type: "POST",
    url: "/review/update/",
    data: {
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
      review_id: reviewId,
      content: content,
    },
    success: function (data) {
      if (data.status === "success") {
        $.toast({
          heading: "Success",
          text: data.message,
          showHideTransition: "slide",
          icon: "success",
          position: "top-right",
          loaderBg: "#05BD11",
        });
        $(`#card-review-item{{ review.id }} .card-review-item__content-text`)
          .text(data.review.content)
          .show();
        $(`#card-review-item{{ review.id }} .editReviewForm`).hide();
        $(`#card-review-item{{ review.id }} .card-review-item__timestamp`)
          .text(data.review.timestamp)
          .show();
        $(`#card-review-item{{ review.id }} .card-review-item__actions`).show();
      } else {
        $.toast({
          heading: "Error",
          text: "Something went wrong",
          showHideTransition: "slide",
          icon: "error",
          position: "top-right",
          loaderBg: "#FF0000",
        });
      }
    },
    error: function (error) {
      $.toast({
        heading: "Error",
        text: "Something went wrong",
        showHideTransition: "slide",
        icon: "error",
        position: "top-right",
        loaderBg: "#FF0000",
      });
    },
  });
});
