"""Build the homeschool attendance and lesson log workbook.

Usage: python build_homeschool_log.py [output.xlsx]

Uploaded to Google Drive with conversion on, so formulas target Google Sheets.
"""
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SUBJECTS = ["Bible", "Math", "Reading", "Read-aloud", "Art", "Outdoor group",
            "Library group", "Sacramentum", "Jiu Jitsu", "Science", "History",
            "Writing", "Music", "Field trip"]
ROWS = 300
HEADER_FILL = PatternFill("solid", fgColor="E3EFDD")
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

    dl = wb.active
    dl.title = "Daily log"
    dl.append(["Date", "Day", "School day?", "Subjects covered (comma separated)",
               "Hours", "What we did", "Notes / wins / struggles"])
    for r in range(2, ROWS + 1):
        dl.cell(row=r, column=1).number_format = "yyyy-mm-dd"
        dl.cell(row=r, column=2, value=f'=IF(A{r}="","",TEXT(A{r},"ddd"))')
    style_header(dl, 7)
    set_widths(dl, [12, 6, 11, 40, 7, 50, 40])
    dv = DataValidation(type="list", formula1='"yes,no"', allow_blank=True)
    dl.add_data_validation(dv)
    dv.add(f"C2:C{ROWS}")

    cov = wb.create_sheet("Coverage")
    cov.append(["Measure", "Value"])
    cov.append(["School days logged", "=COUNTIF('Daily log'!$C:$C,\"yes\")"])
    cov.append(["Total hours", "=SUM('Daily log'!$E:$E)"])
    cov.append(["Days this week", "=COUNTIFS('Daily log'!$C:$C,\"yes\",'Daily log'!$A:$A,\">=\"&(TODAY()-WEEKDAY(TODAY(),2)+1))"])
    cov.append([])
    cov.append(["Subject", "Days covered", "Share of school days"])
    start = cov.max_row + 1
    for i, s in enumerate(SUBJECTS):
        r = start + i
        cov.cell(row=r, column=1, value=s)
        cov.cell(row=r, column=2, value=f"=COUNTIF('Daily log'!$D:$D,\"*\"&A{r}&\"*\")")
        cov.cell(row=r, column=3, value=f'=IF($B$2=0,"",B{r}/$B$2)')
        cov.cell(row=r, column=3).number_format = "0%"
    for c in range(1, 4):
        cov.cell(row=start - 1, column=c).font = BOLD
        cov.cell(row=start - 1, column=c).fill = HEADER_FILL
    style_header(cov, 2)
    set_widths(cov, [26, 14, 20])

    rl = wb.create_sheet("Reading log")
    rl.append(["Date started", "Date finished", "Title", "Author", "Read-aloud or independent",
               "Pages / chapters", "Notes"])
    for r in range(2, ROWS + 1):
        rl.cell(row=r, column=1).number_format = "yyyy-mm-dd"
        rl.cell(row=r, column=2).number_format = "yyyy-mm-dd"
    style_header(rl, 7)
    set_widths(rl, [13, 13, 34, 22, 22, 16, 40])
    dv2 = DataValidation(type="list", formula1='"Read-aloud,Independent"', allow_blank=True)
    rl.add_data_validation(dv2)
    dv2.add(f"E2:E{ROWS}")

    cu = wb.create_sheet("Curriculum")
    cu.append(["Subject", "Resource / book", "Status", "Where it is", "Notes"])
    style_header(cu, 5)
    set_widths(cu, [16, 40, 14, 24, 40])
    dv3 = DataValidation(type="list", formula1='"Planned,In use,Finished,Dropped"', allow_blank=True)
    cu.add_data_validation(dv3)
    dv3.add(f"C2:C{ROWS}")
    dv4 = DataValidation(type="list", formula1='"' + ",".join(SUBJECTS) + '"', allow_blank=True)
    cu.add_data_validation(dv4)
    dv4.add(f"A2:A{ROWS}")

    wb.save(path)
    print("wrote", path)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "homeschool_log.xlsx")
