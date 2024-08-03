import uuid
from abc import ABC, abstractmethod

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


class CaptchaResolver(ABC):
    @abstractmethod
    def resolve(self, captcha_image_path: str) -> str:
        pass


class BaseBot(ABC):
    WAIT_TIMEOUT_SECONDS = 5

    def __init__(self) -> None:
        options = Options()
        options.add_argument("--start-maximized")
        self._driver = webdriver.Remote(
            command_executor=settings.SELENIUM_COMMAND_EXECUTOR,
            options=options,
        )
        self._wait = WebDriverWait(self._driver, self.WAIT_TIMEOUT_SECONDS)

        self._resultados = []
        self._erro = None

        self._execution_id = uuid.uuid4()

    def executar(self):
        try:
            self.processo()

        except Exception as e:
            self._erro = e

        finally:
            try:
                self._teardown()

            except Exception:
                pass

            return self._resultados, self._erro

    @abstractmethod
    def processo(self):
        pass

    def _teardown(self):
        self._driver.quit()
