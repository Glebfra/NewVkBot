from vkbottle import CtxStorage, Keyboard, KeyboardButtonColor, Text

ctx_storage = CtxStorage()


class DefaultKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)
        self.keyboard.add(Text("Домашка"), color=KeyboardButtonColor.PRIMARY)
        self.keyboard.add(Text("Добавить домашку"), color=KeyboardButtonColor.POSITIVE)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard


class SelectHomeworkKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)
        for subject in ctx_storage.get('homework'):
            self.keyboard.add(Text(subject), color=KeyboardButtonColor.SECONDARY)
        self.keyboard.row()
        self.keyboard.add(Text('Назад'), color=KeyboardButtonColor.SECONDARY)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard


class TalkingKeyboard(object):
    def __init__(self):
        self.keyboard = Keyboard(one_time=True, inline=False)
        self.keyboard.add(Text('Хватит'), color=KeyboardButtonColor.NEGATIVE)

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
        self.keyboard.add(Text('Отправить всем!'), color=KeyboardButtonColor.NEGATIVE)

    def get_keyboard(self):
        self.__init__()
        return self.keyboard
