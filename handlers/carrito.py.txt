from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.sheets_service import sheets
from utils.formatters import crear_resumen_carrito, format_money

async def agregar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    cantidad = int(query.data.replace('add_', ''))
    producto = context.user_data.get('producto_actual')
    
    if not producto:
        return
    
    check = sheets.check_stock(producto['sku'], cantidad)
    if not check.get('disponible'):
        await query.edit_message_text(
            f"❌ Solo quedan {check.get('stock_actual', 0)} u.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Volver", callback_data=f'prod_{producto["sku"]}')
            ]])
        )
        return
    
    if 'carrito' not in context.user_data:
        context.user_data['carrito'] = []
    
    carrito = context.user_data['carrito']
    existente = next((i for i in carrito if i['sku'] == producto['sku']), None)
    
    if existente:
        existente['cantidad'] += cantidad
        existente['subtotal'] = existente['precio'] * existente['cantidad']
    else:
        carrito.append({
            'sku': producto['sku'],
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': cantidad,
            'subtotal': producto['precio'] * cantidad
        })
    
    total = sum(i['subtotal'] for i in carrito)
    
    mensaje = (
        f"✅ *Agregado:*\n*{producto['nombre']}*\n"
        f"Cantidad: {cantidad}\n\n"
        f"🛒 Carrito: {len(carrito)} productos\n"
        f"💰 Total: {format_money(total)}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛍️ Seguir comprando", callback_data='cat_menu')],
        [InlineKeyboardButton("📋 Ver carrito", callback_data='ver_carrito')],
        [InlineKeyboardButton("💳 Finalizar", callback_data='checkout_mp')]
    ]
    
    await query.edit_message_text(
        mensaje,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def ver_carrito(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    carrito = context.user_data.get('carrito', [])
    
    if not carrito:
        await query.edit_message_text(
            "🛒 Vacío",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛍️ Ver Catálogo", callback_data='cat_menu')]
            ])
        )
        return
    
    texto, subtotal, desc, total = crear_resumen_carrito(carrito)
    
    keyboard = [
        [InlineKeyboardButton("💳 Pagar con MP", callback_data='checkout_mp')],
        [InlineKeyboardButton("💵 Efectivo (-10%)", callback_data='checkout_efectivo')],
        [InlineKeyboardButton("🗑️ Vaciar", callback_data='vaciar_carrito')],
        [InlineKeyboardButton("🔙 Volver", callback_data='cat_menu')]
    ]
    
    await query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def vaciar_carrito(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['carrito'] = []
    await query.edit_message_text(
        "🗑️ *Carrito vaciado*",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🛍️ Catálogo", callback_data='cat_menu')
        ]])
    )
