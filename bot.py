import telebot
from telebot import types
from pixellib.instance import instance_segmentation
import os
bot = telebot.TeleBot(token)
#кнопки
markup = types.InlineKeyboardMarkup(row_width=2)
item0 = types.InlineKeyboardButton(text="все объекты", callback_data="все объекты")
item1 = types.InlineKeyboardButton(text="людей", callback_data="людей")
item2 = types.InlineKeyboardButton(text="машины", callback_data="машины")
item3 = types.InlineKeyboardButton(text="животных", callback_data="животных")
kb = markup.add(item0, item1, item2,item3)


@bot.message_handler(commands=['start'])
def welcome(message):
    #markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #item1 = types.KeyboardButton(text="найди чтото на картинке")
    #item2 = types.KeyboardButton(text="Аоаоаоао")

    #kb = markup.add(item1, item2) 
    bot.send_message(message.chat.id, 'Здравствуйте. Я - бот,предназначенный находить объекты на фотографиях.отправь мне фото')# reply_markup=kb)
    #kb = telebot.types.ReplyKeyboardRemove()

#запрашиваем фото
#запрашиваем фото
@bot.message_handler(content_types = ['photo'])
def echo_photo_bot(message):
    chat_id = message.chat.id
    input_image = message.photo[0].file_id
    bot.send_photo(chat_id, input_image, message.caption)   
    bot.send_message(chat_id, 'это твое фото,что будем искать?', reply_markup=kb )
   
    file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    src="D:/project/"+file_info.file_path;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.send_photo(chat_id, downloaded_file, message.caption )   
    bot.reply_to(message,"Фото добавлено") 
  



    
#обработчик кнопочки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    def object_detection_on_an_image(download_photo):
            segment_image = instance_segmentation()
            segment_image.load_model("D:\project\mask_rcnn_coco.h5")  
            if call.data == "все объекты":
                bot.send_message(call.message.chat.id, "мы ищем все объекты")

       

                segment_image.segmentImage(
                    image_path=download_photo,
                    show_bboxes=True,
        
                    output_image_name=download_photo
                )


            elif call.data == "людей":
                bot.send_message(call.message.chat.id, "мы ищем людей")
        

                segment_image.segmentImage(
                    image_path=download_photo,
                    show_bboxes=True,
        
                    output_image_name=download_photo
                )
            elif call.data == "машины":
                bot.send_message(call.message.chat.id, "мы ищем машины")

        

                segment_image.segmentImage(
                    image_path=download_photo,
                    show_bboxes=True,
        
                    output_image_name=download_photo
                )
            elif call.data == "животных":
           
                bot.send_message(call.message.chat.id, "мы ищем животных")

        

                segment_image.segmentImage(
                    image_path=download_photo,
                    show_bboxes=True,
        
                    output_image_name=download_photo
        )

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="отправьте фото", reply_markup=None)
#нахождение элементов
    def main():
        object_detection_on_an_image('photos/file_27.jpg')


    if __name__ == '__main__':
        main()

@bot.message_handler(commands=['photo'])
def photo_output_message(message):
    output_name = open('photos/file_24.jpg','rb')
    bot.send_photo(message.chat.id,output_name,'это твое фото,и на это я потратил 2 часа')

bot.polling(none_stop=True)
