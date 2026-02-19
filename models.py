from peewee import *

db = SqliteDatabase('database.db')

class Cliente(Model):
    nome = CharField()
    telefone = CharField()
    endereco = TextField(null=True)

    class Meta:
        database = db

class OrdemServico(Model):
    cliente = ForeignKeyField(Cliente, backref='ordens')
    descricao = TextField()
    valor = DecimalField(decimal_places=2)
    status = CharField(default='Pendente') # Pendente, Pronto, Entregue
    data_entrega = DateField()

    class Meta:
        database = db

# Cria as tabelas se não existirem
db.connect()
db.create_tables([Cliente, OrdemServico])