import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from config import config
from database.db import init_db
from handlers.start import start_command, volver_inicio
from handlers.catalogo import menu_categorias, mostrar_productos, detalle_producto
from handlers.carrito import agregar_producto, ver_carrito, vaciar_carrito
from handlers.checkout import checkout_mp, checkout_efectivo, confirmar_pedido_final

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update: Update, context):
    logger.error(f"Error: {context.error}")
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text("😅 Error. Escribí /start")
    except:
        pass

def main():
    logger.info("Iniciando TCG Pet Store Bot v2...")
    
    try:
        init_db()
        logger.info("Base de datos OK")
    except Exception as e:
        logger.error(f"Error DB: {e}")
    
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Comandos
    application.add_handler(CommandHandler("start", start_command))
    
    # Callbacks
    application.add_handler(CallbackQueryHandler(volver_inicio, pattern='^volver_inicio$'))
    application.add_handler(CallbackQueryHandler(menu_categorias, pattern='^cat_menu$'))
    application.add_handler(CallbackQueryHandler(mostrar_productos, pattern='^cat_'))
    application.add_handler(CallbackQueryHandler(detalle_producto, pattern='^prod_'))
    application.add_handler(CallbackQueryHandler(agregar_producto, pattern='^add_'))
    application.add_handler(CallbackQueryHandler(ver_carrito, pattern='^ver_carrito$'))
    application.add_handler(CallbackQueryHandler(vaciar_carrito, pattern='^vaciar_carrito$'))
    application.add_handler(CallbackQueryHandler(checkout_mp, pattern='^checkout_mp$'))
    application.add_handler(CallbackQueryHandler(checkout_efectivo, pattern='^checkout_efectivo$'))
    application.add_handler(CallbackQueryHandler(confirmar_pedido_final, pattern='^confirmar_efectivo$'))
    
    application.add_error_handler(error_handler)
    
    print("🚀 TCG Pet Store v2 iniciado!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
