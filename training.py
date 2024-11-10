'''
App für das Trainingstagebuch.
'''
import os
import sys
import enum
from datetime import datetime
import signal
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
import pandas as pd

console = Console()
log = logging.getLogger("rich")

FORMAT = '%(message)s'
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            tracebacks_suppress=True,
        )
    ]
)


def cleanup():
    '''Aufräumen'''
    sys.exit(0)


def signal_handler(sig, frame):
    '''Signal Handler'''
    if sig == signal.SIGINT:
        console.print("Schließe Trainingstagebuch...", style="magenta")
    elif sig == signal.SIGTERM:
        log.error("Schließe Trainingstagebuch...")
    cleanup()


# Signal Handler für SIGINT (triggered by STRG+C) und SIGTERM (Terminiation Request) registrieren
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class Trainingsart(enum.Enum):
    '''Enum für die verschiedenen Trainingsarten'''
    LIEGESTUETZ = "Liegestütz"
    SITUP = "Situp"


def read_data(file_path) -> pd.DataFrame:
    '''Lesen der Daten aus dem Trainingstagebuch mit Pandas'''
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        df['Datum'] = pd.to_datetime(
            df['Datum'], format='mixed', dayfirst=True)
        return df
    except FileNotFoundError:
        console.print(Panel("Trainingsdaten nicht vorhanden!",
                      title="Error", style="red"))
        signal_handler(signal.SIGTERM, None)
        return pd.DataFrame()


def filter_current_date(df_in):
    '''Filtern der Daten nach dem aktuellen Datum'''
    current_date = datetime.now().strftime('%Y-%m-%d')
    return df_in[df_in['Datum'].dt.strftime('%Y-%m-%d') == current_date]


def filter_by_week(df_in):
    '''Filtern der Daten nach der aktuellen Woche'''
    current_week = datetime.now().isocalendar()[1]
    console.print("Aktuelle Woche: ",
                  f"[blue]{current_week}[/blue]")
    df_in['Week'] = df_in['Datum'].dt.isocalendar().week
    return df_in[df_in['Week'] == current_week]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def input_reps() -> int:
    '''Summe der Wiederholungen einfügen'''
    error = "Ungültige Eingabe: Wert muss eine Zahl sein zwischen 1 und 200"
    try:
        if (val_from_input :=
                int(input(
                    'Anzahl der Wiederholungen eintragen: '))
            ) <= 0 or val_from_input > 200:
            log.error(error)
            return 0
        return val_from_input
    except ValueError:
        log.error(error)
    except KeyboardInterrupt:
        print("\n")
        signal_handler(signal.SIGTERM, None)
    except EOFError:
        log.error(error)
    return 0


def input_date() -> str:
    '''Datum einfügen'''
    current_dt = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    try:
        if datetime.strptime(val_from_input := input('Datum eintragen (T,M): '), '%d,%m' if val_from_input else ''):
            if val_from_input == '':
                return current_dt
            current_year = datetime.now().year
            return datetime.strptime(val_from_input, '%d,%m').replace(
                year=current_year).strftime('%d.%m.%Y 00:00:00')
    except ValueError as e:
        log.warning(e)
    except KeyboardInterrupt:
        print("\n")
        signal_handler(signal.SIGTERM, None)
    except EOFError as e:
        log.warning(e)
    return current_dt


def write_data(file_path, anzahl_reps, datum_reps=None) -> None:
    '''Schreiben der Daten in das Traningstagebuch'''
    if anzahl_reps == 0:
        return
    # Werte in das CSV schreiben
    data = {
        "Datum": datum_reps,
        "Art": Trainingsart.LIEGESTUETZ.value,
        "Wiederholung": anzahl_reps
    }
    # Schreiben der Daten in das CSV
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            if not file.read(1):
                file.write("Datum,Art,Wiederholung\n")

        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(
                f"{data['Datum']},{data['Art']},{data['Wiederholung']}\n")
    except OSError as e:
        log.error(e)
        signal_handler(signal.SIGTERM, None)


def print_data(data):
    '''Ausgabe der Daten'''
    data = data.sort_values('Datum')
    data['Datum'] = pd.to_datetime(data['Datum'])
    table = Table(show_header=True, header_style="magenta")
    for col in data.columns:
        table.add_column(col)
    df = data.astype(str).copy()
    for row in df.itertuples(index=False):
        table.add_row(*row)
    console.print(table)


def main(file_path: str) -> None:
    '''Hauptfunktion'''

    df_all = read_data(file_path)
    filtered_week = filter_by_week(df_all)
    console.print("Gesamt diese Woche:",
                  f"[blue]{filtered_week['Wiederholung'].sum()}[/blue]")

    reps = input_reps()
    if reps == 0:
        return
    write_data(file_path, reps, input_date())
    df_all = read_data(file_path)
    filtered_data = filter_current_date(df_all)
    print_data(filtered_data)
    console.print(
        "Total heute:", f"[blue]{filtered_data['Wiederholung'].sum()}[/blue]")


def init() -> None:
    '''Initialisierung'''
    console.print("Starte Trainingstagebuch...", style="magenta")
    console.print("Trainingstagebuch: Schließen mit STRG+C", style="magenta")


if __name__ == "__main__":

    try:
        data_path = resource_path('training_data.csv')
        init()
        while True:
            main(data_path)
    except KeyboardInterrupt as e:
        console.print(e)
        signal_handler(signal.SIGINT, None)
