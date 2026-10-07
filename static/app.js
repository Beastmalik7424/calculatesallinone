(function () {
  "use strict"

  var MSG = {
    en: {
      zakatNoPrice: "Net zakatable wealth is {net}. Enter the silver price per gram to check Nisab. No Zakat amount is shown until Nisab is verified.",
      zakatBelow: "Net wealth {net} is below Nisab of {nisab}. Zakat is not due on this wealth.",
      zakatHawl: "Net wealth {net} is above Nisab of {nisab}. Zakat is due only after one full lunar year (hawl). Tick the lunar year box when that period is complete.",
      zakatDue: "Zakat payable at 2.5 percent: {amount}. Confirm the calculation and rules with a qualified scholar before you pay.",
      bmiInput: "Enter a weight from 2 to 500 kg and a height from 50 to 300 cm.",
      bmiInputImp: "Enter a weight from 4 to 1100 lb, a height of 1 to 9 ft, and inches from 0 to 11.9.",
      bmiResult: "Your BMI is {bmi}, which is in the {label} range for adults (WHO). BMI is a screening measure, not a diagnosis.",
      bmiUnder: "underweight",
      bmiNormal: "normal weight",
      bmiOver: "overweight",
      bmiObese: "obesity",
      profitEnter: "Enter a cost price and a selling price of zero or more.",
      profitWord: "Profit",
      lossWord: "Loss",
      profitNA: "Percentage is N/A because cost price is zero.",
      profitPct: "percent of cost price",
      ageEnter: "Enter your date of birth.",
      ageFuture: "Date of birth cannot be in the future.",
      ageCheck: "Please check the date of birth.",
      ageResult: "Age: {y} years, {m} months and {d} days. Total days lived: {t}.",
      discInput: "Enter a price of zero or more and a discount from 0 to 100 percent.",
      discResult: "You save {saved}. Final price: {final}. Tax is not included.",
      convEnter: "Enter a numeric value.",
      convKelvin: "Kelvin cannot be below zero, which is absolute zero.",
      convNeg: "A {cat} cannot be negative.",
      convResult: "{v} {from} equals {out} {to}.",
      calcError: "Error",
      calcDiv: "Cannot divide by zero",
      tasbihNone: "No target set.",
      tasbihReached: "Target of {goal} reached. Press Reset to start again.",
      tasbihLeft: "{left} to go for a target of {goal}.",
      themeDark: "Dark mode",
      themeLight: "Light mode",
      numeric: "en-US",
      units: {
        kg: "kilograms", g: "grams", lb: "pounds", oz: "ounces",
        m: "meters", cm: "centimeters", km: "kilometers", ft: "feet", in: "inches", mi: "miles",
        C: "Celsius", F: "Fahrenheit", K: "Kelvin"
      },
      cats: { weight: "weight", length: "length", temp: "temperature" }
    },
    ur: {
      zakatNoPrice: "خالص قابلِ زکوٰۃ مال {net} ہے۔ نصاب چیک کرنے کے لیے چاندی کی فی گرام قیمت لکھیں۔ نصاب کی تصدیق تک زکوٰۃ کی رقم نہیں دکھائی جائے گی۔",
      zakatBelow: "خالص مال {net} نصاب {nisab} سے کم ہے۔ اس مال پر زکوٰۃ واجب نہیں۔",
      zakatHawl: "خالص مال {net} نصاب {nisab} سے زیادہ ہے۔ زکوٰۃ قمری سال مکمل ہونے کے بعد واجب ہوگی۔ مدت پوری ہونے پر قمری سال والا خانہ نشان زد کریں۔",
      zakatDue: "2.5 فیصد زکوٰۃ واجب الادا: {amount}۔ ادائیگی سے پہلے حساب اور اصولوں کی تصدیق کسی مستند عالم سے کریں۔",
      bmiInput: "وزن 2 سے 500 کلو گرام اور قد 50 سے 300 سینٹی میٹر کے درمیان لکھیں۔",
      bmiInputImp: "وزن 4 سے 1100 پاؤنڈ، قد 1 سے 9 فٹ، اور انچ 0 سے 11.9 کے درمیان لکھیں۔",
      bmiResult: "آپ کا BMI {bmi} ہے، جو بالغوں کے لیے WHO کے مطابق {label} کی حد میں ہے۔ BMI ایک اسکریننگ پیمانہ ہے، تشخیص نہیں۔",
      bmiUnder: "کم وزن",
      bmiNormal: "معمول کا وزن",
      bmiOver: "زیادہ وزن",
      bmiObese: "موٹاپا",
      profitEnter: "قیمت خرید اور قیمت فروخت صفر یا اس سے زیادہ لکھیں۔",
      profitWord: "منافع",
      lossWord: "نقصان",
      profitNA: "فیصد N/A ہے کیونکہ قیمت خرید صفر ہے۔",
      profitPct: "فیصد قیمت خرید پر",
      ageEnter: "اپنی تاریخ پیدائش لکھیں۔",
      ageFuture: "تاریخ پیدائش مستقبل کی نہیں ہو سکتی۔",
      ageCheck: "براہ کرم تاریخ پیدائش دوبارہ دیکھیں۔",
      ageResult: "عمر: {y} سال، {m} مہینے اور {d} دن۔ زندگی کے کل دن: {t}۔",
      discInput: "قیمت صفر یا اس سے زیادہ اور ڈسکاؤنٹ 0 سے 100 فیصد کے درمیان لکھیں۔",
      discResult: "آپ کی بچت {saved}۔ آخری قیمت: {final}۔ ٹیکس شامل نہیں ہے۔",
      convEnter: "عددی قدر لکھیں۔",
      convKelvin: "کیلون صفر سے کم نہیں ہو سکتا، کیونکہ یہ مطلق صفر ہے۔",
      convNeg: "{cat} منفی نہیں ہو سکتی۔",
      convResult: "{v} {from} برابر ہے {out} {to} کے۔",
      calcError: "خرابی",
      calcDiv: "صفر سے تقسیم نہیں ہو سکتی",
      tasbihNone: "کوئی ہدف مقرر نہیں۔",
      tasbihReached: "ہدف {goal} پورا ہو گیا۔ دوبارہ شروع کرنے کے لیے ری سیٹ دبائیں۔",
      tasbihLeft: "ہدف {goal} کے لیے {left} باقی۔",
      themeDark: "ڈارک موڈ",
      themeLight: "لائٹ موڈ",
      numeric: "ur-PK",
      units: {
        kg: "کلو گرام", g: "گرام", lb: "پاؤنڈ", oz: "اونس",
        m: "میٹر", cm: "سینٹی میٹر", km: "کلو میٹر", ft: "فٹ", in: "انچ", mi: "میل",
        C: "سینٹی گریڈ", F: "فارن ہائیٹ", K: "کیلون"
      },
      cats: { weight: "وزن", length: "لمبائی", temp: "درجہ حرارت" }
    }
  }

  var UNITS = {
    weight: { keys: ["kg", "g", "lb", "oz"], base: { kg: 1, g: 0.001, lb: 0.45359237, oz: 0.028349523125 } },
    length: { keys: ["m", "cm", "km", "ft", "in", "mi"], base: { m: 1, cm: 0.01, km: 1000, ft: 0.3048, in: 0.0254, mi: 1609.344 } },
    temp: { keys: ["C", "F", "K"], base: {} }
  }

  function lang () {
    return document.documentElement.lang === "ur" ? "ur" : "en"
  }

  function t (key, vars) {
    var table = MSG[lang()]
    var text = table[key] !== undefined ? table[key] : MSG.en[key]
    if (vars) {
      Object.keys(vars).forEach(function (name) {
        text = text.split("{" + name + "}").join(String(vars[name]))
      })
    }
    return text
  }

  function $ (id) {
    return document.getElementById(id)
  }

  function num (id) {
    var el = $(id)
    if (!el || el.value === "") return null
    var v = Number(el.value)
    return isFinite(v) ? v : null
  }

  function say (id, text) {
    var el = $(id)
    if (el) el.textContent = text
  }

  function fmt (n) {
    return n.toLocaleString(MSG[lang()].numeric, { maximumFractionDigits: 2 })
  }

  /* Zakat: Nisab is 612.36 g of silver. The amount is shown only after the Nisab and hawl checks. */
  function initZakat () {
    var form = $("zakat-form")
    if (!form) return
    var assetIds = ["z-cash", "z-gold", "z-silver", "z-stock", "z-recv"]
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var assets = 0
      assetIds.forEach(function (id) {
        assets += num(id) || 0
      })
      var net = Math.max(0, assets - (num("z-debts") || 0))
      var price = num("z-silverprice")
      if (price === null || price <= 0) {
        say("zakat-result", t("zakatNoPrice", { net: fmt(net) }))
        return
      }
      var nisab = 612.36 * price
      if (net < nisab) {
        say("zakat-result", t("zakatBelow", { net: fmt(net), nisab: fmt(nisab) }))
        return
      }
      if (!$("z-hawl").checked) {
        say("zakat-result", t("zakatHawl", { net: fmt(net), nisab: fmt(nisab) }))
        return
      }
      say("zakat-result", t("zakatDue", { amount: fmt(net * 0.025) }))
    })
  }

  /* BMI: WHO adult ranges. Imperial inches must be 0 to 11.9. */
  function initBMI () {
    var form = $("bmi-form")
    if (!form) return
    var unit = $("bmi-unit")
    function toggle () {
      var metric = unit.value === "metric"
      $("bmi-metric").classList.toggle("hidden", !metric)
      $("bmi-imperial").classList.toggle("hidden", metric)
    }
    unit.addEventListener("change", toggle)
    toggle()
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var bmi = 0
      if (unit.value === "metric") {
        var kg = num("b-kg")
        var cm = num("b-cm")
        if (kg === null || cm === null || kg < 2 || kg > 500 || cm < 50 || cm > 300) {
          say("bmi-result", t("bmiInput"))
          return
        }
        bmi = kg / Math.pow(cm / 100, 2)
      } else {
        var lb = num("b-lb")
        var ft = num("b-ft")
        var inch = num("b-in") || 0
        if (lb === null || ft === null || lb < 4 || lb > 1100 || ft < 1 || ft > 9 || inch < 0 || inch >= 12) {
          say("bmi-result", t("bmiInputImp"))
          return
        }
        bmi = 703 * lb / Math.pow(ft * 12 + inch, 2)
      }
      var label = bmi < 18.5 ? t("bmiUnder") : bmi < 25 ? t("bmiNormal") : bmi < 30 ? t("bmiOver") : t("bmiObese")
      say("bmi-result", t("bmiResult", { bmi: bmi.toFixed(1), label: label }))
    })
  }

  function initProfit () {
    var form = $("pl-form")
    if (!form) return
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var cost = num("p-cost")
      var sell = num("p-sell")
      if (cost === null || sell === null || cost < 0 || sell < 0) {
        say("pl-result", t("profitEnter"))
        return
      }
      var diff = sell - cost
      var word = diff >= 0 ? t("profitWord") : t("lossWord")
      var amount = fmt(Math.abs(diff))
      if (cost === 0) {
        say("pl-result", word + ": " + amount + ". " + t("profitNA"))
        return
      }
      var pct = (diff / cost) * 100
      say("pl-result", word + ": " + amount + " (" + Math.abs(pct).toFixed(2) + " " + t("profitPct") + ").")
    })
  }

  function initAge () {
    var form = $("age-form")
    if (!form) return
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var value = $("a-dob").value
      if (!value) {
        say("age-result", t("ageEnter"))
        return
      }
      var parts = value.split("-").map(Number)
      var dob = new Date(parts[0], parts[1] - 1, parts[2])
      var now = new Date()
      var today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      if (dob > today) {
        say("age-result", t("ageFuture"))
        return
      }
      var years = today.getFullYear() - dob.getFullYear()
      var months = today.getMonth() - dob.getMonth()
      var days = today.getDate() - dob.getDate()
      if (days < 0) {
        months -= 1
        days += new Date(today.getFullYear(), today.getMonth(), 0).getDate()
      }
      if (months < 0) {
        months += 12
        years -= 1
      }
      if (years > 150) {
        say("age-result", t("ageCheck"))
        return
      }
      var total = Math.floor((Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()) - Date.UTC(parts[0], parts[1] - 1, parts[2])) / 86400000)
      say("age-result", t("ageResult", { y: years, m: months, d: days, t: fmt(total) }))
    })
  }

  function initDiscount () {
    var form = $("disc-form")
    if (!form) return
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var price = num("d-price")
      var pct = num("d-pct")
      if (price === null || pct === null || price < 0 || pct < 0 || pct > 100) {
        say("disc-result", t("discInput"))
        return
      }
      var saved = Math.round(price * pct) / 100
      var final = Math.round((price - saved) * 100) / 100
      say("disc-result", t("discResult", { saved: fmt(saved), final: fmt(final) }))
    })
  }

  function unitName (key) {
    return MSG[lang()].units[key]
  }

  function fillUnits () {
    var cat = $("u-cat").value
    var from = $("u-from")
    var to = $("u-to")
    from.innerHTML = ""
    to.innerHTML = ""
    UNITS[cat].keys.forEach(function (key) {
      var a = document.createElement("option")
      a.value = key
      a.textContent = unitName(key)
      from.appendChild(a)
      var b = document.createElement("option")
      b.value = key
      b.textContent = unitName(key)
      to.appendChild(b)
    })
    to.selectedIndex = 1
  }

  function toCelsius (v, unit) {
    if (unit === "C") return v
    if (unit === "F") return (v - 32) * 5 / 9
    return v - 273.15
  }

  function fromCelsius (c, unit) {
    if (unit === "C") return c
    if (unit === "F") return c * 9 / 5 + 32
    return c + 273.15
  }

  function initConverter () {
    var form = $("conv-form")
    if (!form) return
    $("u-cat").addEventListener("change", fillUnits)
    fillUnits()
    form.addEventListener("submit", function (e) {
      e.preventDefault()
      var cat = $("u-cat").value
      var v = num("u-val")
      var from = $("u-from").value
      var to = $("u-to").value
      if (v === null) {
        say("conv-result", t("convEnter"))
        return
      }
      if (cat === "temp") {
        if (from === "K" && v < 0) {
          say("conv-result", t("convKelvin"))
          return
        }
        var converted = fromCelsius(toCelsius(v, from), to)
        say("conv-result", t("convResult", { v: fmt(v), from: unitName(from), out: converted.toFixed(2), to: unitName(to) }))
        return
      }
      if (v < 0) {
        say("conv-result", t("convNeg", { cat: MSG[lang()].cats[cat] }))
        return
      }
      var base = UNITS[cat].base
      var out = v * base[from] / base[to]
      var shown = Number(out.toPrecision(6)).toLocaleString(MSG[lang()].numeric, { maximumFractionDigits: 6 })
      say("conv-result", t("convResult", { v: fmt(v), from: unitName(from), out: shown, to: unitName(to) }))
    })
  }

  /* Standard calculator: recursive descent parser with parentheses. No eval, no Function constructor. */
  function evaluate (expr) {
    var tokens = expr.match(/\d+\.?\d*|[+\-*\/()]/g)
    if (!tokens) throw new Error("incomplete")
    var pos = 0

    function peek () {
      return tokens[pos]
    }

    function next () {
      pos += 1
      return tokens[pos - 1]
    }

    function factor () {
      var tok = next()
      if (tok === undefined) throw new Error("incomplete")
      if (tok === "-") return -factor()
      if (tok === "(") {
        var inner = sum()
        if (next() !== ")") throw new Error("incomplete")
        return inner
      }
      var n = Number(tok)
      if (!isFinite(n)) throw new Error("invalid")
      return n
    }

    function product () {
      var value = factor()
      while (peek() === "*" || peek() === "/") {
        var op = next()
        var right = factor()
        if (op === "/") {
          if (right === 0) throw new Error("divzero")
          value = value / right
        } else {
          value = value * right
        }
      }
      return value
    }

    function sum () {
      var value = product()
      while (peek() === "+" || peek() === "-") {
        var op = next()
        var right = product()
        value = op === "+" ? value + right : value - right
      }
      return value
    }

    var result = sum()
    if (pos !== tokens.length) throw new Error("incomplete")
    if (!isFinite(result)) throw new Error("invalid")
    return result
  }

  function initCalculator () {
    var pad = $("calc-pad")
    if (!pad) return
    var display = $("calc-display")
    var expr = ""
    function render (text) {
      display.textContent = text === "" ? "0" : text.replace(/\*/g, "×").replace(/\//g, "÷").replace(/-/g, "−")
    }
    pad.addEventListener("click", function (e) {
      var btn = e.target.closest("button")
      if (!btn) return
      var key = btn.getAttribute("data-key")
      if (key === "C") {
        expr = ""
        render("")
      } else if (key === "BS") {
        expr = expr.slice(0, -1)
        render(expr)
      } else if (key === "%") {
        expr = expr.replace(/(\d+\.?\d*)$/, function (m) { return String(Number(m) / 100) })
        render(expr)
      } else if (key === "=") {
        try {
          var value = evaluate(expr)
          expr = String(Math.round(value * 1e10) / 1e10)
          render(expr)
        } catch (err) {
          display.textContent = err.message === "divzero" ? t("calcDiv") : t("calcError")
          expr = ""
        }
      } else if (/^[+\-*\/]$/.test(key)) {
        if (expr === "" && key !== "-") return
        if (/[+\-*\/]$/.test(expr) && expr.length > 1) expr = expr.slice(0, -1)
        expr += key
        render(expr)
      } else {
        expr += key
        render(expr)
      }
    })
  }

  function initTasbih () {
    var countEl = $("t-count")
    if (!countEl) return
    var target = $("t-target")
    var progress = $("t-progress")
    var count = 0
    try {
      count = Number(window.localStorage.getItem("tasbih-count")) || 0
    } catch (err) {
      count = 0
    }
    function save () {
      try {
        window.localStorage.setItem("tasbih-count", String(count))
      } catch (err) {
        return
      }
    }
    function paint () {
      countEl.textContent = String(count)
      var goal = Number(target.value)
      if (goal === 0) {
        progress.textContent = t("tasbihNone")
      } else if (count >= goal) {
        progress.textContent = t("tasbihReached", { goal: goal })
      } else {
        progress.textContent = t("tasbihLeft", { left: goal - count, goal: goal })
      }
    }
    $("t-tap").addEventListener("click", function () {
      count += 1
      save()
      paint()
    })
    $("t-reset").addEventListener("click", function () {
      count = 0
      save()
      paint()
    })
    target.addEventListener("change", paint)
    paint()
  }

  function initStopwatch () {
    var display = $("sw-display")
    if (!display) return
    var startedAt = 0
    var elapsed = 0
    var timer = null
    function pad (n) {
      return String(n).padStart(2, "0")
    }
    function paint () {
      var ms = elapsed
      var h = Math.floor(ms / 3600000)
      var m = Math.floor(ms / 60000) % 60
      var s = Math.floor(ms / 1000) % 60
      var cs = Math.floor(ms / 10) % 100
      display.textContent = pad(h) + ":" + pad(m) + ":" + pad(s) + "." + pad(cs)
    }
    function tick () {
      var now = performance.now()
      elapsed += now - startedAt
      startedAt = now
      paint()
    }
    $("sw-start").addEventListener("click", function () {
      if (timer) return
      startedAt = performance.now()
      timer = setInterval(tick, 50)
    })
    $("sw-stop").addEventListener("click", function () {
      if (!timer) return
      tick()
      clearInterval(timer)
      timer = null
    })
    $("sw-reset").addEventListener("click", function () {
      if (timer) clearInterval(timer)
      timer = null
      elapsed = 0
      paint()
    })
    paint()
  }

  /* Dark mode: the class is set before first paint in the page head. This only switches it and remembers the choice. */
  function initTheme () {
    var btn = $("theme-toggle")
    if (!btn) return
    function isDark () {
      return document.documentElement.classList.contains("dark")
    }
    function label () {
      btn.textContent = isDark() ? t("themeLight") : t("themeDark")
      btn.setAttribute("aria-pressed", isDark() ? "true" : "false")
    }
    btn.addEventListener("click", function () {
      var dark = !isDark()
      document.documentElement.classList.toggle("dark", dark)
      try {
        window.localStorage.setItem("theme", dark ? "dark" : "light")
      } catch (err) {
        return
      }
      label()
    })
    label()
  }

  function initAds () {
    var slots = document.querySelectorAll(".adsbygoogle")
    if (!slots.length) return
    slots.forEach(function () {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({})
      } catch (err) {
        return
      }
    })
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme()
    initZakat()
    initBMI()
    initProfit()
    initAge()
    initDiscount()
    initConverter()
    initCalculator()
    initTasbih()
    initStopwatch()
    initAds()
  })
})()
