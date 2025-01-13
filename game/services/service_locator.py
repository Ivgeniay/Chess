

class ServiceLocator:
    _services = {}

    @classmethod
    def register(cls, service_type: type, instance: object) -> object:
        """
        Регистрирует сервис в локаторе.

        :param service_type: Тип сервиса (класс).
        :param instance: Экземпляр сервиса.
        """
        if service_type in cls._services:
            raise ValueError(f"Сервис {service_type} уже зарегистрирован.")
        cls._services[service_type] = instance
        return instance

    @classmethod
    def get(cls, service_type: type) -> object:
        if service_type not in cls._services:
            raise ValueError(f"Сервис {service_type} не найден.")
        return cls._services[service_type]

    @classmethod
    def unregister(cls, service_type: type) -> None:
        """
        Удаляет сервис из локатора.

        :param service_type: Тип сервиса (класс).
        """
        if service_type in cls._services:
            del cls._services[service_type]
        else:
            raise ValueError(f"Сервис {service_type} не зарегистрирован.")
