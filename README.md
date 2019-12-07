# HitoriBOT

Bot de anime 100% brasileiro e open-source. Sinta-se livre para contribuir como desejar ao projeto.

Bot criado usando a linguagem de programação Python, e a biblioteca Discordpy.

Caso esteja interessado em ajudar no desenvolvimento, basta fazer seu primeiro pull request e começar a desenvolver.

## Adicione o BOT ao seu servidor:
Basta clicar no link a seguir, e clickar em adicionar: (necessário permissões de moderação para adicionar)
<https://discordapp.com/oauth2/authorize?client_id=650197869990772736&scope=bot&permissions=228416>


### O que ele pode fazer:

* Recomendar um anime, manga, filme, manwha, manhua ou doujin ao usuario usando como base a lista de mais populares do MAL, da pagina 1 à 30.
    Sintax: /recommendme anime, < manga, manwha, manhua, doujin >

* Pesquisar qualquer anime ou mangá na database do MAL e retornar ao usuario em forma de embed no chat.
    Sintax: /search < anime, manga, character, person > < nome >

* Retornar ao usuario os animes que irão sair no dia em questão.
    Sintax: /schedule < dia-da-semana > (Ex: /schedule terça [não usar feira])
    Sintax: /schedule < today > ou < tomorrow > # Retorna os lançamentos do dia ou do dia seguinte.

#### CHANGELOG

* Adicionado opção de schedule, para o dia atual, seguinte e qualquer dia da semana.

##### TO-DO

* Função reminder:
  Lembrar o usuario sobre animes que o mesmo está acompanhando no dia em que eles forem lançar.
  Ainda em fase de implementação.
  
