$(function(){
  $("#Configs").change(function(){
    var endpoint = $(this).attr("data-api") + '_api/config/' + $(this).attr("data-device") + "/" + $(this).val()
    console.log(endpoint);
    $.ajax({
      url: endpoint,
      type: "GET",
      async: true,
      contentType: "charset=utf-8",
      success: function(result){
        $('#config_table').html(result);
      }
    });
  });
})
