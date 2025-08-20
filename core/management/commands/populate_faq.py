# from django.core.management.base import BaseCommand
# from core.models import FAQ  # adjust if your model is elsewhere


# class Command(BaseCommand):
#     help = "Populate the FAQ table with default questions and answers"

#     def handle(self, *args, **kwargs):
#         data = [
#             {
#                 "question": 'What is the difference between "Seen" and "Found"?',
#                 "answer": '"Seen" means someone has spotted the pet but hasn\'t caught it. "Found" indicates that the animal is with the finder.',
#             },
#             {
#                 "question": 'What helps find lost pets?',
#                 "answer": 'The community is the main driving force – people who share, report sightings, or take in animals. Our platform connects finders with owners.',
#             },
#             {
#                 "question": 'How can I report a found pet?',
#                 "answer": 'Simply sign up and post a found report with a photo, location, and description.',
#             },
#             {
#                 "question": "What should I do if I see a pet but can't catch it?",
#                 "answer": 'Use the "Seen" function and post information with a description, time, and location. This can be very helpful for owners!',
#             },
#             {
#                 "question": 'Can I use the platform from my mobile phone?',
#                 "answer": 'Yes! Our website is fully adapted for mobile devices. You can add posts, search for pets, and contact finders anywhere.',
#             },
#             {
#                 "question": 'How long does my post remain active?',
#                 "answer": 'The post remains active until you remove it or mark it as "found" / "returned to owner".',
#             },
#             {
#                 "question": 'Are there any safety tips when meeting a finder or owner?',
#                 "answer": 'Always meet in public places when possible. If you feel unsafe, bring a friend or choose a veterinary clinic as a meeting place.',
#             },
#             {
#                 "question": 'Can I add other animals, not just dogs or cats?',
#                 "answer": 'Yes, of course! Although the platform is more oriented towards dogs and cats, you can also add other animals by selecting the species "Other".',
#             },
#             {
#                 "question": 'Can I offer a reward for finding my pet?',
#                 "answer": "We don't encourage offering rewards as it can create unexpected situations. The community often helps from the heart – the main goal is to safely return the pet home.",
#             },
#         ]

#         FAQ.objects.all().delete()  # Optional: clear existing FAQs first

#         for index, item in enumerate(data):
#             FAQ.objects.create(
#                 question=item["question"],
#                 answer=item["answer"],
#                 order=index,
#                 is_active=True,
#             )

#         self.stdout.write(self.style.SUCCESS("FAQs populated successfully."))
from django.core.management.base import BaseCommand
from core.models import FAQ  # adjust if your model is elsewhere


