import telebot
from telebot import types
from pixellib.instance import instance_segmentation
from google_images_search import GoogleImagesSearch


import os
class MyBot:
    def __init__(self):
        self.token = "6095239590:AAGLodvJdqeE7EK-dfiFtZgsr8WtSwwd1-4"
        self.bot = telebot.TeleBot(self.token)
        self.name_photo = ''
        self.markup1 = types.InlineKeyboardMarkup(row_width=2)
        self.markup2 = types.InlineKeyboardMarkup(row_width=2)
        self.item0 = types.InlineKeyboardButton(text="все объекты", callback_data="все объекты")
        self.item1 = types.InlineKeyboardButton(text="людей", callback_data="людей")
        self.item2 = types.InlineKeyboardButton(text="машины", callback_data="машины")
        self.item3 = types.InlineKeyboardButton(text="животных", callback_data="животных")
        self.item4 = types.InlineKeyboardButton(text="поиск по фото", callback_data="поиск")
        self.kb = self.markup1.add(self.item0, self.item1, self.item2, self.item3)
        self.kb2 = self.markup2.add(self.item4)
    def run(self):
        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            self.bot.reply_to(message, "Привет! Я бот для поиска объектов. Отправь мне фото:")

        

            #запрашиваем фото
        @self.bot.message_handler(content_types = ['photo'])
        def echo_photo_bot(message):
            chat_id = message.chat.id
            input_image = message.photo[0].file_id
            self.bot.send_photo(chat_id, input_image, message.caption)   
            self.bot.send_message(chat_id, 'это твое фото,как ты хочешь его назвать?')
                
            file_info = self.bot.get_file(message.photo[len(message.photo)-1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            @self.bot.message_handler(content_types = ['text'])
            def rewrite_name_file(message):
                text = message.text
                self.bot.send_message(chat_id, f"Вы назвали фото: {text}")        
                new_file_path = "D:/project/photos/" + message.text + ".jpg"
                print(new_file_path)
                self.name_photo = new_file_path
                with open(new_file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                self.bot.reply_to(message,"Фото добавлено", reply_markup=self.kb)
            ##обработчик кнопочки           
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            generation()
            segment_image = instance_segmentation()
            
            if call.data == "все объекты":
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="мы ищем все объекты", reply_markup=None)
                generation.object_detection_on_an_image(self.name_photo)
                self.bot.send_message(call.message.chat.id, "чтобы получить результат,напишите /photo")

            elif call.data == "людей":
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="мы ищем людей", reply_markup=None)
                target_class = segment_image.select_target_classes(person=True)
                generation.object_detection_on_an_image(self.name_photo, target_class)                  
                self.bot.send_message(call.message.chat.id, "чтобы получить результат,напишите /photo")

            elif call.data == "машины":
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="мы ищем машины", reply_markup=None)
                target_class = segment_image.select_target_classes(car=True, bus=True, truck=True)
                generation.object_detection_on_an_image(self.name_photo, target_class)
                self.bot.send_message(call.message.chat.id, "чтобы получить результат,напишите /photo")

            elif call.data == "животных":
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="мы ищем животных", reply_markup=None)
                target_class = segment_image.select_target_classes(bird=True, cat=True, dog=True, horse=True, sheep=True,
                      cow=True, elephant=True, bear=True, zebra=True,giraffe=True,)
                generation.object_detection_on_an_image(self.name_photo, target_class)
                self.bot.send_message(call.message.chat.id, "чтобы получить результат,напишите /photo")
            elif call.data == "поиск":
                generation.search_images_by_photo(self.name_photo)
                
        @self.bot.message_handler(commands=['photo'])
        def photo_output_message(message):
            output_name = open(self.name_photo,'rb')
            print(self.name_photo)
            self.bot.send_photo(message.chat.id,output_name,'это твое фото,и на это я потратил 2 часа', reply_markup=self.kb2)
   
        self.bot.polling(none_stop=True)

class generation(MyBot):
    def object_detection_on_an_image(download_photo, target_choosen):
            segment_image = instance_segmentation()
            segment_image.load_model("mask_rcnn_coco.h5")
            segment_image.segmentImage(
                image_path=download_photo,
                segment_target_classes=target_choosen,
                show_bboxes=True,
                output_image_name=download_photo
            )
    def search_images_by_photo(photo_path):
        GCS_DEVELOPER_KEY = 'AIzaSyBkcyaos4CM74v9JhNDhVAQvjX4rjOUPbc'
        GCS_CX = ''
        # Инициализация GoogleImagesSearch с вашими учетными данными API
        gis = GoogleImagesSearch('AIzaSyBkcyaos4CM74v9JhNDhVAQvjX4rjOUPbc', '553103447540-olct55v2775driffsbun6p41sftgct6p.apps.googleusercontent.com')#553103447540-olct55v2775driffsbun6p41sftgct6p.apps.googleusercontent.com

        # Выполнение поиска по фото
        search_params = {
            'image_url': '',
            'img_file': photo_path,
            'num': 10,  # Количество результатов, которые вы хотите получить
            'safe_search': True,
        }

        gis.search(search_params)

        # Обработка результатов поиска
        for image in gis.results():
            print(image.url)

if __name__ == '__main__':
    my_bot = MyBot()
    my_bot.run()




