# Family Organization Plan, 2026-27

Plan for keeping Elizabeth's homeschooling, the shared workouts, and Eric's work
blocks organized on one Google account. Written 2026-09-08. The Google Doc copy
lives in Drive under "Family Organization 2026-27".

## What is already in place

- **Eric's work template** (Personal calendar, Mon-Fri, America/New_York):
  06:45-07:45 Lift or walk with Elizabeth (7 days), 08:45-11:45 Coding / poker
  study, 12:00-16:30 Poker main block, 17:30-20:30 Poker evening block (Mon-Thu),
  Fri 17:30 Backlog sweep and 18:15 Weekly close-out.
- **"Elizabeth" calendar**: shared with Eric as writer. Empty for Aug 24 to Sep 20.
- **"Family" calendar**: owned by Eric, empty, time zone is set to UTC (should be
  America/New_York before anything goes on it).
- **Drive**: "Homeschool stuff" folder (curriculum book lists, two signed
  homeschool review PDFs), a "My Workouts" sheet from 2020 with one row, and a
  2017 "Daily Schedule Template".
- **New**: folder "Family Organization 2026-27" created in My Drive to hold
  everything below.

## Tool 1: Homeschool block schedule as a shared calendar

**Where it lives.** A dedicated "Homeschool" Google calendar, shared with
Elizabeth with "Make changes to events" permission. A separate calendar can be
toggled on and off, gets its own colour on both phones, and stays out of
Elizabeth's personal calendar. Creating a calendar is a one-minute step in
Google Calendar settings that only the account owner can do (the API access
here can add events but cannot create calendars). Fallback if you would rather
not: use the existing Family calendar.

**How it is built.**
- One recurring weekly event per block, Mon-Fri, taken from your block
  schedule. Each event carries the subject, the materials, and a one-line
  "done when" so anyone covering the block knows what finished looks like.
- Colours by subject family (core academics, reading, hands-on, outside).
- Break weeks and holidays as all-day events, with the recurring blocks
  excluded on those dates so the calendar never shows school on a day off.
- Term start and end as all-day markers.
- A 15-minute shared "Homeschool: plan next week" event on Friday, next to
  Eric's existing 18:15 close-out, so both weekly reviews happen together.

**Fit with Eric's day.** Elizabeth's morning chain (breakfast, coffee, milking,
feeding, start school) finishes around 08:45 now that the lift is at 06:45, so
a 09:00 to 12:00 core block is the natural shape. Eric's free windows on a
weekday are 07:45-08:45, 16:30-17:30 (screen break, good for an outdoor or
read-aloud block), Friday after 16:30, and weekends. Any block Eric leads goes
in one of those windows so the poker blocks stay protected.

**Needed from you:** the block schedule as it stands, the school-year start and
end dates and break weeks, who is being taught and their grade, and Elizabeth's
Google email address for sharing.

## Tool 2: Shared workout tracker (Google Sheet)

**Tabs.**
- `Log`: one row per set. Date, Who, Session type (Lift, Kettlebell, Walk,
  Mobility, Run), Exercise, Set, Reps, Weight, RPE, Duration, Notes.
- `Exercises`: the dropdown list with muscle group, so entries stay consistent.
- `Weekly`: lifting days per person per week against the 3-4 day target from
  the note on the 06:45 block, plus total sessions and the 06:45 streak.
- `PRs`: best weight and reps per exercise per person, filled by formula.
- `Dashboard`: this week vs last week, one glance on a phone.

**Phone entry.** A Google Form that writes straight into `Log`, so logging a
set from the garage takes seconds and nobody edits the sheet on a phone.

**Built from** the workout data you share next. The 2020 "My Workouts" row and
any history you have get imported so the PRs tab starts with real numbers.

## Tool 3: Homeschool attendance and lesson log (Google Sheet)

The signed review PDFs in Drive mean someone reviews the year, and a log is the
evidence. Tabs: `Daily log` (date, subjects covered, hours, notes), `Coverage`
(days and hours per subject, filled by formula), `Reading log`, and
`Curriculum` (the books from the PDFs in "Homeschool stuff", with status).
A second Google Form feeds `Daily log` so Elizabeth can fill it in two minutes
at the end of the school day.

## Tool 4: Household recurring items on the Family calendar

Fix the Family calendar time zone, then put only the things that need a
reminder on it: appointments, animal care that is not daily, deliveries,
anything either of you would otherwise have to remember. Daily chores stay off
the calendar. This calendar is already shared, so nothing new to set up.

## Tool 5: Weekly family check (15 minutes)

One shared event and one short checklist doc: next week's exceptions to the
homeschool blocks, appointments, who covers which block, and the workout plan.
It sits beside Eric's Friday close-out so it does not add a new time slot.

## Optional: a rebuild script in this repo

A small Python script that reads the block schedule from a CSV and creates or
updates the calendar events. It makes each term's schedule change a one-file
edit instead of re-entering events by hand. Worth doing only if the schedule
changes more than once or twice a year.

## Order of work

1. Next chat: you share the block schedule and workout data. Build the
   Homeschool calendar events and the workout sheet plus form in that session.
2. Then: attendance log sheet and form, Family calendar time zone fix, weekly
   check event and checklist.
3. Later, if wanted: the rebuild script.

## Open questions

1. Create a new "Homeschool" calendar, or use the Family calendar?
2. Who is being homeschooled, and what grade?
3. School-year dates and planned break weeks?
4. Does your state or reviewer require a specific attendance format (days, hours,
   subjects)?
5. Elizabeth's Google email, for sharing the sheets and forms.
