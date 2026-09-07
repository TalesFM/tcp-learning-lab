# tcp-learning-lab

Laboratório de estudo para compreender o protocolo TCP por meio de teoria, experimentação prática com Python e análise de tráfego de rede com Wireshark.

## Qual problema quis resolver?

Eu não quero apenas saber a definição de TCP ou memorizar seus conceitos. Quero entender **como o protocolo realmente funciona durante uma comunicação**.

A partir disso, este projeto busca responder perguntas como:

* O que acontece quando uma conexão TCP é estabelecida?
* Como o TCP identifica uma conexão?
* Como funcionam SYN, ACK e FIN?
* Como os números de sequência e confirmações funcionam?
* Como os dados da aplicação são transportados pelo TCP?
* Como esses conceitos aparecem em uma captura de rede?
* Como posso observar experimentalmente aquilo que estudei na teoria?

A proposta é transformar conceitos abstratos em fenômenos que possam ser **executados, observados e analisados**.

---

## Como o laboratório funciona?

O estudo segue um ciclo simples:

```text
TEORIA
  ↓
EXPERIMENTO
  ↓
CAPTURA DE REDE
  ↓
ANÁLISE
  ↓
CONSOLIDAÇÃO DO CONHECIMENTO
```

Primeiro, estudo determinado conceito do TCP.

Depois, crio ou modifico um experimento para provocar esse comportamento.

Em seguida, utilizo o Wireshark para observar o que aconteceu na comunicação de rede.

Por fim, comparo o comportamento observado com aquilo que foi estudado teoricamente.

---

## Estrutura do projeto

```text
tcp-learning-lab/
├── README.md
├── LICENSE
├── tcp-review.md
└── tcp.py
```

### `tcp-review.md`

Contém a revisão teórica dos principais conceitos fundamentais do TCP, incluindo:

* função do TCP;
* posição do TCP na pilha de protocolos;
* portas e sockets;
* estabelecimento de conexão;
* TCP segment;
* números de sequência;
* ACKs;
* confiabilidade;
* controle de fluxo;
* encerramento da conexão.

### `tcp.py`

Implementa um pequeno laboratório TCP em Python.

O mesmo programa cria:

* um servidor TCP;
* um cliente TCP;
* uma conexão entre eles;
* uma transferência de dados;
* uma resposta do servidor;
* o encerramento da conexão.

O objetivo não é criar uma aplicação complexa, mas produzir uma comunicação TCP controlada que possa ser observada e estudada.

---

## Configuração do endereço IP

O endereço IP utilizado pelo laboratório depende da configuração de rede da máquina onde o experimento será executado.

No meu ambiente, o endereço utilizado é:

`192.168.0.57`

Esse valor está definido no arquivo `tcp.py`:

```python
SERVER_IP = "192.168.0.57"
```

**Ao executar o laboratório em outra máquina, esse endereço pode ser diferente.** Nesse caso, é necessário alterar o valor de `SERVER_IP` no código.

Para descobrir os endereços das interfaces de rede no Linux, utilize:

```bash
ip addr
```

Procure pela interface de rede que esteja ativa e identifique o endereço IPv4 associado a ela. Por exemplo:

```text
inet 192.168.0.57/24
```

Nesse caso, o endereço utilizado no programa será:

```text
192.168.0.57
```

### Observação

O endereço `127.0.0.1` também pode ser utilizado para comunicação entre programas no próprio computador. Neste laboratório, porém, utilizo o endereço da interface de rede local para possibilitar a investigação do tráfego TCP associado à comunicação.

__



# Experimento prático

## Objetivo

Observar uma comunicação TCP real gerada pelo próprio programa e relacionar os eventos observados no Wireshark com o funcionamento interno do protocolo.

O experimento utiliza o endereço da rede local:

```text
192.168.0.57
```

e a porta:

```text
5000
```

O programa executa cliente e servidor no mesmo computador.

```text
┌──────────────────────────────────────┐
│              MEU PC                  │
│                                      │
│  Python                              │
│                                      │
│  ┌────────────┐      ┌────────────┐  │
│  │   CLIENT   │ ───► │   SERVER   │  │
│  │            │ ◄─── │            │  │
│  └────────────┘      └────────────┘  │
│                                      │
│          TCP / PORTA 5000            │
└──────────────────────────────────────┘
```

O cliente se conecta ao servidor, envia uma mensagem e recebe uma resposta.

---

# Executando o experimento

Execute:

```bash
python3 tcp.py
```

