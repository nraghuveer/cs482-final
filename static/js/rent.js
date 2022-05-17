function refreshAllMovies() {
  email = $("#email").val();

  $("#all").html("<tr><th>name</th><th>available-stock</th></tr>");
  $.get("/dbMovie/").done(function (data) {
    for (i = 0; i < data.length; i++) {
      if (data[i].stock <= data[i].checked) {
        continue;
      }
      $("#all").append(
        `<tr onclick=rentMovie('${data[i].name}')><td>` +
          data[i].name +
          "</td><td>" +
          (data[i].stock - data[i].checked) +
          "</td></tr>"
      );
    }
  });
}

function setMessage(data) {
  $("#message").html(data["message"]);
  if (data["status"] != 200) {
    $("#message").css("color", "red");
  } else {
    $("#message").css("color", "black");
  }
}

function returnMovie(movie) {
  var email = $("#email").val();
  if (!email) {
    return;
  }
  $.post("/dbRent/", { action: "return", movie: movie, email: email })
    .done(setMessage)
    .done(refresh);
}

function rentMovie(movie) {
  email = $("#email").val();
  if (!email) {
    return;
  }
  $.post("/dbRent/", { action: "rent", movie: movie, email: email })
    .done(setMessage)
    .done(refresh);
}

function refreshRentedMovies() {
  var email = $("#email").val();
  $("#rented").html("<tr><th>name</th></tr>");
  $.get("/dbRent/", { action: "return", email: email }).done(function (data) {
    data = data["rentals"];
    for (i = 0; i < data.length; i++) {
      var movie = data[i].movie_id;
      $("#rented").append(
        `<tr onclick=returnMovie('${movie}')><td>` + movie + "</td></tr>"
      );
    }
  });
}

function refresh() {
  refreshRentedMovies();
  refreshAllMovies();
}

$(function () {
  setMessage({ message: "" });
  $("#submit").bind("click", function () {
    $.get("/dbUser/", {
      email: $("#email").val(),
    })
      .done(function (data) {
        setMessage(data);
        $("#first_name").html(data["user"]["first_name"]);
        $("#last_name").html(data["user"]["last_name"]);
      })
      .done(refresh);
  });
});
