from vkbottle import CtxStorage, Keyboard, KeyboardButtonColor, Text

ctx_storage = CtxStorage()

Subject = ctx_storage.get('Subject')
File = ctx_storage.get('File')


class AbstractKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard


class DefaultKeyboard(AbstractKeyboard):
    def __init__(self):
        super().__init__()
        self.keyboard.add(Text("Домашка"), color=KeyboardButtonColor.SECONDARY)
        self.keyboard.add(Text("Расписание"), color=KeyboardButtonColor.SECONDARY)
        self.keyboard.row()
        self.keyboard.add(Text("Неделя"), color=KeyboardButtonColor.SECONDARY)
        self.keyboard.add(Text("Добавить домашку"), color=KeyboardButtonColor.POSITIVE)
        self.keyboard.row()
        self.keyboard.add(Text("ChatGPT"), color=KeyboardButtonColor.PRIMARY)


class BackKeyboard(AbstractKeyboard):
    def __init__(self):
        super().__init__()
        self.keyboard.add(Text("Назад"), color=KeyboardButtonColor.SECONDARY)


class SelectHomeworkKeyboard(AbstractKeyboard):
    def __init__(self):
        super().__init__()
        db = ctx_storage.get('db')
        db.connect()
        for index, subject in enumerate(Subject.select()):
            if not index % 3 and index != 0:
                self.keyboard.row()
            self.keyboard.add(Text(subject.name), color=KeyboardButtonColor.SECONDARY)
        self.keyboard.row()
        self.keyboard.add(Text('Назад'), color=KeyboardButtonColor.SECONDARY)
        db.close()


class AdminDefaultKeyboard(AbstractKeyboard):
    def __init__(self):
        super().__init__()
        self.keyboard.add(Text('Домашка'), color=KeyboardButtonColor.PRIMARY)
        self.keyboard.add(Text('Добавить домашку'), color=KeyboardButtonColor.POSITIVE)
        self.keyboard.row()
        self.keyboard.add(Text('Добавить админа'), color=KeyboardButtonColor.POSITIVE)
        self.keyboard.add(Text('Удалить админа'), color=KeyboardButtonColor.NEGATIVE)
        self.keyboard.row()
        self.keyboard.add(Text('Удалить предмет'), color=KeyboardButtonColor.NEGATIVE)
        self.keyboard.row()
        self.keyboard.add(Text('Отправить всем!'), color=KeyboardButtonColor.NEGATIVE)
