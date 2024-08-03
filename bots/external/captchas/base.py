from abc import ABC, abstractmethod


class CaptchaResolver(ABC):
    @abstractmethod
    def resolve(self, captcha_image_path: str) -> str:
        pass
