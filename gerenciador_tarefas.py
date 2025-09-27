"""Exercício Integrador — Gerenciador de Tarefas
Objetivo: Implementar um sistema simples de gerenciamento de tarefas em Python, com suporte a:

- Enum com propriedades → para representar prioridades.
- Descritores → para validar strings não vazias e datas não passadas.
- dataclasses com InitVar → para integrar valores recebidos no construtor e validar via descritores.
- Polimorfismo leve (uso de __str__) para exibir tarefas formatadas.
- Persistência em arquivos CSV e JSON.
- Interface de linha de comando (CLI) com menu interativo.
-------------------------------------------------------------------------------------------------------------------
Parte 1 — Enum Prioridade

- Crie uma enum.Enum chamada Prioridade com valores: BAIXA, MEDIA, ALTA.
- Adicione uma propriedade peso que retorna um número inteiro usado para ordenação (ex.: ALTA=3, MEDIA=2, BAIXA=1).
- Sobrescreva __str__ para que a exibição seja apenas o nome (ALTA, MEDIA, BAIXA).
-------------------------------------------------------------------------------------------------------------------
Parte 2 — Descritores de Validação

NaoVazio:
- Aceita apenas str.
- Rejeita strings vazias ou só com espaços.

DataNaoPassada:
- Aceita apenas objetos datetime.date.
- Rejeita datas anteriores a hoje (mas aceita a data de hoje).

Ambos devem implementar __set_name__, __get__, __set__.
-------------------------------------------------------------------------------------------------------------------
Parte 3 — Dataclass Tarefa
Use @dataclass para definir Tarefa.

- Atributos:
nome → validado por NaoVazio.
prazo → validado por DataNaoPassada.
prioridade: Prioridade → padrão Prioridade.MEDIA.
concluida: bool → padrão False.
Use InitVar para _nome e _prazo recebidos no __init__, de forma que o __post_init__ dispare os descritores para validação.

- Implemente __str__ para exibir a tarefa no formato:
[PRIORIDADE] YYYY-MM-DD  Nome da tarefa  (concluída: ✓/ )
-------------------------------------------------------------------------------------------------------------------
Parte 4 — Classe GerenciadorTarefas

Implemente métodos para:
adicionar_tarefa(tarefa: Tarefa)
Valida o tipo antes de adicionar.

listar_tarefas(...)
Parâmetros:
ordem_por: "prioridade" (padrão) ou "prazo".
incluir_concluidas: bool.
enumerar: se True, exibe numeradas.
Ordenação usa prioridade.peso ou prazo.

marcar_concluida(indice, valor=True, ...)
Marca ou reabre tarefas pelo índice exibido.

Persistência:
salvar_csv(caminho) / carregar_csv(caminho)
salvar_json(caminho) / carregar_json(caminho)
-------------------------------------------------------------------------------------------------------------------
Parte 5 — Utilitários de Parsing

Implemente funções auxiliares:
_parse_data_iso(s: str) -> date
Aceita formato "YYYY-MM-DD" ou "DD/MM/YYYY",
Qualquer outro formato deve levantar erro: raise ValueError(f"data inválida: {s!r}. Use YYYY-MM-DD (ou DD/MM/YYYY).").

_parse_prioridade(s: str) -> Prioridade
Converte string em Prioridade, ex.: 'ALTA' deve virar Prioridade.ALTA;
Ignore maiúsculas e minúsculas.

_parse_bool(s: str) -> bool
Converte string ("s", "sim", "1", "true", etc.) em booleano.
-------------------------------------------------------------------------------------------------------------------
Parte 6 — CLI (Interface em Linha de Comando)
Implemente um loop com menu textual:

========== GERENCIADOR DE TAREFAS ==========
1) Carregar CSV
2) Carregar JSON
3) Salvar CSV
4) Salvar JSON
5) Adicionar tarefa
6) Listar por prioridade
7) Listar por prazo
8) Marcar tarefa como concluída
9) Reabrir tarefa
0) Sair

Cada opção chama os métodos apropriados do GerenciadorTarefas.
Ao adicionar tarefa, leia os dados do usuário (nome, prazo, prioridade, concluída).
Exemplo de Uso Esperado
========== GERENCIADOR DE TAREFAS ==========
1) Carregar CSV
2) Carregar JSON
3) Salvar CSV
4) Salvar JSON
5) Adicionar tarefa
6) Listar por prioridade
7) Listar por prazo
8) Marcar tarefa como concluída
9) Reabrir tarefa
0) Sair
Escolha uma opção: 5
Nome da tarefa: Preparar slides
Prazo (YYYY-MM-DD ou DD/MM/YYYY): 25/09/2025
Prioridade (ALTA/MEDIA/BAIXA) [padrão MEDIA]: ALTA
Já concluída? (s/N): n
Tarefa adicionada com sucesso!
Ordenado por prioridade:
 1. [ALTA] 2025-09-25  Preparar slides  (concluída:  )
 """
