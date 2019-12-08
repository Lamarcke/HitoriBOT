# HitoriBOT

Bot de anime 100% brasileiro e open-source. Sinta-se livre para contribuir como desejar ao projeto.

Bot criado usando a linguagem de programação Python, e a biblioteca Discordpy.

Caso esteja interessado em ajudar no desenvolvimento, basta fazer seu primeiro pull request e começar a desenvolver.

## Adicione o BOT ao seu servidor:

Basta clicar no link a seguir, e clickar em adicionar: (necessário permissões de moderação para adicionar)
<https://discordapp.com/oauth2/authorize?client_id=650197869990772736&scope=bot&permissions=228416>


### O que ele pode fazer:

- **Explicação dos commandos disponiveis e suas respectivas sintaxes ( "/" sem aspas é o prefixo para realizar comandos.)**

Digite /help para visualizar os comandos no chat do discord.

* Recomendar um anime, manga, filme, manwha, manhua ou doujin ao usuario usando como base a lista de mais populares do MAL, da pagina 1 à 30.
    
    /recommendme anime, < manga, manwha, manhua, doujin >

* Pesquisar qualquer anime ou mangá na database do MAL e retornar ao usuario em forma de embed no chat.
    
    /search < anime, manga, character, person > < nome >

* Retornar ao usuario os animes que irão sair no dia em questão.
    
    /airing < dia-da-semana > (Ex: /airing terça [não usar feira])
    
    /airing < today > ou < tomorrow > # Retorna os lançamentos do dia ou do dia seguinte.

* Rádio de anime 100% funcional, permite avançar estaçoes e acompanhar as estaçoes escolhidas pelo BOT.
    
    /radio # Entra no canal de voz atual e sintoniza com a estação escolhida pelo Bot.
    
    /radio update # Atualiza a estação sendo tocada atualmente e sintoniza com a escolhida pelo BOT atualmente.
    
    /radio next # Avança uma estação no servidor atual, utilize "update" para retornar a estação que o BOT está tocando atualmente.
     


#### CHANGELOG


* Adicionado opção de schedule, para o dia atual, seguinte e qualquer dia da semana.

* Adicionado radio HitoriBOT, é radio de otaco, mas pode ouvir que é só musga boa (eu epero)

* Implementado comando help aprimorado.

##### TO-DO
* Aprimorar Pesquisa:
  Adicionar opção de genero as pesquisas com o bot.

* Função reminder:
  Lembrar o usuario sobre animes que o mesmo está acompanhando no dia em que eles forem lançar.
  Ainda em fase de implementação.
  
