# Conversor de Monedas con Flask

## Descripción

Aplicación web desarrollada con **Python y Flask** que permite convertir valores entre diferentes monedas utilizando tasas de cambio en tiempo real obtenidas desde la **API Frankfurter**. La aplicación permite seleccionar la moneda de origen, la moneda destino y la cantidad a convertir, mostrando el resultado junto con la tasa de cambio actual.

---

## Requisitos

Antes de ejecutar el proyecto se necesita:

* Python 3.8 o superior
* pip
* Conexión a internet

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/conversor-monedas-flask.git
```

2. Entrar a la carpeta del proyecto:

```bash
cd conversor-monedas-flask
```

3. Instalar las dependencias necesarias:

```bash
pip install flask requests matplotlib
```

---

## Ejecución

Para iniciar la aplicación ejecutar:

```bash
python conversor.py
```

Después abrir el navegador en:

```
http://localhost:5000
```

---

## Uso

1. Seleccionar la **moneda de origen**.
2. Seleccionar la **moneda destino**.
3. Introducir la **cantidad a convertir**.
4. Presionar el botón **Convertir** para obtener el resultado.

La aplicación mostrará el monto convertido, la tasa de cambio utilizada y un gráfico con el historial del tipo de cambio de los últimos días.

---

## Tecnologías utilizadas

* Python
* Flask
* Requests
* Matplotlib
* HTML
* CSS
* API Frankfurter

---

## Autor

Proyecto académico desarrollado como práctica de **consumo de APIs REST con Flask** y visualización de datos en aplicaciones web.

