(function ($) {
  "use strict";

  var STORAGE_PREFIX = "riho-";
  var ALLOWED_COLORS = ["color-1", "color-2", "color-3", "color-4", "color-5", "color-6"];
  var ALLOWED_WRAPPERS = ["compact-wrapper", "horizontal-wrapper"];
  var colorStylesheet = document.getElementById("color");
  var staticCssBase = colorStylesheet ? colorStylesheet.href.replace(/color-[1-6]\.css(?:\?.*)?$/, "") : "";

  function getPreference(name) {
    return localStorage.getItem(STORAGE_PREFIX + name);
  }

  function setPreference(name, value) {
    localStorage.setItem(STORAGE_PREFIX + name, value);
  }

  function setBodyTheme(theme) {
    document.body.classList.remove("dark-only", "dark-sidebar", "light-only");
    if (theme && theme !== "light-only") document.body.classList.add(theme);
  }

  function applyPreferences() {
    var color = getPreference("color");
    if (colorStylesheet && ALLOWED_COLORS.indexOf(color) !== -1) {
      colorStylesheet.href = staticCssBase + color + ".css";
    }

    var primary = getPreference("primary");
    var secondary = getPreference("secondary");
    if (primary) document.documentElement.style.setProperty("--theme-deafult", primary);
    if (secondary) document.documentElement.style.setProperty("--theme-secondary", secondary);

    setBodyTheme(getPreference("theme"));

    var direction = getPreference("direction");
    document.documentElement.dir = direction === "rtl" ? "rtl" : "ltr";

    var wrapper = getPreference("wrapper");
    var pageWrapper = document.getElementById("pageWrapper");
    if (pageWrapper && ALLOWED_WRAPPERS.indexOf(wrapper) !== -1) {
      pageWrapper.classList.remove.apply(pageWrapper.classList, ALLOWED_WRAPPERS);
      pageWrapper.classList.add(wrapper);
    }
    if (pageWrapper) pageWrapper.classList.toggle("box-layout", getPreference("boxed") === "true");

    var sidebarLayout = getPreference("sidebar-layout");
    if (sidebarLayout === "stroke-svg" || sidebarLayout === "fill-svg") {
      $(".sidebar-wrapper").attr("data-layout", sidebarLayout);
    }
  }

  applyPreferences();

  $(function () {
    applyPreferences();

    $(".customizer-links #c-pills-home-tab").on("click", function () {
      $(".customizer-contain, .customizer-links").addClass("open");
    });
    $(".customizer-contain .icon-close").on("click", function () {
      $(".customizer-contain, .customizer-links").removeClass("open");
    });

    $(".customizer-color:not(.dark) li").on("click", function () {
      var color = $(this).attr("data-attr");
      if (ALLOWED_COLORS.indexOf(color) === -1) return;
      setPreference("color", color);
      setPreference("primary", $(this).attr("data-primary"));
      setPreference("secondary", $(this).attr("data-secondary"));
      setPreference("theme", "light-only");
      applyPreferences();
    });

    $(".customizer-color.dark li").on("click", function () {
      var color = $(this).attr("data-attr");
      if (ALLOWED_COLORS.indexOf(color) === -1) return;
      setPreference("color", color);
      setPreference("primary", $(this).attr("data-primary"));
      setPreference("secondary", $(this).attr("data-secondary"));
      setPreference("theme", "dark-only");
      applyPreferences();
    });

    $(".color-apply-btn").on("click", function () {
      setPreference("primary", document.getElementById("ColorPicker1").value);
      setPreference("secondary", document.getElementById("ColorPicker2").value);
      applyPreferences();
    });

    $(".customizer-mix li").on("click", function () {
      setPreference("theme", $(this).attr("data-attr"));
      applyPreferences();
    });

    $(".sidebar-setting li").on("click", function () {
      setPreference("sidebar-layout", $(this).attr("data-attr"));
      applyPreferences();
    });

    $(".sidebar-type li").on("click", function () {
      var wrapper = $(this).attr("data-attr") === "normal-sidebar" ? "horizontal-wrapper" : "compact-wrapper";
      setPreference("wrapper", wrapper);
      applyPreferences();
    });

    $(".main-layout li").on("click", function () {
      setPreference("direction", $(this).attr("data-attr") === "rtl" ? "rtl" : "ltr");
      setPreference("boxed", $(this).hasClass("box-layout") ? "true" : "false");
      applyPreferences();
    });
  });
})(jQuery);
