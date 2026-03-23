from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import config

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if 'carrito' not in context.user_data:
        context.user_data['carrito'] = []
    
    welcome_text = (
        f"🐕‍🦺 *¡Bienvenido a {config.BUSINESS_NAME}!* 🐈\n\n"
        f"Hola *{user.first_name}*, soy *Luna*, tu asesora de nutrición animal.\n\n"
        "Represento a *TIT CAN GROSS (TCG)*, 15 años en Formosa.\n\n"
        "✨ *Marcas:* Master Crock | Upper Crock\n\n"
        "¿Qué necesitás hoy?"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛍️ Ver Catálogo", callback_data='cat_menu')],
        [InlineKeyboardButton("🛒 Ver Mi Carrito", callback_data='ver_carrito')],
        [InlineKeyboardButton("💳 Métodos de Pago", callback_data='info_pagos')],
        [InlineKeyboardButton("🚚 Envíos", callback_data='info_envios')]
    ]
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def volver_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🛍️ Ver Catálogo", callback_data='cat_menu')],
        [InlineKeyboardButton("🛒 Ver Mi Carrito", callback_data='ver_carrito')]
    ]
    
    await query.edit_message_text(
        "🏠 *MENÚ PRINCIPAL*",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
