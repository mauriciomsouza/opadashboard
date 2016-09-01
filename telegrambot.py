# coding: utf-8
from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    bot.sendMessage(
        update.message.chat_id,
        text='Hi! My name is OPA! Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                         one_time_keyboard=True))

    return GENDER


def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s" % (user.first_name, update.message.text))
    bot.sendMessage(
        update.message.chat_id,
        text='I see! Please send me a photo of yourself, '
        'so I know what you look like, or send /skip if you don\'t want to.')

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s" % (user.first_name, 'user_photo.jpg'))
    bot.sendMessage(update.message.chat_id,
                    text='Gorgeous! Now, send me your location please, '
                    'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='I bet you look great! Now, send me your '
                    'location please, or send /skip.')

    return LOCATION


def location(bot, update):
    address = {
        'name': '2mL design',
        'address': 'R. Real Grandeza, 183 - Botafogo, Rio de Janeiro - RJ, '
        '22281-035',
        'telephone': '(21) 99789-6617',
        'rating': 5
    }
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f"
                % (user.first_name, user_location.latitude,
                   user_location.longitude))
    bot.sendMessage(update.message.chat_id,
                    text='Maybe I can visit you sometime! '
                    'At last, I will tell you a perfect place! \n'
                    ' {name} {address} {telephone} {rating}'.format(**address)
                    )

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='You seem a bit paranoid! '
                    'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    bot.sendMessage(update.message.chat_id,
                    text='Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("252694819:AAEcMEmofbbQ3UUuatdaDmG4KYJ6cyH19cQ")
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender)],
            PHOTO: [MessageHandler([Filters.photo], photo),
                    CommandHandler('skip', skip_photo)],
            LOCATION: [MessageHandler([Filters.location], location),
                       CommandHandler('skip', skip_location)],
            BIO: [MessageHandler([Filters.text], bio)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
