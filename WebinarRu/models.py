import datetime
from typing import Optional, Sequence, Literal

from pydantic import BaseModel


__all__ = [
    "User",
    "Member",
    "EventParticipant",
    "EventSessionParticipant",
    "AccessSettings",
    "EventSession",
    "Event",
    "CreatedEvent",
    "CreatedEventSession",
    "Timezone",
    "File",
    "ChatMessage",
    "EventSessionStats",
    "UserStats",
    "WebhookData",
    "WebhookMessage"
]


class User(BaseModel):
    id: Optional[int] = None  # — UserID сотрудника организации;
    name: Optional[str] = None  # — имя сотрудника команды;
    email: Optional[str] = None  # — электронная почта;
    secondName: Optional[str] = None  # — фамилия;


class Member(User):
    patrName: Optional[str] = None  # — отчество;
    nickname: Optional[str] = None  # — имя в чате;
    membershipId: Optional[int] = None  # — идентификатор сотрудника в организации;
    role: Optional[str] = None  # — роль в организации;
    phone: Optional[str] = None  # — телефон;
    position: Optional[str] = None  # — должность;
    organization: Optional[str] = None  # — компания;
    sex: Optional[str] = None  # — половая принадлежность;
    photo: Optional[dict] = None  # — аватар с миниатюрами.
    avatar: Optional[dict] = None  # — аватар с миниатюрами.


class EventParticipant(User):
    id: Optional[int] = None  # — уникальный идентификатор участника в вебинаре (partisipationID);
    eventId: Optional[int] = None  # — ID серии мероприятий(Event), на которую зарегистрирован пользователь.
    eventSessionId: Optional[int] = None  # —  ID сессии мероприятия(EventSession), на
    # Которую зарегистрирован пользователь. Если пользователь
    # зарегистрирован на всю серию целиком - это поле будет пустым (null).
    userId: Optional[int] = None  # — уникальный идентификатор пользователя на платформе;
    url: Optional[str] = None  # — токен для формирования уникальной ссылки на вебинар;
    role: Optional[str] = None  # — роль в вебинаре. Подробнее о ролях;
    registerStatus: Optional[str] = None  # — статус регистрации;
    paymentStatus: Optional[str] = None  # — статус оплаты;
    visited: Optional[bool] = None  # — статус посещения;
    isAccepted: Optional[int] = None  # — статус доступа участника.
    # Если участник на модерации будет 0, если доступ разрешен, то 1.
    isSeen: Optional[int] = None  # — техническое поле, не используется для сотрудников.
    agreementStatus: Optional[str] = None  # — техническое поле, не используется.
    isOnline: Optional[str] = None  # — статус присутствия участия на вебинаре в данный момент.

    def __str__(self):
        return f"{self.name},{self.secondName},{self.email},{self.visited}"


class EventSessionParticipant(User):
    id: Optional[int] = None  # — уникальный идентификатор (partisipationID) пользователя;
    isAccepted: Optional[int] = None  # — статус доступа участника.
    role: Optional[str] = None  # — роль в вебинаре. Подробнее о ролях;
    registerStatus: Optional[str] = None  # — статус регистрации;
    paymentStatus: Optional[str] = None  # — статус оплаты;
    registerDate: Optional[datetime.datetime] = None  # дата регистрации;
    additionalFieldValues: Optional[list] = None  # дополнительные поля из формы регистрации;
    visited: Optional[bool] = None  # статус посещения.

    def __str__(self):
        return f"{self.name},{self.secondName},{self.email},{self.visited}"


class AccessSettings(BaseModel):
    # - isPasswordRequired — доступ с паролем, или без него
    # - isRegistrationRequired — доступ с регистрацией, или без неё
    # - isModerationRequired — доступ с залом ожидания, или без него
    isPasswordRequired: bool
    isRegistrationRequired: bool
    isModerationRequired: bool

    @property
    def to_dict(self) -> dict:
        return {
            "accessSettings[isPasswordRequired]": 1 if self.isPasswordRequired else 0,
            "accessSettings[isRegistrationRequired]": 1 if self.isRegistrationRequired else 0,
            "accessSettings[isModerationRequired]": 1 if self.isModerationRequired else 0,
        }


