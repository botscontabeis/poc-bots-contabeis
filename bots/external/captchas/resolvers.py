from anticaptchaofficial.imagecaptcha import imagecaptcha

from .base import CaptchaResolver


class AntiCaptchaOfficialCaptchaResolver(CaptchaResolver):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def resolve(self, captcha_image_path) -> str:
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(self._api_key)

        captcha_text = solver.solve_and_return_solution(captcha_image_path)

        if captcha_text != 0:
            return captcha_text

        raise Exception(f"Erro na resolução do Captcha: {solver.error_code} - {solver.err_string}")