O programa deverá realizar aproximadamente este fluxo:

```text
SERVER → LISTEN
CLIENT → CONNECT
TCP CONNECTION → ESTABLISHED
CLIENT → SEND
SERVER → RECEIVE
SERVER → SEND
CLIENT → RECEIVE
CONNECTION → CLOSED
```

---

# Analisando com Wireshark

O Python mostra o comportamento da aplicação.

O Wireshark permite observar **como esse comportamento aparece no tráfego de rede**.

Primeiro, abra o Wireshark e selecione a interface de rede utilizada pelo computador.

Neste laboratório, a interface utilizada é:

```text
wlx002e2d103bcf
```

Depois, utilize o filtro:

```text
tcp.port == 5000
```

Com o Wireshark capturando os pacotes, execute novamente:

```bash
python3 tcp.py
```

O objetivo é analisar a comunicação enquanto ela acontece.

---

# O que analisar na captura?

## 1. ESTABELECIMENTO DA CONEXÃO

Procure os primeiros pacotes TCP.

O comportamento esperado é:

```text
CLIENT                    SERVER

   SYN ───────────────────►
       ◄──────────── SYN, ACK
   ACK ───────────────────►
```

Esse é o **Three-Way Handshake**.

A análise deve buscar responder:

* Qual máquina enviou o primeiro SYN?
* Qual é a porta de origem?
* Qual é a porta de destino?
* Qual é o número de sequência?
* O que o SYN-ACK confirma?
* Por que existe um terceiro ACK?

---

## 2. TRANSFERÊNCIA DE DADOS

Depois do estabelecimento da conexão, procure os pacotes que transportam:

```text
HELLO FROM CLIENT!
```

Analise:

* número de sequência;
* número de confirmação;
* tamanho dos dados;
* flags TCP;
* porta de origem;
* porta de destino.

O objetivo é relacionar os dados enviados pelo Python com o segmento TCP observado no Wireshark.

---

## 3. RESPOSTA DO SERVIDOR

O servidor envia:

```text
HELLO FROM SERVER!
```

Procure esse tráfego na captura.

Compare os números de sequência e ACK com os pacotes anteriores.

A pergunta principal é:

> Como o TCP controla a posição dos dados que estão sendo enviados e recebidos?

---

## 4. ENCERRAMENTO DA CONEXÃO

Depois que a comunicação termina, analise os pacotes finais.

Procure:

```text
FIN
ACK
FIN
ACK
```

O objetivo é entender como uma conexão TCP é encerrada e por que o encerramento envolve mais de um pacote.

---

# Relação entre teoria e prática

Este laboratório busca evitar uma separação entre "estudar TCP" e "usar TCP".

Cada conceito estudado deve poder ser relacionado a algo observável.

Por exemplo:

| Conceito            | Onde observar                 |
| ------------------- | ----------------------------- |
| Portas              | TCP source/destination port   |
| Three-Way Handshake | SYN, SYN-ACK, ACK             |
| Sequence Number     | Campo Sequence Number         |
| ACK                 | Campo Acknowledgment Number   |
| Dados               | TCP payload                   |
| Flags               | SYN, ACK, FIN etc.            |
| Encerramento        | FIN e ACK                     |
| Socket              | Código Python                 |
| Comunicação TCP     | Captura completa no Wireshark |

---

# Próximas investigações

Este projeto será expandido conforme novos conceitos forem estudados.

Possíveis experimentos:

* investigar números de sequência em diferentes transmissões;
* observar ACKs;
* provocar transmissões maiores;
* estudar controle de fluxo;
* observar retransmissões;
* analisar perda de pacotes;
* estudar encerramento com FIN;
* investigar RST;
* comparar diferentes comportamentos de conexão;
* relacionar o comportamento observado com a implementação do TCP no sistema operacional.

A intenção é que cada experimento responda a uma pergunta específica e produza uma evidência observável.

---

# Objetivo de aprendizagem

O objetivo final não é apenas conseguir escrever um programa que utilize TCP.

É conseguir olhar para uma captura de rede e explicar **o que está acontecendo, por que está acontecendo e como isso se relaciona com o funcionamento do protocolo**.

O Python é utilizado para produzir situações controladas.

O Wireshark é utilizado para observar essas situações.

A teoria é utilizada para explicar os resultados.

```text
ESTUDAR
   ↓
IMPLEMENTAR
   ↓
OBSERVAR
   ↓
QUESTIONAR
   ↓
ANALISAR
   ↓
COMPREENDER
```
