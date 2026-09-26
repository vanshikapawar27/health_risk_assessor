"""
AI-Powered Personal Health Risk Assessor
==========================================
A CLI tool that uses ML to assess daily health risk based on lifestyle inputs.
Tracks history, shows trends, and provides personalized recommendations.

Author: BYOP Project
"""

import asyncio
import json
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from assessor import HealthAssessor
from data_manager import DataManager
from recommender import Recommender

console = Console()


def print_banner():
    console.print(Panel.fit(
        "[bold green]🩺 AI-Powered Personal Health Risk Assessor[/bold green]\n"
        "[dim]Track daily habits · Predict risk · Stay ahead of your health[/dim]",
        border_style="green"
    ))


def get_user_inputs() -> dict:
    """Collect lifestyle metrics from the user via CLI."""
    console.print("\n[bold cyan]📋 Daily Health Check-In[/bold cyan]\n")

    def ask_float(prompt, min_val, max_val):
        while True:
            try:
                val = float(console.input(f"  [yellow]{prompt}[/yellow]: "))
                if min_val <= val <= max_val:
                    return val
                console.print(f"  [red]Please enter a value between {min_val} and {max_val}[/red]")
            except ValueError:
                console.print("  [red]Invalid input. Please enter a number.[/red]")

    def ask_int(prompt, min_val, max_val):
        while True:
            try:
                val = int(console.input(f"  [yellow]{prompt}[/yellow]: "))
                if min_val <= val <= max_val:
                    return val
                console.print(f"  [red]Please enter a value between {min_val} and {max_val}[/red]")
            except ValueError:
                console.print("  [red]Invalid input. Please enter an integer.[/red]")

    data = {
        "age":            ask_int("Age (years) [1-120]", 1, 120),
        "bmi":            ask_float("BMI [10.0-60.0]", 10.0, 60.0),
        "sleep_hours":    ask_float("Sleep last night (hours) [0-24]", 0, 24),
        "steps":          ask_int("Steps walked today [0-50000]", 0, 50000),
        "water_ml":       ask_int("Water intake today (ml) [0-5000]", 0, 5000),
        "stress_level":   ask_int("Stress level [1=low, 10=extreme]", 1, 10),
        "heart_rate":     ask_int("Resting heart rate (bpm) [40-200]", 40, 200),
        "diet_quality":   ask_int("Diet quality today [1=poor, 10=excellent]", 1, 10),
        "exercise_mins":  ask_int("Exercise duration today (minutes) [0-300]", 0, 300),
        "screen_hours":   ask_float("Screen time today (hours) [0-24]", 0, 24),
        "smoking":        ask_int("Smoking (cigarettes today) [0-60]", 0, 60),
        "alcohol_units":  ask_int("Alcohol units today [0=none, 1=1 unit, etc.] [0-20]", 0, 20),
    }

    return data


