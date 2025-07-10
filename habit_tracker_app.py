import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import date, datetime, timedelta
import sqlite3
import matplotlib.pyplot as plt
import random

# ---------- Database Setup ----------
conn = sqlite3.connect("habits.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    log_date TEXT,
    done INTEGER,
    UNIQUE(habit_id, log_date)
)
""")
conn.commit()

# ---------- Quotes ----------
quotes = [
    "Keep going, you're doing great!",
    "Small steps lead to big changes.",
    "Progress over perfection.",
    "Stay consistent, not perfect.",
    "You’re one day closer to your goal!"
]


# ---------- Main App ----------
class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Habit Tracker")
        self.root.geometry("700x550")

        # Gradient Background Canvas
        self.bg_canvas = tk.Canvas(root, width=700, height=550)
        self.bg_canvas.pack(fill="both", expand=True)
        self.draw_gradient()

        # Content Frame
        self.content_frame = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
        self.bg_canvas.create_window(350, 275, window=self.content_frame)

        # Title
        title = tk.Label(self.content_frame, text="📘 Daily Habit Tracker", font=("Helvetica", 18, "bold"), bg="#ffffff")
        title.pack(pady=10)

        self.habit_listbox = tk.Listbox(self.content_frame, width=50, height=10, font=("Arial", 12))
        self.habit_listbox.pack(pady=10)

        # Buttons
        buttons = [
            ("➕ Add Habit", self.add_habit),
            ("✅ Mark as Done", self.mark_done),
            ("📊 View Weekly Progress", self.view_progress),
            ("📈 Show Chart", self.show_chart),
            ("📆 Calendar Heatmap", self.show_calendar),  # New
            ("🔄 Refresh", self.refresh),
        ]

        for text, command in buttons:
            btn = tk.Button(self.content_frame, text=text, command=command, width=30,
                            font=("Arial", 11, "bold"), bg="#4CAF50", fg="white")
            btn.pack(pady=5)

        self.refresh()
        self.show_daily_reminder()
        self.schedule_reminder()

    def draw_gradient(self):
        for i in range(0, 550):
            r = int(255 - (i / 3))
            g = int(230 - (i / 4))
            b = 255
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.bg_canvas.create_line(0, i, 700, i, fill=color)

    def refresh(self):
        self.habit_listbox.delete(0, tk.END)
        cursor.execute("SELECT id, name FROM habits")
        for habit_id, name in cursor.fetchall():
            today = date.today().isoformat()
            cursor.execute("SELECT done FROM habit_logs WHERE habit_id=? AND log_date=?", (habit_id, today))
            result = cursor.fetchone()
            status = "✅" if result and result[0] == 1 else "❌"
            self.habit_listbox.insert(tk.END, f"{name} - {status}")

    def add_habit(self):
        name = simpledialog.askstring("Habit Name", "Enter habit name:")
        if not name:
            return
        desc = simpledialog.askstring("Description", "Enter description (optional):")
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO habits (name, description, created_at) VALUES (?, ?, ?)", (name, desc, today))
        conn.commit()
        self.refresh()

    def mark_done(self):
        index = self.habit_listbox.curselection()
        if not index:
            messagebox.showinfo("No Selection", "Please select a habit.")
            return

        cursor.execute("SELECT id FROM habits")
        habits = cursor.fetchall()
        habit_id = habits[index[0]][0]

        today = date.today().isoformat()
        cursor.execute("""
            INSERT OR REPLACE INTO habit_logs (habit_id, log_date, done)
            VALUES (?, ?, 1)
        """, (habit_id, today))
        conn.commit()
        messagebox.showinfo("Great Job!", random.choice(quotes))
        self.refresh()

    def view_progress(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("📊 Weekly Habit Progress")
        result_window.geometry("450x300")

        tree = ttk.Treeview(result_window, columns=("Habit", "Done (Last 7 Days)"), show='headings')
        tree.heading("Habit", text="Habit")
        tree.heading("Done (Last 7 Days)", text="Days Done")
        tree.pack(fill=tk.BOTH, expand=True)

        cursor.execute("SELECT id, name FROM habits")
        for habit_id, name in cursor.fetchall():
            past_7 = [(date.today() - timedelta(days=i)).isoformat() for i in range(7)]
            cursor.execute(f"""
                SELECT COUNT(*) FROM habit_logs
                WHERE habit_id = ? AND log_date IN ({','.join('?'*7)}) AND done = 1
            """, (habit_id, *past_7))
            count = cursor.fetchone()[0]
            tree.insert("", tk.END, values=(name, f"{count}/7"))

    def show_chart(self):
        cursor.execute("SELECT id, name FROM habits")
        habits = cursor.fetchall()

        habit_names = []
        done_counts = []

        for habit_id, name in habits:
            cursor.execute("SELECT COUNT(*) FROM habit_logs WHERE habit_id=? AND done=1", (habit_id,))
            count = cursor.fetchone()[0]
            habit_names.append(name)
            done_counts.append(count)

        if not habit_names:
            messagebox.showinfo("No Data", "Add and mark habits to view chart.")
            return

        plt.figure(figsize=(8, 4))
        plt.bar(habit_names, done_counts, color='teal')
        plt.title("Habit Completion Count")
        plt.ylabel("Days Completed")
        plt.xlabel("Habits")
        plt.tight_layout()
        plt.show()

    def show_calendar(self):
        index = self.habit_listbox.curselection()
        if not index:
            messagebox.showwarning("Select Habit", "Please select a habit to view its calendar heatmap.")
            return

        cursor.execute("SELECT id, name FROM habits")
        habits = cursor.fetchall()
        habit_id, habit_name = habits[index[0]]

        days = [date.today() - timedelta(days=i) for i in range(29, -1, -1)]
        done_days = []
        for d in days:
            cursor.execute("SELECT done FROM habit_logs WHERE habit_id = ? AND log_date = ?", (habit_id, d.isoformat()))
            row = cursor.fetchone()
            done_days.append(1 if row and row[0] == 1 else 0)

        # 5 weeks × 6 days layout
        matrix = [done_days[i:i+6] for i in range(0, len(done_days), 6)]

        fig, ax = plt.subplots()
        im = ax.imshow(matrix, cmap='Greens', aspect='auto')
        ax.set_title(f"{habit_name} - Last 30 Days", fontsize=14)
        ax.set_xticks(range(6))
        ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        ax.set_yticks(range(len(matrix)))
        ax.set_yticklabels([f"Week {i+1}" for i in range(len(matrix))])

        plt.colorbar(im, ax=ax, label='Done (0 = No, 1 = Yes)')
        plt.tight_layout()
        plt.show()

    def show_daily_reminder(self):
        messagebox.showinfo("⏰ Daily Reminder", random.choice(quotes))

    def schedule_reminder(self):
        self.root.after(3600000, self.reminder_callback)  # 1 hour

    def reminder_callback(self):
        self.show_daily_reminder()
        self.schedule_reminder()


# ---------- Run App ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()
