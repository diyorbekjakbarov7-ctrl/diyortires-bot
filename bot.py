async def run_bot():

    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # 📜 Tarix
    app.add_handler(
        MessageHandler(
            filters.Regex("^📜 Tarix$"),
            show_history
        )
    )

    # 📦 Ombor
    app.add_handler(
        MessageHandler(
            filters.Regex("^📦 Ombor$"),
            show_stock
        )
    )

    # ➕ Tovar qo'shish
    add_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➕ Tovar qo'shish$"),
                add_product_start
            )
        ],
        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    product_name
                )
            ],
            PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    product_price
                )
            ],
            QUANTITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    product_quantity
                )
            ]
        },
        fallbacks=[]
    )

    app.add_handler(add_handler)

    # ➖ Sotildi
    sell_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➖ Sotildi$"),
                sell_start
            )
        ],
        states={
            SELL_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    sell_name
                )
            ],
            SELL_QUANTITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    sell_quantity
                )
            ]
        },
        fallbacks=[]
    )

    app.add_handler(sell_handler)

    print("Bot ishga tushdi...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()