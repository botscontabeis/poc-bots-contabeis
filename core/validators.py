from django.core.exceptions import ValidationError


def valida_cnpj_ou_cpf(cliente):
    if cliente.cnpj and cliente.cpf:
        raise ValidationError("O cadastro de um Cliente não pode ter CNPJ e CPF. Preencha somente um dos dois.")


def valida_tamanho_cnpj(value):
    if value and len(value) != 14:
        raise ValidationError(f"O CNPJ {value} não possui 14 dígitos.")

    return value


def valida_tamanho_cpf(value):
    if value and len(value) != 11:
        raise ValidationError(f"O CPF {value} não possui 11 dígitos.")

    return value