def display_results(risk_label: str, risk_prob: dict, inputs: dict, recommendations: list):
    """Display assessment results in a rich formatted view."""

    color_map = {"Low": "green", "Medium": "yellow", "High": "red"}
    color = color_map.get(risk_label, "white")

    console.print()
    console.print(Panel(
        f"[bold {color}]Risk Level: {risk_label.upper()}[/bold {color}]\n\n"
        f"[dim]Low: {risk_prob['Low']:.1%}  |  "
        f"Medium: {risk_prob['Medium']:.1%}  |  "
        f"High: {risk_prob['High']:.1%}[/dim]",
        title="[bold]🔍 Assessment Result[/bold]",
        border_style=color
    ))

    # Input summary table
    table = Table(title="📊 Today's Metrics", box=box.ROUNDED, border_style="blue")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="white")
    table.add_column("Status", justify="center")

    status_rules = {
        "bmi": lambda v: "✅" if 18.5 <= v <= 24.9 else ("⚠️" if v < 18.5 or v <= 29.9 else "🔴"),
        "sleep_hours": lambda v: "✅" if 7 <= v <= 9 else ("⚠️" if 6 <= v < 7 else "🔴"),
        "steps": lambda v: "✅" if v >= 8000 else ("⚠️" if v >= 5000 else "🔴"),
        "water_ml": lambda v: "✅" if v >= 2000 else ("⚠️" if v >= 1500 else "🔴"),
        "stress_level": lambda v: "✅" if v <= 3 else ("⚠️" if v <= 6 else "🔴"),
        "heart_rate": lambda v: "✅" if 60 <= v <= 100 else ("⚠️" if 50 <= v <= 110 else "🔴"),
        "diet_quality": lambda v: "✅" if v >= 7 else ("⚠️" if v >= 5 else "🔴"),
        "exercise_mins": lambda v: "✅" if v >= 30 else ("⚠️" if v >= 15 else "🔴"),
        "screen_hours": lambda v: "✅" if v <= 4 else ("⚠️" if v <= 7 else "🔴"),
        "smoking": lambda v: "✅" if v == 0 else "🔴",
        "alcohol_units": lambda v: "✅" if v == 0 else ("⚠️" if v <= 2 else "🔴"),
    }

    labels = {
        "age": "Age", "bmi": "BMI", "sleep_hours": "Sleep (hrs)",
        "steps": "Steps", "water_ml": "Water (ml)", "stress_level": "Stress (1-10)",
        "heart_rate": "Heart Rate (bpm)", "diet_quality": "Diet Quality (1-10)",
        "exercise_mins": "Exercise (mins)", "screen_hours": "Screen Time (hrs)",
        "smoking": "Cigarettes", "alcohol_units": "Alcohol Units"
    }

    for key, label in labels.items():
        val = inputs[key]
        status = status_rules.get(key, lambda v: "—")(val)
        table.add_row(label, str(val), status)

    console.print(table)

    # Recommendations
    if recommendations:
        console.print("\n[bold magenta]💡 Personalized Recommendations:[/bold magenta]")
        for i, rec in enumerate(recommendations, 1):
            console.print(f"  [white]{i}.[/white] {rec}")


async def show_trend(data_manager: DataManager):
    """Show historical risk trend."""
    history = await data_manager.load_history()
    if not history:
        console.print("[dim]No history yet. Complete your first assessment![/dim]")
        return

    console.print("\n[bold cyan]📈 Your Risk Trend (Last 7 entries)[/bold cyan]\n")
    table = Table(box=box.SIMPLE, border_style="cyan")
    table.add_column("Date", style="dim")
    table.add_column("Risk Level", justify="center")
    table.add_column("BMI")
    table.add_column("Sleep")
    table.add_column("Steps")
    table.add_column("Stress")

    color_map = {"Low": "green", "Medium": "yellow", "High": "red"}
    for entry in history[-7:]:
        risk = entry.get("risk_label", "—")
        color = color_map.get(risk, "white")
        table.add_row(
            entry.get("date", "—"),
            f"[{color}]{risk}[/{color}]",
            str(entry.get("bmi", "—")),
            str(entry.get("sleep_hours", "—")),
            str(entry.get("steps", "—")),
            str(entry.get("stress_level", "—")),
        )

    console.print(table)


async def main():
    print_banner()

    assessor = HealthAssessor()
    data_manager = DataManager()
    recommender = Recommender()

    while True:
        console.print("\n[bold]What would you like to do?[/bold]")
        console.print("  [cyan]1.[/cyan] 🩺 New Health Assessment")
        console.print("  [cyan]2.[/cyan] 📈 View My Risk History")
        console.print("  [cyan]3.[/cyan] ❌ Exit")

        choice = console.input("\n  [yellow]Enter choice (1/2/3)[/yellow]: ").strip()

        if choice == "1":
            inputs = get_user_inputs()

            with Progress(SpinnerColumn(), TextColumn("[cyan]Analyzing your data..."), transient=True) as progress:
                progress.add_task("", total=None)
                await asyncio.sleep(1.2)  # simulate async model inference
                risk_label, risk_prob = assessor.predict(inputs)
                recommendations = recommender.generate(inputs, risk_label)

            display_results(risk_label, risk_prob, inputs, recommendations)
            await data_manager.save_entry(inputs, risk_label)
            console.print("\n[dim green]✅ Entry saved to history.[/dim green]")

        elif choice == "2":
            await show_trend(data_manager)

        elif choice == "3":
            console.print("\n[bold green]Stay healthy! 💪 Goodbye.[/bold green]\n")
            break

        else:
            console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")


if __name__ == "__main__":
    asyncio.run(main())
