import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker

from ..validators import valida_cnpj_ou_cpf, valida_tamanho_cnpj, valida_tamanho_cpf


@pytest.mark.django_db
def test_valida_cnpj_ou_cpf_exception():
    cliente = baker.make("core.Cliente")
    cliente.cpf = "0" * 11
    cliente.cnpj = "0" * 14

    with pytest.raises(ValidationError) as exc:
        valida_cnpj_ou_cpf(cliente)

    assert exc.value.message == "O cadastro de um Cliente não pode ter CNPJ e CPF. Preencha somente um dos dois."


@pytest.mark.django_db
def test_valida_cnpj_ou_cpf_cliente_cnpj():
    cliente = baker.make("core.Cliente")
    cliente.cnpj = "0" * 14
    cliente.save()

    assert cliente.cnpj and not cliente.cpf


@pytest.mark.django_db
def test_valida_cnpj_ou_cpf_cliente_cpf():
    cliente = baker.make("core.Cliente")
    cliente.cpf = "0" * 11
    cliente.save()

    assert cliente.cpf and not cliente.cnpj


def test_valida_tamanho_cnpj_exception():
    cnpj_curto = "0" * 10
    with pytest.raises(ValidationError) as exc:
        valida_tamanho_cnpj(cnpj_curto)

    assert exc.value.message == f"O CNPJ {cnpj_curto} não possui 14 dígitos."


def test_valida_tamanho_cnpj():
    cnpj_curto = "0" * 14

    assert cnpj_curto == valida_tamanho_cnpj(cnpj_curto)


def test_valida_tamanho_cpf_exception():
    cpf_curto = "0" * 10
    with pytest.raises(ValidationError) as exc:
        valida_tamanho_cpf(cpf_curto)

    assert exc.value.message == f"O CPF {cpf_curto} não possui 11 dígitos."


def test_valida_tamanho_cpf():
    cpf_curto = "0" * 11

    assert cpf_curto == valida_tamanho_cpf(cpf_curto)
