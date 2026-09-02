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

  // ---- Header shadow-on-scroll (Design System V2) -------------------------
  // Pure class toggle; the visual transition is defined in CSS and already
  // honors prefers-reduced-motion via the global rule at the top of
  // style.css. No layout shift, no animation loop -- one scroll listener,
  // passive, reading a single boolean.
  (function headerScrollState() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var ticking = false;
    function update() {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
      ticking = false;
    }
    window.addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(update);
      },
      { passive: true }
    );
    update();
  })();

  // ---- Scroll-reveal (Design System V2) ------------------------------------
  // Optional, additive only: every targeted element is real, already-visible
  // page content (cards, FAQ rows, trust badges, section headers) -- if this
  // never runs (no JS, old browser, reduced motion), nothing is hidden and
  // nothing breaks. Respects prefers-reduced-motion explicitly, not just via
  // CSS, so the observer itself never fires unnecessary work for those users.
  (function scrollReveal() {
    var reduceMotion =
      window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var targets = document.querySelectorAll(
      [
        ".service-card",
        ".info-card",
        ".faq-item",
        ".hero-trust li",
        ".section-head",
        ".step-list li",
      ].join(",")
    );
    if (!targets.length) return;
    if (reduceMotion || typeof window.IntersectionObserver !== "function") {
      // Nothing to animate for these visitors / this browser -- leave the
      // elements exactly as server-rendered (fully visible, no .reveal class).
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    targets.forEach(function (el, i) {
      el.classList.add("reveal");
      // Small, capped stagger within each visual group so a row of cards
      // doesn't all pop in in a single frame -- purely cosmetic, never
      // delays content that's already in view on load.
      el.style.transitionDelay = Math.min(i % 6, 6) * 40 + "ms";
      io.observe(el);
    });
  })();

  // ---- Light/dark theme toggle (v1.6.0) ------------------------------------
  // The <html data-theme="..."> attribute is the single source of truth.
  // A tiny inline script in <head> (layout.py:head()) already set it
  // synchronously from localStorage before first paint, so there is no
  // flash of the wrong theme -- this block only wires up the click
  // handlers and keeps the toggle buttons' accessible state in sync.
  // No stored preference at all means "follow the OS" -- CSS alone
  // handles that case via @media (prefers-color-scheme: dark), so this
  // code never writes an attribute unless the visitor actually clicks.
  (function themeToggle() {
    var STORAGE_KEY = "sg-theme";
    var toggles = document.querySelectorAll(".theme-toggle");
    if (!toggles.length) return;

    function prefersDark() {
      return !!(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
    }

    function isDarkActive() {
      var explicit = document.documentElement.getAttribute("data-theme");
      if (explicit === "dark") return true;
      if (explicit === "light") return false;
      return prefersDark();
    }

    function syncToggleState() {
      var dark = isDarkActive();
      toggles.forEach(function (btn) {
        btn.setAttribute("aria-pressed", dark ? "true" : "false");
        btn.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
      });
    }

    toggles.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next = isDarkActive() ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        try {
          localStorage.setItem(STORAGE_KEY, next);
        } catch (e) {
          // Private browsing / storage disabled -- theme still applies for
          // this page view, it just won't persist to the next one.
        }
        syncToggleState();
        trackEvent("theme_toggle", { theme: next });
      });
    });

    syncToggleState();
  })();
})();