class Command(BaseCommand):
    help = "Populate the FAQ table with default questions and answers in multiple languages"

    def handle(self, *args, **kwargs):
        data = [
            {
                "question": {
                    "en": 'What is the difference between "Seen" and "Found"?',
                    "lv": 'Kāda ir atšķirība starp "Redzēts" un "Atrasts"?',
                    "ru": 'В чем разница между "Видел" и "Найдено"?'
                },
                "answer": {
                    "en": '"Seen" means someone has spotted the pet but hasn\'t caught it. "Found" indicates that the animal is with the finder.',
                    "lv": '"Redzēts" nozīmē, ka kāds ir pamanījis dzīvnieku, bet nav noķēris. "Atrasts" nozīmē, ka dzīvnieks ir pie atradēja.',
                    "ru": '"Видел" означает, что кто-то заметил животное, но не поймал его. "Найдено" означает, что животное у нашедшего.'
                }
            },
            {
                "question": {
                    "en": 'What helps find lost pets?',
                    "lv": 'Kas palīdz atrast pazudušus mājdzīvniekus?',
                    "ru": 'Что помогает найти потерянных домашних животных?'
                },
                "answer": {
                    "en": 'The community is the main driving force – people who share, report sightings, or take in animals. Our platform connects finders with owners.',
                    "lv": 'Kopiena ir galvenais dzinējspēks – cilvēki, kas dalās, ziņo par novērojumiem vai uzņem dzīvniekus. Mūsu platforma savieno atradējus ar īpašniekiem.',
                    "ru": 'Сообщество является основным двигателем – люди, которые делятся, сообщают о наблюдениях или принимают животных. Наша платформа соединяет находчиков с владельцами.'
                }
            },
            {
                "question": {
                    "en": 'How can I report a found pet?',
                    "lv": 'Kā es varu ziņot par atrastu mājdzīvnieku?',
                    "ru": 'Как я могу сообщить о найденном питомце?'
                },
                "answer": {
                    "en": 'Simply sign up and post a found report with a photo, location, and description.',
                    "lv": 'Vienkārši reģistrējieties un ievietojiet atrasta dzīvnieka ziņojumu ar foto, atrašanās vietu un aprakstu.',
                    "ru": 'Просто зарегистрируйтесь и разместите сообщение о найденном питомце с фотографией, местоположением и описанием.'
                }
            },
            {
                "question": {
                    "en": "What should I do if I see a pet but can't catch it?",
                    "lv": 'Ko man darīt, ja es redzu dzīvnieku, bet nevaru to noķert?',
                    "ru": 'Что мне делать, если я вижу питомца, но не могу его поймать?'
                },
                "answer": {
                    "en": 'Use the "Seen" function and post information with a description, time, and location. This can be very helpful for owners!',
                    "lv": 'Izmantojiet funkciju "Redzēts" un ievietojiet informāciju ar aprakstu, laiku un atrašanās vietu. Tas var būt ļoti noderīgi īpašniekiem!',
                    "ru": 'Используйте функцию "Видел" и разместите информацию с описанием, временем и местоположением. Это может быть очень полезно для владельцев!'
                }
            },
            {
                "question": {
                    "en": 'Can I use the platform from my mobile phone?',
                    "lv": 'Vai es varu izmantot platformu no sava mobilā tālruņa?',
                    "ru": 'Могу ли я использовать платформу со своего мобильного телефона?'
                },
                "answer": {
                    "en": 'Yes! Our website is fully adapted for mobile devices. You can add posts, search for pets, and contact finders anywhere.',
                    "lv": 'Jā! Mūsu mājaslapa ir pilnībā pielāgota mobilajām ierīcēm. Jūs varat pievienot ziņas, meklēt dzīvniekus un sazināties ar atradējiem jebkur.',
                    "ru": 'Да! Наш сайт полностью адаптирован для мобильных устройств. Вы можете добавлять сообщения, искать животных и связываться с находчиками в любом месте.'
                }
            },
            {
                "question": {
                    "en": 'How long does my post remain active?',
                    "lv": 'Cik ilgi mana ziņa paliek aktīva?',
                    "ru": 'Как долго мое сообщение остается активным?'
                },
                "answer": {
                    "en": 'The post remains active until you remove it or mark it as "found" / "returned to owner".',
                    "lv": 'Ziņa paliek aktīva līdz jūs to noņemat vai atzīmējat kā "atrasta" / "atgriezta īpašniekam".',
                    "ru": 'Сообщение остается активным, пока вы не удалите его или не отметите как "найдено" / "возвращено владельцу".'
                }
            },
            {
                "question": {
                    "en": 'Are there any safety tips when meeting a finder or owner?',
                    "lv": 'Vai ir kādi drošības padomi, satiekot atradēju vai īpašnieku?',
                    "ru": 'Есть ли советы по безопасности при встрече с находчиком или владельцем?'
                },
                "answer": {
                    "en": 'Always meet in public places when possible. If you feel unsafe, bring a friend or choose a veterinary clinic as a meeting place.',
                    "lv": 'Vienmēr satikieties publiskās vietās, ja iespējams. Ja jūtaties nedroši, ņemiet līdzi draugu vai izvēlieties veterināro klīniku kā tikšanās vietu.',
                    "ru": 'Всегда встречайтесь в общественных местах, если это возможно. Если вы чувствуете себя небезопасно, возьмите с собой друга или выберите ветеринарную клинику в качестве места встречи.'
                }
            },
            {
                "question": {
                    "en": 'Can I add other animals, not just dogs or cats?',
                    "lv": 'Vai es varu pievienot citus dzīvniekus, ne tikai suņus vai kaķus?',
                    "ru": 'Могу ли я добавить других животных, не только собак или кошек?'
                },
                "answer": {
                    "en": 'Yes, of course! Although the platform is more oriented towards dogs and cats, you can also add other animals by selecting the species "Other".',
                    "lv": 'Jā, protams! Lai gan platforma vairāk orientēta uz suņiem un kaķiem, jūs varat pievienot arī citus dzīvniekus, izvēloties sugu "Citi".',
                    "ru": 'Да, конечно! Хотя платформа больше ориентирована на собак и кошек, вы также можете добавить других животных, выбрав вид "Другое".'
                }
            },
            {
                "question": {
                    "en": 'Can I offer a reward for finding my pet?',
                    "lv": 'Vai es varu piedāvāt atlīdzību par mana dzīvnieka atrašanu?',
                    "ru": 'Могу ли я предложить вознаграждение за нахождение моего питомца?'
                },
                "answer": {
                    "en": 'We don\'t encourage offering rewards as it can create unexpected situations. The community often helps from the heart – the main goal is to safely return the pet home.',
                    "lv": 'Mēs neiesakām piedāvāt atlīdzību, jo tas var radīt neparedzētas situācijas. Kopiena bieži palīdz no sirds – galvenais mērķis ir droši atgriezt dzīvnieku mājās.',
                    "ru": 'Мы не рекомендуем предлагать вознаграждение, так как это может создать неожиданные ситуации. Сообщество часто помогает от сердца – основная цель – безопасно вернуть питомца домой.'
                }
            },
        ]

        FAQ.objects.all().delete()  # Optional: clear existing FAQs first

        for index, item in enumerate(data):
            FAQ.objects.create(
                question_en=item["question"]["en"],
                question_ru=item["question"]["ru"],
                question_lv=item["question"]["lv"],
                answer_en=item["answer"]["en"],
                answer_ru=item["answer"]["ru"],
                answer_lv=item["answer"]["lv"],
                order=index,
                is_active=True,
            )

        self.stdout.write(self.style.SUCCESS("FAQs populated successfully in all languages."))
