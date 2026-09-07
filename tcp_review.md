# Revisão completa, estruturada e organizada do básico de TCP

## Prefácio

1. **O que é TCP e por que ele existe**
    
2. **TCP dentro da pilha**
    
3. **Portas e sockets**
    
4. **O estabelecimento da conexão**
    
5. **Segmentos TCP**
    
6. **Sequence + ACK**
    
7. **Confiabilidade**
    
8. **Controle de fluxo**
    
9. **Encerramento**
    

---

## 1 - O que é TCP e por que ele existe?

O **TCP (Transmission Control Protocol)** é um protocolo da camada de transporte criado para fornecer uma comunicação **confiável e ordenada** entre dois pontos.

Ele foi desenvolvido para lidar com problemas comuns das redes, como perda de dados, dados chegando fora de ordem e necessidade de retransmissão.

Ao longo do tempo, o TCP recebeu melhorias e extensões. Atualmente, diversos protocolos da camada de aplicação, como HTTP, HTTPS, SSH, FTP, SMTP, IMAP, POP3, Telnet, SMB e LDAP, podem utilizar TCP como protocolo de transporte, deixando para ele responsabilidades como estabelecimento da conexão, ordenação, confirmação e retransmissão dos dados.

O TCP possui diversas capacidades, como:

- estabelecer conexões usando SYN, SYN-ACK e ACK;
    
- utilizar números de sequência para manter os dados na ordem correta;
    
- utilizar ACKs para confirmar o recebimento dos dados;
    
- realizar retransmissões quando necessário;
    
- realizar controle de fluxo para evitar sobrecarregar o receptor;
    
- realizar controle de congestionamento para adaptar a transmissão às condições da rede;
    
- encerrar conexões de forma controlada;
    
- manter estados da conexão, como `LISTEN`, `SYN-SENT`, `ESTABLISHED`, `FIN-WAIT` e outros.
    

Em resumo, o TCP não apenas transporta dados. Ele **gerencia diversos aspectos da comunicação entre os dois lados**.

### TCP é um programa ou software?

O TCP é um **protocolo**, não um programa.

Um protocolo é um conjunto de regras que define como os computadores devem estabelecer conexões e trocar dados.

Essas regras são implementadas por software no sistema operacional, normalmente como parte da pilha de rede do kernel. Os programas acessam essa implementação através de **sockets**.

Windows, Linux e macOS possuem implementações diferentes do TCP, mas todas seguem o mesmo padrão fundamental definido pelas especificações do protocolo. Por isso, computadores com sistemas operacionais diferentes conseguem estabelecer conexões TCP entre si.

As implementações não precisam ser iguais. O importante é que sigam as regras do protocolo e sejam compatíveis entre si.

Em resumo:

**TCP = regras do protocolo.**  
**Implementação TCP = software que executa essas regras.**  
**Kernel = local onde essa implementação normalmente funciona.**  
**Socket = interface usada pelos programas para acessar a comunicação de rede.**

---

## 2 - TCP dentro da pilha

Quando digo **“TCP dentro da pilha”**, estou falando sobre o local que o protocolo ocupa no conjunto de camadas utilizadas para realizar uma comunicação de rede.

Um exemplo simplificado é:

```text
Aplicação
   ↓
TCP
   ↓
IP
   ↓
Ethernet / Wi-Fi
```

Por exemplo:

```text
HTTP → TCP → IP → Ethernet/Wi-Fi
```

O fluxo funciona da seguinte forma: uma aplicação utiliza um **protocolo da camada de aplicação**, que utiliza um **protocolo da camada de transporte**, como TCP, para transportar os dados. O TCP então utiliza o IP para realizar a comunicação entre os hosts.

Cada camada possui suas próprias responsabilidades.

---

## 3 - Portas e sockets

O **socket** é uma interface que permite que uma aplicação se comunique pela rede.

Os programas utilizam sockets para solicitar ao sistema operacional operações de comunicação, como enviar e receber dados, iniciar conexões e encerrá-las.

