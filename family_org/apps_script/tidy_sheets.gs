/**
 * Tidy the family sheets. Paste this whole file into Extensions > Apps Script
 * on the sheet, save, then run tidyWorkoutLog (on the workout sheet) or
 * tidyHomeschoolLog (on the homeschool sheet) and approve the permission
 * prompt once. After that a "Family tools" menu appears on reload so either
 * can be re-run at any time. Both are safe to run more than once.
 */

var PEOPLE = ['Elizabeth', 'Eric'];
var EXERCISES = [
  ['Deadlift', 'Posterior chain'],
  ['Bench press', 'Chest, triceps'],
  ['Curls', 'Biceps'],
  ['Squat', 'Legs'],
  ['Overhead press', 'Shoulders'],
  ['Row', 'Back'],
  ['Kettlebell swing', 'Posterior chain'],
  ['Walk', 'Conditioning (Unit = min)'],
  ['Mobility', 'Recovery (Unit = min)'],
];
var SUBJECTS = ['Bible', 'Math', 'Reading', 'Read-aloud', 'Art', 'Outdoor group',
  'Library group', 'Sacramentum', 'Jiu Jitsu', 'Science', 'History', 'Writing',
  'Music', 'Field trip'];
var WEEKS = 40;
var FIRST_WEEK = [2026, 8, 31]; // year, month, day of the first Monday
var HEADER_BG = '#dde5f0';

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Family tools')
    .addItem('Tidy workout log', 'tidyWorkoutLog')
    .addItem('Tidy homeschool log', 'tidyHomeschoolLog')
    .addToUi();
}

// ---------------------------------------------------------------- workout

