"""Graphical ETL database explorer for the PostgreSQL-backed ETL pipeline.

This module provides a Tkinter-based user interface that lets the user:
- browse tables loaded by the ETL pipeline
- search by primary key for individual records
- view a customer summary for a selected user

The app connects to PostgreSQL using the same database connection helper
used by the ETL pipeline and displays results in a table grid.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

try:
    from .database import connect
except ImportError:
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from src.database import connect


load_dotenv(Path(__file__).resolve().with_name(".env"))


TABLE_CONFIG = {
    "users": {"pk": "user_id", "label": "Users"},
    "products": {"pk": "product_id", "label": "Products"},
    "sessions": {"pk": "session_id", "label": "Sessions"},
    "interactions": {"pk": "interaction_id", "label": "Interactions"},
    "purchases": {"pk": "purchase_id", "label": "Purchases"},
    "reviews": {"pk": "review_id", "label": "Reviews"},
    "stg_rejects": {"pk": None, "label": "Rejected Rows"},
}


class DatabaseApp(tk.Tk):
    """Tkinter application for browsing ETL database tables and customer summaries.

    The app provides two main views:
    - Table Browser: load and inspect rows from configured database tables
    - Customer 360: look up a user and show profile, purchase, session, and review summaries
    """

    def __init__(self):
        super().__init__()
        self.title("ETL Database Explorer")
        self.geometry("1300x800")
        self.minsize(1100, 700)

        self.table_var = tk.StringVar(value="users")
        self.limit_var = tk.IntVar(value=100)
        self.search_var = tk.StringVar()
        self.customer_id_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        self._build_style()
        self._build_ui()
        self.load_table()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Helvetica", 18, "bold"))
        style.configure("SubHeader.TLabel", font=("Helvetica", 11, "bold"))
        style.configure("Action.TButton", padding=(12, 6))

    def _build_ui(self):
        outer = ttk.Frame(self, padding=16)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 12))

        ttk.Label(header, text="ETL Database Explorer", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Browse PostgreSQL tables, inspect records, and look up a customer summary.",
        ).pack(anchor="w", pady=(4, 0))

        self.notebook = ttk.Notebook(outer)
        self.notebook.pack(fill="both", expand=True)

        self.browser_tab = ttk.Frame(self.notebook, padding=12)
        self.customer_tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.browser_tab, text="Table Browser")
        self.notebook.add(self.customer_tab, text="Customer 360")

        self._build_browser_tab()
        self._build_customer_tab()

        status_bar = ttk.Label(outer, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", pady=(10, 0))

    def _build_browser_tab(self):
        controls = ttk.Frame(self.browser_tab)
        controls.pack(fill="x", pady=(0, 12))

        ttk.Label(controls, text="Table:", style="SubHeader.TLabel").grid(row=0, column=0, sticky="w")
        table_combo = ttk.Combobox(
            controls,
            textvariable=self.table_var,
            values=list(TABLE_CONFIG.keys()),
            state="readonly",
            width=20,
        )
        table_combo.grid(row=0, column=1, padx=(8, 20), sticky="w")
        table_combo.bind("<<ComboboxSelected>>", lambda _event: self._on_table_change())

        ttk.Label(controls, text="Rows:", style="SubHeader.TLabel").grid(row=0, column=2, sticky="w")
        rows_spin = ttk.Spinbox(controls, from_=10, to=1000, increment=10, textvariable=self.limit_var, width=10)
        rows_spin.grid(row=0, column=3, padx=(8, 20), sticky="w")

        ttk.Button(controls, text="Load Table", style="Action.TButton", command=self.load_table).grid(
            row=0, column=4, padx=(0, 8)
        )

        ttk.Label(controls, text="Search value:", style="SubHeader.TLabel").grid(row=1, column=0, pady=(12, 0), sticky="w")
        search_entry = ttk.Entry(controls, textvariable=self.search_var, width=32)
        search_entry.grid(row=1, column=1, columnspan=2, pady=(12, 0), sticky="we")

        ttk.Button(controls, text="Find Record", style="Action.TButton", command=self.search_record).grid(
            row=1, column=4, pady=(12, 0), sticky="w"
        )

        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(2, weight=0)

        tree_frame = ttk.Frame(self.browser_tab)
        tree_frame.pack(fill="both", expand=True)

        self.table_tree = ttk.Treeview(tree_frame, show="headings")
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.table_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.table_tree.xview)
        self.table_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.table_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

    def _build_customer_tab(self):
        top = ttk.Frame(self.customer_tab)
        top.pack(fill="x", pady=(0, 12))

        ttk.Label(top, text="Customer ID:", style="SubHeader.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.customer_id_var, width=30).grid(row=0, column=1, padx=(8, 12), sticky="w")
        ttk.Button(top, text="Load Customer", style="Action.TButton", command=self.load_customer_summary).grid(
            row=0, column=2, sticky="w"
        )
        ttk.Button(top, text="Clear", command=self._clear_customer_summary).grid(row=0, column=3, padx=(8, 0), sticky="w")

        summary_frame = ttk.Frame(self.customer_tab)
        summary_frame.pack(fill="both", expand=True)

        self.customer_text = tk.Text(summary_frame, wrap="word", height=24)
        customer_scroll = ttk.Scrollbar(summary_frame, orient="vertical", command=self.customer_text.yview)
        self.customer_text.configure(yscrollcommand=customer_scroll.set)

        self.customer_text.pack(side="left", fill="both", expand=True)
        customer_scroll.pack(side="right", fill="y")

        self.customer_text.insert("1.0", "Enter a user_id to load customer profile and purchase summary.")
        self.customer_text.configure(state="disabled")

    def _on_table_change(self):
        self.search_var.set("")
        self.load_table()

    def _clear_tree(self):
        self.table_tree.delete(*self.table_tree.get_children())
        self.table_tree["columns"] = ()

    def _format_frame_for_display(self, frame: pd.DataFrame) -> pd.DataFrame:
        formatted = frame.copy()
        for column in formatted.columns:
            if pd.api.types.is_datetime64_any_dtype(formatted[column]):
                formatted[column] = formatted[column].dt.strftime("%Y-%m-%d %H:%M:%S")
        return formatted.fillna("")

    def _run_query(self, query, params=None):
        connection = connect()
        try:
            return pd.read_sql_query(query, connection, params=params)
        finally:
            connection.close()

    def _display_dataframe(self, frame: pd.DataFrame, empty_message: str):
        self._clear_tree()

        if frame.empty:
            self.status_var.set(empty_message)
            return

        display_frame = self._format_frame_for_display(frame)
        self.table_tree["columns"] = list(display_frame.columns)

        for column in display_frame.columns:
            self.table_tree.heading(column, text=column)
            self.table_tree.column(column, width=max(120, min(220, len(column) * 12)), anchor="w")

        for row in display_frame.itertuples(index=False, name=None):
            self.table_tree.insert("", "end", values=row)

        self.status_var.set(f"Loaded {len(display_frame)} rows from {self.table_var.get()}.")

    def load_table(self):
        table_name = self.table_var.get()
        if table_name not in TABLE_CONFIG:
            messagebox.showerror("Invalid table", f"Unknown table: {table_name}")
            return

        try:
            limit = int(self.limit_var.get())
        except tk.TclError:
            messagebox.showerror("Invalid input", "Row limit must be a number.")
            return

        query = f"SELECT * FROM {table_name} LIMIT %s"
        try:
            frame = self._run_query(query, params=[limit])
            self._display_dataframe(frame, f"No rows found in {table_name}.")
        except Exception as exc:
            messagebox.showerror("Database error", str(exc))
            self.status_var.set("Unable to load table data.")

    def search_record(self):
        table_name = self.table_var.get()
        pk_column = TABLE_CONFIG.get(table_name, {}).get("pk")

        if not pk_column:
            messagebox.showinfo("Search unavailable", "The selected table does not have a primary-key search configured.")
            return

        search_value = self.search_var.get().strip()
        if not search_value:
            messagebox.showwarning("Missing value", "Enter a value to search for.")
            return

        query = f"SELECT * FROM {table_name} WHERE {pk_column} = %s LIMIT 100"

        try:
            frame = self._run_query(query, params=[search_value])
            self._display_dataframe(frame, f"No record found in {table_name} for {pk_column} = {search_value}.")
        except Exception as exc:
            messagebox.showerror("Database error", str(exc))
            self.status_var.set("Search failed.")

    def _clear_customer_summary(self):
        self.customer_text.configure(state="normal")
        self.customer_text.delete("1.0", "end")
        self.customer_text.insert("1.0", "Enter a user_id to load customer profile and purchase summary.")
        self.customer_text.configure(state="disabled")

    def load_customer_summary(self):
        user_id = self.customer_id_var.get().strip()
        if not user_id:
            messagebox.showwarning("Missing value", "Enter a user_id first.")
            return

        try:
            user_frame = self._run_query(
                "SELECT user_id, age, gender, country, city, signup_date, income_level, preferred_category, loyalty_tier "
                "FROM users WHERE user_id = %s",
                params=[user_id],
            )
            purchase_summary = self._run_query(
                """
                SELECT
                    COUNT(*) AS num_purchases,
                    COALESCE(SUM(total_amount), 0) AS total_spend,
                    COALESCE(AVG(total_amount), 0) AS avg_order_value,
                    COALESCE(SUM(quantity), 0) AS total_items
                FROM purchases
                WHERE user_id = %s
                """,
                params=[user_id],
            )
            session_summary = self._run_query(
                "SELECT COUNT(*) AS num_sessions, COALESCE(SUM(CASE WHEN is_converted THEN 1 ELSE 0 END), 0) AS converted_sessions FROM sessions WHERE user_id = %s",
                params=[user_id],
            )
            review_summary = self._run_query(
                "SELECT COUNT(*) AS num_reviews, COALESCE(AVG(rating), 0) AS avg_rating FROM reviews WHERE user_id = %s",
                params=[user_id],
            )
        except Exception as exc:
            messagebox.showerror("Database error", str(exc))
            self.status_var.set("Customer lookup failed.")
            return

        if user_frame.empty:
            messagebox.showinfo("Not found", f"No user found for user_id = {user_id}.")
            self._clear_customer_summary()
            self.status_var.set("Customer not found.")
            return

        user_info = self._format_frame_for_display(user_frame).iloc[0].to_dict()
        purchases = purchase_summary.iloc[0].to_dict()
        sessions = session_summary.iloc[0].to_dict()
        reviews = review_summary.iloc[0].to_dict()

        report_lines = [
            f"Customer profile for {user_id}",
            "",
            "User information:",
        ]
        for key, value in user_info.items():
            report_lines.append(f"  {key}: {value}")

        report_lines.extend(
            [
                "",
                "Purchase summary:",
            ]
        )
        for key, value in purchases.items():
            report_lines.append(f"  {key}: {value}")

        report_lines.extend(
            [
                "",
                "Session summary:",
            ]
        )
        for key, value in sessions.items():
            report_lines.append(f"  {key}: {value}")

        report_lines.extend(
            [
                "",
                "Review summary:",
            ]
        )
        for key, value in reviews.items():
            report_lines.append(f"  {key}: {value}")

        self.customer_text.configure(state="normal")
        self.customer_text.delete("1.0", "end")
        self.customer_text.insert("1.0", "\n".join(report_lines))
        self.customer_text.configure(state="disabled")
        self.status_var.set(f"Loaded customer summary for {user_id}.")


def main():
    app = DatabaseApp()
    app.mainloop()


if __name__ == "__main__":
    main()