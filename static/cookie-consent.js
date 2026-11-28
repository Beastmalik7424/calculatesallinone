(function () {
  "use strict";

  var KEY = "cookie_consent";
  var ACCEPTED = "accepted";
  var REJECTED = "rejected";

  function readChoice() {
    try {
      var value = window.localStorage.getItem(KEY);
      return value === ACCEPTED || value === REJECTED ? value : null;
    } catch (error) {
      return null;
    }
  }

  function saveChoice(value) {
    try {
      window.localStorage.setItem(KEY, value);
    } catch (error) {
      // Keep the current-page choice in memory when browser storage is blocked.
    }
  }

  function loadAdsAfterConsent() {
    var client = document.querySelector('meta[name="ca-adsense-client"]');
    var slot = document.querySelector('meta[name="ca-adsense-slot"]');
    var ready = document.querySelector('meta[name="ca-adsense-consent-ready"]');
    if (!client || !slot || !ready || ready.content !== "true") return;
    if (!client.content || !/^ca-pub-\d{16}$/.test(client.content) || !/^\d+$/.test(slot.content)) return;
    if (document.querySelector('script[data-ca-adsense-loaded="true"]')) return;

    var script = document.createElement("script");
    script.async = true;
    script.crossOrigin = "anonymous";
    script.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + encodeURIComponent(client.content);
    script.setAttribute("data-ca-adsense-loaded", "true");
    script.onload = function () {
      var placements = document.querySelectorAll("ins.adsbygoogle:not([data-adsbygoogle-status])");
      placements.forEach(function () {
        try {
          (window.adsbygoogle = window.adsbygoogle || []).push({});
        } catch (error) {
          // Ad rendering failures must not interrupt calculator functionality.
        }
      });
    };
    document.head.appendChild(script);
  }

  function addBanner() {
    if (!document.body || document.getElementById("ca-cookie-consent")) return;
    var style = document.createElement("style");
    style.setAttribute("data-ca-cookie-consent-style", "true");
    style.textContent =
      "#ca-cookie-consent{position:fixed;z-index:2147483000;left:12px;right:12px;bottom:12px;max-width:720px;margin:0 auto;padding:10px;border:1px solid #94a3b8;border-radius:12px;background:#fff;color:#172033;box-shadow:0 8px 28px rgba(15,23,42,.22);font:14px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif}" +
      "#ca-cookie-consent *{box-sizing:border-box}" +
      "#ca-cookie-consent p{margin:0 0 8px}" +
      "#ca-cookie-consent a{color:#0759a5;text-decoration:underline;text-underline-offset:2px}" +
      "#ca-cookie-consent .ca-cookie-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px}" +
      "#ca-cookie-consent button{min-width:0;min-height:42px;width:100%;padding:8px 12px;border:1px solid #475569;border-radius:8px;background:#f8fafc;color:#172033;font:inherit;font-weight:650;cursor:pointer}" +
      "#ca-cookie-consent button:focus-visible{outline:3px solid #0759a5;outline-offset:2px}" +
      "@media(prefers-color-scheme:dark){#ca-cookie-consent{background:#192433;color:#f1f5fb;border-color:#64748b}#ca-cookie-consent a{color:#93c5fd}#ca-cookie-consent button{background:#263548;color:#f1f5fb;border-color:#94a3b8}}";
    document.head.appendChild(style);

    var previousPadding = document.body.style.paddingBottom;
    var originalComputedPadding = parseFloat(window.getComputedStyle(document.body).paddingBottom) || 0;
    var banner = document.createElement("section");
    banner.id = "ca-cookie-consent";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Cookie and advertising preferences");
    banner.innerHTML =
      '<p>Allow optional advertising cookies? Your choice is saved in this browser. Read the <a href="/privacy/">Privacy Policy</a>.</p>' +
      '<div class="ca-cookie-actions">' +
      '<button type="button" id="ca-cookie-accept">Accept</button>' +
      '<button type="button" id="ca-cookie-reject">Reject</button>' +
      '</div>';
    document.body.appendChild(banner);

    function reserveBottomSpace() {
      if (!banner.isConnected) return;
      // Zakat uses a fixed first-screen Calculate action. Keep the preference
      // banner below the header instead of covering that action or its hit area.
      if (document.getElementById("zakat-submit")) {
        banner.style.top = window.innerWidth >= 768 ? "124px" : "108px";
        banner.style.bottom = "auto";
      } else {
        banner.style.top = "auto";
        banner.style.bottom = "12px";
      }
      var height = Math.ceil(banner.getBoundingClientRect().height) + 24;
      document.body.style.paddingBottom = Math.max(originalComputedPadding, height) + "px";
    }

    function hide() {
      window.removeEventListener("resize", reserveBottomSpace);
      document.body.style.paddingBottom = previousPadding;
      if (banner.parentNode) banner.parentNode.removeChild(banner);
      if (style.parentNode) style.parentNode.removeChild(style);
    }

    banner.querySelector("#ca-cookie-accept").addEventListener("click", function () {
      saveChoice(ACCEPTED);
      hide();
      loadAdsAfterConsent();
    });
    banner.querySelector("#ca-cookie-reject").addEventListener("click", function () {
      saveChoice(REJECTED);
      hide();
    });
    reserveBottomSpace();
    window.addEventListener("resize", reserveBottomSpace);
  }

  var choice = readChoice();
  if (choice === ACCEPTED) {
    loadAdsAfterConsent();
  } else if (choice !== REJECTED) {
    addBanner();
  }
})();
