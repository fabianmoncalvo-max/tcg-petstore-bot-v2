from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.sheets_service import sheets
from utils.formatters import format_money

async def menu_categorias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    texto = "🛍️ *CATÁLOGO TCG*\n\n¿Para quién buscás?"
    
    keyboard = [
        [InlineKeyboardButton("🐕 Perros", callback_data='cat_Perros')],
        [InlineKeyboardButton("🐈 Gatos", callback_data='cat_Gatos')],
        [InlineKeyboardButton("⭐ Destacados", callback_data='cat_destacados')],
        [InlineKeyboardButton("🔙 Volver", callback_data='volver_inicio')]
    ]
    
    await query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def mostrar_productos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    categoria = query.data.replace('cat_', '')
    
    if categoria == 'destacados':
        productos = sheets.get_productos(solo_stock=True)
        productos = [p for p in productos if p.get('destacado')]
        titulo = "⭐ Destacados"
    else:
        productos = sheets.get_productos(categoria=categoria, solo_stock=False)
        titulo = f"🐕 Perros" if categoria == "Perros" else "🐈 Gatos"
    
    if not productos:
        await query.edit_message_text("😔 No hay productos", reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Volver", callback_data='cat_menu')
        ]]))
        return
    
    texto = f"*{titulo}*\n\n"
    keyboard = []
    
    for p in productos[:10]:
        stock_ok = p['stock'] > 0
        emoji = "✅" if stock_ok else "❌"
        texto += f"{emoji} *{p['nombre']}*\n💰 {format_money(p['precio'])} | 📦 {p['stock']}u\n\n"
        
        if stock_ok:
            keyboard.append([InlineKeyboardButton(
                f"🛒 {p['nombre'][:25]}...", callback_data=f'prod_{p["sku"]}'
            )])
    
    keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data='cat_menu')])
    
    await query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def detalle_producto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    sku = query.data.replace('prod_', '')
    producto = sheets.get_producto(sku)
    
    if not producto:
        await query.edit_message_text("❌ No encontrado")
        return
    
    context.user_data['producto_actual'] = producto
    
    stock_emoji = "🟢" if producto['stock'] > 10 else "🟡" if producto['stock'] > 0 else "🔴"
    
    texto = (
        f"*{producto['nombre']}* {stock_emoji}\n\n"
        f"💰 {format_money(producto['precio'])}\n"
        f"📦 Stock: `{producto['stock']}` u.\n\n"
        f"_{producto.get('descripcion', '')}_\n\n"
        f"*¿Cuántas querés?*"
    )
    
    keyboard = []
    if producto['stock'] > 0:
        max_cant = min(producto['stock'], 5)
        row = [InlineKeyboardButton(str(i), callback_data=f'add_{i}') for i in range(1, max_cant + 1)]
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data=f'cat_{producto["categoria"]}')])
    
    await query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