class EventSession(BaseModel):
    id: Optional[int] = None  # —  идентификатор (eventsessionID);
    name: Optional[str] = None  # — название;
    description: Optional[str] = None  # — описание;
    status: Optional[str] = None  # — текущее состояние вебинара;
    accessSettings: Optional[AccessSettings | dict] = None  #
    # - isPasswordRequired — доступ с паролем, или без него
    # - isRegistrationRequired — доступ с регистрацией, или без неё
    # - isModerationRequired — доступ с залом ожидания, или без него
    access: Optional[int] = None  # — (Архивный способ передачи данных) уровень доступа мероприятия;
    additionalFields: Optional[str | dict] = None  # — информация о дополнительных регистрационных полях;
    lang: Optional[str] = None  # — язык интерфейса мероприятия;
    startsAt: Optional[datetime.datetime] = None  # — дата начала мероприятия;
    timezoneId: Optional[int] = None  # — тайм-зона. Параметр в пользовательских сценариях не используется;
    timezone: Optional[str | dict] = None  # — часовой пояс, установленный при создании вебинара;
    endsAt: Optional[datetime.datetime] = None  # — дата завершения мероприятия;
    organizationId: Optional[int] = None  # — идентификатор организации, которой принадлежит мероприятие
    type: Optional[str] = None  # — тип мероприятия. Может быть вебинар, а может быть встречи. Разница в типах
    # мероприятия;
    createUser: Optional[User] = None  # — подробные данные о владельце мероприятия;
    image: Optional[str | dict] = None  # - фоновое изображение страницы вебинара;
    startType: Optional[str] = None  # — тип вебинара
    # (manual - ручной запуск, autostart - автозапуск, autowebinar - автовебинар);
    lectors: Optional[Sequence[Member]] = None  # — информация о лекторах, добавленных к мероприятию;
    tags: Optional[Sequence] = None  # — набор используемых тегов;
    announceFiles: Optional[Sequence] = None  # — информация о файлах, добавленных к анонсу мероприятия;
    files: Optional[Sequence] = None  # — информация о файлах, добавленных к мероприятию.

    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"name: {self.name}\n"
            f"description: {self.description}\n"
            f"status: {self.status}\n"
            f"startsAt: {str(self.startsAt)}\n"
            f"endsAt: {str(self.endsAt)}\n"
            f"type: {self.type}\n"
            f"startType: {self.startType}\n"
            # f"lectors: {self.lectors}\n"
        )


class Event(BaseModel):
    id: int = None  # идентификатор (EventID) в числовом формате;
    name: str = None  # название;
    description: Optional[str] = None  # — описание;
    status: Optional[str] = None  # текущее состояние вебинара;
    accessSettings: Optional[AccessSettings] = None
    # - isPasswordRequired — доступ с паролем, или без него
    # - isRegistrationRequired — доступ с регистрацией, или без неё
    # - isModerationRequired — доступ с залом ожидания, или без него
    access: Optional[int] = None  # (Архивный способ передачи данных) уровень доступа мероприятия;
    additionalFields: Optional[str | dict] = None  # — информация о дополнительных регистрационных полях;
    rule: Optional[str] = None  # Правило повторения серии мероприятий. У несерийного события правило будет равно
    # FREQ=DAILY;COUNT=1;
    lang: Optional[str] = None  # язык мероприятия;
    startsAt: Optional[datetime.datetime] = None  # дата начала мероприятия;
    utcStartsAt: Optional[datetime.datetime] = None  # дата начала в формате timestamp;
    createUserId: Optional[int] = None  # идентификатор владельца мероприятия (userID);
    timezoneId: Optional[int] = None  # Тайм-зона. Параметр в пользовательских сценариях не используется;;
    endsAt: Optional[datetime.datetime] = None  # дата завершения мероприятия;
    organizationId: Optional[int] = None  # идентификатор организации, которой принадлежит мероприятие;
    type: Optional[str] = None  # тип мероприятия. Может быть вебинар, а может быть встречи
    createUser: Optional[User] = None  # информация о владельце вебинара (id, имя/фамилия, email);
    image: Optional[str | dict] = None  # ссылка на фоновое изображение;
    lectors: Optional[Sequence[Member]] = None  # информация о лекторах, добавленных к мероприятию;
    tags: Optional[Sequence] = None  # набор используемых тегов;
    announceFiles: Optional[Sequence] = None  # информация о файлах, добавленных к анонсу мероприятия;
    files: Optional[Sequence] = None  # информация о файлах, добавленных к мероприятию;
    eventSessions: Optional[Sequence[EventSession]] = None  # информация о мероприятиях, входящих в этот Event.

    # eventSessionsID выдается в числовом формате.

    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"Название: {self.name}\n"
            f"Статус: {self.status}\n"
            f"Начало: {str(self.startsAt)}\n"
            f"Окончание: {str(self.endsAt)}\n"
            f"Правило повторения: {self.rule}\n"
            # f"lectors: {self.lectors}\n"
        )


