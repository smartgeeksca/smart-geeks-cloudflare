/**
 * Smart Geeks -- progressive-enhancement behavior layer.
 *
 * Everything this file does is optional enhancement:
 *  - Mobile nav and FAQ accordions are native <details>/<summary> and need
 *    no JS at all.
 *  - The contact form works as a plain HTML POST without this file; here we
 *    upgrade it to an AJAX submission with inline validation and a redirect
 *    to /thank-you/ on confirmed success.
 *  - Analytics events only fire when window.__SG_ANALYTICS_CONFIG carries a
 *    real GA4 measurement ID (see src/templates/layout.py:analytics_snippet).
 */
(function () {
  "use strict";

  function trackEvent(name, params) {
    var cfg = window.__SG_ANALYTICS_CONFIG;
    if (!cfg || !cfg.ga4MeasurementId || typeof window.gtag !== "function") return;
    // Never send form field values or other PII in analytics events.
    window.gtag("event", name, params || {});
  }

  function trackConversion(labelKey) {
    var cfg = window.__SG_ANALYTICS_CONFIG;
    if (!cfg || !cfg.googleAdsConversionId || typeof window.gtag !== "function") return;
    var label = cfg.conversionLabels && cfg.conversionLabels[labelKey];
    if (!label) return;
    window.gtag("event", "conversion", { send_to: cfg.googleAdsConversionId + "/" + label });
  }

  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track]");
    if (!el) return;
    var kind = el.getAttribute("data-track");
    trackEvent(kind, { link_url: el.href || undefined });
    if (kind === "phone_click") trackConversion("phone_click");
    if (kind === "whatsapp_click") trackConversion("whatsapp_click");
  });

  // Close the mobile nav disclosure when a link inside it is activated.
  document.addEventListener("click", function (e) {
    var link = e.target.closest(".mobile-nav-panel a");
    if (!link) return;
    var details = link.closest("details.mobile-nav");
    if (details) details.removeAttribute("open");
  });

  // ---- Contact / landing form progressive enhancement ---------------------
  var MAX_LENGTHS = { name: 100, contact: 150, device: 80, message: 1000 };

  function initForm(form) {
    var status = form.querySelector(".form-status");
    var submitBtn = form.querySelector('button[type="submit"]');

    function setFieldError(field, message) {
      var err = form.querySelector('[data-error-for="' + field.name + '"]');
      if (err) err.textContent = message || "";
      field.setAttribute("aria-invalid", message ? "true" : "false");
    }

    function validate() {
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (field) {
        var value = (field.value || "").trim();
        if (!value) {
          setFieldError(field, "This field is required.");
          ok = false;
        } else if (MAX_LENGTHS[field.name] && value.length > MAX_LENGTHS[field.name]) {
          setFieldError(field, "Please shorten this to " + MAX_LENGTHS[field.name] + " characters or fewer.");
          ok = false;
        } else {
          setFieldError(field, "");
        }
      });
      var emailOrPhone = form.querySelector('[name="contact"]');
      if (emailOrPhone && emailOrPhone.value.trim()) {
        var v = emailOrPhone.value.trim();
        var looksLikeEmail = v.indexOf("@") > -1;
        var looksLikePhone = /^[0-9()+\-.\s]{7,}$/.test(v);
        if (!looksLikeEmail && !looksLikePhone) {
          setFieldError(emailOrPhone, "Enter a valid email address or phone number.");
          ok = false;
        }
      }
      return ok;
    }

    form.addEventListener("submit", function (e) {
      // Honeypot: if filled, silently no-op instead of submitting (bots only).
      var hp = form.querySelector('input[name="website"]');
      if (hp && hp.value) {
        e.preventDefault();
        return;
      }

      if (!validate()) {
        e.preventDefault();
        if (status) {
          status.textContent = "Please fix the highlighted fields and try again.";
          status.className = "form-status is-visible is-error";
        }
        return;
      }

      e.preventDefault();
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Sending..."; }
      if (status) { status.className = "form-status"; status.textContent = ""; }

      fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      })
        .then(function (res) {
          return res.json().catch(function () { return { ok: false }; }).then(function (data) {
            return { httpOk: res.ok, data: data };
          });
        })
        .then(function (result) {
          if (result.httpOk && result.data && result.data.ok) {
            trackEvent("lead_form_submit", { form_id: form.id || undefined });
            trackConversion("form_submit");
            window.location.href = "/thank-you/";
            return;
          }
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Send message"; }
          if (status) {
            status.textContent = (result.data && result.data.message) ||
              "Something went wrong sending your message. Please call or WhatsApp us instead.";
            status.className = "form-status is-visible is-error";
          }
        })
        .catch(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Send message"; }
          if (status) {
            status.textContent = "We couldn't reach the server. Please call or WhatsApp us instead.";
            status.className = "form-status is-visible is-error";
          }
        });
    });
  }

  document.querySelectorAll("form[data-sg-form]").forEach(initForm);
})();
