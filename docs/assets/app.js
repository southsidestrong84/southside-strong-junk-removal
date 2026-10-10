// Mobile menu, and the free-estimate form. The site has no server: the form writes the message for the
// customer and opens their texting app on a phone, or their email app on a computer. Nothing is stored here.
(function () {
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("mobile-nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var form = document.querySelector("form.estimate");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = function (n) { var el = form.elements[n]; return el ? String(el.value || "").trim() : ""; };
    var how = (form.querySelector("input[name=how]:checked") || {}).value || "text";
    var lines = [
      "Free estimate request (website)",
      "Name: " + v("name"),
      "Phone: " + v("phone"),
      "Town: " + v("town"),
      "What needs to go: " + v("items"),
      "Best way to reach me: " + how
    ];
    var body = lines.join("\n");
    var phone = form.getAttribute("data-phone");
    var email = form.getAttribute("data-email");
    var touch = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
    var url = touch
      ? "sms:" + phone + "?&body=" + encodeURIComponent(body + "\n(I can text photos too.)")
      : "mailto:" + email + "?subject=" + encodeURIComponent("Free estimate request: " + (v("town") || "website")) + "&body=" + encodeURIComponent(body);
    var done = form.querySelector(".done");
    if (done) done.hidden = false;
    window.location.href = url;
  });
})();
