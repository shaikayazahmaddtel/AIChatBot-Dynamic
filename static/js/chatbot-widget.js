/*
 * Backward-compatible wrapper for the centralized Dynamic AI SDK.
 * All tenant resolution, authentication, rendering, and chat requests
 * are handled by /static/js/dynamic-ai.js.
 */
(function (window, document) {
  "use strict";

  function loadCentralSDK(callback) {
    if (window.DynamicAI) {
      callback();
      return;
    }

    var existing = document.querySelector('script[src*="/static/js/dynamic-ai.js"]');
    if (existing) {
      existing.addEventListener("load", callback, { once: true });
      return;
    }

    var script = document.createElement("script");
    script.src = "/static/js/dynamic-ai.js";
    script.async = true;
    script.addEventListener("load", callback, { once: true });
    document.head.appendChild(script);
  }

  function initFromLegacyScript() {
    var script = document.currentScript || document.querySelector('script[data-client-id]');
    var customerId = script && (script.getAttribute("data-client-id") || script.getAttribute("data-customer-id"));

    if (!customerId) {
      console.error("DynamicAI requires a registered customer ID.");
      return;
    }

    loadCentralSDK(function () {
      window.DynamicAI.init({ customerId: customerId });
    });
  }

  window.ChatbotWidget = function () {
    throw new Error("ChatbotWidget is deprecated. Use DynamicAI.init({ customerId: ... }).");
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFromLegacyScript, { once: true });
  } else {
    initFromLegacyScript();
  }
})(window, document);
