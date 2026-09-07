# Resultados

## Captura e análise com Wireshark

Após a execução do laboratório TCP em Python, foi realizada uma captura dos pacotes utilizando o **Wireshark**.

Como a comunicação ocorre localmente através de `127.0.0.1`, a captura foi realizada na interface **Loopback (`lo`)**.

Foi utilizado o filtro:

```text
tcp.port == 5000
```

A captura permitiu observar o fluxo completo da comunicação TCP, incluindo:

* **Three-Way Handshake:** `SYN → SYN, ACK → ACK`
* **Transmissão dos dados** entre cliente e servidor
* **ACKs** utilizados para confirmar o recebimento dos dados
* **Encerramento da conexão TCP**

### Resultado

A imagem abaixo apresenta a captura realizada durante a execução do laboratório:

<img width="1366" height="202" alt="image" src="https://github.com/user-attachments/assets/d3195e36-5af6-420f-8408-f3a637941f5f" />


A análise confirmou, através dos pacotes capturados, o funcionamento prático do protocolo TCP durante o estabelecimento, transmissão de dados e encerramento da conexão.
