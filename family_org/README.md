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
- `build_sheets.py`: writes `workout_log.csv` and `homeschool_log.csv`, each
  one tab with the log on the left and a formula summary panel on the right.
  Uploading a CSV to Google Drive with conversion on produces a native Google
  Sheet and evaluates the formulas (verified 2026-09-08). No dependencies.

```
python family_org/build_sheets.py out_dir
```
- `apps_script/tidy_sheets.gs`: paste into Extensions > Apps Script on either
  Google Sheet and run `tidyWorkoutLog` or `tidyHomeschoolLog`. Moves the
  summary panel to its own tabs, adds dropdowns, headers, widths, banding,
  and colours. The CSV upload path cannot carry formatting, so this is the
  one manual step.
