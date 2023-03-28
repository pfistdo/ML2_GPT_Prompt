function ask_gpt() {
  var question = document.getElementById("question").value;
  var data = {
    query: question
  };

  if (question != '') {
    // Add chat element to chat container
    add_chat_element(question, "User");
    $.ajax({
      url: "model/ask_gpt", // point to server-side URL
      dataType: "text", // what to expect back from server
      data: data,
      type: "post",
      success: function (response) {
        // alert(response, "success");
      },
      error: function (response) {
        // alert(response, "danger");
      },
      complete: function (response) {
        // Add chat element to chat container
        add_chat_element(response.responseText, "Bot");
        document.getElementById("question").value = "";
      }
    });
  } else {
    //   alert("Please select an image to upload!", "danger");
  }
}

function add_chat_element(text, type) {
  var chat = document.getElementById("chat-container");
  var element = document.createElement("div");
  // element.classList.add("chat-" + type);
  text = "<b>" + type + ": " + "</b>" + text
  element.innerHTML = text;
  chat.appendChild(element);
  chat.scrollTop = chat.scrollHeight;
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