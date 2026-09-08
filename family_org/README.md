# family_org

Planning notes and helper scripts for the 2026-27 family organization setup:
Elizabeth's homeschool block schedule as a shared Google Calendar, a shared
workout tracker sheet, and a homeschool attendance log.

- `PLAN.md`: the plan and open questions. A Google Doc copy lives in Drive
  under "Family Organization 2026-27".
- `homeschool_blocks.csv`: the weekly block schedule as it was entered on the
  shared "Elizabeth" calendar on 2026-09-08 (day, start, end, title, Google
  colour id, notes). Edit this when the schedule changes; it is the source of
  truth for re-entering events.
- `build_workout_sheet.py`: builds `workout_log.xlsx` (Log, Exercises,
  Settings, PRs, Weekly tabs) with the paper log transcribed in. Requires
  `openpyxl`. Upload the result to Drive and open it with Google Sheets, then
  File > Save as Google Sheets.
- `build_homeschool_log.py`: builds `homeschool_log.xlsx` (Daily log,
  Coverage, Reading log, Curriculum tabs). Same upload steps.

```
pip install openpyxl
python family_org/build_workout_sheet.py workout_log.xlsx
python family_org/build_homeschool_log.py homeschool_log.xlsx
```