#------------------------------------------------------------------------------------------------------------------
# solução

from enum import Enum, auto
#import datetime
from dataclasses import dataclass, InitVar
from typing import ClassVar
import datetime, json, csv, sys, os, time

#------------------------------------------------------------------------------------------------------------------
# parte 1 - Enum Prioridade
#------------------------------------------------------------------------------------------------------------------

# criar classe Prioridade com Enum
class Prioridade(Enum):
    # definir os valores da enumeração
    BAIXA = auto()
    MEDIA = auto()
    ALTA = auto()
    #---------------------------------------------------------------------------------------------------
    # definir peso com property
    @property
    def peso(self):
        if self == Prioridade.BAIXA:
            return 1    
        if self == Prioridade.MEDIA:
            return 2
        if self == Prioridade.ALTA:
            return 3
    #---------------------------------------------------------------------------------------------------
    # definir representação em string
    def __str__(self):
        return self.name  # retorna "BAIXA", "MEDIA" ou "ALTA"
   
#------------------------------------------------------------------------------------------------------------------
# parte 2 - Descritores de Validação
#------------------------------------------------------------------------------------------------------------------

# criar a classe descritor para validar as strings de entrada
class NaoVazio:
    # criar método __set_name__ (serve para registrar o nome do atributo)
    def __set_name__(self, owner, name):
        self.name = name
    #---------------------------------------------------------------------------------------------------
    # criar método __get__ (serve para obter o valor da variável privada)
    def __get__(self, instance, owner):
        if instance is None:  
            return self                                # se não houver instância, retorna o descritor
        return getattr(instance, "_"+self.name, None)  # retorna o valor pegando do __dict__ usando getattr
    #---------------------------------------------------------------------------------------------------
    # criar o método __set__ (serve para definir o valor da variável privada de forma válida)
    def __set__(self, instance, value):
        # caso o valor não seja uma string ou se for vazia ou apenas espaços, levanta um ValueError
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Valor de nome inválido!")
        setattr(instance, "_"+self.name, value)       # salva valor no __dict__ com prefixo _


# criar a classe descritor para validar as datas
class DataNaoPassada:
    # criar método __set_name__
    def __set_name__(self, owner, name):
        self.name = name
    #---------------------------------------------------------------------------------------------------
    # criar método __get__
    def __get__(self, instance, owner):
        if instance is None:  
            return self                                # se não houver instância, retorna o descritor
        return getattr(instance, "_"+self.name, None)  # retorna o valor pegando do __dict__ com getattr
    #---------------------------------------------------------------------------------------------------
    # criar o método __set__
    def __set__(self, instance, value):
        # caso o valor não seja um objeto datetime.date ou se for uma data que passou, levanta um ValueError
        if not isinstance(value, datetime.date):
            raise ValueError(f"Valor de data inválido!")
        if value < datetime.date.today():
            raise ValueError(f" A data já passou!")

        setattr(instance, "_"+self.name, value)  # salva valor no __dict__ com prefixo _

#------------------------------------------------------------------------------------------------------------------
# parte 3 : Dataclass Tarefa
#------------------------------------------------------------------------------------------------------------------

# usar dataclass para criar a classe Tarefa
# nesse caso, usar InitVar para receber os valores do __init__ gerado pelo @dataclass
# atribuir os valores depois com __post_init__ (já validados)


