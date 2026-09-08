"""Build the shared workout log workbook.

Usage: python build_workout_sheet.py [output.xlsx]

The .xlsx is uploaded to Google Drive with conversion on, so the formulas are
written for Google Sheets (MAXIFS, COUNTUNIQUEIFS, SPLIT). Plate loads are
entered as written on the garage sheet, for example "45+45+10", and the Total
column works them out under the notation chosen on the Settings tab.
"""
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

PEOPLE = ["Elizabeth", "Eric"]
EXERCISES = [
    ("Deadlift", "Posterior chain", "Bar plus plates per side"),
    ("Bench press", "Chest, triceps", "Bar plus plates per side"),
    ("Curls", "Biceps", "Dumbbell or bar; set Unit to lb or reps"),
    ("Squat", "Legs", ""),
    ("Overhead press", "Shoulders", ""),
    ("Row", "Back", ""),
    ("Kettlebell swing", "Posterior chain", "Weight of the bell"),
    ("Walk", "Conditioning", "Put minutes in Load, Unit = min"),
    ("Mobility", "Recovery", "Put minutes in Load, Unit = min"),
]
LOG_ROWS = 400
FIRST_WEEK = date(2026, 8, 31)
WEEKS = 52

# Transcribed from the paper log (Sept 2026). Load is exactly as written.
ENTRIES = [
    (date(2026, 9, 1), "Elizabeth", "Deadlift", "45+10", "lb", ""),
    (date(2026, 9, 1), "Eric", "Deadlift", "45+45+10", "lb", ""),
    (date(2026, 9, 5), "Elizabeth", "Deadlift", "45+10+5", "lb", ""),
    (date(2026, 9, 5), "Eric", "Deadlift", "45+45+10+5", "lb", ""),
    (date(2026, 9, 1), "Elizabeth", "Bench press", "20", "lb", ""),
    (date(2026, 9, 1), "Eric", "Bench press", "45+10+2.5", "lb", ""),
    (date(2026, 9, 5), "Elizabeth", "Bench press", "20", "lb", ""),
    (date(2026, 9, 5), "Eric", "Bench press", "45+10+5", "lb", ""),
    (date(2026, 9, 1), "Elizabeth", "Curls", "55", "",
     "Unit unclear on the paper (lb or total reps). Set Unit and Total fills in."),
    (date(2026, 9, 1), "Eric", "Curls", "20", "",
     "Unit unclear on the paper (lb or total reps)."),
    (date(2026, 9, 5), "Elizabeth", "Curls", "55", "",
     "Written as 55 (total). Unit unclear: lb or reps?"),
    (date(2026, 9, 5), "Eric", "Curls", "90", "",
     "Unit unclear on the paper (lb or total reps)."),
]

HEADER_FILL = PatternFill("solid", fgColor="DDE5F0")
BOLD = Font(bold=True)


