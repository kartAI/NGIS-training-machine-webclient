
let scrollHeight = Math.max(
    document.body.scrollHeight, document.documentElement.scrollHeight,
    document.body.offsetHeight, document.documentElement.offsetHeight,
    document.body.clientHeight, document.documentElement.clientHeight
  );


  function nav() {
    const url = window.location.href;
    if (url.endsWith("/upload.html") || url.endsWith("/map.html")|| url.endsWith("/coords.html")) {
      document.location.href = "./order.html";
    } else if (url.endsWith("/order.html")) {
      document.location.href = "./confirm.html";
    }
  }