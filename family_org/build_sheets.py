"""Build the two family sheets as CSV files for upload to Google Drive.

Usage: python build_sheets.py [output_dir]

Drive converts a CSV into a native Google Sheet and evaluates any cell that
starts with "=", so each file is one tab with the log on the left and a
formula-driven summary panel on the right. Formulas are written for Google
Sheets (SPLIT, MAXIFS, COUNTUNIQUEIFS).
"""
import csv
import sys
from datetime import date

PEOPLE = ["Elizabeth", "Eric"]
EXERCISES = ["Deadlift", "Bench press", "Curls", "Squat", "Overhead press",
             "Row", "Kettlebell swing"]
LOG_ROWS = 1000
FIRST_WEEK = date(2026, 8, 31)
WEEKS = 40

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

SUBJECTS = ["Bible", "Math", "Reading", "Read-aloud", "Art", "Outdoor group",
            "Library group", "Sacramentum", "Jiu Jitsu", "Science", "History",
            "Writing", "Music", "Field trip"]


def grid(rows, cols):
    return [[""] * cols for _ in range(rows)]


def workout_rows():
    # Columns: A-G log | H gap | I-N summary panel
    g = grid(2 + len(PEOPLE) * len(EXERCISES) + 3 + WEEKS + 2, 14)
    g[0][:7] = ["Date", "Who", "Exercise", "Load (as written)", "Unit", "Total lb", "Notes"]
    for i, (d, who, ex, load, unit, note) in enumerate(ENTRIES, start=1):
        g[i][:5] = [d.isoformat(), who, ex, load, unit]
        g[i][6] = note
    # One MAP formula fills the whole Total column, so new rows need no copying.
    g[1][5] = (f'=MAP(D2:D{LOG_ROWS},E2:E{LOG_ROWS},LAMBDA(d,e,IF(OR(d="",e<>"lb"),"",'
               f'IF($J$2="per side",2*SUM(SPLIT(d,"+"))-INDEX(SPLIT(d,"+"),1),SUM(SPLIT(d,"+"))))))')

    # Settings block
    g[0][8:11] = ["Setting", "Value", "What it does"]
    g[1][8:11] = ["Plate notation", "per side",
                  "per side: first number is the bar, the rest are plates on ONE side "
                  "(Total = bar + 2 x plates). Change to: total"]
    g[2][8:11] = ["Lifting days target per week", "3",
                  "From the 06:45 block note: 3 or 4 lifting days, the rest walks or mobility."]

    # PR block
    r0 = 4
    g[r0][8:14] = ["PRs: Who", "Exercise", "Best total lb", "Date of best", "Last logged", "Entries"]
    r = r0 + 1
    for who in PEOPLE:
        for ex in EXERCISES:
            n = r + 1
            crit = f'$B:$B,$I{n},$C:$C,$J{n}'
            g[r][8] = who
            g[r][9] = ex
            g[r][10] = f'=IFERROR(1/(1/MAXIFS($F:$F,{crit})),"")'
            g[r][11] = f'=IF(K{n}="","",TEXT(MAXIFS($A:$A,{crit},$F:$F,K{n}),"yyyy-mm-dd"))'
            g[r][12] = f'=IFERROR(TEXT(1/(1/MAXIFS($A:$A,{crit})),"yyyy-mm-dd"),"")'
            g[r][13] = f'=COUNTIFS({crit})'
            r += 1

    # Weekly block: one formula per column via SEQUENCE and MAP.
    r0 = r + 1
    g[r0][8:14] = ["Week of (Mon)", "Elizabeth lift days", "Eric lift days",
                   "Elizabeth sessions", "Eric sessions", "On target?"]
    first, last = r0 + 2, r0 + 1 + WEEKS
    wk = f"I{first}:I{last}"
    g[r0 + 1][8] = (f'=ARRAYFORMULA(TEXT(SEQUENCE({WEEKS},1,DATE({FIRST_WEEK.year},'
                    f'{FIRST_WEEK.month},{FIRST_WEEK.day}),7),"yyyy-mm-dd"))')

    def days(who, lifts):
        unit = ',$E:$E,"lb"' if lifts else ""
        return (f'=MAP({wk},LAMBDA(w,IF(w="","",COUNTUNIQUEIFS($A:$A,$B:$B,"{who}"{unit},'
                f'$A:$A,">="&DATEVALUE(w),$A:$A,"<"&(DATEVALUE(w)+7)))))')

    g[r0 + 1][9] = days("Elizabeth", True)
    g[r0 + 1][10] = days("Eric", True)
    g[r0 + 1][11] = days("Elizabeth", False)
    g[r0 + 1][12] = days("Eric", False)
    g[r0 + 1][13] = (f'=MAP({wk},J{first}:J{last},K{first}:K{last},LAMBDA(w,a,b,'
                     f'IF(OR(w="",DATEVALUE(w)>TODAY()),"",IF(AND(a>=VALUE($J$3),b>=VALUE($J$3)),"yes","no"))))')
    return g


def homeschool_rows():
    # Columns: A-G daily log | H gap | I-K coverage | L gap | M-S reading log
    g = grid(len(SUBJECTS) + 8, 19)
    g[0][:7] = ["Date", "Day", "School day?", "Subjects covered (comma separated)",
                "Hours", "What we did", "Notes / wins / struggles"]
    g[1][1] = f'=ARRAYFORMULA(IF(A2:A{LOG_ROWS}="","",TEXT(A2:A{LOG_ROWS},"ddd")))'

    g[0][8:10] = ["Coverage", "Value"]
    g[1][8:10] = ["School days logged", '=COUNTIF($C:$C,"yes")']
    g[2][8:10] = ["Total hours", "=SUM($E:$E)"]
    g[3][8:10] = ["School days this week",
                  '=COUNTIFS($C:$C,"yes",$A:$A,">="&(TODAY()-WEEKDAY(TODAY(),2)+1))']
    g[5][8:11] = ["Subject", "Days covered", "Share of school days"]
    for i, s in enumerate(SUBJECTS):
        r = 6 + i
        n = r + 1
        g[r][8] = s
        g[r][9] = f'=COUNTIF($D:$D,"*"&I{n}&"*")'
        g[r][10] = f'=IF($J$2=0,"",TEXT(J{n}/$J$2,"0%"))'

    g[0][12:19] = ["Reading log: started", "Finished", "Title", "Author",
                   "Read-aloud or independent", "Pages / chapters", "Notes"]
    return g


def write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        for row in rows:
            while row and row[-1] == "":
                row = row[:-1]
            w.writerow(row)
    print("wrote", path)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    write(f"{out}/workout_log.csv", workout_rows())
    write(f"{out}/homeschool_log.csv", homeschool_rows())