@dataclass
class Tarefa:
    # InitVar recebe no __init__ de Tarefa
    _nome: InitVar[str]
    _prazo: InitVar[datetime.date]


    # # atributos validados/controlados pelos descritores
    # nome: str = NaoVazio()
    # prazo: datetime.date = DataNaoPassada()


    # descritores como ClassVar => dataclass ignora como campo do __init__
    nome: ClassVar[NaoVazio] = NaoVazio()
    prazo: ClassVar[DataNaoPassada] = DataNaoPassada()
   
    # prioridade: Prioridade → padrão Prioridade.MEDIA.
    prioridade: Prioridade = Prioridade.MEDIA
   
    # concluida: bool → padrão False.
    concluida: bool = False
    #---------------------------------------------------------------------------------------------------    
    # disparar os descritores para validação
    def __post_init__(self, _nome, _prazo):
        type(self).nome.__set__(self, _nome)
        type(self).prazo.__set__(self, _prazo)
    #---------------------------------------------------------------------------------------------------
    # representar em string com  __str__
    def __str__(self):
        if self.concluida:
            return f"[{self.prioridade}] {self.prazo} {self.nome} (concluída: ✓)"
        else:
            return f"[{self.prioridade}] {self.prazo} {self.nome} (concluída: ✗)"
       
#------------------------------------------------------------------------------------------------------------------
# parte 4 - classe GerenciadorTarefas e Persistência
#------------------------------------------------------------------------------------------------------------------