Como o sistema operacional é responsável pela implementação do TCP, o socket funciona como o meio pelo qual a aplicação acessa os recursos de comunicação de rede fornecidos pelo sistema operacional.

Em resumo:

> **Socket é a interface entre o programa e a comunicação de rede fornecida pelo sistema operacional.**

### Portas

Uma **porta** é um número utilizado pelo TCP ou UDP para identificar um endpoint lógico de comunicação dentro de um host.

Por exemplo:

```text
192.168.1.10:443
      ↑      ↑
     IP    porta
```

O endereço IP identifica o host, enquanto a porta identifica um endpoint lógico de comunicação naquele host.

Uma aplicação pode associar seu serviço a uma determinada porta através do socket.

Porta e socket **não são a mesma coisa**.

Um mesmo número de porta pode estar envolvido em várias conexões TCP simultaneamente, pois as conexões podem ser diferenciadas por informações como:

```text
IP de origem
Porta de origem
IP de destino
Porta de destino
```

Em resumo:

> **Porta = número que identifica um endpoint lógico de comunicação.**  
> **Socket = interface utilizada pelo programa para acessar a comunicação de rede.**

---

## 4 - O estabelecimento da conexão

Antes de dois programas começarem a trocar dados usando TCP, é necessário estabelecer uma conexão.

Para isso, o TCP realiza um processo chamado **3-way handshake**, que consiste em três etapas.

Primeiro, o cliente envia um **SYN**, indicando que deseja iniciar uma conexão.

O servidor responde com **SYN + ACK**, indicando que recebeu o pedido e também está disposto a estabelecer a conexão.

Por fim, o cliente envia um **ACK**, confirmando o recebimento da resposta.

De forma simplificada:

```text
Cliente → SYN → Servidor
Cliente ← SYN + ACK ← Servidor
Cliente → ACK → Servidor
```

Depois dessas etapas, a conexão TCP está estabelecida e os dois lados podem começar a trocar dados.

O SYN também participa da **sincronização dos números de sequência iniciais** utilizados pela conexão.

---

## 5 - Segmentos TCP

Um **segmento TCP** é uma unidade de dados formada pelo TCP.

Quando uma aplicação envia dados através de um socket, o TCP recebe esses dados e adiciona informações próprias, formando um segmento TCP.

Essas informações permitem que o TCP controle a comunicação.

Um segmento TCP possui, entre outras informações:

- porta de origem;
    
- porta de destino;
    
- número de sequência;
    
- número de confirmação (ACK);
    
- flags;
    
- janela;
    
- dados da aplicação, quando houver.
    

De forma simplificada:

```text
Dados da aplicação
        ↓
      TCP
        ↓
Cabeçalho TCP + dados
        ↓
  Segmento TCP
```

O segmento TCP posteriormente é encapsulado pelo IP para ser transportado pela rede.

---

## 6 - Sequence + ACK

Os **números de sequência** e os **ACKs** são algumas das partes mais importantes do TCP porque permitem acompanhar os dados enviados e recebidos.

Quando o TCP envia dados, ele utiliza números de sequência para identificar a posição dos bytes dentro da comunicação.

O outro lado, ao receber os dados, envia um **ACK** informando qual é o próximo número de sequência que espera receber.

Por exemplo, de forma simplificada, se um computador envia dados correspondentes às posições 1–1000, o outro pode responder com um:

```text
ACK 1001
```

Isso significa que os dados até a posição 1000 foram recebidos e que o próximo byte esperado começa na posição 1001.

Dessa forma, o TCP consegue identificar dados que ainda não foram recebidos, detectar determinadas situações de perda, realizar retransmissões e manter os dados na ordem correta.

Em resumo:

> **Sequence Number = identifica a posição dos dados.**  
> **ACK = informa o próximo número de sequência esperado.**

---

## 7 - Confiabilidade

A **confiabilidade** é uma das principais características do TCP.

