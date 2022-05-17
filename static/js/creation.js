function setMessage(data) {
  console.log(data);
  $("#message").html(data["message"]);
  if (data["status"] != 200) {
    $("#message").css("color", "red");
  } else {
    $("#message").css("color", "black");
  }
}

$(function () {
  setMessage({ message: "" });
  $("#submit").bind("click", function () {
    $.post("/dbUser/", {
      email: $("#email").val(),
      first_name: $("#first_name").val(),
      last_name: $("#last_name").val(),
    }).done(setMessage);
  });
});
