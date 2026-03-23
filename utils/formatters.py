def format_money(amount):
    if amount is None:
        return "$ 0"
    return f"${amount:,.0f}".replace(",", ".")

def crear_resumen_carrito(carrito, descuento_tipo=None):
    if not carrito:
        return "🛒 Carrito vacío", 0, 0, 0
    
    texto = "🛒 *TU CARRITO*\n\n"
    subtotal = 0
    
    for i, item in enumerate(carrito, 1):
        item_total = item['precio'] * item['cantidad']
        subtotal += item_total
        texto += f"{i}. *{item['nombre']}*\n"
        texto += f"   `{item['cantidad']} x {format_money(item['precio'])}` = *{format_money(item_total)}*\n\n"
    
    descuento = 0
    if descuento_tipo == 'efectivo':
        descuento = subtotal * 0.10
        texto += "💵 Descuento efectivo (10%): " + format_money(descuento) + "\n"
    elif descuento_tipo == 'transferencia':
        descuento = subtotal * 0.05
        texto += "📲 Descuento transferencia (5%): " + format_money(descuento) + "\n"
    
    total = subtotal - descuento
    texto += f"💰 *Subtotal:* {format_money(subtotal)}\n"
    if descuento > 0:
        texto += f"🏷️ *Descuento:* -{format_money(descuento)}\n"
    texto += f"💵 *TOTAL:* `{format_money(total)}`"
    
    return texto, subtotal, descuento, total
