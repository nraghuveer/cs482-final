function refresh() {
  $("#movies").html(
    "<tr><th>name</th><th>stock</th><th>checked</th><th>actions</th></tr>"
  );
  $.get("/dbMovie/").done(function (data) {
    for (i = 0; i < data.length; i++) {
      var param = '"' + data[i].name + '"';
      $("#movies").append(
        "<tr><td>" +
          data[i].name +
          "</td><td>" +
          data[i].stock +
          "</td><td>" +
          data[i].checked +
          "</td><td>" +
          "<button onclick=addStock(" +
          param +
          ")>+</button>" +
          "<button onclick=removeStock(" +
          param +
          ")>-</button>" +
          "</td></tr>"
      );
    }
  });
}

function setMessage(data) {
  refresh();
  $("#message").html(data["message"]);
  if (data["status"] != 200) {
    $("#message").css("color", "red");
  } else {
    $("#message").css("color", "black");
  }
}

function addStock(name) {
  $.post("/dbMovie/", { action: "add", movie: name }).done(refresh);
}

function removeStock(name) {
  $.post("/dbMovie/", { action: "remove", movie: name }).done(refresh);
}

$(function () {
  $("#submit").bind("click", function () {
    $.post("/dbMovie/", { action: "new", name: $("#name").val() }).done(
      setMessage
    );
  });
  refresh();
});
