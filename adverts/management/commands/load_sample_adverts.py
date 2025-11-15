"""
Management command to load sample adverts.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from accounts.models import User
from adverts.models import Category, Advert
from adverts.services import markdown_to_html


class Command(BaseCommand):
    help = 'Load sample adverts into database'

    def handle(self, *args, **options):
        # Создаем тестового пользователя если его нет
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'username': 'testuser',
                'is_active': True,
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created test user: {user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Using existing user: {user.email}'))
        
        # Список тестовых объявлений
        sample_adverts = [
            {
                'category': 'tanks',
                'title': 'Ищу танка для рейдов',
                'body_md': '## Ищу опытного танка\n\nИщу **опытного танка** для участия в рейдах.\n\n### Требования:\n- Опыт игры от 6 месяцев\n- Наличие полного сетового доспеха\n- Умение работать в команде\n\n### Что предлагаю:\n- Стабильный состав\n- Распределение лута по справедливости\n- Помощь с экипировкой\n\n**Контакты:** пишите в личные сообщения'
            },
            {
                'category': 'healers',
                'title': 'Нужен хилер для гильдии',
                'body_md': '## Ищем хилеров в гильдию\n\nНаша гильдия **"Рыцари Света"** ищет активных хилеров.\n\n### Условия:\n- Уровень 80+\n- Опыт PvE контента\n- Активность 3-4 раза в неделю\n\n### Бонусы:\n- Помощь с прокачкой\n- Гилд банк с расходниками\n- Обучение от опытных игроков\n\nПишите для обсуждения деталей!'
            },
            {
                'category': 'dps',
                'title': 'Набор ДД для данжа',
                'body_md': '## Собираю группу для данжа\n\nИщу **2 ДД** для прохождения сложного данжа.\n\n### Что нужно:\n- Минимальный DPS: 5000+\n- Знание механик боссов\n- Готовность к нескольким попыткам\n\n### Распределение:\n- Лут по ротации\n- Расходники за счет группы\n\n**Время:** сегодня в 20:00 по МСК'
            },
            {
                'category': 'merchants',
                'title': 'Продаю редкие материалы',
                'body_md': '## Торговля материалами\n\nПродаю следующие материалы:\n\n- **Мифрил** - 50г за единицу\n- **Руны усиления** - 100г\n- **Эликсиры силы** - 75г\n\n### Условия:\n- Оплата наличными\n- Скидки при покупке от 10 штук\n- Возможен обмен на другие ресурсы\n\n**Локация:** столица, торговый квартал'
            },
            {
                'category': 'guildmasters',
                'title': 'Набор в гильдию "Драконы Севера"',
                'body_md': '## Приглашаем в гильдию\n\nГильдия **"Драконы Севера"** открывает набор новых членов!\n\n### О нас:\n- Активная PvP и PvE деятельность\n- Организованные рейды\n- Дружелюбное сообщество\n\n### Требования:\n- Уровень 70+\n- Активность\n- Уважение к другим игрокам\n\nПрисоединяйтесь к нам!'
            },
            {
                'category': 'questgivers',
                'title': 'Помощь с квестами',
                'body_md': '## Помогаю с прохождением квестов\n\nПредлагаю помощь с:\n\n- Прохождением сложных квестовых цепочек\n- Поиском редких предметов\n- Выполнением групповых заданий\n\n### Услуги:\n- **Прохождение квеста** - 200г\n- **Поиск предмета** - 100г\n- **Групповой квест** - 300г\n\nПишите для обсуждения!'
            },
            {
                'category': 'blacksmiths',
                'title': 'Кузнечные услуги',
                'body_md': '## Профессиональный кузнец\n\nИзготавливаю оружие и доспехи на заказ.\n\n### Что могу сделать:\n- **Оружие** любого уровня\n- **Доспехи** из редких материалов\n- **Улучшение** существующего снаряжения\n\n### Цены:\n- Обычное оружие - от 500г\n- Эпическое оружие - от 2000г\n- Улучшение - от 300г\n\nМатериалы заказчика или могу предоставить свои (доплата).'
            },
            {
                'category': 'leatherworkers',
                'title': 'Кожевник - изготовление на заказ',
                'body_md': '## Кожевные изделия\n\nИзготавливаю кожаные доспехи и аксессуары.\n\n### Ассортимент:\n- Кожаные доспехи\n- Сумки и рюкзаки\n- Кожаные аксессуары\n\n### Особенности:\n- Использую только качественные материалы\n- Возможна персонализация\n- Гарантия качества\n\n**Срок изготовления:** 1-2 дня'
            },
            {
                'category': 'alchemists',
                'title': 'Продажа зелий и эликсиров',
                'body_md': '## Алхимические товары\n\nПродаю зелья и эликсиры собственного производства.\n\n### В наличии:\n- **Зелья лечения** - 25г\n- **Зелья маны** - 30г\n- **Эликсиры силы** - 50г\n- **Эликсиры защиты** - 45г\n\n### Оптовые скидки:\n- От 20 штук - скидка 10%\n- От 50 штук - скидка 20%\n\nВсе зелья свежие, только что изготовленные!'
            },
            {
                'category': 'spellcasters',
                'title': 'Обучение заклинаниям',
                'body_md': '## Мастер заклинаний\n\nОбучаю магическим заклинаниям и ритуалам.\n\n### Что могу научить:\n- Боевые заклинания\n- Защитные чары\n- Лечебные ритуалы\n- Транспортные заклинания\n\n### Условия обучения:\n- Базовые знания магии обязательны\n- Оплата по договоренности\n- Индивидуальный подход\n\n**Продолжительность курса:** зависит от выбранного направления'
            },
        ]
        
        created_count = 0
        for advert_data in sample_adverts:
            try:
                category = Category.objects.get(slug=advert_data['category'])
                body_md = advert_data['body_md']
                body_html = markdown_to_html(body_md)
                
                advert, created = Advert.objects.get_or_create(
                    title=advert_data['title'],
                    author=user,
                    defaults={
                        'category': category,
                        'body_md': body_md,
                        'body_html': body_html,
                        'status': Advert.Status.PUBLISHED,
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: {advert.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped (already exists): {advert.title}'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Category {advert_data["category"]} not found!'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} sample adverts!'))

