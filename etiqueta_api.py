from flask import Flask, request, send_file
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/etiqueta')
def generar_etiqueta():
    producto = request.args.get('producto')
    lote = request.args.get('lote')
    entrada = request.args.get('entrada')
    caducidad = request.args.get('caducidad')
    ubicacion = request.args.get('ubicacion')
    cantidad = request.args.get('cantidad')

    # Generar código QR
    qr_data = f"Lote: {lote}\nProducto: {producto}\nCad: {caducidad}"
    qr = qrcode.make(qr_data).resize((250, 250))

    # Crear lienzo
    etiqueta = Image.new('RGB', (600, 300), color='white')
    draw = ImageDraw.Draw(etiqueta)

    # Cargar fuente del sistema o usar predeterminada
    try:
        font = ImageFont.truetype("arial.ttf", size=18)
    except:
        font = ImageFont.load_default()

    # Añadir texto
    draw.text((10, 10), f"Producto: {producto}", fill="black", font=font)
    draw.text((10, 40), f"Lote: {lote}", fill="black", font=font)
    draw.text((10, 70), f"Entrada: {entrada}", fill="black", font=font)
    draw.text((10, 100), f"Caducidad: {caducidad}", fill="black", font=font)
    draw.text((10, 130), f"Ubicación: {ubicacion}", fill="black", font=font)
    draw.text((10, 160), f"Cantidad: {cantidad}", fill="black", font=font)

    # Insertar QR
    etiqueta.paste(qr, (330, 20))

    # Exportar como imagen
    output = io.BytesIO()
    etiqueta.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')

# 🚀 Ejecutar la app

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


    app.run(debug=True)