O TCP utiliza números de sequência, ACKs e retransmissões para fornecer à aplicação um fluxo de dados **ordenado e confiável**.

Como a rede pode perder dados ou fazer com que eles cheguem fora de ordem, o TCP acompanha o que já foi recebido.

Quando dados não são recebidos corretamente, o TCP pode realizar uma retransmissão.

Os números de sequência também permitem identificar a posição dos dados e ajudar o TCP a reorganizar os dados antes de entregá-los à aplicação.

Por exemplo:

```text
Parte 1 → recebida
Parte 2 → perdida
Parte 3 → recebida
```

O TCP consegue perceber que existe uma parte faltando e pode retransmitir os dados necessários.

Em resumo:

> **TCP utiliza sequência, ACKs e retransmissões para fornecer um fluxo de dados confiável e ordenado à aplicação.**

Isso não significa que o TCP consiga garantir a entrega em qualquer situação. Se a conexão falhar definitivamente, por exemplo, os dados podem não chegar ao destino.

---

## 8 - Controle de fluxo

O **controle de fluxo** é um mecanismo do TCP que impede que o transmissor envie dados mais rapidamente do que o receptor consegue armazenar e processar.

O receptor possui uma quantidade limitada de memória disponível para armazenar os dados recebidos. Por isso, ele informa ao transmissor quanto espaço possui disponível através da **janela de recepção (Receive Window)**.

O transmissor utiliza essa informação para controlar a quantidade de dados que mantém em trânsito.

Por exemplo:

```text
Receptor → Window = 5000
```

Isso indica que o receptor está disposto a aceitar aproximadamente 5000 bytes adicionais dentro da janela anunciada.

Se o receptor ficar com pouco espaço disponível, a janela pode diminuir.

Se a janela chegar a zero, o transmissor precisa interromper o envio de novos dados até que o receptor anuncie espaço novamente.

Em resumo:

> **Controle de fluxo = impedir que o transmissor sobrecarregue o receptor.**

É importante não confundir controle de fluxo com **controle de congestionamento**.

- **Controle de fluxo:** protege o receptor.
    
- **Controle de congestionamento:** adapta a transmissão às condições da rede.
    

---

## 9 - Encerramento

Quando a comunicação entre dois programas termina, o TCP precisa encerrar a conexão de forma controlada.

Para isso, utiliza principalmente a flag **FIN (Finish)**.

Diferentemente do estabelecimento da conexão, que utiliza o 3-way handshake, o encerramento normal pode envolver quatro mensagens, porque cada lado encerra sua transmissão separadamente.

De forma simplificada:

```text
Cliente → FIN → Servidor
Cliente ← ACK ← Servidor

Cliente ← FIN ← Servidor
Cliente → ACK → Servidor
```

Primeiro, um dos lados envia um **FIN**, indicando que terminou de enviar dados.

O outro lado responde com um **ACK**, confirmando o recebimento do FIN. Porém, ele ainda pode possuir dados para enviar.

Depois que também terminar de enviar seus dados, esse lado envia seu próprio **FIN**.

Por fim, o primeiro lado responde com outro **ACK**.

Dessa forma, cada lado encerra individualmente sua parte da comunicação.

O TCP também possui estados relacionados ao encerramento, como:

```text
FIN-WAIT-1
FIN-WAIT-2
CLOSE-WAIT
LAST-ACK
TIME-WAIT
CLOSED
```

O estado **TIME-WAIT**, por exemplo, existe para garantir que o encerramento seja tratado corretamente e evitar que segmentos atrasados de uma conexão anterior interfiram em uma nova conexão.

Além do encerramento normal com FIN, uma conexão TCP também pode ser encerrada de forma abrupta utilizando **RST (Reset)**.

Em resumo:

> **FIN = indica que aquele lado terminou de enviar dados.**  
> **ACK = confirma o recebimento.**  
> **FIN + ACK = permitem o encerramento controlado da conexão TCP.**