function tidyWorkoutLog() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var log = ss.getSheets()[0];
  log.setName('Log');

  // The summary panel used to live in columns H:N of the log. Remove it.
  log.getRange('H:N').clear();

  // Exercises tab feeds the Exercise dropdown.
  var ex = resetSheet_(ss, 'Exercises');
  ex.getRange(1, 1, 1, 2).setValues([['Exercise', 'Muscle group / notes']]);
  ex.getRange(2, 1, EXERCISES.length, 2).setValues(EXERCISES);
  styleRow_(ex, 1, 2);
  ex.setFrozenRows(1);
  ex.setColumnWidth(1, 160);
  ex.setColumnWidth(2, 240);

  // Summary tab: settings, PRs, weekly counts.
  var sm = resetSheet_(ss, 'Summary');
  sm.getRange('A1:C3').setValues([
    ['Setting', 'Value', 'What it does'],
    ['Plate notation', 'per side',
      'per side: the first number is the bar, the rest are plates on ONE side, so Total = bar + 2 x plates. Choose total for a plain sum.'],
    ['Lifting days target per week', 3,
      'Three or four lifting days a week, the rest walks or mobility.'],
  ]);
  sm.getRange('B2').setDataValidation(list_(['per side', 'total']));
  sm.getRange('C2:C3').setWrap(true);
  styleRow_(sm, 1, 3);

  var r = 5;
  sm.getRange(r, 1, 1, 6).setValues([[
    'PRs: who', 'Exercise', 'Best total lb', 'Date of best', 'Last logged', 'Entries']]);
  styleRow_(sm, r, 6);
  r += 1;
  var prRows = [];
  PEOPLE.forEach(function (who) {
    EXERCISES.forEach(function (e) {
      var n = r + prRows.length;
      var crit = 'Log!$B:$B,$A' + n + ',Log!$C:$C,$B' + n;
      prRows.push([
        who, e[0],
        '=IFERROR(1/(1/MAXIFS(Log!$F:$F,' + crit + ')),"")',
        '=IF(C' + n + '="","",MAXIFS(Log!$A:$A,' + crit + ',Log!$F:$F,C' + n + '))',
        '=IFERROR(1/(1/MAXIFS(Log!$A:$A,' + crit + ')),"")',
        '=COUNTIFS(' + crit + ')',
      ]);
    });
  });
  sm.getRange(r, 1, prRows.length, 6).setValues(prRows);
  sm.getRange(r, 4, prRows.length, 2).setNumberFormat('yyyy-mm-dd');
  r += prRows.length + 1;

  sm.getRange(r, 1, 1, 6).setValues([[
    'Week of (Mon)', 'Elizabeth lift days', 'Eric lift days',
    'Elizabeth sessions', 'Eric sessions', 'On target?']]);
  styleRow_(sm, r, 6);
  var first = r + 1;
  var last = r + WEEKS;
  var wk = 'A' + first + ':A' + last;
  var days = function (who, liftsOnly) {
    var unit = liftsOnly ? ',Log!$E:$E,"lb"' : '';
    return '=MAP(' + wk + ',LAMBDA(w,IF(w="","",COUNTUNIQUEIFS(Log!$A:$A,Log!$B:$B,"' +
      who + '"' + unit + ',Log!$A:$A,">="&w,Log!$A:$A,"<"&(w+7)))))';
  };
  sm.getRange(first, 1).setFormula(
    '=SEQUENCE(' + WEEKS + ',1,DATE(' + FIRST_WEEK.join(',') + '),7)');
  sm.getRange(first, 1, WEEKS, 1).setNumberFormat('yyyy-mm-dd');
  sm.getRange(first, 2).setFormula(days('Elizabeth', true));
  sm.getRange(first, 3).setFormula(days('Eric', true));
  sm.getRange(first, 4).setFormula(days('Elizabeth', false));
  sm.getRange(first, 5).setFormula(days('Eric', false));
  sm.getRange(first, 6).setFormula(
    '=MAP(' + wk + ',B' + first + ':B' + last + ',C' + first + ':C' + last +
    ',LAMBDA(w,a,b,IF(OR(w="",w>TODAY()),"",IF(AND(a>=$B$3,b>=$B$3),"yes","no"))))');
  var target = sm.getRange(first, 6, WEEKS, 1);
  sm.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('yes')
      .setBackground('#d9ead3').setRanges([target]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('no')
      .setBackground('#f4cccc').setRanges([target]).build(),
  ]);
  [220, 150, 150, 150, 150, 110].forEach(function (w, i) { sm.setColumnWidth(i + 1, w); });
  sm.setFrozenRows(1);

  // Log tab: the Total column formula, dropdowns, and formatting.
  log.getRange('F2').setFormula(
    '=MAP(D2:D1000,E2:E1000,LAMBDA(d,e,IF(OR(d="",e<>"lb"),"",' +
    'IF(Summary!$B$2="per side",2*SUM(SPLIT(d,"+"))-INDEX(SPLIT(d,"+"),1),SUM(SPLIT(d,"+"))))))');
  log.getRange('F1').setNote('Filled automatically by the formula in F2. Do not type in this column.');
  styleRow_(log, 1, 7);
  log.setFrozenRows(1);
  log.getRange('A2:A1000').setNumberFormat('yyyy-mm-dd');
  log.getRange('B2:B1000').setDataValidation(list_(PEOPLE));
  log.getRange('C2:C1000').setDataValidation(
    SpreadsheetApp.newDataValidation()
      .requireValueInRange(ex.getRange('A2:A50'), true).setAllowInvalid(true).build());
  log.getRange('E2:E1000').setDataValidation(list_(['lb', 'reps', 'min']));
  log.getRange('F2:F1000').setFontColor('#555555');
  [110, 100, 150, 150, 70, 90, 420].forEach(function (w, i) { log.setColumnWidth(i + 1, w); });
  band_(log, 'A1:G1000');
  ss.setActiveSheet(log);
}

// ------------------------------------------------------------- homeschool

