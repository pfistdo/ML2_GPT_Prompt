function ask_gpt() {
  var question = document.getElementById("question").value;
  var data = {
    query: question
  };

  if (question != '') {
    $.ajax({
      url: "model/ask_gpt", // point to server-side URL
      dataType: "text", // what to expect back from server
      data: data,
      type: "post",
      success: function (response) {
        alert(response, "success");
      },
      error: function (response) {
        alert(response, "danger");
      },
    });
  } else {
    //   alert("Please select an image to upload!", "danger");
  }
}

// Bootstrap alert
const alert = (message, type) => {
  const alertPlaceholder = document.getElementById('alerts')
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}