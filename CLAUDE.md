Projeto: site Tenda Cigana (da Thays Rosa, esposa do Rafa, cartomante cigana)

Onde está
* Pasta: C:\Users\Rafa\Projetos\tenda-cigana. Um index.html (HTML, CSS e JS num arquivo só) e a pasta assets/ com as imagens.
* Repositório git só local por enquanto (sem GitHub). Criar o repositório e publicar só quando o Rafa pedir.
* Para testar: python -m http.server 8082 dentro da pasta.

Pedido original
* Seguir o caminho do Bem Dito Tarot (C:\Users\Rafa\Desktop\bemdito-taro), mas nos tons e na luz das fotos da pasta "site thays" na área de trabalho (velas, vinho, dourado, roxo, rosa, carroças com flores e lanternas).
* Baralho com prévia que leva ao WhatsApp da Thays: (17) 99124-1828 (wa.me/5517991241828).
* Logomarca linda e quente; carroça andando pelo site; carroça grande onde a pessoa entra (como a casinha do Bem Dito); card rosa da Thays com o contato; roda de carroça no painel.

Decisões de design
* Fontes: Cinzel Decorative (títulos), Cormorant Garamond (frases), Great Vibes (script: Thays Rosa, chamadas), Mulish (texto).
* Cores no :root: vinho, ouro, vela, roxo, rosa, turquesa (da carroça do jardim), fundo marrom bem escuro.
* Logo: emblema em SVG (symbol #emblema): tenda listrada com bola de cristal, lua, "TENDA CIGANA" em arco e fita rosa "Thays Rosa". Usado na abertura, topo, herói e rodapé.
* Abertura: (removida na rodada 6; as cortinas ficam abertas nas bordas do herói).
* Brasas subindo e poeira dourada atrás do mouse (canvas #faiscas).
* Som desligado por padrão (pandeiro, cartas e brilho feitos com WebAudio). O pandeiro da carroça toca sempre que é tocado.
* Botão "?" com popover em cada recurso interativo.

Seções
1. Herói: fundo assets/velas.webp, logo, frase do flyer da Thays.
2. Baralho: 36 cartas do baralho cigano (Lenormand) desenhadas em SVG. Carta do dia ou Três cartas (o que foi, o que é, o que vem). Cada carta tem polaridade (positiva, de alerta, neutra) tirada da imagem "Polaridade das cartas" da pasta. Mensagens e conselhos foram escritos pelo Claude: a Thays precisa revisar.
3. Bola de cristal: pergunta de sim ou não, 18 respostas (texto do Claude), leva a pergunta ao WhatsApp.
4. Carroça: foto assets/carroca-ouro.webp; toque na porta dá zoom e clarão e abre o interior (tela cheia, SVG 1600x900; no celular arrasta para os lados). Dentro: ervas (foto assets/ervas.webp), velas por cor, moedas da sorte (bênçãos), pandeiro, lanternas que trocam de cor, bola de cristal e carta do conselho.
5. Povo cigano: silhueta dourada assets/danca.webp e conselhos que giram. Os três primeiros vieram das imagens da pasta; os outros três são do Claude.
6. Thays: card rosa (inclina com o mouse) com o WhatsApp.
* Carroça pequena (SVG) atravessa o pé da tela de tempos em tempos, com rodas girando na velocidade certa; tocar nela leva à seção da carroça.
* Roda de carroça fixa no canto: gira com a rolagem, o aro mostra o progresso e o toque abre o menu das seções.

O que ainda falta
* Revisão da Thays: mensagens das 36 cartas, respostas da bola, ervas, velas, bênçãos e conselhos.
* Foto real da Thays (o site não usa foto dela; as fotos da pasta são de referência e algumas têm marca d'água de outros perfis, por isso não foram usadas).
* Instagram ou outros contatos, se ela quiser.

Rodada "realismo" (10/10/2026)
* O Rafa achou o primeiro visual infantil: quer tudo realista, no estilo da foto da carroça. Sem tenda na logo e sem babado (franja) no topo.
* Cartas: são as 36 da imagem "Polaridade das cartas" (54e7f8d2...jpg), recortadas por ferramentas/recortar_cartas.py, ampliadas 4x com Real-ESRGAN e exportadas por ferramentas/exportar_cartas.py para assets/cartas (360x840). A 20 (Parque) e a 36 (Cruz) tinham marcas por cima e foram repintadas com inpainting.
* Imagens geradas na RX 7900 XTX com o Juggernaut XL (diffusers + DirectML): verso das cartas, interior da carroça, bola de cristal, rosa na bola da logo e carroça de lado. ferramentas/preparar_cenas.py separa a carroça em corpo + roda (as rodas giram no passeio e na roda do canto).
* Interior da carroça: foto assets/interior.webp num SVG 1344x768 com pontos de toque (lanternas trocam a cor da luz, bola, baralho, velas, ervas, bênção). Pandeiro e moedas saíram.

Rodada 3 (10/10/2026)
* Abertura: cortina de veludo realista (assets/cortina.webp, só o meio do veludo, sem babado) em 7 faixas por lado que ondulam e franzem ao abrir.
* Logo: rosa com 5 cartas (9, 32, 24, 31, 33) em leque e perspectiva atrás (ferramentas/montar_logo.py -> assets/logo-centro.webp); "Thays Rosa" grande em Great Vibes rosa-claro, sem fita; "TENDA CIGANA" em Cinzel Decorative 900.
* Letras encorpadas: títulos peso 900, script com contorno fino da própria cor, frases em Cormorant 600/700.
* Carroça que passeia: é a da foto "Entre na carroça" recortada (ferramentas/rodas_carroca.py). Não é espelhada: anda para onde a frente aponta (esquerda e fundo), diminuindo e subindo um pouco. O aro das rodas fica parado no corpo; só o miolo (raios e cubo) gira, desentortado para círculo e entortado de volta no CSS com a inclinação medida (rotate + scaleX).
* Músicas: só pandeiro (o Rafa não gostou do violão/violino sintetizado). musica.js tem 4 ritmos de pandeiro solo com viradas (tapa, platinela seca, sacudida, rulo).
* A carroça alterna o lado a cada passagem (direita->esquerda como na foto; esquerda->direita espelhada).
* Interior vivo e leve: respiração lenta, paralaxe com mouse/inclinação, chamas, luzinhas da guirlanda, fumaça de incenso e poeira (canvas só com a carroça aberta).
* Painéis de vela e bola usam fotos geradas (assets/velas, assets/bola.webp).
* Gramofone (canto inferior esquerdo): musica.js compõe e toca 4 músicas ciganas tranquilas no navegador (violão Karplus-Strong, pandeiro, baixo, violino), sem arquivo de áudio e sem direitos autorais. Trocar de disco levanta o disco e muda a cor do selo.

Rodada 4 (11/10/2026)
* Interior da carroça agora é a mesa vista do alto (ferramentas/montar_mesa.py): imagem gerada, papel e carta de jogo apagados por inpainting e 5 cartas do baralho (33, 24, 31, 16, 9) + monte de versos deitados em perspectiva. Pontos: bola (globo aceso), lanterna, ervas e rosas, velas, bênção (prato), baralho.
* Seção "Jogos da tenda" (#jogos), 5 abas: leitura da mão (linhas acendem na foto), borra de café (xícara gira, vira e a borra desenha 3 símbolos), Roda da Fortuna (gira com o dedo ou botão, 8 setores), moedas da sorte (3 moedas rosa/lua giram em 3D), fitas de pedido (amarradas na foto da carroça, guardadas no localStorage do visitante). Imagens em assets/jogos (ferramentas/preparar_jogos.py). Textos dos jogos escritos pelo Claude: a Thays precisa revisar.

Rodada 5 (11/10/2026)
* Cortinas da abertura no tom do fundo da foto 734a6773...jpg (a cigana com cartas): esquerda de brocado roxo com bordado dourado (assets/cortina-roxa.webp), direita de seda vermelha bordada (assets/cortina-vermelha.webp). Geradas na placa (gerador/montar_rodada5.py, escolhidas roxa-93 e vermelha-91, exportadas por ferramentas/preparar_cortinas.py); a foto em si não é usada (é de outro perfil, com marca d'água).
* Cada lado é uma foto em "cover" com a borda de dentro no meio da tela, cortada em 7 faixas; a foto inteira fica também atrás das faixas para as frestas do ondular não mostrarem o site. assets/cortina.webp continua só no cartão da Thays.
* gerar.py força o dispositivo de execução na placa (com o VAE no processador o diffusers achava que era tudo no processador).

Rodada 6 (11/10/2026)
* Sem cena de abertura: as cortinas ficam já abertas nas bordas da primeira tela (herói), presas no meio com borlas douradas, fazendo a barriga. Foto gerada (presa-vermelha-102) cortada em esquerda e direita por ferramentas/preparar_rodada6.py -> assets/cortina-presa-esq.webp e -dir.webp. No celular aparece só o lado de fora de cada cortina. (cortina-roxa.webp e cortina-vermelha.webp da rodada 5 não são mais usadas.)
* Carroça que passeia agora é dourada e puxada por dois cavalos (vardo-cavalos-112, sem fundo: assets/cavalos-corpo.webp; miolo da roda de trás em assets/cavalos-roda.webp, girando em volta do cubo). Faz o roteiro da Rural (site vai-de-rural): atravessa o pé da tela, vira fora da tela e volta, sem parar; espelhada na volta para os cavalos irem sempre na frente; sacoleja e levanta poeira atrás. As fotos antigas carroca-corpo/roda1/roda2 não são mais usadas.
* Seção "Sobre este espaço" (#sobre), no fim: texto de compromisso com a cultura cigana que a Thays trouxe (em primeira pessoa, assinado Thays Rosa). Link no menu do topo, no menu da roda e no rodapé.

Rodada 7 (11/10/2026)
* Cavalos à frente dos varais: os cavalos da vardo-cavalos-112 foram recortados pelo contorno medido à mão (ferramentas/gerador/cavalos_contorno.py); a frente da carroça foi repintada sem eles (gerador/separar_cavalos.py, inpainting; escolhida a semente 141, que pôs uma plataforma com buquê de rosas na frente). ferramentas/preparar_rodada7.py monta tudo: cavalos 695 px à frente, varal dourado prolongado até a carroça, as duas rodas separadas para girar (cavalos-roda e cavalos-roda2) e as pernas cortadas em 4 faixas (cavalos-perna-1..4) que balançam em trote em volta do quadril/ombro. O inpainting estourou a memória da placa na 2ª semente (lá o VAE fica na placa); uma bastou.
* Leitura da mão agora é pela foto: tocar no espaço abre a câmera ou a galeria. A IA é o MediaPipe Hand Landmarker (Google, gratuito), rodando no navegador: modelo em assets/ia/hand_landmarker.task, código pelo jsDelivr (@mediapipe/tasks-vision@0.10.14). Mede palma e dedos (forma Terra/Ar/Fogo/Água, indicador x anelar, polegar, abertura dos dedos), desenha as 3 linhas pelos pontos da mão e a pessoa escolhe como cada linha é. A foto não sai do aparelho. Textos dos traços escritos pelo Claude: a Thays precisa revisar.

Rodada 8 (11/10/2026)
* Povos ciganos: na seção #povo, bandeira romani (SVG) e um cartão por povo (Calon, Kalderash, Matchuaia, Lovara, Horahané, Sinti). Cada um abre a sua página em tela cheia, com endereço próprio (#povos/<id>; o voltar do celular e o Esc fecham). Os textos ficam no objeto POVOS do index.html, escritos pelo Claude só com fatos bem conhecidos (origem, língua, ofícios, chegada ao Brasil), com nota de que cada família tem a sua história, seguindo o texto "Sobre". A Thays precisa revisar.
* Leitor "Ouvir a página" em cada página de povo: voz do próprio aparelho (Web Speech API, pt-BR), sem serviço externo; lê frase por frase, destaca o parágrafo lido e rola até ele. Mesmo jeito do site da Vai de Rural.

Cuidados técnicos
* GERAR IMAGEM NA PLACA: no DirectML o dispositivo 0 é o vídeo integrado do Ryzen (512 MB) e deu tela azul VIDEO_MEMORY_MANAGEMENT_INTERNAL três vezes. Sempre escolher a RX 7900 XTX pelo nome. Em meia precisão o DirectML devolve imagem cinza: usar fp32. O VAE fica no processador (na placa estourou a memória em 1344x768). No Real-ESRGAN (Vulkan) a ordem é outra: -g 0 é a RX 7900 XTX.
* As imagens são geradas por ferramentas/preparar_imagens.py a partir da pasta "site thays".
* Brilhos decorativos do interior não podem receber toque: regra .interior [fill="url(#i-brilho)"] { pointer-events: none; }.
* Testes com Playwright usando o Chrome do computador (channel="chrome"), em 1440x900 e 390x844.
* Commit e push só quando o Rafa pedir.
