import os
import threading
import time
from flask import Flask, render_template, redirect, url_for
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

url = 'https://docs.google.com/spreadsheets/d/1Mu6z8g0m0LhjGmEszyXIdiNMegUCRqCgULBoEMq42RI/export?format=csv'

graficas = [
    'static/grafica1.png',
    'static/grafica2.png',
    'static/grafica3.png',
    'static/grafica4.png'
]

def generar_graficas(df=None):
    if df is None:
        df = pd.read_csv(url)

    sns.set_theme(style="darkgrid")

    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='age', hue='sex', kde=True, multiple='stack')
    plt.title("Distribución de edades por sexo")
    plt.savefig(graficas[0])
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x='class', hue='survived')
    plt.title("Supervivencia por clase")
    plt.savefig(graficas[1])
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=df, x='pclass', y='fare')
    plt.title("Distribución de tarifas por clase")
    plt.savefig(graficas[2])
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.violinplot(data=df, x='sex', y='age', hue='survived', split=True)
    plt.title("Edad por sexo y supervivencia")
    plt.savefig(graficas[3])
    plt.close()

def actualizar_graficas():
    try:
        df = pd.read_csv(url)
        for grafica in graficas:
            if os.path.exists(grafica):
                os.remove(grafica)
        generar_graficas(df)
        print("Gráficas actualizadas manualmente.")
    except Exception as e:
        print(f"Error al actualizar gráficas: {e}")

def actualizar_periodicamente():
    while True:
        actualizar_graficas()
        time.sleep(3600)  # cada hora

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisis2')
def analisis2():
    return render_template('analisis2.html')

@app.route('/actualizar')
def actualizar():
    actualizar_graficas()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not all(os.path.exists(g) for g in graficas):
        generar_graficas()

    threading.Thread(target=actualizar_periodicamente, daemon=True).start()
   
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