def style_header(ws, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = BOLD
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"


def set_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def build(path):
    wb = Workbook()

    # Settings
    st = wb.active
    st.title = "Settings"
    st.append(["Setting", "Value", "What it does"])
    st.append(["Plate notation", "per side",
               "per side: first number is the bar, the rest are plates on ONE side, "
               "so Total = bar + 2 x plates. total: Total is the plain sum."])
    st.append(["Lifting days target per week", 3,
               "From the note on the 06:45 block: three or four lifting days, the rest walks or mobility."])
    style_header(st, 3)
    set_widths(st, [30, 14, 90])
    dv_note = DataValidation(type="list", formula1='"per side,total"', allow_blank=False)
    st.add_data_validation(dv_note)
    dv_note.add("B2")

    # Exercises
    ex = wb.create_sheet("Exercises")
    ex.append(["Exercise", "Muscle group", "Notes"])
    for row in EXERCISES:
        ex.append(list(row))
    style_header(ex, 3)
    set_widths(ex, [22, 20, 44])

    # Log
    log = wb.create_sheet("Log", 0)
    log.append(["Date", "Who", "Exercise", "Load (as written)", "Unit", "Total lb", "Notes"])
    for r, (d, who, exn, load, unit, note) in enumerate(ENTRIES, start=2):
        log.cell(row=r, column=1, value=d).number_format = "yyyy-mm-dd"
        log.cell(row=r, column=2, value=who)
        log.cell(row=r, column=3, value=exn)
        log.cell(row=r, column=4, value=load)
        log.cell(row=r, column=5, value=unit)
        log.cell(row=r, column=7, value=note)
    for r in range(2, LOG_ROWS + 1):
        log.cell(row=r, column=1).number_format = "yyyy-mm-dd"
        d = f"D{r}"
        log.cell(row=r, column=6, value=(
            f'=IF(OR({d}="",E{r}<>"lb"),"",'
            f'IF(Settings!$B$2="per side",'
            f'2*SUM(SPLIT({d},"+"))-INDEX(SPLIT({d},"+"),1),'
            f'SUM(SPLIT({d},"+"))))'
        ))
    style_header(log, 7)
    set_widths(log, [12, 12, 18, 18, 8, 10, 60])
    dv_who = DataValidation(type="list", formula1='"' + ",".join(PEOPLE) + '"', allow_blank=True)
    dv_ex = DataValidation(type="list", formula1=f"=Exercises!$A$2:$A${len(EXERCISES) + 1}", allow_blank=True)
    dv_unit = DataValidation(type="list", formula1='"lb,reps,min"', allow_blank=True)
    for dv, col in ((dv_who, "B"), (dv_ex, "C"), (dv_unit, "E")):
        log.add_data_validation(dv)
        dv.add(f"{col}2:{col}{LOG_ROWS}")

    # PRs
    pr = wb.create_sheet("PRs")
    pr.append(["Who", "Exercise", "Best total lb", "Date of best", "Last logged", "Entries"])
    r = 2
    for who in PEOPLE:
        for exn, _, _ in EXERCISES:
            pr.cell(row=r, column=1, value=who)
            pr.cell(row=r, column=2, value=exn)
            crit = f'Log!$B:$B,$A{r},Log!$C:$C,$B{r}'
            pr.cell(row=r, column=3, value=f'=IFERROR(1/(1/MAXIFS(Log!$F:$F,{crit})),"")')
            pr.cell(row=r, column=4, value=f'=IF(C{r}="","",MAXIFS(Log!$A:$A,{crit},Log!$F:$F,C{r}))')
            pr.cell(row=r, column=5, value=f'=IFERROR(1/(1/MAXIFS(Log!$A:$A,{crit})),"")')
            pr.cell(row=r, column=6, value=f'=COUNTIFS({crit})')
            pr.cell(row=r, column=4).number_format = "yyyy-mm-dd"
            pr.cell(row=r, column=5).number_format = "yyyy-mm-dd"
            r += 1
    style_header(pr, 6)
    set_widths(pr, [12, 18, 14, 14, 14, 10])

    # Weekly
    wk = wb.create_sheet("Weekly")
    wk.append(["Week of (Mon)", "Elizabeth lift days", "Eric lift days",
               "Elizabeth sessions", "Eric sessions", "On target?"])
    for i in range(WEEKS):
        r = i + 2
        wk.cell(row=r, column=1, value=f"=DATE({FIRST_WEEK.year},{FIRST_WEEK.month},{FIRST_WEEK.day})+{7 * i}")
        wk.cell(row=r, column=1).number_format = "yyyy-mm-dd"
        win = f'Log!$A:$A,">="&$A{r},Log!$A:$A,"<"&($A{r}+7)'
        wk.cell(row=r, column=2, value=f'=COUNTUNIQUEIFS(Log!$A:$A,Log!$B:$B,"Elizabeth",Log!$E:$E,"lb",{win})')
        wk.cell(row=r, column=3, value=f'=COUNTUNIQUEIFS(Log!$A:$A,Log!$B:$B,"Eric",Log!$E:$E,"lb",{win})')
        wk.cell(row=r, column=4, value=f'=COUNTUNIQUEIFS(Log!$A:$A,Log!$B:$B,"Elizabeth",{win})')
        wk.cell(row=r, column=5, value=f'=COUNTUNIQUEIFS(Log!$A:$A,Log!$B:$B,"Eric",{win})')
        wk.cell(row=r, column=6, value=(
            f'=IF($A{r}>TODAY(),"",IF(AND(B{r}>=Settings!$B$3,C{r}>=Settings!$B$3),"yes","no"))'
        ))
    style_header(wk, 6)
    set_widths(wk, [14, 18, 14, 18, 14, 11])

    wb.save(path)
    print("wrote", path)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "workout_log.xlsx")
