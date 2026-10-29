/* Browser-only Gregorian date arithmetic. No network, cookies or storage. */
(function(root) {
  'use strict';
  var DAY_MS = 86400000;

  function isLeapYear(year) {
    return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  }

  function daysInMonth(year, month) {
    if (month === 2) return isLeapYear(year) ? 29 : 28;
    return [1, 3, 5, 7, 8, 10, 12].indexOf(month) !== -1 ? 31 : 30;
  }

  function parseCalendarDate(value) {
    var match = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/.exec(value || '');
    if (!match) throw new Error('Enter a valid start date.');
    var year = Number(match[1]);
    var month = Number(match[2]);
    var day = Number(match[3]);
    if (year < 1 || year > 9999 || month < 1 || month > 12 ||
        day < 1 || day > daysInMonth(year, month)) {
      throw new Error('Enter a valid Gregorian date.');
    }
    return { year: year, month: month, day: day };
  }

  function toIso(d) {
    return String(d.year).padStart(4, '0') + '-' +
      String(d.month).padStart(2, '0') + '-' + String(d.day).padStart(2, '0');
  }

  function dayNumber(d) {
    // setUTCFullYear avoids Date.UTC's special interpretation of years 00-99.
    var date = new Date(0);
    date.setUTCFullYear(d.year, d.month - 1, d.day);
    date.setUTCHours(0, 0, 0, 0);
    return Math.round(date.getTime() / DAY_MS);
  }

  function leapDaysBefore(d) {
    var beforeYear = d.year - 1;
    var total = Math.floor(beforeYear / 4) -
      Math.floor(beforeYear / 100) + Math.floor(beforeYear / 400);
    if (isLeapYear(d.year) &&
      (d.month > 2 || (d.month === 2 && d.day > 29))) total += 1;
    return total;
  }

  function calculateDays(startText, yearsText) {
    var start = parseCalendarDate(startText);
    var input = String(yearsText == null ? '' : yearsText).trim();
    if (!/^[0-9]+$/.test(input)) throw new Error('Enter a whole number of years.');
    var years = Number(input);
    if (!Number.isSafeInteger(years) || years > 9999 - start.year) {
      throw new Error('Choose fewer years so the end date is within year 9999.');
    }
    var endYear = start.year + years;
    var endDay = Math.min(start.day, daysInMonth(endYear, start.month));
    var end = { year: endYear, month: start.month, day: endDay };
    var days = dayNumber(end) - dayNumber(start);
    return {
      days: days,
      endDate: toIso(end),
      leapDays: leapDaysBefore(end) - leapDaysBefore(start),
      weeks: Math.floor(days / 7),
      remainingDays: days % 7,
      hours: days * 24,
      minutes: days * 1440
    };
  }

  function init() {
    var form = document.getElementById('years-days-form');
    if (!form) return;
    var startInput = document.getElementById('yd-start');
    var yearsInput = document.getElementById('yd-years');
    var error = document.getElementById('yd-error');
    var fields = ['days', 'end', 'weeks', 'hours', 'minutes', 'leap'];
    var today = new Date();
    startInput.value = String(today.getFullYear()).padStart(4, '0') + '-' +
      String(today.getMonth() + 1).padStart(2, '0') + '-' +
      String(today.getDate()).padStart(2, '0');
    var format = function(n) { return n.toLocaleString('en-US'); };
    function render() {
      try {
        var r = calculateDays(startInput.value, yearsInput.value);
        error.textContent = '';
        document.getElementById('yd-days').textContent = format(r.days) + ' days';
        document.getElementById('yd-end').textContent = 'End date: ' + r.endDate;
        document.getElementById('yd-weeks').textContent = format(r.weeks) +
          ' weeks and ' + r.remainingDays + ' days';
        document.getElementById('yd-hours').textContent = format(r.hours);
        document.getElementById('yd-minutes').textContent = format(r.minutes);
        document.getElementById('yd-leap').textContent = format(r.leapDays);
      } catch (e) {
        fields.forEach(function(id) {
          document.getElementById('yd-' + id).textContent = '—';
        });
        error.textContent = e.message;
      }
    }
    form.addEventListener('submit', function(e) { e.preventDefault(); render(); });
    startInput.addEventListener('change', render);
    yearsInput.addEventListener('change', render);
    render();
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { isLeapYear: isLeapYear, parseCalendarDate: parseCalendarDate,
      calculateDays: calculateDays };
  }
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
  }
})(this);

