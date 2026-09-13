from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

COLORES_HEX = {
    "Blanco": "#FFFFFF",
    "Negro": "#000000",
    "Azul": "#0057B8",
    "Azul Marino": "#1F3A5F",
    "Azul Claro": "#7EC8E3",
    "Turquesa": "#30D5C8",
    "Rojo": "#CC0000",
    "Terracota": "#E2725B",
    "Gris": "#808080",
    "Verde": "#008000",
    "Rosa": "#FF69B4"
}

@app.route("/")
def inicio():

    archivo_excel = os.path.join(
        os.path.dirname(__file__),
        "MenSecrets_Inventario_v1.xlsx"
    )

    df = pd.read_excel(
        archivo_excel,
        sheet_name="PRODUCTOS"
    )

    productos = []

    for _, fila in df.iterrows():

        activo = str(
            fila["Activo"]
        ).strip().upper()

        if activo != "SI":
            continue

        if int(fila["Stock"]) <= 0:
            continue

        colores = []

        for color in str(
            fila["Colores"]
        ).split(","):

            color = color.strip()

            colores.append({
                "nombre": color,
                "hex": COLORES_HEX.get(
                    color,
                    "#CCCCCC"
                )
            })

        producto = {
            "sku": str(fila["SKU"]),
            "categoria": str(fila["Categoría"]),
            "nombre": str(fila["Nombre"]),
            "marca": str(fila["Marca"]),
            "precio": float(fila["Precio"]),
            "stock": int(fila["Stock"]),
            "foto": str(fila["Foto"]),
            "descripcion": str(fila["Descripción"]),
            "promo": str(fila["Promo2x24"]).strip().upper(),
            "tallas": [
                t.strip()
                for t in str(
                    fila["Tallas"]
                ).split(",")
            ],
            "colores": colores
        }

        productos.append(producto)

    categorias = sorted(
        list(
            set(
                p["categoria"]
                for p in productos
            )
        )
    )

    return render_template(
        "index.html",
        productos=productos,
        categorias=categorias
    )

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )