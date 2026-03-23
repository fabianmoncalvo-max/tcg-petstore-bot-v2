from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.mercadopago_service import mp_service
from utils.formatters import crear_resumen_carrito, format_money
from config import config
from datetime import datetime

async def checkout_mp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    carrito = context.user_data.get('carrito', [])
    if not carrito:
        return
    
    pedido_id = f"TCG{datetime.now().strftime('%y%m%d%H%M')}{str(update.effective_user.id)[-4:]}"
    context.user_data['pedido_actual'] = pedido_id
    
    items_mp = []
    for item in carrito:
        items_mp.append({
            "title": item['nombre'],
            "quantity": item['cantidad'],
            "unit_price": float(item['precio'])
        })
    
    user = update.effective_user
    payer_data = {
        'nombre': user.first_name,
        'email': f"{user.id}@tcg.com"
    }
    
    preferencia = mp_service.crear_preferencia(pedido_id, items_mp, payer_data)
    
    if not preferencia:
        await query.edit_message_text("❌ Error al crear pago")
        return
    
    texto, _, _, total = crear_resumen_carrito(carrito)
    
    mensaje = (
        f"💳 *PAGO MERCADO PAGO*\n\n"
        f"{texto}\n\n"
        f"🆔 Pedido: `{pedido_id}`\n\n"
        f"Click en **PAGAR AHORA**"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 PAGAR AHORA", url=preferencia['init_point'])],
        [InlineKeyboardButton("🔙 Volver", callback_data='ver_carrito')]
    ]
    
    await query.edit_message_text(
        mensaje,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Notificar admin
    await context.bot.send_message(
        chat_id=config.ADMIN_CHAT_ID,
        text=f"🛒 Nuevo pedido MP\nCliente: {user.first_name}\nTotal: {format_money(total)}"
    )

async def checkout_efectivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    carrito = context.user_data.get('carrito', [])
    if not carrito:
        return
    
    texto, subtotal, _, _ = crear_resumen_carrito(carrito, 'efectivo')
    total = subtotal * 0.90
    
    mensaje = (
        f"💵 *PAGO EN EFECTIVO*\n\n"
        f"{texto}\n\n"
        f"💰 *Total con 10% descuento:* `{format_money(total)}`\n\n"
        f"¿Confirmás?"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirmar", callback_data='confirmar_efectivo')],
        [InlineKeyboardButton("🔙 Volver", callback_data='ver_carrito')]
    ]
    
    await query.edit_message_text(
        mensaje,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def confirmar_pedido_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    carrito = context.user_data.get('carrito', [])
    if not carrito:
        return
    
    pedido_id = f"TCG{datetime.now().strftime('%y%m%d%H%M')}{str(update.effective_user.id)[-4:]}"
    total = sum(i['subtotal'] for i in carrito) * 0.90
    
    context.user_data['carrito'] = []
    
    mensaje = (
        f"✅ *¡PEDIDO CONFIRMADO!*\n\n"
        f"🆔 *Número:* `{pedido_id}`\n"
        f"💰 *Total:* `{format_money(total)}`\n"
        f"💳 *Método:* Efectivo\n\n"
        f"Nos contactaremos para coordinar entrega.\n"
        f"¡Gracias! 🐕‍🦺"
    )
    
    await query.edit_message_text(mensaje, parse_mode='Markdown')
    
    # Notificar admin
    await context.bot.send_message(
        chat_id=config.ADMIN_CHAT_ID,
        text=f"🚨 PEDIDO EFECTIVO\nID: {pedido_id}\nTotal: {format_money(total)}\nCliente: {update.effective_user.first_name}"
    )
