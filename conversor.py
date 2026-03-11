import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuración de Frankfurter API
BASE_URL = "https://api.frankfurter.app"

def get_available_currencies():
    """Obtiene la lista de monedas disponibles dinámicamente."""
    try:
        response = requests.get(f"{BASE_URL}/currencies")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching currencies: {e}")
        return None

def convert_currency(from_curr, to_curr, amount):
    """Realiza la conversión de moneda y obtiene la tasa y fecha."""
    try:
        url = f"{BASE_URL}/latest?amount={amount}&from={from_curr}&to={to_curr}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        result = data['rates'][to_curr]
        rate = result / float(amount)
        date = data['date']
        
        return {
            'result': round(result, 2),
            'rate': round(rate, 4),
            'date': date
        }
    except Exception as e:
        print(f"Error converting currency: {e}")
        return None

def generate_history_chart(from_curr, to_curr):
    """Genera un gráfico de los últimos 30 días y lo devuelve en base64."""
    try:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        url = f"{BASE_URL}/{start_date}..{end_date}?from={from_curr}&to={to_curr}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        rates_data = data['rates']
        dates = sorted(rates_data.keys())
        values = [rates_data[date][to_curr] for date in dates]
        
        if not values:
            return None

        # Crear el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(dates, values, marker='o', linestyle='-', color='#4a90e2', linewidth=2, markersize=4)
        
        # Encontrar min y max
        min_val = min(values)
        max_val = max(values)
        min_idx = values.index(min_val)
        max_idx = values.index(max_val)
        
        # Marcar min y max
        plt.plot(dates[min_idx], min_val, 'ro', label=f'Mín: {min_val:.4f}')
        plt.plot(dates[max_idx], max_val, 'go', label=f'Máx: {max_val:.4f}')
        
        plt.title(f"Evolución {from_curr} a {to_curr} (Últimos 30 días)")
        plt.xlabel("Fecha")
        plt.ylabel("Tasa de Cambio")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return img_base64
    except Exception as e:
        print(f"Error generating chart: {e}")
        return None

@app.route('/')
def index():
    currencies = get_available_currencies()
    if currencies is None:
        return redirect(url_for('error_page'))
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    from_curr = request.form.get('from_curr')
    to_curr = request.form.get('to_curr')
    amount = request.form.get('amount')
    
    if not amount or not from_curr or not to_curr:
        return redirect(url_for('index'))
    
    # Manejar caso donde origen y destino son iguales
    if from_curr == to_curr:
        result_data = {
            'result': round(float(amount), 2),
            'rate': 1.0,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
    else:
        result_data = convert_currency(from_curr, to_curr, amount)
    
    if result_data is None:
        return redirect(url_for('error_page'))
    
    chart_url = generate_history_chart(from_curr, to_curr)
    
    return render_template('resultado.html', 
                           result=result_data['result'], 
                           rate=result_data['rate'], 
                           date=result_data['date'], 
                           from_curr=from_curr, 
                           to_curr=to_curr, 
                           amount=amount,
                           chart_url=chart_url)

@app.route('/error')
def error_page():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
