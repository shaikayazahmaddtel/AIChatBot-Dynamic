/* Dynamic AI centralized widget SDK. */
(function (window, document) {
  "use strict";

  var DEFAULTS = {
    apiBase: "https://chatbot.midget.jsscript",
    title: "AI Assistant",
    primaryColor: "#2563eb"
  };

  function DynamicAI() {
    this.config = null;
    this.iframe = null;
    this.button = null;
    this.token = null;
    this.sessionId = null;
  }

  DynamicAI.prototype.init = function (options) {
    options = options || {};
    if (!options.customerId) {
      throw new Error("DynamicAI.init requires customerId");
    }

    this.config = Object.assign({}, DEFAULTS, options);
    this.createButton();
    this.initializeWidgetToken();
    return this;
  };

  DynamicAI.prototype.createButton = function () {
    if (document.getElementById("dynamic-ai-launcher")) return;

    var self = this;
    var button = document.createElement("button");
    button.id = "dynamic-ai-launcher";
    button.type = "button";
    button.setAttribute("aria-label", "Open AI assistant");
    button.textContent = "💬";
    button.style.cssText = [
      "position:fixed", "right:20px", "bottom:20px", "width:58px", "height:58px",
      "border:0", "border-radius:50%", "background:" + this.config.primaryColor,
      "color:#fff", "font-size:25px", "cursor:pointer", "z-index:2147483646",
      "box-shadow:0 8px 24px rgba(0,0,0,.2)"
    ].join(";");

    button.addEventListener("click", function () {
      self.open();
    });
    document.body.appendChild(button);
    this.button = button;
  };

  DynamicAI.prototype.initializeWidgetToken = function () {
    var self = this;
    fetch(this.config.apiBase + "/api/v1/chatbot/widget/init", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        customerId: this.config.customerId,
        website_url: window.location.origin
      })
    })
      .then(function (response) {
        if (!response.ok) throw new Error("Unable to initialize chatbot widget");
        return response.json();
      })
      .then(function (payload) {
        self.token = payload.token;
      })
      .catch(function (error) {
        console.error("DynamicAI initialization failed:", error);
      });
  };

  DynamicAI.prototype.open = function () {
    if (this.iframe) {
      this.iframe.style.display = "block";
      return;
    }

    if (!this.token) {
      console.warn("DynamicAI is still initializing. Try again in a moment.");
      return;
    }

    var iframe = document.createElement("iframe");
    iframe.src = this.config.apiBase + "/widget?token=" + encodeURIComponent(this.token);
    iframe.title = this.config.title;
    iframe.allow = "clipboard-write";
    iframe.style.cssText = [
      "position:fixed", "right:20px", "bottom:90px", "width:380px", "height:600px",
      "max-width:calc(100vw - 24px)", "max-height:calc(100vh - 110px)",
      "border:0", "border-radius:16px", "background:#fff", "z-index:2147483645",
      "box-shadow:0 16px 48px rgba(0,0,0,.25)"
    ].join(";");

    document.body.appendChild(iframe);
    this.iframe = iframe;
  };

  DynamicAI.prototype.close = function () {
    if (this.iframe) this.iframe.style.display = "none";
  };

  window.DynamicAI = new DynamicAI();
})(window, document);