class CreatedEvent(BaseModel):
    eventId: int  # идентификатор шаблона
    link: str  # публичная ссылка на лендинг мероприятия

    def __str__(self):
        return f"{self.eventId}: {self.link}"


class CreatedEventSession(BaseModel):
    eventSessionId: int  # идентификатор вебинара
    link: str  # Ссылка на сессию. В пользовательских сценариях не используется


class Timezone(BaseModel):
    id: int  # уникальный идентификатор часового пояса (TimeZone);
    name: str  # имя часового пояса (TimeZone);
    description: str  # описание часового пояса (TimeZone);
    offset: int  # смещение часового пояса в секундах;


class File(BaseModel):
    id: Optional[int] = None  # — идентификатор файла/папки;
    parent: Optional[str | dict] = None  # — папка, в которой находится файл/папка. NULL — корневая папка;
    isDeleted: Optional[bool] = None  # — флаг удаления файла/папки. Значения:
    # - true — файл удален;
    # - false — файл доступен в файловом менеджере;
    createAt: Optional[datetime.datetime] = None  # — дата создания/загрузки файла/папки;
    name: Optional[str] = None  # — имя файла/папки;
    type: Optional[Literal['file', 'folder', 'presentation', 'slide', 'test']] = None  # — тип. Значения:
    # - file — файл;
    # - folder — папка;
    user: Optional[Member] = None  # — владелец файла/папки;
    organization: Optional[int | dict] = None  # — принадлежность к Организации;
    path: Optional[str] = None  # — относительный путь файла. В пользовательских сценариях не используется;
    url: Optional[str] = None  # — полный путь файла;
    downloadUrl: Optional[str] = None  # — ссылка на скачивание файла. В пользовательских сценариях не используется;
    thumbnailUrl: Optional[str] = None  # — ссылка на миниатюру картики. В пользовательских сценариях не используется;
    thumbnails: Optional[list | dict] = None  # — миниатюры картинок;
    size: Optional[int] = None  # — размер файла в байтах;
    format: Optional[str] = None  # — расширение файла;
    isHidden: Optional[bool] = None  # — доступность файла. В пользовательских сценариях не используется;
    isSystem: Optional[bool] = None  # — принадлежность файла системе. В пользовательских сценариях не используется;
    mimeType: Optional[str] = None  # — MIME тип файла. В пользовательских сценариях не используется;
    typeFile: Optional[
        Literal['video', 'presentation', 'slide', 'test', 'record', 'ConvertedRecord']
    ] = None  # — тип файла.
    uri: Optional[str] = None  # — uri файла. В пользовательских сценариях не используется;
    thumbnailUri: Optional[str] = None  # — ссылка на миниатюру картинки. В пользовательских сценариях не используется.

    duration: Optional[int] = None  # — длительность видео или теста;
    description: Optional[str] = None  # — описание. Для видео Yotube/Vimeo:
    src: Optional[str] = None  # — ссылка на видео;
    author: Optional[str] = None  # — имя автора видео;
    authorUrl: Optional[str] = None  # — канал автора на Yotube/Vimeo;
    videoId: Optional[int] = None  # — id видео на Vimeo.

    slides: Optional[list | dict] = None  # Набор слайдов. Доступны после конвертации.

    number: Optional[int] = None  # порядок слайда;
    rotate: Optional[int] = None  # угол поворота.

    minAnswers: Optional[int] = None  # минимальное количество ответов, для того чтобы пройти тест;
    minPoints: Optional[int] = None  # минимальное количество баллов;
    assessType: Optional[str] = None  # по какому критерию судить прохождение теста: minAnswers или minPoints;
    contextType: Optional[str] = None  # тест/голосование;
    questions: Optional[list] = None  # вопросы и ответы на них, либо голосование с вариантами ответа;
    testResult: Optional[int] = None  # файл результатов теста.

    cuts: Optional[str] = None  # поле, которое показывает вырезанные отрезки видео в записи.
    # Определяются по полям start – end;
    password: Optional[str] = None  # пароль на запись;
    isViewable: Optional[bool] = None  # открыта ли запись для общего доступа;
    eventSession: Optional[EventSession] = None  # принадлежность вебинару;
    state: Optional[str] = None  # Состояние.

    convertedAt: Optional[datetime.datetime] = None  # дата конвертации;
    progress: Optional[int] = None  # состояние конвертации в %.


