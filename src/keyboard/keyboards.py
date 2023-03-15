from vkbottle import CtxStorage, Keyboard, KeyboardButtonColor, Text

ctx_storage = CtxStorage()


class DefaultKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)
        self.keyboard.add(Text("Домашка"), color=KeyboardButtonColor.PRIMARY)
        self.keyboard.add(Text("Добавить домашку"), color=KeyboardButtonColor.POSITIVE)
        self.keyboard.row()
        self.keyboard.add(Text("Расписание"), color=KeyboardButtonColor.SECONDARY)
        self.keyboard.add(Text("Неделя"), color=KeyboardButtonColor.SECONDARY)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard


class BackKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)
        self.keyboard.add(Text("Назад"), color=KeyboardButtonColor.SECONDARY)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard


class SelectHomeworkKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)
        for index, subject in enumerate(ctx_storage.get('homework')):
            if not index % 3 and index != 0:
                self.keyboard.row()
            self.keyboard.add(Text(subject), color=KeyboardButtonColor.SECONDARY)
        self.keyboard.row()
        self.keyboard.add(Text('Назад'), color=KeyboardButtonColor.SECONDARY)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard


class AdminDefaultKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)
        self.keyboard.add(Text('Домашка'), color=KeyboardButtonColor.PRIMARY)
        self.keyboard.add(Text('Добавить домашку'), color=KeyboardButtonColor.POSITIVE)
        self.keyboard.row()
        self.keyboard.add(Text('Добавить админа'), color=KeyboardButtonColor.POSITIVE)
        self.keyboard.add(Text('Удалить админа'), color=KeyboardButtonColor.NEGATIVE)
        self.keyboard.row()
        self.keyboard.add(Text('Удалить предмет'), color=KeyboardButtonColor.NEGATIVE)
        self.keyboard.row()
        self.keyboard.add(Text('Отправить всем!'), color=KeyboardButtonColor.NEGATIVE)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard
