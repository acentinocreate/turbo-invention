# Formaço — versão 2.0.1

Ateliê tipográfico local para reconstruir referências autorizadas, extrair construções, desenhar glifos vetoriais e desenvolver famílias editáveis. Interface, mensagens e termos tipográficos em português.

## Abrir

Extraia a pasta e abra **index.html** no navegador. O HTML contém CSS, JavaScript, bibliotecas e avisos completos de licença. Nenhuma instalação, compilação, conta, chave, CDN ou servidor é necessária para editar e exportar. O funcionamento normal não faz chamadas de rede. Os documentos não são dependências do aplicativo.

Para desenvolvimento, opcionalmente execute `python -m http.server 8080` na pasta. Cada tarefa na nuvem já possui checkout isolado; use-o sem criar worktrees adicionais, salvo solicitação explícita.

## Começar do zero

No topo, clique em **Novo projeto**. Para guardar o trabalho anterior, clique em **Salvar projeto atual** na janela. Depois clique em **Começar do zero**; **Cancelar** mantém tudo como está. O projeto fica vazio de referências e desenhos, com estilos e componentes iniciais sem aprovação. O tema é mantido. **Desfazer** recupera o projeto anterior enquanto o histórico desta sessão existir; após fechar ou recarregar, use a cópia JSON salva. O salvamento local passa a guardar o novo projeto. Dados ilegíveis de uma sessão de recuperação continuam preservados e exigem cópia JSON do novo trabalho.

## Novidades

- Zoom de 25% a 3200%, centrado no cursor; roda do mouse, botões −/+ e **Ajustar à tela**. **Espaço + arrastar**, botão central ou **Mover vista** deslocam a vista. Zoom não altera contornos nem entra no histórico de edição.
- Nós e alças mantêm tamanho de interação na tela. A câmera fica estável durante ajustes. Pontos coincidentes no fechamento aparecem como um único nó e se movem juntos.
- Operações booleanas preservam curvas completas e contraformas intactas. Trechos resultantes podem ser reconstruídos como Bézier com verificação de desvio. Círculos simples usam quatro nós por contorno; formas complexas não são obrigadas a ter quatro nós.
- **Reduzir nós…** permite comparar uma simplificação de glifos antigos antes de aplicar. Desvio e contagens ficam na inspeção. Bloqueios e desfazer são respeitados.
- **Extrair construções das referências…** propõe peças de desenhos confirmados, apresenta origem/método e aponta construções ausentes. Adaptar uma haste para diagonal não observada exige seleção explícita.
- Acentos reutilizam a letra-base já desenhada. Alinhamento de mestres preserva contornos que já correspondem, sem reamostrar tudo.
- Seletor de componentes corrigido, rascunhos preservados ao trocar de peça, nomes como **Arco e ombro**, botão **Voltar à letra** e glossário.

## Primeiro projeto

1. Em **01 / Referências**, use **Exemplos originais** ou importe PNG/JPEG/SVG autorizado. Identifique caractere e estilo. O seletor abaixo dos botões escolhe uma referência existente.
2. Compare a **Sobreposição**, com opacidade/alinhamento ajustáveis. Imagens originais e corrigidas ficam separadas. Corrija raster antes de vetorizar; SVG preenchido simples carrega contornos diretamente.
3. Repare nós/alças. Clique em **Confirmar reconstrução**, depois **Analisar forma confirmada**. Vetorizar não comprova precisão.
4. Use **Extrair construções das referências…**. Selecione propostas, confira recortes e aprove peças que aceitar. Componentes ausentes precisam de desenho, outra referência ou aceitação explícita de uma proposta original.
5. Escolha modo, medidas, aberturas, terminais e formas de a/g. **Aprovar estas decisões** não aprova glifos.
6. Em **03 / Ampliar e atualizar**, proponha **Representantes H O A n o a g**. Compare, aplique seletivamente e revise antes de ampliar. Desenhos reconstruídos, editados, aprovados e bloqueados são preservados.
7. Desenvolva extremos Leve/Negrito e estruturas itálicas separadamente. Revise representantes antes de interpolar. Incompatibilidades ficam identificadas, sem substituição silenciosa.
8. Examine português, diagonais e espaçamento na **Prova**. Ajuste margens, avanços, pares e âncoras.
9. **Salvar projeto** baixa JSON editável; **Abrir projeto** restaura. Exporte um estilo ou a família habilitada. Fontes são estáticas: edições exigem reexportação.

## Referências e fidelidade

Não há contornos de fontes prontas escondidos nem modelo remoto. Receitas anatômicas usam componentes vetoriais. H/O/n e peças originais foram desenhados independentemente para este projeto.

A análise mede limites, estima hastes em três linhas de varredura e observa inclinação de uma borda longa. Não reconhece letras nem infere automaticamente intenção óptica, serifas, terminais ou anatomias ausentes. Inclinação observada é separada da adicional solicitada.

A extração usa referências principais confirmadas do estilo atual. O/o/0 podem fornecer um bojo completo; n fornece arco. Bordas longas fornecem recortes de hastes/travessas. Diagonais observadas fornecem trechos convertidos a eixo local. Bojos parciais e ombros recortados são alternativas desmarcadas. Um H não estabelece uma curva O. Nenhuma extração aprova automaticamente a peça.

| Modo | Comportamento |
| --- | --- |
| Reconstrução fiel | Preserva desenhos individuais; ampliação automática desativada. |
| Ampliação coerente | Adapta componentes autorizados às anatomias, para revisão. |
| Desenvolvimento regularizado | Também aplica grade de duas unidades aos candidatos novos. |

**Preservar exatamente** recusa redimensionamento, mudanças incompatíveis de espessura/eixo, inclinação e regularização. Outras políticas permitem adaptação; proporções sutis podem mudar. Notas são lembretes, não comandos geométricos.

Geométricas, grotescas e modulares são as construções mais diretamente atendidas. Outros estilos podem usar peças próprias. Junções contextuais, pontes de estêncil, cursivas e anatomias orgânicas/experimentais complexas precisam de desenhos independentes. Não há inferência fiel universal a partir de uma letra.

## Editor e curvas

Caneta: clique para reta, arraste para Bézier. Enter fecha; Delete exclui nó; setas movem seleção; Ctrl/Cmd-Z e Shift-Z desfazem/refazem fora de campos. Coordenadas e navegação de pontos permitem edição por teclado.

Há subdivisão, divisão/união, abrir/fechar, duplicação, transformação, espelhamento e operações booleanas. Estas usam polygon-clipping e achatamento adaptativo de 0,6 unidade. Preservam contornos inteiros correspondentes e reconstroem curvas com tolerância nominal de 0,8 unidade. Aproximações recusadas mantêm segmentos. A precisão canônica é uma unidade, igual no editor, prova e exportações.

**Reduzir nós…** exige comparação/aplicação explícitas. Tolerância solicitada e desvio efetivo ficam na inspeção; o desvio não pode superar a tolerância mais 1,5 unidade de margem de precisão. Cantos detectados, orientação e contornos são preservados; resultados inválidos são recusados. Desenhos antigos não são simplificados ao abrir.

Em candidatos gerados, segmentos minúsculos que cruzam após arredondamento podem ser retirados apenas com desvio até 1,5 unidade e geometria válida. O reparo é registrado para revisão e não atua sobre componentes exatos.

## Família, acentos e exportação

Cinco pesos e itálicos: Leve 300, Regular 400, Médio 500, Seminegrito 600, Negrito 700. Estilos adicionais podem ser nomeados/desabilitados. Regular não estabelece automaticamente os extremos.

Interpolação verifica contagem, comandos, orientação, ordem/nesting e decisões. **Alinhar contornos dos extremos** preserva pares correspondentes e reamostra apenas incompatíveis em 64 pontos. Isso não comprova correspondência semântica. Topologias diferentes precisam de desenho independente. Correções locais não são sobrescritas por atualizações compartilhadas.

Propostas itálicas alteram anatomias/terminais/proporções limitados, além da inclinação. Mestres retos/itálicos são separados. **Criar oblíquo** apenas inclina o desenho reto.

São 136 mapeamentos padrão: A–Z/a–z, algarismos, acentos portugueses solicitados, Ü/ü, Ç/ç, ordinais, pontuação, moedas, espaço/NBSP e seis marcas combinantes. Âncoras e ajustes por glifo/estilo posicionam acentos. Mapeamentos adicionais aceitam um escalar Unicode, incluindo plano suplementar; duplicatas/controles são recusados.

Prova e fonte usam os mesmos avanços e ajustes de pares. Espaçamento geral, entrelinha e modo monoespaçado são opções da prova. Caracteres ausentes aparecem tracejados.

SVG de glifo/grupo/conjunto/prova/comparação; OTF CFF; WOFF válido sem compressão; ZIP da família com fontes, projeto, README e licença escolhida. Geometria inválida, aberta, degenerada ou com cruzamentos detectados bloqueia exportação.

Fontes contêm cmap, contornos reais, métricas, pesos/indicadores itálicos, nomes seguros e famílias legadas/tipográficas, GPOS de pares/marcas, GDEF e GSUB ccmp para composições portuguesas. H + agudo sem precomposto verifica posicionamento real de marca independentemente da composição.

Não oferecidos: fontes variáveis, hinting, importação de fontes locais, marca-sobre-marca, múltiplas marcas/contextos arbitrários, grupos/geração automática de kerning, tipografia vertical, ferramentas de pixels/líquido. Validade técnica não comprova qualidade visual.

## Limites e recuperação

| Recurso | Limite |
| --- | --- |
| Referência | 8 MB; 4096 × 4096; 24 imagens |
| Projeto JSON | 32 MB |
| Glifos / estilos | 256 / 24 |
| Comandos por glifo/componente | 8000 |
| Coordenadas / avanço | ±10.000 / 0–4000 unidades |
| Histórico | 40 etapas / 64 MB serializados |
| Texto da prova | 12.000 caracteres |
| Vetorização raster | até 220 × 280, preservando proporção |
| Imagem corrigida | até 1200 × 700 |

São limites, não garantias de desempenho. Vetorização e perspectiva por vizinho mais próximo podem perder detalhes. Largura corrigida 0 preserva proporção. SVG aceita geometria preenchida simples e rejeita scripts, eventos, entidades, recursos externos, estilos, texto, imagens, filtros, máscaras, traços/retângulos arredondados não convertidos e viewports aninhados.

Falha de armazenamento mantém edição e pede backup. Salvamento ilegível é preservado para download bruto, sem sobrescrita. Importação inválida mantém o projeto. Histórico não sobrevive à recarga. Origens file:// e HTTP têm armazenamento separado: transfira por JSON. Projetos da versão anterior continuam compatíveis.

## Navegadores e verificações

Chromium 151/Linux x86-64 em HTTP local: automação executada. Viewports 1440 × 1100 e 390 × 844. Máquina: quatro núcleos de quota e 32 GiB. A tentativa file:// nesta máquina é bloqueada por política administrativa. Firefox, Safari, instalação desktop, celulares físicos e limites máximos não foram testados aqui.

Veja `RELATORIO_ATUALIZACAO.md` e resultados em `tests/`. `IMPLEMENTATION_REPORT.md` e `README_V1_EN.md` são registros históricos da primeira versão.

Com Python playwright/fonttools/uharfbuzz e Chromium em `/usr/bin/chromium`, inicie o servidor local e execute:

```sh
python tests/build.py
python tests/browser_checks.py
python tests/editor_checks.py
python tests/revision_checks.py
python tests/family_checks.py
python tests/validate_fonts.py
python tests/delivery_checks.py
python tests/native_family_checks.py
```

O último requer Fontconfig (`fc-scan`); não instala fontes. Dependências já empacotadas em `src/vendor.js`; compilação reúne shell e módulos em HTML. Manifestos fixados em `tests/` permitem recompilar bibliotecas em diretório de desenvolvimento separado. Usuários finais precisam apenas do HTML.

## Licenças e publicação

Código, peças e ativos originais: MIT (`LICENSE`). Dependências mantêm avisos completos em `LICENSES.txt` e no HTML; créditos em `DEPENDENCIES.md`. Sem fontes/imagens de terceiros sem licença. Preserve avisos na redistribuição.

`assets/`: ícone, cartão e capturas reais. `examples/`: fontes candidatas, SVGs e projetos editáveis, como estudos técnicos originais, não famílias profissionalmente aprovadas. Referências importadas e licença da fonte criada permanecem sob responsabilidade do usuário. Não se afirma disponibilidade jurídica da marca Formaço.