class GerenciadorTarefas:
   
    # método construtor
    def __init__(self):
        self.tarefas = [] # lista de tarefas
    #---------------------------------------------------------------------------------------------------
    # adicionar tarefa(verificando se a entrada é do tipo Tarefa, senão levanta TypeError)
    def add_tarefa(self, tarefa: Tarefa):
        if not isinstance(tarefa, Tarefa):
            raise TypeError("A tarefa deve ser do tipo Tarefa!")
       
        # se a tarefa já está na lista de tarefas
        if tarefa not in self.tarefas:
            self.tarefas.append(tarefa) # adiciona a tarefa na lista
    #---------------------------------------------------------------------------------------------------
    # listar tarefas (com parâmetros de ordenação e filtro)
    def listar_tarefas(self, ordem_por="prioridade", incluir_concluidas=True, enumerar=False):
       
        # criar uma cópia da lista de tarefas
        tarefas = self.tarefas[:]
        #---------------------------------------------------------------------------------------------------
        # filtrar tarefas concluídas (lista apenas as não concluídas)
        if not incluir_concluidas:
            tarefas_nao_concluidas = []
            for tarefa in tarefas:
                if not tarefa.concluida:
                    tarefas_nao_concluidas.append(tarefa)
            tarefas = tarefas_nao_concluidas
        #---------------------------------------------------------------------------------------------------
        # ordenar tarefas por prioridade ou prazo
        if ordem_por == "prioridade":
            tarefas.sort(key=lambda t: t.prioridade.peso, reverse=True) # ordena por prioridade
        elif ordem_por == "prazo":
            tarefas.sort(key=lambda t: t.prazo)      # ordena por prazo


        linhas = []
        for i, tarefa in enumerate(tarefas, start=1):
            if enumerar:
                linha = f"{i}. {tarefa}"
                linhas.append(linha)
            else:
                linha = str(tarefa)
                linhas.append(linha)
               
        resultado = "\n".join(linhas)
        return resultado
    #---------------------------------------------------------------------------------------------------
    # método para mostrar apenas tarefas concluídas no terminal
    def listar_tarefas_concluidas(self, enumerar=False):
        linhas = []
        for t in self.tarefas:
            if t.concluida:
                linhas.append(str(t))

        linhas_formatadas = []
        for i, tarefa in enumerate(linhas, start=1):
            if enumerar:
                linha = f"{i}. {tarefa}"
            else:
                linha = str(tarefa)
            linhas_formatadas.append(linha)
            
        if not linhas_formatadas:
            return "Nenhuma tarefa concluída encontrada."
        
        resultado = "\n".join(linhas_formatadas)
        return resultado
    
    # método para mostrar apenas tarefas não concluídas no terminal
    def listar_tarefas_nao_concluidas(self, enumerar=False):
        linhas = []
        for t in self.tarefas:
            if not t.concluida:
                linhas.append(str(t))

        linhas_formatadas = []
        for i, tarefa in enumerate(linhas, start=1):
            if enumerar:
                linha = f"{i}. {tarefa}"
            else:
                linha = str(tarefa)
            linhas_formatadas.append(linha)
            
        if not linhas_formatadas:
            return "Nenhuma tarefa não concluída encontrada."
        
        resultado = "\n".join(linhas_formatadas)
        return resultado
    #---------------------------------------------------------------------------------------------------
    # marcar tarefa como concluída ou reabrir de acordo com o valor passado
    def marcar_concluida(self, indice, valor=True):
        # procura tarefa com o índice informado
        try:
            tarefa = self.tarefas[indice - 1]
        except IndexError:
            raise ValueError("Índice da tarefa é inválido!") # se não achar, levanta um ValueError
        # marca tarefa como concluída ou não
        tarefa.concluida = valor

    # Persistência
    # TODO: melhorar lógica de salvamento dos arquivos json e CSV para não salvar duplicatas
    #---------------------------------------------------------------------------------------------------
    # arquivo json
    #---------------------------------------------------------------------------------------------------
    # método para salvar as tarefas no arquivo tarefas.json (usando forma de dict)
    def salvar_json(self, caminho="tarefas.json"):
        # tentar abrir o arquivo json, caso esteja vazio, inicia o salvamento dos dados com uma lista vazia
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            dados = []

        # sobrescreve os dados com as tarefas atuais
        dados = []
        for t in self.tarefas:
            dados.append({
                "nome": t.nome,
                "prazo": t.prazo.isoformat(), # usa o formato para data
                "prioridade": t.prioridade.name,
                "concluida": t.concluida
            })


        # escrever dados no arquivo
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    #---------------------------------------------------------------------------------------------------
    # carregar/ler dados lidos de tarefas.json
    def carregar_json(self, caminho="tarefas.json"):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            for d in dados:
                tarefa = Tarefa(
                    _nome=d["nome"],
                    _prazo=datetime.date.fromisoformat(d["prazo"]),
                    prioridade=Prioridade[d["prioridade"]],
                    concluida=d.get("concluida", False)
                )
                self.add_tarefa(tarefa)
    #---------------------------------------------------------------------------------------------------
    # arquivo CSV
    #---------------------------------------------------------------------------------------------------
    # método para salvar as tarefas no arquivo tarefas.csv
    def salvar_csv(self, caminho="tarefas.csv"):
        with open("tarefas.csv", "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["nome", "prazo", "prioridade", "concluida"])
            for t in self.tarefas:
                writer.writerow([t.nome, t.prazo.isoformat(), t.prioridade.name, t.concluida])
    #---------------------------------------------------------------------------------------------------
    # método para carregar os dados de tarefas.csv e recriar Tarefa
    def carregar_csv(self, caminho="tarefas.csv"):
        with open("tarefas.csv", "r", encoding="utf-8") as arquivo:
            reader = csv.DictReader(arquivo)
            for linha in reader:
                tarefa = Tarefa(
                    _nome=linha["nome"],
                    _prazo=datetime.date.fromisoformat(linha["prazo"]),
                    prioridade=Prioridade[linha["prioridade"]],
                    concluida=linha["concluida"].lower() == "true"
                )
                self.add_tarefa(tarefa)

#------------------------------------------------------------------------------------------------------------------
# parte 5 - Utilitários de Parsing
#------------------------------------------------------------------------------------------------------------------

# método para aceitar apenas formato YYYY-MM-DD ou DD/MM/YYYY
def _parse_data_iso(s: str) -> datetime.date:
     # tentar primeiro o formato ISO
    try:
        # tentar primeiro o formato ISO
        return datetime.date.fromisoformat(s)
 
   # tentar segundo formato
    except ValueError:
        try:
             return datetime.datetime.strptime(s, "%d/%m/%Y").date()
           
        # se não conseguir nenhum dos dois, levanta ValueError
        except ValueError:
            raise ValueError(f"Data inválida: {s!r}. Por favor, use YYYY-MM-DD ou DD/MM/YYYY")

# método para converter string em Prioridade
def _parse_prioridade(s: str) -> Prioridade:
    # tenta formatar string
    try:
        return Prioridade[s.strip().upper()]
# caso não consiga, levanta ValueError
    except KeyError:
        raise ValueError(f"Prioridade inválida: {s!r}. Por favor, use ALTA, MEDIA ou BAIXA")


# método para converter entradas de "sim" em booleano
def _parse_bool(s: str) -> bool:
    s = s.strip().lower()


    if s in ("s", "sim", "1", "true", "t", "y", "yes", "si"):
        return True
   
    if s in ("n", "nao", "0", "não", "false", "f", "no"):
        return False
   
    raise ValueError(f"valor booleano inválido: {s!r}. Por favor, use s/n, y/n, yes/no, sim/não, true/false, t/f ...")

#------------------------------------------------------------------------------------------------------------------
# parte 6 - CLI (Interface em Linha de Comando)
#------------------------------------------------------------------------------------------------------------------
# navegação do usuário
def main():
   
    # cria o gerenciador de tarefas
    gerenciador = GerenciadorTarefas()

    while True:
        print("-----------------------------------------------------------------------------------------------")
        print("                           GERENCIADOR DE TAREFAS")
        print("-----------------------------------------------------------------------------------------------")
        print("MENU PRINCIPAL:\n")
        print("1  - Carregar CSV")
        print("2  - Carregar JSON")
        print("3  - Salvar CSV")
        print("4  - Salvar JSON")
        print("5  - Adicionar tarefa")
        print("6  - Listar tarefas concluídas")
        print("7  - Listar tarefas não concluídas")
        print("8  - Listar por prioridade")
        print("9  - Listar por prazo")
        print("10 - Marcar tarefa como concluída")
        print("11 - Reabrir tarefa")
        print("0  - Sair")
        print("-----------------------------------------------------------------------------------------------")
        escolha = input("Escolha uma opção: ").strip()

        try:
            if escolha == "1":
                gerenciador.carregar_csv(caminho="tarefas.csv")
                print("CSV carregado com sucesso!")
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "2":
                gerenciador.carregar_json(caminho="tarefas.json")
                print("JSON carregado com sucesso!")
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "3":
                gerenciador.salvar_csv(caminho="tarefas.csv")
                print("CSV salvo com sucesso!")
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "4":
                gerenciador.salvar_json(caminho="tarefas.json")
                print("JSON salvo com sucesso!")
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "5":
                nome = input("Nome da tarefa: ")
                prazo_str = input("Prazo (YYYY-MM-DD ou DD/MM/YYYY): ")
                prazo = _parse_data_iso(prazo_str)


                prioridade_str = input("Prioridade (ALTA/MEDIA/BAIXA) [padrão MEDIA]: ").strip()
                prioridade = _parse_prioridade(prioridade_str) if prioridade_str else Prioridade.MEDIA


                concluida_str = input("Já concluída? (s/N): ").strip()
                concluida = _parse_bool(concluida_str) if concluida_str else False


                tarefa = Tarefa(_nome=nome, _prazo=prazo, prioridade=prioridade, concluida=concluida)
                gerenciador.add_tarefa(tarefa)


                print("Tarefa adicionada com sucesso!")
                print("Ordenado por prioridade:")
                print(gerenciador.listar_tarefas(ordem_por="prioridade", enumerar=True))
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')
                    
                    
            elif escolha == "6":
                print(gerenciador.listar_tarefas_concluidas(enumerar=True))
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "7":
                print(gerenciador.listar_tarefas_nao_concluidas(enumerar=True))
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "8":
                print(gerenciador.listar_tarefas(ordem_por="prioridade", enumerar=True))
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "9":
                print(gerenciador.listar_tarefas(ordem_por="prazo", enumerar=True))
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "10":
                indice = int(input("Número da tarefa: "))
                gerenciador.marcar_concluida(indice, True)
                print("Tarefa concluída!")
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "11":
                indice = int(input("Número da tarefa: "))
                gerenciador.marcar_concluida(indice, False)
                print("Tarefa reaberta!")
                limpa_tela = input("Pressione Enter para continuar...")
                if limpa_tela == "":
                    os.system('cls')


            elif escolha == "0":
                print("\nSaindo...")
                time.sleep(1)
                print("-----------------------------------------------------------------------------------------------")
                print("Fim do programa")
                os.system('cls')
                sys.exit(0)



            else:
                print("Opção inválida! Tente novamente com uma das opções listadas no menu.")
                limpa_tela = input("Pressione Enter para voltar...")
                if limpa_tela == "":
                    os.system('cls')


        except Exception as e:
            print(f"Erro: {e}")

#------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    main()
