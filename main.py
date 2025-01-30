from vkbottle import PhotoMessageUploader, GroupEventType, GroupTypes
from vkbottle.bot import Bot, Message, rules

bot = Bot("API_KEY")  # заменить
photo_uploader = PhotoMessageUploader(bot.api)


# handler для "первого сообщения", по факту реагирует если разрешить сообщения
@bot.on.raw_event(GroupEventType.MESSAGE_ALLOW, dataclass=GroupTypes.MessageAllow)
async def greetings_handler(event: GroupTypes.MessageAllow):
    user_id = event.object.user_id

    await bot.api.messages.send(
        user_id=user_id,
        message="Привет!",
        random_id=0
    )


# handler для фото
@bot.on.message(rules.AttachmentTypeRule("photo"))
async def photo_handler(m: Message):
    if m.attachments and m.attachments[0].photo:
        photo = m.attachments[0].photo
        owner_id = photo.owner_id
        photo_id = photo.id
        access_key = m.attachments[0].photo.access_key

        await m.answer(attachment=f"photo{owner_id}_{photo_id}_{access_key}", reply_to=m.id)


bot.run_forever()