function tidyHomeschoolLog() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var log = ss.getSheets()[0];
  log.setName('Daily log');

  // The coverage panel and reading log used to live in columns H:S. Remove them.
  log.getRange('H:S').clear();

  var cov = resetSheet_(ss, 'Coverage');
  cov.getRange('A1:B4').setValues([
    ['Coverage', 'Value'],
    ['School days logged', "=COUNTIF('Daily log'!$C:$C,\"yes\")"],
    ['Total hours', "=SUM('Daily log'!$E:$E)"],
    ['School days this week',
      "=COUNTIFS('Daily log'!$C:$C,\"yes\",'Daily log'!$A:$A,\">=\"&(TODAY()-WEEKDAY(TODAY(),2)+1))"],
  ]);
  styleRow_(cov, 1, 2);
  cov.getRange('A6:C6').setValues([['Subject', 'Days covered', 'Share of school days']]);
  styleRow_(cov, 6, 3);
  var rows = SUBJECTS.map(function (s, i) {
    var n = 7 + i;
    return [s,
      "=COUNTIF('Daily log'!$D:$D,\"*\"&A" + n + "&\"*\")",
      '=IF($B$2=0,"",B' + n + '/$B$2)'];
  });
  cov.getRange(7, 1, rows.length, 3).setValues(rows);
  cov.getRange(7, 3, rows.length, 1).setNumberFormat('0%');
  [200, 130, 170].forEach(function (w, i) { cov.setColumnWidth(i + 1, w); });

  var rd = resetSheet_(ss, 'Reading log');
  rd.getRange(1, 1, 1, 7).setValues([[
    'Date started', 'Date finished', 'Title', 'Author',
    'Read-aloud or independent', 'Pages / chapters', 'Notes']]);
  styleRow_(rd, 1, 7);
  rd.setFrozenRows(1);
  rd.getRange('A2:B500').setNumberFormat('yyyy-mm-dd');
  rd.getRange('E2:E500').setDataValidation(list_(['Read-aloud', 'Independent']));
  [110, 110, 260, 180, 180, 130, 300].forEach(function (w, i) { rd.setColumnWidth(i + 1, w); });

  var cu = resetSheet_(ss, 'Curriculum');
  cu.getRange(1, 1, 1, 5).setValues([[
    'Subject', 'Resource / book', 'Status', 'Where it is', 'Notes']]);
  styleRow_(cu, 1, 5);
  cu.setFrozenRows(1);
  cu.getRange('A2:A200').setDataValidation(list_(SUBJECTS));
  cu.getRange('C2:C200').setDataValidation(list_(['Planned', 'In use', 'Finished', 'Dropped']));
  [130, 280, 110, 180, 300].forEach(function (w, i) { cu.setColumnWidth(i + 1, w); });

  log.getRange('B2').setFormula('=ARRAYFORMULA(IF(A2:A1000="","",TEXT(A2:A1000,"ddd")))');
  styleRow_(log, 1, 7);
  log.setFrozenRows(1);
  log.getRange('A2:A1000').setNumberFormat('yyyy-mm-dd');
  log.getRange('C2:C1000').setDataValidation(list_(['yes', 'no']));
  log.getRange('D2:G1000').setWrap(true);
  [110, 60, 90, 260, 70, 320, 300].forEach(function (w, i) { log.setColumnWidth(i + 1, w); });
  band_(log, 'A1:G1000');
  ss.setActiveSheet(log);
}

// ---------------------------------------------------------------- helpers

function resetSheet_(ss, name) {
  var old = ss.getSheetByName(name);
  if (old) ss.deleteSheet(old);
  return ss.insertSheet(name);
}

function styleRow_(sheet, row, ncols) {
  sheet.getRange(row, 1, 1, ncols).setFontWeight('bold').setBackground(HEADER_BG);
}

function list_(values) {
  return SpreadsheetApp.newDataValidation()
    .requireValueInList(values, true).setAllowInvalid(true).build();
}

function band_(sheet, a1) {
  sheet.getBandings().forEach(function (b) { b.remove(); });
  sheet.getRange(a1).applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);
}
