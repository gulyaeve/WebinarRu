import datetime
from typing import Optional, Sequence

from pydantic import BaseModel


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


class Participant(User):
    id: Optional[int] = None  # — уникальный идентификатор участника в вебинаре (partisipationID);
    eventId: Optional[int] = None  # — ID серии мероприятий(Event), на которую зарегистрирован пользователь.
    eventSessionId: Optional[int] = None  # —  ID сессии мероприятия(EventSession), на
    # которую зарегистрирован пользователь. Если пользователь
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
    description: Optional[str] = None  # —  описание;
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
    startType: Optional[str] = None  # — тип вебинара (manual - ручной запуск, autostart - автозапуск, autowebinar -
    # автовебинар);
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
    description: Optional[str] = None  # —  описание;
    status: Optional[str] = None  # текущее состояние вебинара;
    accessSettings: Optional[AccessSettings] = None
    # - isPasswordRequired — доступ с паролем, или без него
    # - isRegistrationRequired — доступ с регистрацией, или без неё
    # - isModerationRequired — доступ с залом ожидания, или без него
    access: Optional[int] = None  # (Архивный способ передачи данных) уровень доступа мероприятия;
    additionalFields: Optional[str | dict] = None  # — информация о дополнительных регистрационных полях;
    rule: Optional[str] = None  # правило повторения серии мероприятий. У несерийного события правило будет равно
    # FREQ=DAILY;COUNT=1;
    lang: Optional[str] = None  # язык мероприятия;
    startsAt: Optional[datetime.datetime] = None  # дата начала мероприятия;
    utcStartsAt: Optional[datetime.datetime] = None  # дата начала в формате timestamp;
    createUserId: Optional[int] = None  # идентификатор владельца мероприятия (userID);
    timezoneId: Optional[int] = None  # тайм-зона. Параметр в пользовательских сценариях не используется;;
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


class CreatedEventSession(BaseModel):
    eventSessionId: int  # идентификатор вебинара
    link: str  # ссылка на сессию. В пользовательских сценариях не используется


class Timezone(BaseModel):
    id: int  # уникальный идентификатор часового пояса (TimeZone);
    name: str  # имя часового пояса (TimeZone);
    description: str  # описание часового пояса (TimeZone);
    offset: int  # смещение часового пояса в секундах;