class ChatMessage(BaseModel):
    id: Optional[int] = None  # идентификатор сообщения;
    authorName: Optional[str] = None  # имя автора сообщения;
    text: Optional[str] = None  # текст сообщения;
    isModerated: Optional[bool] = None  # Флаг модерации сообщения. Зависит от настроек мероприятия,
    # по умолчанию модерация отключена;
    sentByAdmin: Optional[bool] = None  # отправлено ли сообщение админом мероприятия;
    avatarUrl: Optional[str] = None  # url аватара отправителя;
    thumbnails: Optional[list] = None  # аватар отправителя в различных разрешениях;
    authorId: Optional[int] = None  # id отправителя.
    createAt: Optional[datetime.datetime] = None,
    updateAt: Optional[datetime.datetime] = None,
    updateUserId: Optional[int] = None,
    additionalData: Optional[str] = None,
    attachments: Optional[Sequence] = None,


class EventSessionStats(BaseModel):
    id: Optional[int] = None  # —  идентификатор (eventsessionID);
    name: Optional[str] = None  # — название;
    startsAt: Optional[datetime.datetime] = None  # — дата начала мероприятия;
    endsAt: Optional[datetime.datetime] = None  # — дата завершения мероприятия;
    duration: Optional[int] = None  # — длительность мероприятия в секундах;
    eventId: Optional[int] = None  # — eventID в числовом формате;
    questionCount: Optional[int] = None  # — общее количество вопросов в вебинаре;
    userQuestionCount: Optional[int] = None  # — количество вопросов, заданных участником;
    chatMessageCount: Optional[int] = None  # — общее количество сообщений в чате вебинара;
    userChatMessageCount: Optional[int] = None  # — количество сообщений в чате, написанное участником;
    # additionalFieldValues: Optional[list, dict, str] = None  # — данные из регистрационной формы.
    # Для каждого поля отображаются следующая информация:
    # label — название поля;
    # value — введенные участником данные;
    actualInvolvement: Optional[int | str] = None  # - фактическая активность
    # (время, которое участник был на мероприятии и не переключался на другие вкладки, другие программы,
    # не выключал звук у ведущих);
    speechDuration: Optional[int] = None  # — сколько в часах/минутах был активный звук от данного участника.
    # Если он не был в эфире, то будет 00:00/
    percentOfTotalSpeechDuration: Optional[int | str] = None  # — сколько времени говорил данный участник
    # относительного общего наговоренного времени (не может быть больше 100%);
    usersReactionClicks: Optional[int] = None  # - количество нажатий на огонёк;
    percentOfTotalReactionClicks: Optional[int | str] = None  # - процент нажатий на огонёк данного участника,
    # от общего количество нажатий;
    actualParticipantActivityPercent: Optional[int | float] = None  # - процент присутствия от активного времени
    # ведущих;
    rating: Optional[int] = None  # - рейтинг участника;
    # attentionControl: Optional[int] = None # - данные модуля контроля присутствия.
    # Для каждого из участников отображаются следующие данные:
    # percent — процент подтверждённых окон, от общего количества.
    # shownCount — общее количество окон подтверждения;
    # confirmedCount — количество окон, подтверждённых участником;
    connections: Optional[list] = None  # — все подключения участника к мероприятию.
    # Для каждого подключения отображается следующая информация:
    # joined — время входа;
    # leaved — время выхода;
    # duration — продолжительность присутствия в секундах;
    # country — страна;
    # city — город;
    # referrer — источник перехода;
    # platform — устройство, с которого было подключение. Значения:
    #         Web — компьютер;
    #         iOs — приложение iOs;
    #         Android — приложение Android.
    utms: Optional[list] = None  # — массив данных о полученных utm-метках.
    # Передаются следующие данные, если они есть:
    # utm_source
    # utm_medium
    # utm_campaign
    # utm_content
    # utm_term
    # utm_custom - все прочие метки


