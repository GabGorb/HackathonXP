📘 DOCUMENTO DE ESCOPO — INVESTCUP
________________________________________
1. Visão Geral do Problema
A alfabetização financeira no Brasil permanece extremamente baixa. A maioria dos jovens:
• cresce sem orientação prática sobre como investir;
• não entende riscos, patrimônio ou diversificação;
• sente medo e insegurança ao iniciar sua vida financeira;
• tem como primeiro contato jogos de azar digitais (“tigrinho” e similares), que incentivam impulsividade, perdas e vício.
Ou seja:
A primeira experiência financeira do jovem brasileiro é, muitas vezes, negativa, arriscada e deseducativa.
O desafio atual é reverter esse cenário, oferecendo uma experiência:
✔ divertida
✔ segura
✔ educativa
✔ social
✔ baseada em mercado real
✔ acessível via WhatsApp, plataforma que todos já usam
________________________________________
2. Proposta de Valor
Criamos o InvestCup, um fantasy game financeiro dentro do WhatsApp — simples, acessível e sem necessidade de instalar aplicativos.
No InvestCup, o jovem:
• monta sua carteira;
• compra e vende ações reais (preços reais de mercado);
• compete em um ranking global;
• recebe comentários educativos gerados por IA;
• aprende de forma prática, jogando.
A experiência inclui:
✔ ranking global
✔ carteira persistente
✔ preços reais via Alpha Vantage
✔ comentários gerados por IA (estilo narrador empolgado)
✔ histórico completo salvo no Firebase
✔ aprendizado natural sobre risco, diversificação, patrimônio e tomada de decisão
Se existem jogos que ensinam jovens a perder dinheiro, por que não criar um que ensine a ganhar?
________________________________________
3. Objetivos da Solução
🎯 Objetivo Principal
Introduzir jovens no mundo dos investimentos de forma saudável, divertida e acessível, usando o WhatsApp como canal natural de entrada.
🎯 Objetivos Específicos
• Ensinar conceitos reais de diversificação, risco, patrimônio e estratégia.
• Reduzir a barreira de entrada (não precisa instalar aplicativo).
• Criar ambiente social e cooperativo.
• Estimular conversas sobre dinheiro entre amigos, escolas e famílias.
• Substituir experiências negativas por uma alternativa educativa e gamificada.
• Desenvolver hábitos financeiros sustentáveis desde cedo.
________________________________________
4. Arquitetura Atualizada da Solução
4.1 Visão Geral do Fluxo
Usuário → WhatsApp → Webhook Meta → Flask → Engine InvestCup → Firebase → IA → WhatsApp
________________________________________
4.2 Componentes Principais
________________________________________
✔ 1. WhatsApp Cloud API (Meta)
• Recebe mensagens dos usuários
• Envia respostas automaticamente
• Permite que qualquer pessoa interaja com o InvestCup
________________________________________
✔ 2. Backend Python (Flask)
• Endpoint /webhook
• Roteamento das mensagens
• Integração com Firebase, IA e Alpha Vantage
• Envio de respostas ao WhatsApp
________________________________________
✔ 3. Engine do Jogo (game_engine.py)
Gerencia:
• registro de jogadores
• carteira e patrimônio
• compras e vendas
• precificação em tempo real
• ranking global
• diversificação
• salvamento automático
________________________________________
✔ 4. Banco de Dados (Firebase Firestore)
• Armazena jogadores
• Mantém a carteira persistente
• Suporta partidas contínuas e retornos posteriores
• Permite ranking global real
________________________________________
✔ 5. Integração com Mercado (Alpha Vantage)
• Preços reais de ativos da B3
• Atualizações em tempo real
• Fallback automático quando necessário
________________________________________
✔ 6. Narrador IA (Groq API)
• Gera comentários dinâmicos sobre o ranking
• Linguagem divertida e motivacional
• Engaja jogadores
• Respostas rápidas e custo baixo
________________________________________
✔ 7. Interpretador de Comandos (bot.py)
Comandos suportados:
• entrar Nome
• ativos
• comprar TICKER QTD
• vender TICKER QTD
• carteira
• ranking
• ajuda
________________________________________
4.3 Diagrama Textual do Fluxo

Usuário (WhatsApp) -> WhatsApp Cloud API (Meta -> Servidor Flask (app.py) -> Parser de Comandos (bot.py) -> Motor do Jogo (Engine) (game_engine.py) -> Firebase Firestore (persistência) + IA Narradora (Groq API) -> Resposta Final (texto formatado) ->  WhatsApp Cloud API (envia ao usuário) -> Usuário recebe resposta
________________________________________

5. Fluxo da Experiência do Usuário
1.	O usuário manda mensagem ao número oficial do InvestCup.
2.	Digita entrar Gabriel.
3.	O sistema registra o jogador no Firebase.
4.	Usa o comando ativos para ver opções.
5.	Compra ações reais com: comprar PETR4 10.
6.	Consulta sua carteira com carteira.
7.	Vê a classificação global com ranking.
8.	Recebe comentário empolgado gerado por IA.
________________________________________
6. Didática da Solução
O InvestCup ensina através da prática:
✔ Diversificação
✔ Preço médio
✔ Risco x retorno
✔ Estratégia
✔ Evolução do patrimônio
✔ Tomada de decisão
✔ Comparação saudável
Sem aulas cansativas — aprender fazendo.
________________________________________
7. Inovação e Diferenciais
Inovações técnicas
• Jogo 100% no WhatsApp
• Combinação WhatsApp + IA + mercado real
• Firebase para persistência
• Comentários dinâmicos gerados por IA
• Multijogador automático
• Zero fricção (não exige instalação)
Inovações sociais
• Alternativa educativa aos jogos de azar
• Incentiva hábitos financeiros positivos
• Estimula conversas sobre dinheiro
• Pode ser usado em escolas, universidades, famílias
________________________________________
8. Sustentabilidade e Riscos
Riscos técnicos
• Rate limit da Meta
• Limites da Alpha Vantage
• Crescimento rápido inesperado
Mitigação:
• Cache inteligente de preços
• Uso do Firebase (escala automática)
• Tokens permanentes
• Logs e monitoramento
Sustentabilidade
• Custo operacional baixíssimo
• Uso de infra gratuita da Meta e Firebase
• Escalável para milhares de usuários
________________________________________
9. Roadmap Futuro
MVP Atual – Já Implementado
• Carteira persistente
• Comprar e vender
• Ranking global
• IA para comentários
• Preços reais
• WhatsApp Bot totalmente funcional
________________________________________


Versão 2 – Expansão Educativa
• Missões diárias
• Quizzes financeiros
• Sistema de XP e medalhas
• Alertas educativos personalizados
________________________________________
Versão 3 – Plataforma Integrada
🆕 Integração com o aplicativo mobile
• Login único sincronizado
• Painel completo do usuário
• Dashboard de patrimônio
• Gráficos e evolução temporal
• Histórico completo de operações
• Gamificação avançada
• Trilhas financeiras guiadas
• Push notifications
________________________________________
Versão 4 – Ecossistema Nacional InvestCup
• Ranking entre escolas/universidades
• Trilhas e módulos educacionais
• Simuladores de investimento
• Marketplace de cursos básicos
• API pública para parceiros
________________________________________
Link para o Github do Código Inicial e protótipo pronto pelo Command Prompt: GabGorb/HackathonXP

Link para o vídeo da Solução: https://youtu.be/NaqYOfyXKEc
