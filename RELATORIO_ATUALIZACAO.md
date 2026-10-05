# Formaço 2.0.1 — atualização solicitada

Data: 2026-10-05. Aplicativo: `index.html`, independente dos documentos. Interface e vocabulário tipográfico em português. Fontes/arte de terceiros não foram adicionadas; módulos novos são código original sob MIT.

## Atualização 2.0.1: novo projeto

Adicionado **Novo projeto** no topo, com confirmação, download opcional da cópia anterior e recuperação por Desfazer durante a sessão. Limpa referências, glifos, notas, mapeamentos personalizados, ajustes de pares e decisões; repõe estilos e componentes iniciais sem aprovação. Mantém o tema e reinicia controles de referência e edição. O projeto novo substitui o salvamento saudável, mas não sobrescreve dados ilegíveis preservados para recuperação.

Executados em Chromium 151, HTTP local, 1440 × 1100 e 390 × 844: **17 verificações de reinício aprovadas**, em `tests/reset-results.json`, incluindo cancelar, cópia JSON, desfazer/refazer, recarregar, tema, ausência de transbordamento móvel, armazenamento cheio, recuperação, erros de console e chamadas remotas. Também reexecutadas as **24 verificações gerais do navegador**, todas aprovadas. Reprodução: `python -m http.server 8080`, depois `python tests/reset_checks.py` e `python tests/browser_checks.py` com Playwright Python e Chromium em `/usr/bin/chromium`.

Os testes de fontes e demais verificações abaixo correspondem à versão 2.0 e não foram reexecutados para esta mudança de interface. A geração de contornos e fontes não foi alterada. A restrição administrativa a file:// permanece; esta atualização foi testada por HTTP, sem afirmar um teste local file:// executado.

## Mudanças implementadas

**Zoom e edição:** ampliação de 25% a 3200% pelo cursor, roda, botões e ajuste à tela. Deslocamento por Espaço + arrastar, botão central ou ferramenta Mover vista. Câmera estável durante edição; nós/alças com tamanho constante na tela. Pontos de fechamento coincidentes não duplicam marcadores e são editados juntos.

**Menos nós:** curvas completas e contraformas que permanecem intactas nas operações booleanas retêm seus controles Bézier. Trechos novos são ajustados por aproximação cúbica com controle de desvio e validação geométrica; cantos detectados ficam preservados. Se o ajuste falhar, o trecho conserva segmentos. O contador central de g e os contornos de O usam quatro nós cúbicos nos casos circulares simples testados. Não se força uma forma irregular a quatro nós.

Glifos antigos possuem **Reduzir nós…**, com comparação, tolerância solicitada, desvio efetivo, bloqueio de resultados inválidos e desfazer. Abrir um projeto não simplifica automaticamente seu desenho. O alinhamento de mestres mantém os contornos que já correspondem e reamostra apenas os incompatíveis.

**Português:** controles, mensagens de validação, medidas, estados, estilos padrão, opções de componentes, guias e inspeção traduzidos. Glossário incluído. Os identificadores internos do JSON e comandos SVG/OpenType permanecem estáveis para compatibilidade; conteúdo importado e nomes escolhidos pelo usuário não são traduzidos automaticamente.

**Poucas referências:** extração assistida a partir das referências principais confirmadas do estilo atual, com propostas de hastes, travessas, bojos, ombros e diagonais observadas. Cada proposta registra referência, método e confiança descritiva. Recortes incompletos e adaptações não observadas ficam desmarcados; construções ausentes são apontadas. Aplicação seletiva e undo mantêm as peças sem aprovação até revisão. Glifos existentes não são regenerados automaticamente.

Formas reais de O/n podem alimentar bojos/ombros para outras anatomias, preservando inclusive irregularidades dos contornos de origem. Acentos gerados aproveitam o glifo-base já editado em vez de reconstruir outra base procedural. Isso melhora o aproveitamento de letras de um logotipo; não estabelece automaticamente todas as construções de uma família a partir de uma única letra.

## Defeitos identificados e corrigidos

- Um componente em edição impedia selecionar outro e o menu voltava ao anterior. A troca funciona, conserva rascunhos não salvos e exige salvar suas alterações antes da aprovação; há **Voltar à letra**.
- A prévia normalizada da haste para diagonais aparecia como quadrado. Agora é mostrada como haste em eixo local; a receita define sua inclinação na letra.
- Booleanas transformavam curvas/contraformas inteiras em numerosos segmentos. A recuperação de contornos intactos e o ajuste cúbico corrigem esse fluxo.
- Pontos coincidentes de fechamento eram exibidos/editados separadamente. Agora compartilham posição e ajuste das alças vizinhas.
- Durante a regressão, arredondamento de uma junção do cifrão itálico gerou um segmento de aproximadamente uma unidade que se cruzava. O candidato pode reparar apenas esses segmentos minúsculos, com desvio até 1,5 unidade e registro para revisão. Componentes exatos e desenhos existentes não sofrem essa correção automática.
- Mensagens de exportação podiam identificar o caractere selecionado, em vez do glifo efetivamente inválido. Agora identificam o glifo responsável.

