// Pushes tracking-plan events to the Google Tag Manager data layer.
// GTM then forwards them to GA4 and the Meta Pixel (see docs/gtm_setup.md).

window.dataLayer = window.dataLayer || [];

// Keep the UTM parameters of the landing page for the whole session.
(function storeUtm() {
  var params = new URLSearchParams(window.location.search);
  ["utm_source", "utm_medium", "utm_campaign"].forEach(function (key) {
    if (params.get(key)) sessionStorage.setItem(key, params.get(key));
  });
})();

function utm() {
  return {
    utm_source: sessionStorage.getItem("utm_source") || "(direct)",
    utm_medium: sessionStorage.getItem("utm_medium") || "(none)",
    utm_campaign: sessionStorage.getItem("utm_campaign") || undefined,
  };
}

function track(eventName, params) {
  var payload = Object.assign(
    { event: eventName, page_type: document.body.dataset.pageType, page_path: window.location.pathname },
    utm(),
    params || {}
  );
  window.dataLayer.push(payload);
  if (window.console) console.log("[tracking]", payload); // helps when testing in GTM preview mode
}

// Fire signup_completed only once per sign-up, even if the user double-clicks or reloads.
function trackOnce(eventName, uniqueId, params) {
  var key = "tracked_" + eventName + "_" + uniqueId;
  if (sessionStorage.getItem(key)) return;
  sessionStorage.setItem(key, "1");
  track(eventName, params);
}

document.addEventListener("DOMContentLoaded", function () {
  // CTA clicks
  document.querySelectorAll("[data-cta]").forEach(function (el) {
    el.addEventListener("click", function () {
      track("cta_clicked", { cta_location: el.dataset.cta });
    });
  });

  // Plan selection
  document.querySelectorAll("[data-plan]").forEach(function (el) {
    el.addEventListener("click", function () {
      sessionStorage.setItem("plan_name", el.dataset.plan);
      track("pricing_plan_selected", { plan_name: el.dataset.plan, plan_price: Number(el.dataset.price) });
    });
  });

  // Sign-up form
  var form = document.getElementById("signup-form");
  if (!form) return;
  var plan = sessionStorage.getItem("plan_name") || "standard";
  var started = false;

  form.addEventListener("input", function () {
    if (!started) {
      started = true;
      track("signup_started", { plan_name: plan, form_version: form.dataset.version });
    }
  });

  form.querySelectorAll("[data-step-next]").forEach(function (button) {
    button.addEventListener("click", function () {
      var step = Number(button.dataset.stepNext);
      var fields = form.querySelectorAll('[data-step="' + step + '"] [required]');
      var invalid = Array.prototype.find.call(fields, function (f) { return !f.checkValidity(); });
      if (invalid) {
        track("form_error", { field_name: invalid.name, error_type: invalid.validity.valueMissing ? "missing" : "invalid" });
        invalid.reportValidity();
        return;
      }
      track("signup_step_completed", { step_number: step, step_name: button.dataset.stepName });
      showStep(step + 1);
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault(); // demo site: no real backend
    var signupId = "su_" + Date.now();
    trackOnce("signup_completed", signupId, {
      plan_name: plan,
      company_size: form.elements["company_size"].value,
      signup_id: signupId,
    });
    form.innerHTML = "<p>Thank you, your account request is received.</p>";
  });

  function showStep(n) {
    form.querySelectorAll("[data-step]").forEach(function (s) {
      s.hidden = Number(s.dataset.step) !== n;
    });
  }
  showStep(1);
});
