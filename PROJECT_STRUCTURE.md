# Habit Tracker App – Project Structure

Below is a suggested organized structure for the `habit_tracker_app.py` project, designed to improve maintainability and scalability. You can use this as a guide for refactoring your codebase:

```
habit_tracker_app/
│
├── habit_tracker_app.py       # Main application file containing GUI and logic
│
├── database/
│   ├── __init__.py
│   └── db_manager.py          # Handles database setup and queries
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # Main Tkinter window and layout
│   └── dialogs.py             # Custom dialogs (add habit, reminders, etc.)
│
├── models/
│   ├── __init__.py
│   ├── habit.py               # Habit model and logic
│   └── habit_log.py           # Habit log model and logic
│
├── charts/
│   ├── __init__.py
│   ├── bar_chart.py           # Bar chart plotting logic
│   └── calendar_heatmap.py    # Calendar heatmap plotting logic
│
├── utils/
│   ├── __init__.py
│   ├── reminders.py           # Reminder and scheduling utilities
│   └── quotes.py              # Quotes collection and randomizer
│
├── requirements.txt           # Project dependencies
└── README.md                  # Documentation
```

---

## Description of Folders & Files

- **habit_tracker_app.py**  
  Entry point for the application. Responsible for initializing the main window.

- **database/db_manager.py**  
  Handles all database interactions (setup, CRUD operations, etc.).

- **ui/main_window.py**  
  Contains the main Tkinter window, layout, and event bindings.

- **ui/dialogs.py**  
  Custom dialogs, popups, and input forms.

- **models/habit.py & models/habit_log.py**  
  Data models representing habits and their logs.

- **charts/bar_chart.py**  
  Logic for displaying bar charts (matplotlib).

- **charts/calendar_heatmap.py**  
  Logic for drawing the calendar heatmap.

- **utils/reminders.py**  
  Functions for scheduling and showing reminders.

- **utils/quotes.py**  
  Quotes and utility for random selection.

---

## Example refactor for `habit_tracker_app.py`

- Move database code into `database/db_manager.py`.
- Move plotting code into `charts/`.
- Move habit logic into `models/`.
- Keep the root Tkinter window and main loop in the main file.
- Import and use classes/functions from the above modules.

---

## Benefits

- **Readability:** Clear separation of concerns.
- **Maintainability:** Easier to update specific features.
- **Scalability:** Easy to add new features (e.g., notifications, reports).
- **Testing:** Models and business logic can be tested independently.

---

## Next Steps

1. Refactor `habit_tracker_app.py` into the above structure.
2. Add `requirements.txt` (include `tkinter`, `matplotlib`, `sqlite3`).
3. Update `README.md` with setup and usage instructions.