## Testes executados

**321 verificações passaram**, mais **10 leituras nativas por Fontconfig**. Evidências reproduzíveis em `tests/*-results.json`.

| Suíte | Verificações aprovadas |
| --- | ---: |
| Fluxo no navegador | 24 |
| Referências e editor | 21 |
| Nova revisão | 30 |
| Família, mestres e armazenamento | 14 |
| FontTools + HarfBuzz independentes | 230 |
| Restauração dos projetos entregues | 2 |
| Fontconfig, separado das anteriores | 10 |

Os testes novos verificaram zoom no cursor, limites, deslocamento sem modificar desenhos, tamanho dos nós em tela, edição ampliada/desfazer, quatro nós cúbicos no contador de g, curvas preservadas no reparo de mestres, redução de um glifo denso de 165 nós com limite de desvio/desfazer, proteção de bloqueios, troca de componentes, interface portuguesa, uma/múltiplas referências, decisão explícita para diagonal não observada, preservação de O assimétrico, procedência da proposta o, reutilização de base editada para acentos e compatibilidade de projeto da versão anterior. Sem exceções não tratadas ou chamadas de rede nesses fluxos.

FontTools/HarfBuzz validaram independentemente os dez OTF/WOFF: mapeamentos, contornos, contraformas/orientação, margens/avanços, pesos, nomes, indicadores itálicos, licença, checksums, kerning, cobertura e posicionamento de marcas, equivalência OTF/WOFF e pares portugueses NFC/NFD. Cada estilo também teve o contador de g verificado como quatro segmentos cúbicos. H + agudo verifica GPOS sem depender de composição preexistente.

O fixture de mestres realizou 53 reparos explícitos e produziu 375 intermediários compatíveis. Foram bloqueados 33 candidatos: topologias diferentes ou cruzamentos na interpolação. Os arquivos de exemplo completam esses casos com propostas independentes explicitamente fornecidas pelo script; o aplicativo não preenche falhas silenciosamente. Aprovações artificiais usadas nos testes foram removidas dos projetos publicados.

Ambiente: Chromium 151.0.7922.173, Linux x86-64, HTTP local, quatro núcleos de quota e 32 GiB de limite. Viewports 1440 × 1100 e 390 × 844. Geração de 136 candidatos: aproximadamente **0,43 s** na regressão final de navegador. Não é promessa de desempenho em projetos máximos ou celulares físicos.

## Não executado e limites

A abertura `file://` foi novamente tentada e bloqueada pela política administrativa desta máquina (`ERR_BLOCKED_BY_ADMINISTRATOR`); a política não foi contornada. O usuário relatou abertura local da versão anterior em seu dispositivo, mas não houve teste automatizado local em dispositivo externo. Firefox/Safari, celulares físicos, instalação e menus de aplicativos desktop, auditoria completa de acessibilidade, carga máxima e revisão profissional externa não foram executados.

Uma letra não determina todas as decisões de outra: contraste óptico, terminais, serifas, a/g, aberturas e anatomias não observadas exigem aprovação ou desenho. A extração é geométrica e assistida; não há reconhecimento automático, aprendizado de estilo por modelo ou garantia de reconstrução perfeita. Recortes podem conter junções e precisam de revisão. Envelope proporcional pode alterar detalhes. Estênceis, cursivas e orgânicas complexas continuam exigindo trabalho manual.

Quatro nós são adequados aos círculos/elipses simples testados, não a todos os contornos. Ajuste cúbico e arredondamento podem alterar detalhes dentro das tolerâncias; a redução informa desvio e pode ser recusada. O reparo em 64 pontos de um contorno incompatível ainda é uma operação explícita que pode exigir refinamento. Compatibilidade técnica não comprova correspondência semântica ou qualidade óptica.

Continuam ausentes: fontes variáveis/hinting, importação de fontes locais, marca-sobre-marca, múltiplas marcas/contextos arbitrários, grupos e geração automática de kerning, scripts contextuais e ferramentas opcionais de pixels/líquido. Limites completos no README. Os exemplos são estudos candidatos, não fontes comercialmente aprovadas.

## Atualizar sem perder o projeto

Na versão anterior, use **Save project**. Abra o novo HTML e use **Abrir projeto** para restaurar o JSON. Nomes próprios e contornos existentes são mantidos. Para o g já denso, use **Coordenadas, geometria, âncoras e espaçamento → Reduzir nós…**, revise a comparação e aplique se aceitar. Desfaça se necessário. Salve uma nova cópia e reexporte fontes após editar.

Reprodução: comandos no README, servidor HTTP local e Chromium. `tests/revision_checks.py` usa o commit original `a8864a0` como fixture histórico de compatibilidade; em um ZIP sem histórico Git, use o arquivo `tests/fixtures/legacy-family.formaco.json` entregue para esse teste.