class UserStats(BaseModel):
    id: Optional[int]  # — UserID;
    email: Optional[str] = None  # — email;
    name: Optional[str] = None  # — имя;
    secondName: Optional[str] = None  # — фамилия;
    patrName: Optional[str] = None  # — отчество;
    sex: Optional[Literal['m', 'f', 'o']] = None  # — половая принадлежность. Значения:
    # - m — мужчина;
    # - f — женщина;
    # - o — не указан;
    phone: Optional[str] = None  # — телефон;
    organization: Optional[str] = None  # — организация, в которой работает участник;
    position: Optional[str] = None  # — должность;
    eventSessions: Optional[Sequence[EventSessionStats]] = None  # список вебинаров, которые посетил участник


class WebhookData(BaseModel):
    eventSessionId: Optional[int] = None
    eventSessionNewStartsAt: Optional[datetime.datetime] = None
    eventSessionOldStartsAt: Optional[datetime.datetime] = None
    eventUrl: Optional[str] = None
    eventName: Optional[str] = None
    reminderDate: Optional[datetime.datetime] = None
    timezoneName: Optional[str] = None
    eventStartsAt: Optional[datetime.datetime] = None
    eventDescription: Optional[str] = None
    recordId: Optional[int] = None
    convertedRecordId: Optional[int] = None

    def __str__(self):
        result = ""
        if self.eventSessionId:
            result += f"id мероприятия: {self.eventSessionId}\n"
        if self.eventName:
            result += f"Название мероприятия: {self.eventName}\n"
        if self.eventDescription:
            result += f"Описание мероприятия: {self.eventDescription}\n"
        if self.eventStartsAt:
            result += f"Время начала: {self.eventStartsAt.strftime('%Y.%m.%d %H:%M')}\n"
        if self.eventSessionNewStartsAt:
            result += f"Новое время начала: {self.eventSessionNewStartsAt.strftime('%Y.%m.%d %H:%M')}\n"
        if self.eventSessionOldStartsAt:
            result += f"Старое время начала: {self.eventSessionOldStartsAt.strftime('%Y.%m.%d %H:%M')}\n"
        if self.eventUrl:
            result += f"Ссылка на мероприятие: {self.eventUrl}\n"
        if self.reminderDate:
            result += f"Дата и время напоминания: {self.reminderDate.strftime('%Y.%m.%d %H:%M')}\n"
        if self.timezoneName:
            result += f"Часовой пояс: {self.timezoneName}\n"
        if self.recordId:
            result += f"id онлайн-записи: {self.recordId}\n"
        if self.convertedRecordId:
            result += f"id сконвертированного файла: {self.convertedRecordId}\n"
        return result


class WebhookMessage(BaseModel):
    event: Literal[
        "eventSession.created",
        "eventSession.startsAt.changed",
        "event.beforeReminder.sent",
        "eventSession.started",
        "eventSession.users.allLeft",
        "eventSession.ended",
        "recordFile.ready",
        "convertedRecord.ready",
    ]
    occurredAt: datetime.datetime
    data: WebhookData

    def __str__(self):
        result = f"Получено уведомление от платформы ({self.occurredAt.strftime('%Y.%m.%d %H:%M')}):\n"
        match self.event:
            case "eventSession.created":
                result += "Создано мероприятие."
            case "eventSession.startsAt.changed":
                result += "Дата начала мероприятия изменена."
            case "event.beforeReminder.sent":
                result += "Отправлено напоминание о мероприятии."
            case "eventSession.started":
                result += "Мероприятие началось."
            case "eventSession.users.allLeft":
                result += "Все участники покинули мероприятие."
            case "eventSession.ended":
                result += "Мероприятие завершено."
            case "recordFile.ready":
                result += "Онлайн-запись мероприятия готова."
            case "convertedRecord.ready":
                result += "Процесс конвертации завершен."
        result += f"\n\n{str(self.data)}"
        return result
