import uuid
from abc import ABC, abstractmethod

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from fake_useragent import UserAgent


class CaptchaResolver(ABC):
    @abstractmethod
    def resolve(self, captcha_image_path: str) -> str:
        pass


class BaseBot(ABC):
    def __init__(self) -> None:
        ua = UserAgent(browsers=["chrome"], os=["windows"], platforms=["pc"])

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument(f"--user-agent={ua.random}")

        self._driver = webdriver.Remote(
            command_executor=settings.SELENIUM_COMMAND_EXECUTOR,
            options=options,
        )
        self._wait = WebDriverWait(self._driver, settings.SELENIUM_WAIT_TIMEOUT_SECONDS)

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
