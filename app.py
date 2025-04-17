import os
from flask import Flask, render_template
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

url = 'https://docs.google.com/spreadsheets/d/1Mu6z8g0m0LhjGmEszyXIdiNMegUCRqCgULBoEMq42RI/export?format=csv'


def generar_graficas(df=None):
#    df = sns.load_dataset('titanic')
    if df is None:
        df = pd.read_csv(url)

    sns.set_theme(style="darkgrid")

    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='age', hue='sex', kde=True, multiple='stack')
    plt.title("Distribución de edades por sexo")
    plt.savefig('static/grafica1.png')
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x='class', hue='survived')
    plt.title("Supervivencia por clase")
    plt.savefig('static/grafica2.png')
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=df, x='pclass', y='fare')
    plt.title("Distribución de tarifas por clase")
    plt.savefig('static/grafica3.png')
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.violinplot(data=df, x='sex', y='age', hue='survived', split=True)
    plt.title("Edad por sexo y supervivencia")
    plt.savefig('static/grafica4.png')
    plt.close()

@app.route('/')
def index():
    try:
        df = pd.read_csv(url)
        generar_graficas(df)

    except Exception as e:
        print(f"Error al leer el CSV: {e}")
    return render_template('index.html')

@app.route('/analisis2')
def analisis2():
    return render_template('analisis2.html')

if __name__ == '__main__':
    generar_graficas()
    port = int(os.environ.get('PORT', 5000))  # Render usa PORT
    app.run(host='0.0.0.0', port=port, debug=True)
