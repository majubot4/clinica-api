from banco import banco


# Classe Usuário
class Usuario(banco.Model):
    id = banco.Column(banco.Integer, primary_key=True)
    username = banco.Column(banco.String(50), unique=True, nullable=False)
    email = banco.Column(banco.String(100), unique=True, nullable=False)
    password = banco.Column(banco.String(255), nullable=False)


# Classe Paciente
class Paciente(banco.Model):
    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100), nullable=False)
    idade = banco.Column(banco.Integer)
    telefone = banco.Column(banco.String(20))


# Classe Médico
class Medico(banco.Model):
    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100), nullable=False)
    especialidade = banco.Column(banco.String(100))


# Classe Consulta
class Consulta(banco.Model):
    id = banco.Column(banco.Integer, primary_key=True)
    data = banco.Column(banco.String(20))
    horario = banco.Column(banco.String(10))


    paciente_id = banco.Column(
        banco.Integer,
        banco.ForeignKey("paciente.id")
    )

    medico_id = banco.Column(
        banco.Integer,
        banco.ForeignKey("medico.id")
    )


    paciente = banco.relationship(
        "Paciente"
    )

    medico = banco.relationship(
        "Medico"
    )