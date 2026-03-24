# Neptunus (Software de gestão para lavanderias)

### Visão Geral
Sistema especializado em automação de fluxo de trabalho para unidades de processamento têxtil (lavanderias). A solução foca na **estabilidade operacional offline** e na gestão rigorosa de ordens de serviço,   
eliminando falhas de registro manual e garantindo a rastreabilidade total de ativos de clientes.

* **Ambiente:** Desktop Local (Windows/Linux).
* **Paradigma:** Orientação a Objetos (PoO) com persistência relacional.

---

### Especificações Técnicas e Arquitetura

O sistema foi arquitetado para ser resiliente a falhas de rede, operando com latência zero no processamento de dados:

* **Core Engine:** **Python 3.12**. Implementação de lógica de negócio modularizada, focada em processamento síncrono e validação estrita de entradas.
* **Interface (HMI):** **Tkinter/CustomTkinter**. Desenvolvimento de uma interface de alta fidelidade visual, otimizada para entrada rápida de dados e baixa carga cognitiva para o operador.
* **Persistência de Dados:** **SQLite**. Engine de banco de dados embutida, garantindo portabilidade absoluta e conformidade **ACID** para as transações de ordens de serviço.
* **Módulo de Relatórios:** Sistema de geração de documentos dinâmicos para controle de entrada/saída de peças e faturamento.

---

### Funcionalidades Críticas

* **Gestão de Ciclo de Vida de O.S.:** Monitoramento em tempo real do status de lavagem, secagem e entrega, com alertas visuais de prazos.
* **Arquitetura de Dados Integrada:** Sincronização automática entre a interface de usuário e o motor de persistência, prevenindo perda de informações em caso de interrupção de hardware.
* **Controle de Inventário e Clientes:** Módulo de busca indexada para recuperação instantânea de históricos de consumo e perfis de clientes.
* **Exportação para Auditoria:** Funcionalidade de extração de dados em formatos estruturados para fechamento de caixa e análise contábil.

---

### Diferenciais de Engenharia

1.  **Soberania de Dados:** O sistema opera de forma totalmente isolada, garantindo a privacidade do cliente e a continuidade do negócio independente de serviços de terceiros ou conectividade externa.
2.  **Baixo Overhead:** Arquitetura otimizada para hardware legado, garantindo performance fluida mesmo em máquinas com recursos limitados de CPU e RAM.
3.  **Modularidade de Negócio:** Código estruturado para permitir a transição escalável para uma arquitetura Web ou Mobile (API-ready), caso a demanda operacional evolua.
