'''Auswertung der Trainingsdaten'''
import logging
import pandas as pd
import matplotlib.pyplot as plt
from training import read_data, resource_path

# Logging Konfiguration 
# Hier sollen die Warnungen von matplotlib und PIL unterdrückt werden.
logging.getLogger("matplotlib").setLevel(logging.ERROR)
logging.getLogger('PIL').setLevel(logging.WARNING)

def run_auswertung():
    '''Auswertung der Daten'''
    plt.clf()
    df: pd.DataFrame = read_data(resource_path('training_data.csv'))
    df['Week'] = df['Datum'].dt.isocalendar().week
    df_week = df.groupby(df['Week'])['Wiederholung'].sum()
    print("Summe gesamt: ", df["Wiederholung"].sum())
    print("Summe pro Monat: ", df.groupby(
        df['Datum'].dt.strftime('%B'))['Wiederholung'].sum())
    print(df_week)
    df_week.plot(kind='bar',
                 xlabel='Kalenderwoche',
                 ylabel='Wiederholungen',
                 title='Wiederholungen pro Woche')
    plt.show()


if __name__ == "__main__":

    run_auswertung()
