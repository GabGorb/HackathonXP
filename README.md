📘 DOCUMENTO DE ESCOPO — FINANCEGAME XP
1. Visão Geral do Problema
A maioria dos jovens brasileiros não possui educação financeira prática, aprendendo sobre investimentos apenas quando já adultos.
Ao mesmo tempo, milhões de jovens entram em contato cedo com jogos gamificados de vício e azar, como “tigrinho” e derivados — que criam:
•	comportamento compulsivo
•	prejuízo financeiro real
•	frustração e afastamento do mundo de investimentos sérios
Ou seja: a primeira experiência financeira de muitos jovens é negativa, arriscada e sem educação.
O desafio do edital pede exatamente uma solução que mude a relação do jovem com finanças, oferecendo uma experiência que seja:
✔ divertida
✔ intuitiva
✔ próxima da realidade
✔ social e cooperativa
✔ acessível para qualquer pessoa
Nosso projeto nasce exatamente dessa lacuna.
________________________________________
2. Proposta de Valor
Criamos o Cartola de Investimentos, um jogo educacional que simula um mini-mercado financeiro dentro do WhatsApp.
Assim como no “Cartola FC” você monta seu time, aqui você monta sua carteira de ações e compete com seus amigos para:
•	diversificar melhor
•	ganhar mais patrimônio
•	tomar decisões inteligentes
•	aprender conceitos financeiros reais
A experiência é totalmente gamificada, com ranking, carteira, compra e venda de ações e feedback educativo.
Além disso, o jogo cria uma alternativa positiva ao vício dos apps de azar:
se existe um jogo que faz o jovem perder dinheiro, por que não criar um jogo que faz ele aprender a ganhar dinheiro?
________________________________________
3. Objetivos da Solução
🎯 Objetivo principal
Dar ao jovem seu primeiro contato saudável e divertido com investimentos, dentro de uma plataforma que ele já usa: o WhatsApp.
🎯 Objetivos específicos
•	Ensinar conceitos reais do mercado (diversificação, patrimônio, preço médio, risco).
•	Reduzir a fricção: não é necessário baixar nenhum aplicativo.
•	Criar um ambiente social, competitivo e educativo.
•	Oferecer uma alternativa gamificada e não viciante, diferente dos jogos de azar.
•	Reduzir o medo inicial de começar a investir.
•	Estimular conversas sobre educação financeira entre amigos e família.
________________________________________
4. Arquitetura da Solução
A arquitetura foi projetada para ser simples, extensível e robusta.
4.1 Visão Geral
Usuário → WhatsApp → Webhook da Meta → Backend Flask → Motor do Jogo → WhatsApp
4.2 Componentes
✔ 1. WhatsApp Cloud API (Meta)
•	Recebe mensagens do usuário
•	Envia respostas do bot
•	Não exige instalar aplicativo novo
✔ 2. Backend (Flask / Python)
Localizado no arquivo app.py 
•	Endpoints de webhook
•	Roteamento de mensagens
•	Módulo de envio de mensagens
•	Integração com a API da Meta
✔ 3. Motor do Jogo (game_engine.py)
Módulo principal da lógica do jogo 
•	Gerenciamento de jogadores
•	Simulação de carteira
•	Registro de compras e vendas
•	Cálculo de ranking
•	Lógica de diversificação
•	Cálculo de patrimônio total
✔ 4. Integração com Mercado (Alpha Vantage)
•	Consulta de preço ao vivo
•	Fallback automático caso falhe
•	Mapeamento para tickers da B3
✔ 5. Parser de comandos (bot.py)
Interpretação das mensagens do usuário 
•	ajuda
•	ativos
•	configurar
•	entrar
•	comprar
•	vender
•	carteira
•	ranking
✔ 6. Arquivo de Configuração (.env)
Contém chaves e tokens necessários 
4.3 Diagrama da Arquitetura

Usuário -> WhatsApp Cloud API -> Webhook (Flask) -> Parsers de Comando

(Webhook + Parsers) -> Engine do Jogo (carteiras, compras, vendas, ranking) -> Alpha Vantage (preço em tempo real)

 ________________________________________
5. Fluxo da Experiência do Usuário
1.	O usuário entra no grupo do WhatsApp do torneio.
2.	O admin envia: configurar 10 7 50000
3.	Cada pessoa envia: entrar Gabriel
4.	Para ver os ativos disponíveis: ativos
5.	Para comprar: comprar PETR4 2
6.	Para vender: vender VALE3 1
7.	Para consultar a carteira: carteira
8.	Para acompanhar o jogo: ranking
________________________________________
6. Didática da Solução
O que o jovem aprende naturalmente ao jogar:
✔ 1. Diversificação
O ranking valoriza ter mais ativos diferentes.
✔ 2. Preço médio
Cada compra altera o “PM”, conceito essencial de investimentos.
✔ 3. Risco x Retorno
Ativos variam, e o ranking reflete isso.
✔ 4. Longo prazo
O jogo incentiva decisões sustentáveis (não especulativas).
✔ 5. Patrimônio total
Não é só “lucro”, mas patrimônio (cash + ativos).
✔ 6. Comparação saudável entre amigos
A competição incentiva aprendizado.
________________________________________
7. Inovação e Aplicabilidade
Inovação
•	Sistema de “Cartola Financeiro” não existe no Brasil.
•	Uso social do WhatsApp para educação financeira.
•	Jogo com preços reais do mercado.
•	Alternativa saudável aos jogos de aposta.
Aplicabilidade
•	Funcionaria em escolas, cursinhos, famílias e grupos de amigos.
•	Pode virar extensão acadêmica (USP, ensino médio, ETEC).
•	Pode virar produto XP para engajamento jovem.
•	Possível expansão para:
o	fundos
o	renda fixa
o	ETFs
o	simulador de risco
o	quests educativas
________________________________________
8. Sustentabilidade e Riscos
✔ Riscos Técnicos
•	Dependência das APIs (Meta e Alpha Vantage).
•	Limite de requisições por minuto (solucionável com cache).
✔ Riscos Educacionais
•	Usuários tentarem “burlar” o jogo
→ Mitigação: regras e validações no engine.
✔ Sustentabilidade
•	Custos quase nulos para operar.
•	WhatsApp torna o produto altamente escalável.
________________________________________
9. Roadmap Futuro
MVP Atual (entrega inicial):
•	Carteira
•	Compras e vendas
•	Ranking
•	Diversificação
•	WhatsApp Bot completo
Versão 2:
•	Missões diárias
•	Quiz financeiro integrado ao fluxo
•	Perfil XP digital para cada jovem
Versão 3:
•	Torneios nacionais
•	Ranking por escola/universidade
•	Parceria educacional com XP
________________________________________
Link para o Github do Código Inicial:
