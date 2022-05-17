function refresh()
{
  $("#items").html("<tr><th>name</th><th>code</th</tr>");
  $.get("/item").done(function(data){
    for (i=0;i<data.length;i++)
    {
      $("#items").append("<tr><td>"+data[i].name+"</td><td>"+data[i].code+"</td></tr>");
    }
  });
}

$(function(){
  refresh();
  $("#submit").bind("click", function(){
    $.post("/item/",{"name":$("#name").val(),"code":$("#code").val()}).done(refresh);
  });
});