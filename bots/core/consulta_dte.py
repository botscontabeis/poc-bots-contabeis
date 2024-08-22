import logging
from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from bots.helpers import convert_base64_to_jpg_and_save_file, delete_file
from core.models import Cliente

from .. import credentials
from .base import BaseBot, CaptchaResolver

logger = logging.getLogger(__name__)


class ConsultaDteBot(BaseBot):
    # App (UVT)
    APP_URL = "https://uvt.set.rn.gov.br/"

    # Locators
    BTN_USUARIO_SENHA = (By.ID, "codeaccess-btn")
    INPUT_CODIGO = (By.ID, "code")
    INPUT_SENHA = (By.ID, "password")
    BTN_ACESSAR = (By.CSS_SELECTOR, '[ng-click="passwordLogin()"]')
    IMG_CAPTCHA = (By.CSS_SELECTOR, '[ng-show="captchaImage"] img')
    INPUT_CAPTCHA = (By.ID, "captcha")
    BTN_SELECIONAR_EMPRESA = (By.CSS_SELECTOR, '[ng-click="selectCompany()"]')
    INPUT_PESQUISAR_EMPRESA = (By.ID, "identificacao")
    LINK_EMPRESA_ENCONTRADA = (By.CSS_SELECTOR, '[ng-click="select($index)"]')
    BTN_DTE = (By.CSS_SELECTOR, '[ng-click="dteShowDetails()"]')
    BTN_FECHAR = (By.CSS_SELECTOR, '[ng-click="cancel()"]')
    MODAL_DTE = (By.CSS_SELECTOR, ".modal-body")

    def __init__(self, clientes: Iterable[Cliente], captcha_resolver: CaptchaResolver) -> None:
        super().__init__()
        self._captcha_resolver = captcha_resolver
        self._clientes = clientes

    def processo(self):
        logger.info("Iniciando processo de consulta de DTE")

        self.acessar_uvt()
        self.fazer_login_pf()

        for cliente in self._clientes:
            self.selecionar_empresa(cliente.cnpj_ou_cpf)
            self.consultar_dte(cliente.id)

        logger.info("Finalizado processo de consulta de DTE")

    def acessar_uvt(self):
        # TODO: mover para classe base de bots da UVT
        logger.info("Acessando UVT")

        self._driver.get(self.APP_URL)

        self._wait.until(ec.element_to_be_clickable(self.BTN_USUARIO_SENHA))

    def fazer_login_pf(self):
        # TODO: mover para classe base de bots da UVT
        # TODO: implementar tratamento de erro quando modal de bloqueio é exibido
        # TODO: implementar exception handler para ElementClickInterceptedException que tira print da tela e salva em arquivo

        logger.info("Fazendo login como pessoa física")

        self._wait.until(ec.element_to_be_clickable(self.BTN_USUARIO_SENHA)).click()
        self._wait.until(ec.element_to_be_clickable(self.INPUT_CODIGO)).send_keys(credentials.UVT_USERNAME)
        self._wait.until(ec.element_to_be_clickable(self.INPUT_SENHA)).send_keys(credentials.UVT_PASSWORD)

        logger.info("Buscando imagem do captcha")
        captcha_base64 = self._wait.until(ec.visibility_of_element_located(self.IMG_CAPTCHA)).get_attribute("src")
        captcha_image_path = f"bots/data/captchas/captcha-{self._execution_id}.jpg"
        convert_base64_to_jpg_and_save_file(captcha_base64, captcha_image_path)

        logger.info("Resolvendo captcha")
        captcha_text = self._captcha_resolver.resolve(captcha_image_path)
        self._wait.until(ec.element_to_be_clickable(self.INPUT_CAPTCHA)).send_keys(captcha_text)

        delete_file(captcha_image_path)

        self._wait.until(ec.element_to_be_clickable(self.BTN_ACESSAR)).click()

        self._wait.until(ec.element_to_be_clickable(self.BTN_SELECIONAR_EMPRESA))
        logger.info("Login realizado com sucesso")

    def selecionar_empresa(self, cnpj_ou_cpf):
        # TODO: tratar caso em que a empresa não é encontrada
        # TODO: mover para classe base de bots da UVT

        logger.info("Selecionando empresa")
        self._wait.until(ec.element_to_be_clickable(self.BTN_SELECIONAR_EMPRESA)).click()
        self._wait.until(ec.element_to_be_clickable(self.INPUT_PESQUISAR_EMPRESA)).send_keys(cnpj_ou_cpf)
        self._wait.until(ec.element_to_be_clickable(self.LINK_EMPRESA_ENCONTRADA)).click()

        self._wait.until(ec.element_to_be_clickable(self.BTN_DTE))

    def consultar_dte(self, id_cliente):
        # TODO: tratar caso em que os dados do DTE não são encontrados

        logger.info(f"Consultando DTE do cliente {id_cliente}")
        self._wait.until(ec.element_to_be_clickable(self.BTN_DTE)).click()
        self._wait.until(ec.element_to_be_clickable(self.BTN_FECHAR))

        resultado_cliente = {"cliente": id_cliente}
        dados_modal_dte = self._wait.until(ec.element_to_be_clickable(self.MODAL_DTE)).text.split("\n")[:-2]
        for dados in dados_modal_dte:
            chave, valor = tuple(dados.split(": "))
            resultado_cliente[chave] = valor

        self._resultados.append(resultado_cliente)

        self._wait.until(ec.element_to_be_clickable(self.BTN_FECHAR)).click()

        self._wait.until(ec.element_to_be_clickable(self.BTN_SELECIONAR_EMPRESA))

        logger.info(f"Finalizada consulta de DTE do cliente {id_cliente}")
