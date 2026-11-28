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
      "#ca-cookie-consent{position:fixed;z-index:2147483000;left:12px;right:12px;max-width:720px;margin:0 auto;padding:8px;border:1px solid #94a3b8;border-radius:10px;background:rgba(255,255,255,.96);color:#172033;box-shadow:0 6px 20px rgba(15,23,42,.18);font:11px/1.25 system-ui,-apple-system,'Segoe UI',sans-serif}" +
      "#ca-cookie-consent *{box-sizing:border-box}" +
      "#ca-cookie-consent .ca-cookie-layout{display:flex;align-items:center;gap:8px}" +
      "#ca-cookie-consent p{flex:1;min-width:0;margin:0}" +
      "#ca-cookie-consent a{color:#0759a5;text-decoration:underline;text-underline-offset:2px}" +
      "#ca-cookie-consent .ca-cookie-actions{display:grid;grid-template-columns:1fr 1fr;flex:0 0 114px;gap:4px}" +
      "#ca-cookie-consent button{min-width:0;min-height:34px;width:100%;padding:5px 4px;border:1px solid #475569;border-radius:7px;background:#f8fafc;color:#172033;font:inherit;font-weight:650;cursor:pointer}" +
      "#ca-cookie-consent button:focus-visible{outline:3px solid #0759a5;outline-offset:2px}" +
      "@media(prefers-color-scheme:dark){#ca-cookie-consent{background:rgba(25,36,51,.97);color:#f1f5fb;border-color:#64748b}#ca-cookie-consent a{color:#93c5fd}#ca-cookie-consent button{background:#263548;color:#f1f5fb;border-color:#94a3b8}}";
    document.head.appendChild(style);

    var previousPadding = document.body.style.paddingBottom;
    var originalComputedPadding = parseFloat(window.getComputedStyle(document.body).paddingBottom) || 0;
    var banner = document.createElement("section");
    banner.id = "ca-cookie-consent";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Cookie and advertising preferences");
    banner.innerHTML =
      '<div class="ca-cookie-layout">' +
      '<p>Optional ad cookies? Read the <a href="/privacy/">Privacy Policy</a>.</p>' +
      '<div class="ca-cookie-actions">' +
      '<button type="button" id="ca-cookie-accept">Accept</button>' +
      '<button type="button" id="ca-cookie-reject">Reject</button>' +
      '</div>' +
      '</div>';
    document.body.appendChild(banner);

    function reserveBottomSpace() {
      if (!banner.isConnected) return;
      var main = document.querySelector("main") || document.body;
      var heading = main.querySelector("h1");
      var controls = Array.prototype.slice.call(
        main.querySelectorAll('input:not([type="hidden"]), select, textarea')
      );
      function isVisible(element) {
        var rect = element.getBoundingClientRect();
        var computed = window.getComputedStyle(element);
        return rect.width > 0 && rect.height > 0 &&
          computed.display !== "none" && computed.visibility !== "hidden";
      }
      var firstControl = controls.find(isVisible);
      if (!firstControl) {
        firstControl = Array.prototype.slice.call(main.querySelectorAll("button")).find(isVisible);
      }
      var height = Math.ceil(banner.getBoundingClientRect().height);
      var top = 8;
      if (heading && firstControl) {
        var headingBottom = heading.getBoundingClientRect().bottom;
        var controlTop = firstControl.getBoundingClientRect().top;
        var gap = controlTop - headingBottom;
        top = gap >= height + 8
          ? headingBottom + (gap - height) / 2
          : controlTop - height - 4;
      } else if (heading) {
        top = heading.getBoundingClientRect().bottom + 8;
      }
      banner.style.top = Math.max(8, Math.round(top)) + "px";
      banner.style.bottom = "auto";
      document.body.style.paddingBottom = Math.max(originalComputedPadding, height + 24) + "px";
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
