import datetime
from .base_api import BaseAPI
from .models import *
from typing import Optional, Literal, Sequence


class WebinarAPI(BaseAPI):
    def __init__(
            self,
            token: str,
            base_link: str = "https://userapi.webinar.ru/v3"
    ):
        super().__init__(base_link)
        self.headers = {
            "x-auth-token": token,
            "Accept": "*/*",
        }

    async def get_members(
            self,
            per_page: Optional[
                Literal[10, 50, 100, 250, 500]
            ] = None,  # perPage
            page: Optional[int] = None,
            user_id: Optional[int] = None,  # id
            role: Optional[Literal['admin', 'lecturer']] = None,
            email: Optional[str] = None,
            position: Optional[str] = None,

    ) -> Optional[Sequence[Member]]:
        """
        Получить данные о сотрудниках Организации
        @param per_page: количество сотрудников на одной странице
        @param page: номер страницы
        @param user_id: UserID сотрудника организации
        @param role: роль в организации
        @param email: почта сотрудника организации
        @param position: должность, указанная в профиле
        @return: Коллекция сотрудников
        """
        params = {}
        params.update({"perPage": per_page}) if per_page is not None else ...
        params.update({"page": page}) if page is not None else ...
        params.update({"id": user_id}) if user_id is not None else ...
        params.update({"role": role}) if role is not None else ...
        params.update({"email": email}) if email is not None else ...
        params.update({"position": position}) if position is not None else ...

        members = await self.get_json("/organization/members", params)
        if members is not None:
            return [Member(**member) for member in members]

    async def search_contacts(
            self,
            contact_ids: Optional[list] = None,
            tags: Optional[list] = None,
            contact_data: Optional[
                dict[
                    Literal['name', 'secondName', 'company', 'email', 'phoneMain', 'position'], str
                ]
            ] = None,
            user_ids: Optional[list] = None,
    ) -> Optional[Sequence[Contact]]:
        """
        Поиск контактов по различным критериям.
        :param contact_ids: Идентификатор контакта
        :param tags: теги контактов
        :param contact_data: данные контактов
        :param user_ids: массив ID пользователей. Можно передать несколько userID.
        :return: Коллекция контактов
        """
        params = {}
        params.update(self._make_massive(contact_ids, "contactIds")) if contact_ids else ...
        params.update(self._make_massive(tags, "tags")) if tags else ...
        params.update(self._make_data_massive(contact_data, "contactsData")) if contact_data else ...
        params.update(self._make_massive(user_ids, "userIds")) if user_ids else ...
        contacts = await self.get_json("/contacts/search", params)
        if contacts is not None:
            return [Contact(**contact) for contact in contacts]

    async def register_to_event(
            self,
            event_id: int,
            email: str,
            name: str,
            second_name: str,
            nickname: Optional[str] = None,
            role: Optional[Literal['ADMIN', 'LECTURER', 'GUEST']] = None,
            is_auto_enter: Optional[bool] = None,
            is_accepted: Optional[bool] = None,
            send_email: Optional[bool] = None,
            avatar: Optional[str] = None,
            pattr_name: Optional[str] = None,
            phone: Optional[str] = None,
            description: Optional[str] = None,
            organization: Optional[str] = None,
            position: Optional[str] = None,
            sex: Optional[str] = None,
    ) -> RegisteredParticipant:
        """
        Регистрация участника.
        :param event_id: Идентификатор серии;
        :param email: Электронная почта участника;
        :param name: Имя участника;
        :param second_name: фамилия участника;
        :param nickname: имя в чате. Никнейм пользователя, который будут видеть другие участники;
        :param role: Роль участника на этом мероприятии;
        :param is_auto_enter: Автовход в вебинар;
        :param is_accepted: автоматическое одобрение участника в мероприятиях;
        :param send_email: рассылка писем с платформы mts-link.ru;
        :param avatar: фото участника. URL картинки;
        :param pattr_name: отчество участника;
        :param phone: телефон участника;
        :param description: описание к карточке пользователя;
        :param organization: организация участника;
        :param position: должность участника;
        :param sex: должность участника;
        :return: Данные зарегистрированного участника.
        """
        data = {}
        data.update({"email": email})
        data.update({"name": name})
        data.update({"secondName": second_name})
        data.update({"nickname": nickname}) if nickname else ...
        data.update({"role": role}) if role else ...
        data.update({"isAutoEnter": str(is_auto_enter).lower()}) if is_auto_enter else ...
        data.update({"isAccepted": str(is_accepted).lower()}) if is_accepted else ...
        data.update({"sendEmail": str(send_email).lower()}) if send_email else ...
        data.update({"avatar": avatar}) if avatar else ...
        data.update({"pattrName": pattr_name}) if pattr_name else ...
        data.update({"phone": phone}) if phone else ...
        data.update({"description": description}) if description else ...
        data.update({"organization": organization}) if organization else ...
        data.update({"position": position}) if position else ...
        data.update({"sex": sex}) if sex else ...
        registered_participant = await self.post_json(f"/events/{event_id}/register", data)
        if registered_participant is not None:
            return RegisteredParticipant(**registered_participant)

    async def invite_to_event(
            self,
            event_id: int,
            users: Sequence[EventParticipantInvite],
            is_auto_enter: Optional[bool] = None,
            send_email: Optional[bool] = None,
    ) -> list[RegisteredParticipant]:
        """
        Регистрация участников.
        :param users: Коллекция участников
        :param is_auto_enter: Автовход в вебинар;
        :param send_email: рассылка писем с платформы mts-link.ru;
        :param event_id: Идентификатор серии;
        :return: Данные зарегистрированного участника.
        """
        data = {}
        users = self._make_data_massive_list([user.dict() for user in users], "users")
        data.update(users)
        data.update({"isAutoEnter": str(is_auto_enter).lower()}) if is_auto_enter else ...
        data.update({"sendEmail": str(send_email).lower()}) if send_email else ...
        registered_participants = await self.post_json(f"/events/{event_id}/invite", data)
        if registered_participants is not None:
            return [
                RegisteredParticipant(**registered_participant) for registered_participant in registered_participants
            ]

    async def get_events_for_user(
            self,
            user_id: int,  # userID
            date_from: Optional[datetime.datetime] = None,  # from
            name: Optional[str] = None,
            status: Optional[
                Sequence[Literal['ACTIVE', 'STOP', 'START']]
            ] = None,
            date_to: Optional[datetime.datetime] = None,  # to
            access_settings: Optional[AccessSettings] = None,  # accessSettings
            access: Optional[Literal[1, 3, 4, 6, 8, 10]] = None,
            page: Optional[int] = None,
            per_page: Optional[Literal[10, 50, 100, 250]] = None,  # perPage
    ) -> Optional[Sequence[Event]]:
        """
        Получить данные о мероприятиях сотрудника организации
        @param user_id: идентификатор сотрудника
        @param date_from: дата начала периода выборки
        @param name: названия вебинара
        @param status: статус вебинаров (массив)
        @param date_to: дата окончания периода выборки
        @param access_settings: доступ к мероприятиям. (isPasswordRequired — доступ с паролем;
        isRegistrationRequired — доступ с регистрацией; isModerationRequired — доступ с залом ожидания)
        @param access: уровень доступа к мероприятиям (1 - свободный доступ; 3 - свободный доступ с паролем;
        4 - регистрация; 6 - регистрация с паролем; 8 - регистрация с последующей ручной модерацией участников;
        10 - регистрация с последующей ручной модерацией участников и с паролем)
        @param page: номер страницы выборки
        @param per_page: количество элементов на одной странице выборки
        @return: Коллекция мероприятий
        """
        params = {}
        params.update({"from": str(date_from)}) if date_from is not None else ...
        params.update({"name": name}) if name is not None else ...
        params.update(self._make_massive(status, "status")) if status is not None else ...
        params.update({"to": str(date_to)}) if date_to is not None else ...
        params.update({"accessSettings": access_settings.to_dict}) if access_settings is not None else ...
        params.update({"access": access}) if access is not None else ...
        params.update({"page": page}) if page is not None else ...
        params.update({"perPage": per_page}) if per_page is not None else ...

        events = await self.get_json(
            f"/users/{user_id}/events/schedule",
            params=params
        )
        if events is not None:
            return [Event(**event) for event in events]

    async def get_events(
            self,
            date_from: Optional[datetime.datetime] = None,  # from
            name: Optional[str] = None,
            status: Optional[Sequence[Literal['ACTIVE', 'STOP', 'START']]] = None,
            date_to: Optional[datetime.datetime] = None,  # to
            access_settings: Optional[AccessSettings] = None,  # accessSettings
            access: Optional[Literal[1, 3, 4, 6, 8, 10]] = None,
            page: Optional[int] = None,
            per_page: Optional[Literal[10, 50, 100, 250]] = None,  # perPage
    ) -> Optional[Sequence[Event]]:
        """
        Получить информацию о мероприятиях
        @param date_from: дата начала периода выборки
        @param name: названия вебинара
        @param status: статус вебинаров (массив)
        @param date_to: дата окончания периода выборки
        @param access_settings: доступ к мероприятиям. (isPasswordRequired — доступ с паролем;
        isRegistrationRequired — доступ с регистрацией; isModerationRequired — доступ с залом ожидания)
        @param access: уровень доступа к мероприятиям (1 - свободный доступ; 3 - свободный доступ с паролем;
        4 - регистрация; 6 - регистрация с паролем; 8 - регистрация с последующей ручной модерацией участников;
        10 - регистрация с последующей ручной модерацией участников и с паролем)
        @param page: номер страницы выборки
        @param per_page: количество элементов на одной странице выборки
        @return: Коллекция мероприятий
        """
        params = {}
        params.update({"from": str(date_from)}) if date_from is not None else ...
        params.update({"name": name}) if name is not None else ...
        params.update(self._make_massive(status, "status")) if status is not None else ...
        params.update({"to": str(date_to)}) if date_to is not None else ...
        params.update({"accessSettings": access_settings.to_dict}) if access_settings is not None else ...
        params.update({"access": access}) if access is not None else ...
        params.update({"page": page}) if page is not None else ...
        params.update({"perPage": per_page}) if per_page is not None else ...

        events = await self.get_json(
            "/organization/events/schedule",
            params=params
        )
        if events is not None:
            return [Event(**event) for event in events]

    async def get_event_info(self, event_id: int) -> Optional[Event]:
        """
        Получить данные о серии (Event)
        @param event_id: идентификатор мероприятия (eventID)
        @return: информация о мероприятии
        """
        event = await self.get_json(f"/organization/events/{event_id}")
        if event is not None:
            return Event(**event)

    async def get_event_participations(
            self,
            event_id: int,
            per_page: Optional[Literal[10, 50, 100, 250, 500]] = None,  # perPage
            page: Optional[int] = None,
    ) -> Optional[Sequence[EventParticipant]]:
        """
        Выгрузить статистику по серии мероприятий.
        Запрос позволяет получить информацию об участниках серии мероприятий
        с настройкой "Регистрация на всю серию".
        @param event_id: Идентификатор мероприятия (eventID)
        @param per_page: количество участников на одной странице
        @param page: номер страницы
        @return: коллекция участников
        """
        params = {}
        params.update({"perPage": per_page}) if per_page is not None else ...
        params.update({"page": page}) if page is not None else ...
        participants = await self.get_json(f"/events/{event_id}/participations", params)
        if participants is not None:
            return [EventParticipant(**participant) for participant in participants]

    async def get_event_session_participations(
            self,
            event_session_id: int,
            per_page: Optional[Literal[10, 50, 100, 250, 500]] = None,  # perPage
            page: Optional[int] = None,
    ) -> Optional[Sequence[EventSessionParticipant]]:
        """
        Позволяет получить информацию об участниках, зарегистрированных на мероприятие
        с указанием факта посещения вебинара.
        :param event_session_id: Идентификатор вебинара
        :param per_page: количество участников на одной странице
        :param page: номер страницы
        :rtype: коллекция участников
        """
        params = {}
        params.update({"perPage": per_page}) if per_page is not None else ...
        params.update({"page": page}) if page is not None else ...
        participants = await self.get_json(f"/eventsessions/{event_session_id}/participations", params)
        if participants is not None:
            return [EventSessionParticipant(**participant) for participant in participants]

    async def get_event_session_info(self, event_session_id: int) -> Optional[EventSession]:
        """
        Получить данные о вебинаре
        @param event_session_id: идентификатор вебинара (eventsessionID)
        @return: информация о вебинаре
        """
        event_session = await self.get_json(f"/eventsessions/{event_session_id}")
        if event_session is not None:
            return EventSession(**event_session)

    async def stop_event_session(self, event_session_id: int) -> Optional[bool]:
        """
        Завершает мероприятие.
        :param event_session_id: идентификатор вебинара (eventsessionID)
        :return: True если завершение успешно
        """
        stop_event_session = await self.put(f"/eventsessions/{event_session_id}/stop")
        if stop_event_session is not None:
            return True if stop_event_session.status == 204 else False

    async def get_timezones(self) -> Optional[Sequence[Timezone]]:
        timezones = await self.get_json("/timezones")
        if timezones is not None:
            return [Timezone(**timezone) for timezone in timezones]

    async def delete_event(self, event_id: int) -> Optional[bool]:
        """
        Полностью удалить серию
        @param event_id: идентификатор мероприятия (eventID)
        @return: True если удаление успешно
        """
        delete_event = await self.delete(f"/organization/events/{event_id}")
        if delete_event is not None:
            return True if delete_event == 204 else False

    async def delete_event_session(
            self,
            event_session_id: int,
            send_email: Optional[bool] = None,  # sendEmail
    ) -> Optional[bool]:
        """
        Удаляется вебинар, статистика, чат/вопросы. Удаление нельзя отменить.
        @param send_email: Рассылка писем с платформы Webinar.ru.
        Флаг определяет отправку письма "К сожалению, мероприятие отменено"
        @param event_session_id: идентификатор вебинара (eventsessionID)
        @return: True если удаление успешно
        """
        params = {}
        params.update({"sendEmail": str(send_email).lower()}) if send_email is not None else ...
        delete_event = await self.delete(f"/eventsessions/{event_session_id}", params)
        if delete_event is not None:
            return True if delete_event == 204 else False

    async def create_event(
            self,
            name: str,
            access_settings: AccessSettings,  # AccessSettings
            access: Literal[1, 3, 4, 6, 8, 10],
            password: Optional[str] = None,
            description: Optional[str] = None,
            # additionalFields,  # COMING SOON
            rule: Optional[str] = None,
            is_event_reg_allowed: Optional[bool] = None,  # isEventRegAllowed
            starts_at: Optional[datetime.datetime] = None,  # startsAt
            ends_at: Optional[datetime.datetime] = None,  # endsAt
            timezone: Optional[int] = None,
            image: Optional[int] = None,
            event_type: Optional[Literal['webinar', 'meeting', 'training']] = None,
            lang: Optional[Literal['RU', 'EN']] = None,
            url_alias: Optional[str] = None,  # urlAlias
            lector_ids: Optional[Sequence] = None,  # lectorIds
            tags: Optional[Sequence[str]] = None,
            duration: Optional[str] = None,
            owner_id: Optional[int] = None,  # ownerId
            default_reminders_enabled: Optional[bool] = None,  # defaultRemindersEnabled
            branding_id: Optional[int] = None,  # brandingId
    ) -> Optional[CreatedEvent]:
        """
        Создать шаблон (Event). Event — техническая “оболочка” мероприятия,
        содержащая в себе его основные параметры: описание, файлы, настройки и правила повторения.
        @param name: Название мероприятия
        @param access_settings: доступ к мероприятиям (isPasswordRequired — доступ с паролем;
        isRegistrationRequired — доступ с регистрацией; isModerationRequired — доступ с залом ожидания)
        @param access: уровень доступа к мероприятию (1 - свободный доступ; 3 - свободный доступ с паролем;
        4 - регистрация; 6 - регистрация с паролем; 8 - регистрация с последующей ручной модерацией участников;
        10 - регистрация с последующей ручной модерацией участников и с паролем)
        @param password: пароль для входа на мероприятие
        @param description: описание мероприятия. Текстовое поле. Отсутствует разметка или верстка
        @param rule: [Обязательно для серии] правило генерации дат повторения событий в серийном мероприятии.
        https://tools.ietf.org/html/rfc5545#section-3.3.10
        @param is_event_reg_allowed: [Обязательно для серии] правило регистрации на серию.
        @param starts_at: Дата/время начала мероприятия
        @param ends_at: [Обязательно для серии] дата/время завершения серии мероприятий
        @param timezone: часовой пояс вебинара. Передаётся в виде id.
        @param image: Фон вебинара. ID файла в файловой системе, который будет использован в качестве фона
        @param event_type: тип мероприятия
        @param lang: язык интерфейса мероприятия
        @param url_alias: замена названия вебинара в ссылке. Заменяет eventID в ссылке на вебинар
        @param lector_ids: ведущий на лендинге. Добавляет иконку с фото и данными ведущего.
        Передается как массив userID сотрудников организации
        @param tags: теги мероприятия. Массив тегов, которые будут добавлены к мероприятию
        @param duration: длительность мероприятия. Меняет значение "Продолжительность" на лендинге,
        но не определяет фактическое время завершения. Значение данного поля должно подпадать под регулярное выражение
        @param owner_id: владелец мероприятия. UserID сотрудника организации
        @param default_reminders_enabled: стандартные напоминания. Включает/отключает набор стандартных напоминаний
        @param branding_id: выбрать шаблон брендирования для мероприятия. Указывается идентификатор шаблона
        @return: eventId — идентификатор шаблона, link — публичная ссылка на лендинг мероприятия
        """
        data = {
            "name": name,
            "AccessSettings": access_settings.to_dict,
            "access": access,
        }
        data.update({"password": password}) if password is not None else ...
        data.update({"description": description}) if description is not None else ...
        data.update({"rule": rule}) if rule is not None else ...
        data.update(
            {"isEventRegAllowed": str(is_event_reg_allowed).lower()}
        ) if is_event_reg_allowed is not None else ...
        data.update(self._datetime_to_dict("startsAt", starts_at)) if starts_at is not None else ...
        data.update(self._datetime_to_dict("endsAt", ends_at)) if ends_at is not None else ...
        data.update({"timezone": timezone}) if timezone is not None else ...
        data.update({"image": image}) if image is not None else ...
        data.update({"type": event_type}) if event_type is not None else ...
        data.update({"lang": lang}) if lang is not None else ...
        data.update({"urlAlias": url_alias}) if url_alias is not None else ...
        data.update(self._make_massive(lector_ids, "lectorIds")) if lector_ids is not None else ...
        data.update(self._make_massive(tags, "tags")) if tags is not None else ...
        data.update({"duration": duration}) if duration is not None else ...
        data.update({"ownerId": owner_id}) if owner_id is not None else ...
        data.update(
            {"defaultRemindersEnabled": str(default_reminders_enabled).lower()}
        ) if default_reminders_enabled is not None else ...
        data.update({"brandingId": branding_id}) if branding_id is not None else ...

        new_event = await self.post_json("/events", data)
        if new_event is not None:
            return CreatedEvent(**new_event)

    async def edit_event(
            self,
            event_id: int,  # eventID
            name: Optional[str] = None,
            access_settings: Optional[AccessSettings] = None,  # AccessSettings
            access: Optional[Literal[1, 3, 4, 6, 8, 10]] = None,
            status: Optional[Literal['ACTIVE', 'STOP', 'START']] = None,
            password: Optional[str] = None,
            description: Optional[str] = None,
            lang: Optional[Literal['RU', 'EN']] = None,
            url_alias: Optional[str] = None,  # urlAlias
            starts_at: Optional[datetime.datetime] = None,  # startsAt
            timezone: Optional[int] = None,
            image: Optional[int] = None,
            duration: Optional[str] = None,
            owner_id: Optional[int] = None,  # ownerId
            branding_id: Optional[int] = None,  # brandingId
    ) -> Optional[bool]:
        """
        Позволяет отредактировать мероприятие Eventid. Обновлять можно только вебинары со статусом ACTIVE
        @param event_id: идентификатор мероприятия
        @param name: название мероприятия
        @param access_settings: доступ к мероприятиям (isPasswordRequired — доступ с паролем;
        isRegistrationRequired — доступ с регистрацией; isModerationRequired — доступ с залом ожидания)
        @param access: уровень доступа к мероприятию (1 - свободный доступ; 3 - свободный доступ с паролем;
        4 - регистрация; 6 - регистрация с паролем; 8 - регистрация с последующей ручной модерацией участников;
        10 - регистрация с последующей ручной модерацией участников и с паролем)
        @param status: статус мероприятия (массив). Передав значение STOP, можно завершить мероприятие
        @param password: пароль для входа на мероприятие
        @param description: описание мероприятия. Текстовое поле. Отсутствует разметка или верстка
        @param lang: язык интерфейса мероприятия
        @param url_alias: замена названия вебинара в ссылке. Заменяет eventID в ссылке на вебинар
        @param starts_at: дата/время начала мероприятия
        @param timezone: часовой пояс вебинара. Передаётся в виде id.
        @param image: Фон вебинара. ID файла в файловой системе, который будет использован в качестве фона
        @param duration: длительность мероприятия. Меняет значение "Продолжительность" на лендинге,
        но не определяет фактическое время завершения. Значение данного поля должно подпадать под регулярное выражение
        @param owner_id: владелец мероприятия. UserID сотрудника организации
        @param branding_id: выбрать шаблон брендирования для мероприятия. Указывается идентификатор шаблона
        @return: True если изменено
        """
        data = {}
        data.update({"name": name}) if name is not None else ...
        data.update({"AccessSettings": access_settings.to_dict}) if access_settings is not None else ...
        data.update({"access": access}) if access is not None else ...
        data.update({"status": status}) if status is not None else ...
        data.update({"password": password}) if password is not None else ...
        data.update({"description": description}) if description is not None else ...
        data.update({"lang": lang}) if lang is not None else ...
        data.update({"urlAlias": url_alias}) if url_alias is not None else ...
        data.update(self._datetime_to_dict("startsAt", starts_at)) if starts_at is not None else ...
        data.update({"timezone": timezone}) if timezone is not None else ...
        data.update({"image": image}) if image is not None else ...
        data.update({"duration": duration}) if duration is not None else ...
        data.update({"ownerId": owner_id}) if owner_id is not None else ...
        data.update({"brandingId": branding_id}) if branding_id is not None else ...

        edited_event = await self.put(f"/events/{event_id}", data)
        if edited_event is not None:
            return True if edited_event.status == 204 else False

    async def create_event_session(
            self,
            event_id: int,
            name: Optional[str] = None,
            access_settings: Optional[AccessSettings] = None,  # accessSettings
            access: Optional[Literal[1, 3, 4, 6, 8, 10]] = None,
            start_type: Optional[Literal['manual', 'autostart', 'autowebinar']] = None,  # startType
            description: Optional[str] = None,
            lang: Optional[Literal['RU', 'EN']] = None,
            starts_at: Optional[datetime.datetime] = None,  # startsAt
            timezone: Optional[int] = None,
            image: Optional[int] = None,
    ) -> Optional[CreatedEventSession]:
        """
        Создать вебинар (Eventsession)
        @param event_id: id шаблона (EventID).
        @param name: Название мероприятия
        @param access_settings: доступ к мероприятиям (isPasswordRequired — доступ с паролем;
        isRegistrationRequired — доступ с регистрацией; isModerationRequired — доступ с залом ожидания)
        @param access: уровень доступа к мероприятию (1 - свободный доступ; 3 - свободный доступ с паролем;
        4 - регистрация; 6 - регистрация с паролем; 8 - регистрация с последующей ручной модерацией участников;
        10 - регистрация с последующей ручной модерацией участников и с паролем)
        @param start_type: тип запуска мероприятия. Значения: manual — ручной запуск мероприятия;
        autostart — автоматический запуск мероприятия в указанное время; autowebinar — автовебинар.
        @param description: Описание мероприятия. Текстовое поле.
        @param lang: Язык интерфейса мероприятия
        @param starts_at: дата/время начала мероприятия
        @param timezone: часовой пояс вебинара. Передаётся в виде id.
        @param image: Фон вебинара. ID файла в файловой системе, который будет использован в качестве фона
        @return: eventsessionId — идентификатор вебинара. Используется для регистрации на вебинары, работы с записью;
        link — ссылка на сессию. В пользовательских сценариях не используется.
        """
        data = {}
        data.update({"name": name}) if name is not None else ...
        data.update({"accessSettings": access_settings.to_dict}) if access_settings is not None else ...
        data.update({"access": access}) if access is not None else ...
        data.update({"startType": start_type}) if start_type is not None else ...
        data.update({"description": description}) if description is not None else ...
        data.update({"lang": lang}) if lang is not None else ...
        data.update(self._datetime_to_dict("startsAt", starts_at)) if starts_at is not None else ...
        data.update({"timezone": timezone}) if timezone is not None else ...
        data.update({"image": image}) if image is not None else ...
        new_event_session = await self.post_json(f"/events/{event_id}/sessions", data)
        if new_event_session is not None:
            return CreatedEventSession(**new_event_session)

    async def edit_event_session(
            self,
            event_session_id: int,  # eventsessionID,
            name: Optional[str] = None,
            access_settings: Optional[AccessSettings] = None,  # AccessSettings
            access: Optional[Literal[1, 3, 4, 6, 8, 10]] = None,
            start_type: Optional[Literal['manual', 'autostart', 'autowebinar']] = None,  # startType
            description: Optional[str] = None,
            lang: Optional[Literal['RU', 'EN']] = None,
            starts_at: Optional[datetime.datetime] = None,  # startsAt
            timezone: Optional[int] = None,
            image: Optional[int] = None,
            duration: Optional[str] = None,
            # additional_fields  # Coming soon
            send_email: Optional[bool] = None,  # sendEmail
            update_context: Optional[Literal['series']] = None,  # updateContext
    ) -> Optional[bool]:
        """
        Запросом обновляются только данные EventSession.
        Обновлять можно только сессии со статусом ACTIVE и START
        @param event_session_id: идентификатор вебинара
        @param name: название мероприятия
        @param access_settings: доступ к мероприятиям
        @param access: уровень доступа к мероприятию
        @param start_type: тип запуска мероприятия
        @param description: описание мероприятия
        @param lang: язык интерфейса мероприятия
        @param starts_at: дата/время начала мероприятия
        @param timezone: часовой пояс вебинар
        @param image: фон вебинара. ID файла в файловой системе, который будет использован в качестве фона
        @param duration: длительность мероприятия
        @param send_email: рассылка писем с платформы Webinar.ru.
        Флаг определяет отправку письма "Вебинар перенесен на другое время"
        @param update_context: параметр, который указывает сервису, что рассылку писем требуется убрать/включить
        в рамках серийного мероприятия для конкретного события в определенную дату
        @return True если изменено
        """
        data = {}
        data.update({"name": name}) if name is not None else ...
        data.update({"AccessSettings": access_settings.to_dict}) if access_settings is not None else ...
        data.update({"access": access}) if access is not None else ...
        data.update({"startType": start_type}) if start_type is not None else ...
        data.update({"description": description}) if description is not None else ...
        data.update({"lang": lang}) if lang is not None else ...
        data.update(self._datetime_to_dict("startsAt", starts_at)) if starts_at is not None else ...
        data.update({"timezone": timezone}) if timezone is not None else ...
        data.update({"image": image}) if image is not None else ...
        data.update({"duration": duration}) if duration is not None else ...
        data.update({"sendEmail": str(send_email).lower()}) if send_email is not None else ...
        data.update({"updateContext": update_context}) if update_context is not None else ...

        edited_event_session = await self.put(f"/eventsessions/{event_session_id}", data)
        if edited_event_session is not None:
            return True if edited_event_session.status == 204 else False

    async def create_webinar(
            self,
            name: str,
            access_settings: AccessSettings,  # AccessSettings
            access: Literal[1, 3, 4, 6, 8, 10],
            password: Optional[str] = None,
            description: Optional[str] = None,
            # additionalFields,  # COMING SOON
            rule: Optional[str] = None,
            is_event_reg_allowed: Optional[bool] = None,  # isEventRegAllowed
            starts_at: Optional[datetime.datetime] = None,  # startsAt
            ends_at: Optional[datetime.datetime] = None,  # endsAt
            timezone: Optional[int] = None,
            image: Optional[int] = None,
            event_type: Optional[Literal['webinar', 'meeting', 'training']] = None,
            lang: Optional[Literal['RU', 'EN']] = None,
            url_alias: Optional[str] = None,  # urlAlias
            lector_ids: Optional[Sequence] = None,  # lectorIds
            tags: Optional[Sequence] = None,
            duration: Optional[str] = None,
            owner_id: Optional[int] = None,  # ownerId
            default_reminders_enabled: Optional[bool] = None,  # defaultRemindersEnabled
            branding_id: Optional[int] = None,  # brandingId
            start_type: Optional[Literal['manual', 'autostart', 'autowebinar']] = None,  # startType
    ) -> Optional[CreatedEvent]:
        """
        Создание шаблона и вебинара.
        @param name: Название мероприятия
        @param access_settings: доступ к мероприятиям (isPasswordRequired — доступ с паролем;
        isRegistrationRequired — доступ с регистрацией; isModerationRequired — доступ с залом ожидания)
        @param access: уровень доступа к мероприятию (1 - свободный доступ; 3 - свободный доступ с паролем;
        4 - регистрация; 6 - регистрация с паролем; 8 - регистрация с последующей ручной модерацией участников;
        10 - регистрация с последующей ручной модерацией участников и с паролем)
        @param password: пароль для входа на мероприятие
        @param description: описание мероприятия. Текстовое поле. Отсутствует разметка или верстка
        @param rule: [Обязательно для серии] правило генерации дат повторения событий в серийном мероприятии.
        https://tools.ietf.org/html/rfc5545#section-3.3.10
        @param is_event_reg_allowed: [Обязательно для серии] правило регистрации на серию.
        @param starts_at: Дата/время начала мероприятия
        @param ends_at: [Обязательно для серии] дата/время завершения серии мероприятий
        @param timezone: часовой пояс вебинара. Передаётся в виде id.
        @param image: Фон вебинара. ID файла в файловой системе, который будет использован в качестве фона
        @param event_type: тип мероприятия
        @param lang: язык интерфейса мероприятия
        @param url_alias: замена названия вебинара в ссылке. Заменяет eventID в ссылке на вебинар
        @param lector_ids: ведущий на лендинге. Добавляет иконку с фото и данными ведущего.
        Передается как массив userID сотрудников организации
        @param tags: теги мероприятия. Массив тегов, которые будут добавлены к мероприятию
        @param duration: длительность мероприятия. Меняет значение "Продолжительность" на лендинге,
        но не определяет фактическое время завершения. Значение данного поля должно подпадать под регулярное выражение
        @param owner_id: владелец мероприятия. UserID сотрудника организации
        @param default_reminders_enabled: стандартные напоминания. Включает/отключает набор стандартных напоминаний
        @param branding_id: выбрать шаблон брендирования для мероприятия. Указывается идентификатор шаблона
        @param start_type: тип запуска мероприятия. Значения: manual — ручной запуск мероприятия;
        autostart — автоматический запуск мероприятия в указанное время; autowebinar — автовебинар.
        @return: eventId — идентификатор шаблона, link — публичная ссылка на лендинг мероприятия
        """
        new_event = await self.create_event(
            name=name,
            access_settings=access_settings,
            access=access,
            password=password,
            description=description,
            rule=rule,
            is_event_reg_allowed=is_event_reg_allowed,
            starts_at=starts_at,
            ends_at=ends_at,
            timezone=timezone,
            image=image,
            event_type=event_type,
            lang=lang,
            url_alias=url_alias,
            lector_ids=lector_ids,
            tags=tags,
            duration=duration,
            owner_id=owner_id,
            default_reminders_enabled=default_reminders_enabled,
            branding_id=branding_id,
        )

        if new_event is not None:
            await self.create_event_session(
                event_id=new_event.eventId,
                start_type=start_type,
            )
            return new_event

    async def get_chat_messages(
            self,
            event_session_id: int,  # eventsessionID
            is_moderated: Optional[bool] = None,  # isModerated
            limit: Optional[int] = None,
            author_id: Optional[int] = None,  # authorId
            private_chat: Optional[bool] = None,  # privateChat
    ) -> Optional[Sequence[ChatMessage]]:
        """
        Получает все сообщения из чата по eventSessionId вебинара.
        :param event_session_id: Идентификатор вебинара
        :param is_moderated: статус модерации сообщений
        :param limit: количество отображаемых сообщений. Значение по умолчанию: последние 100.
        :param author_id: идентификатор пользователя, отправившего сообщение
        :param private_chat: получить приватный чат. Параметр используется только с указанием authorId
        :return: массив сообщений
        """
        params = {}
        params.update({"isModerated": str(is_moderated).lower()}) if is_moderated is not None else ...
        params.update({"limit": limit}) if limit is not None else ...
        params.update({"author_id": author_id}) if author_id is not None else ...
        params.update({"privateChat": str(private_chat).lower()}) if private_chat is not None else ...

        messages = await self.get_json(f"/eventsessions/{event_session_id}/chat", params)
        # print(messages)
        if messages is not None:
            return [ChatMessage(**message) for message in messages]

    async def get_files(
            self,
            user: Optional[int] = None,
            parent: Optional[str] = None,
            file_format: Optional[str] = None,
            is_shared: Optional[bool] = None,  # isShared
    ) -> Optional[Sequence[File]]:
        """
        Получить список файлов
        :param user: ID сотрудника организации
        :param parent: папка. Можно ограничить поиск по конкретной папке
        :param file_format: расширение файла
        :param is_shared: поиск по общей папке
        """
        params = {}
        params.update({"user": user}) if user is not None else ...
        params.update({"parent": parent}) if parent is not None else ...
        params.update({"format": file_format}) if file_format is not None else ...
        params.update({"isShared": str(is_shared).lower()}) if is_shared is not None else ...

        files = await self.get_json("/fileSystem/files", params)
        # pprint(files)
        if files is not None:
            return [File(**file) for file in files]

    async def get_file(
            self,
            file_id: int,  # fileID
            name: Optional[str] = None,
    ) -> Optional[File]:
        """
        Получить файл по его идентификатору
        :param file_id: Идентификатор файла
        :param name: имя файла
        """
        params = {}
        params.update({"name": name}) if name is not None else ...

        file = await self.get_json(f"/fileSystem/file/{file_id}", params)
        # print(file)
        if file is not None:
            return File(**file)

    async def get_event_files(
            self,
            event_id: int,
            file_id: Optional[int] = None,  # fileId
    ) -> Optional[Sequence[File]]:
        """
        Получает список файлов, прикрепленных к серии вебинаров.
        :param event_id: Идентификатор мероприятия
        :param file_id: ID файла
        :return: коллекция файлов
        """
        params = {}
        params.update({"fileId": file_id}) if file_id is not None else ...
        files = await self.get_json(f"/events/{event_id}/files", params)
        # print(files)
        if files is not None:
            return [File(**file['file']) for file in files]

    async def get_event_session_files(
            self,
            event_session_id: int,  # eventsessionsID
            file_id: Optional[int] = None,  # fileId
    ) -> Optional[Sequence[File]]:
        """
        Получает список файлов, прикрепленных к вебинару.
        :param event_session_id: идентификатор вебинара
        :param file_id: ID файла
        :return: коллекция файлов
        """
        params = {}
        params.update({"fileId": file_id}) if file_id is not None else ...
        files = await self.get_json(f"/eventsessions/{event_session_id}/files", params)
        # print(files)
        if files is not None:
            return [File(**file['file']) for file in files]

    async def get_records(
            self,
            date_from: Optional[datetime.datetime] = None,  # from
            record_id: Optional[int] = None,  # id
            period: Optional[Literal['day', 'week', 'month', 'year']] = None,
            date_to: Optional[datetime.datetime] = None,  # to
            user_id: Optional[int] = None,  # userId
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> Optional[Sequence[File]]:
        """
        Получить список записей
        :param date_from: дата начала периода выборки
        :param record_id: ID онлайн-записи
        :param period: период выборки
        :param date_to: дата окончания периода выборки
        :param user_id: ID сотрудника Организации
        :param offset: параметр для пагинации результата. Значения: 0, 10, 20, 30 и т.д.
        :param limit: параметр для определения количества отображаемых результатов
        :return: Коллекция записей
        """
        params = {}
        params.update({"from": str(date_from)}) if date_from is not None else ...
        params.update({"id": record_id}) if record_id is not None else ...
        params.update({"period": period}) if period is not None else ...
        params.update({"to": str(date_to)}) if date_to is not None else ...
        params.update({"userId": user_id}) if user_id is not None else ...
        params.update({"offset": offset}) if offset is not None else ...
        params.update({"limit": limit}) if limit is not None else ...

        records = await self.get_json("/records", params)
        # pprint(records)
        if records is not None:
            return [File(**record) for record in records]

    async def share_online_record_by_id(
            self,
            record_id: int,
            is_viewable: Optional[bool] = None,  # isViewable
            password: Optional[str] = None,
            view_access: Optional[Literal['owner', 'memberships', 'participants', 'all']] = None,
    ):
        """
        Запросом меняются параметры записи: доступность записи по ссылке
        :param record_id: id онлайн-записи
        :param is_viewable: доступность записи;
        :param password: пароль на запись;
        :param view_access: настройка доступа для показа записи.
        """
        params = {}
        params.update({"isViewable": str(is_viewable).lower()}) if is_viewable is not None else ...
        params.update({"password": password}) if password is not None else ...
        params.update({"viewAccess": view_access}) if view_access is not None else ...

        await self.put(f"/records/{record_id}", params)

    async def share_online_record_by_event_session_id(
            self,
            event_session_id: int,  # eventsessionsID
            is_viewable: Optional[bool] = None,  # isViewable
            password: Optional[str] = None,
            view_access: Optional[Literal['owner', 'memberships', 'participants', 'all']] = None,
    ):
        """
        Запросом меняются параметры записи: доступность записи по ссылке,
        настройки доступа и наличие пароля на просмотр
        :param event_session_id: Идентификатор вебинара;
        :param is_viewable: доступность записи;
        :param password: пароль на запись;
        :param view_access: настройка доступа для показа записи.
        """
        params = {}
        params.update({"isViewable": str(is_viewable).lower()}) if is_viewable is not None else ...
        params.update({"password": password}) if password is not None else ...
        params.update({"viewAccess": view_access}) if view_access is not None else ...

        await self.put(f"/eventsessions/{event_session_id}/records", params)

    async def share_online_record_by_email(
            self,
            record_id: int,
    ):
        """
        Запросом отправляется Email-рассылка "Организатор поделился записью вебинара".
        :param record_id: id онлайн-записи
        """
        await self.post_json(f"/records/{record_id}/share")

    async def get_online_record_link(
            self,
            record_id: int,
    ) -> Optional[str]:
        """
        Получить ссылку на запись по идентификатору
        :param record_id: id онлайн-записи
        :return: ссылка на онлайн-запись
        """
        record_link = (await self.get_records(record_id=record_id))[0].link
        if record_link:
            return record_link

    async def get_events_stats(
            self,
            date_from: Optional[datetime.datetime] = None,
            date_to: Optional[datetime.datetime] = None,  # to
            user_id: Optional[int] = None,  # userId
            event_id: Optional[int] = None,  # eventId
    ) -> Optional[Sequence[EventStats]]:
        params = {}
        params.update({"from": str(date_from)}) if date_from is not None else ...
        params.update({"to": str(date_to)}) if date_to is not None else ...
        params.update({"userId": str(user_id)}) if user_id is not None else ...
        params.update({"eventId": str(event_id)}) if event_id is not None else ...
        event_stats = await self.get_json("/stats/events", params)
        if event_stats:
            return [EventStats(**event_stat) for event_stat in event_stats]

    async def get_users_stats(
            self,
            date_from: Optional[datetime.datetime],  # from
            date_to: Optional[datetime.datetime] = None,  # to
            event_id: Optional[int] = None,  # eventId
    ) -> Optional[Sequence[UserStats]]:
        """
        Возвращается массив данных о посещении мероприятий конкретными участниками.
        Внимание! Если не указать from, то дата начала периода выборки будет равна текущей дате и времени и
        данные будут не валидны.
        :return: Массив данных о посещении мероприятий
        :param date_from: Дата начала периода выборки.
        :param date_to: Дата окончания периода выборки. По умолчанию: from +1 год.
        :param event_id: EventID вебинара. Позволяет получить данные о конкретном мероприятии.
        """
        params = {}
        params.update({"from": str(date_from)}) if date_from is not None else ...
        params.update({"to": str(date_to)}) if date_to is not None else ...
        params.update({"eventId": str(event_id)}) if event_id is not None else ...
        users_stats = await self.get_json("/stats/users", params)
        if users_stats is not None:
            return [UserStats(**user_stats) for user_stats in users_stats]

    @staticmethod
    def _datetime_to_dict(title: Literal['startsAt', 'endsAt'], input_datetime: datetime.datetime) -> dict:
        """
        Используется для конвертации даты и времени в словарь совместимый с платформой.
        @param title: Заголовок
        @param input_datetime: дата и время в формате datetime
        @return: словарь для запроса
        """
        return {
            f"{title}[date][year]": input_datetime.year,
            f"{title}[date][month]": input_datetime.month,
            f"{title}[date][day]": input_datetime.day,
            f"{title}[time][hour]": input_datetime.hour,
            f"{title}[time][minute]": input_datetime.minute
        }

    @staticmethod
    def _make_massive(collection: Sequence, label: str) -> dict:
        """
        Используется для преобразования коллекций в массив, совместимый с платформой
        @param collection: список элементов
        @param label: ключ
        @return: словарь, совместимый с платформой
        """
        data = {}
        for index, item in enumerate(collection):
            data.update({f"{label}[{index}]": item})
        return data

    @staticmethod
    def _make_data_massive(collection: dict, label: str) -> dict:
        """
        Используется для преобразования коллекций в массив данных, совместимый с платформой
        @param collection: словарь элементов
        @param label: ключ
        @return: словарь, совместимый с платформой
        """
        data = {}
        for key, item in collection.items():
            data.update({f"{label}[{key}]": item})
        return data

    @staticmethod
    def _make_data_massive_list(collection: list[dict], label: str) -> dict:
        """
        Используется для преобразования коллекций в массив данных, совместимый с платформой
        @param collection: список словарей элементов
        @param label: ключ
        @return: словарь, совместимый с платформой
        """
        data = {}
        for index, value in enumerate(collection):
            for key, item in value.items():
                data.update({f"{label}[{index}][{key}]": item}) if item is not None else ...
        return data
