/* Pandeiro cigano tocado pelo próprio navegador (Web Audio): nenhum arquivo de áudio de terceiros,
   então não há direito autoral envolvido. Cada "disco" é um ritmo de pandeiro solo, com viradas.

   Toques (um caractere por semicolcheia no ritmo):
     T  tapa forte: mão no couro, grave + platinelas fortes
     t  tapa leve
     x  platinela seca (dedo na borda)
     s  sacudida curta
     r  rulo (as platinelas chacoalham sem parar por um instante)
     .  silêncio */
(() => {
  "use strict";

  const DISCOS = [
    { id: "fogueira", nome: "Roda de Fogueira", humor: "pandeiro lento, em 6/8", cor: "#b3203a", bpm: 58, passosPorTempo: 2,
      base: ["T..x.st..x.s", "T..x.st.sx.s", "T..x.st..x.s", "T..xsst.r..."] },
    { id: "caminho", nome: "Caminho de Terra", humor: "pandeiro em valsa, 3/4", cor: "#d9a21f", bpm: 84, passosPorTempo: 4,
      base: ["T...s.x.s.x.", "T...s.x.sxx.", "T...s.x.s.x.", "T.x.s.xsr..."] },
    { id: "saias", nome: "Saias ao Vento", humor: "pandeiro dançante, sem pressa", cor: "#7b3fa0", bpm: 92, passosPorTempo: 4,
      base: ["T.s.t.sx", "T.s.t.sx", "T.sxt.s.", "TxsxTrr."] },
    { id: "lua", nome: "Lua Mansa", humor: "pandeiro bem suave, para ler as cartas", cor: "#2f7f7a", bpm: 56, passosPorTempo: 4,
      base: ["T...s...t...s.x.", "T...s...t.x.s...", "T...s...t...s.x.", "T...s...r......."] },
  ];

  let ctx = null, mestre = null, saida = null, ruido = null, tocando = null, timer = null;
  let proximo = 0, passo = 0;

  function iniciar() {
    if (ctx) return ctx;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    mestre = ctx.createGain(); mestre.gain.value = 0;
    // sala pequena: um pouco de reverb deixa o pandeiro mais vivo
    const eco = ctx.createConvolver(), dur = 1.6, n = ctx.sampleRate * dur, ir = ctx.createBuffer(2, n, ctx.sampleRate);
    for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / n) ** 3; }
    eco.buffer = ir;
    const molhado = ctx.createGain(); molhado.gain.value = .22;
    mestre.connect(ctx.destination); mestre.connect(eco); eco.connect(molhado); molhado.connect(ctx.destination);
    saida = ctx.createGain(); saida.gain.value = 1; saida.connect(mestre);
    ruido = ctx.createBuffer(1, ctx.sampleRate * .5, ctx.sampleRate);
    const d = ruido.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    return ctx;
  }

  // ---------- o pandeiro ----------
  // uma platinela é um par de discos de metal: alguns parciais inarmônicos agudos + um chiado curto
  function platinela(t, vol, dur) {
    const parciais = [3900, 5600, 7300, 9100, 11200];
    for (let k = 0; k < 3; k++) {
      const f = parciais[Math.floor(Math.random() * parciais.length)] * (.94 + Math.random() * .12);
      const o = ctx.createOscillator(); o.type = "sine"; o.frequency.value = f;
      const g = ctx.createGain(); g.gain.setValueAtTime(vol * .14, t); g.gain.exponentialRampToValueAtTime(.0003, t + dur * (.5 + Math.random() * .6));
      o.connect(g).connect(saida); o.start(t); o.stop(t + dur * 1.2);
    }
    const s = ctx.createBufferSource(); s.buffer = ruido;
    const hp = ctx.createBiquadFilter(); hp.type = "highpass"; hp.frequency.value = 5200;
    const pk = ctx.createBiquadFilter(); pk.type = "peaking"; pk.frequency.value = 8000; pk.gain.value = 8; pk.Q.value = 1.2;
    const g = ctx.createGain(); g.gain.setValueAtTime(vol * .5, t); g.gain.exponentialRampToValueAtTime(.0005, t + dur * .7);
    s.connect(hp).connect(pk).connect(g).connect(saida); s.start(t, Math.random() * .3); s.stop(t + dur);
  }
  // o pandeiro tem várias platinelas: elas batem quase juntas, com milissegundos de diferença
  function platinelas(t, vol, dur, quantas = 5) {
    for (let k = 0; k < quantas; k++) platinela(t + k * .0025 + Math.random() * .004, vol * (.7 + Math.random() * .3), dur);
  }
  function couro(t, vol) {
    const o = ctx.createOscillator(); o.type = "sine";
    o.frequency.setValueAtTime(230, t); o.frequency.exponentialRampToValueAtTime(120, t + .08);
    const g = ctx.createGain(); g.gain.setValueAtTime(vol * .5, t); g.gain.exponentialRampToValueAtTime(.001, t + .18);
    o.connect(g).connect(saida); o.start(t); o.stop(t + .2);
    const s = ctx.createBufferSource(); s.buffer = ruido;
    const lp = ctx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 900;
    const gn = ctx.createGain(); gn.gain.setValueAtTime(vol * .35, t); gn.gain.exponentialRampToValueAtTime(.001, t + .05);
    s.connect(lp).connect(gn).connect(saida); s.start(t); s.stop(t + .06);
  }
  function toque(tipo, t, acento) {
    const v = acento;
    switch (tipo) {
      case "T": couro(t, 1 * v); platinelas(t, .9 * v, .3, 6); break;
      case "t": couro(t, .55 * v); platinelas(t, .55 * v, .22, 4); break;
      case "x": platinelas(t, .5 * v, .12, 3); break;
      case "s": // sacudida: a mão leva o pandeiro para frente e para trás
        platinelas(t, .35 * v, .1, 3); platinelas(t + .045, .45 * v, .14, 4); break;
      case "r": { // rulo: chacoalhar contínuo que cresce e some
        const n = 18;
        for (let k = 0; k < n; k++) { const f = k / (n - 1), env = Math.sin(Math.PI * Math.min(1, f * 1.3)) * .9 + .1; platinelas(t + k * .024 + Math.random() * .006, .32 * v * env, .09, 2); }
        break;
      }
    }
  }

  function agendar() {
    if (!tocando) return; // entre parar e trocar de disco o relógio ainda pode chamar
    const d = tocando, seg = 60 / d.bpm / d.passosPorTempo;
    while (proximo < ctx.currentTime + .25) {
      const compasso = Math.floor(passo / d.base[0].length), i = passo % d.base[0].length;
      const ritmo = d.base[compasso % d.base.length], c = ritmo[i];
      // um pouco de balanço (swing) nas semicolcheias fracas e pequenas variações humanas de tempo e força
      const balanco = i % 2 === 1 ? seg * .12 : 0, humano = (Math.random() - .5) * .012;
      const acento = (i === 0 ? 1 : .8) * (.85 + Math.random() * .25);
      if (c !== ".") toque(c, proximo + balanco + humano, acento);
      proximo += seg; passo++;
    }
  }

  function tocar(id) {
    iniciar(); if (ctx.state === "suspended") ctx.resume();
    const d = DISCOS.find(x => x.id === id); if (!d) return;
    clearInterval(timer);
    tocando = d; passo = 0; proximo = ctx.currentTime + .15;
    mestre.gain.cancelScheduledValues(ctx.currentTime);
    mestre.gain.setValueAtTime(mestre.gain.value, ctx.currentTime);
    mestre.gain.linearRampToValueAtTime(.7, ctx.currentTime + 1.2);
    timer = setInterval(agendar, 40);
    agendar();
  }
  function parar() {
    if (!ctx || !tocando) return;
    tocando = null;
    mestre.gain.cancelScheduledValues(ctx.currentTime);
    mestre.gain.setValueAtTime(mestre.gain.value, ctx.currentTime);
    mestre.gain.linearRampToValueAtTime(0, ctx.currentTime + .8);
    setTimeout(() => { if (!tocando) clearInterval(timer); }, 900);
  }
  // troca de disco: abaixa o volume, espera o disco trocar e começa o outro ritmo
  function trocar(id, espera = 900) {
    if (!tocando) return tocar(id);
    parar(); setTimeout(() => tocar(id), espera);
  }
  document.addEventListener("visibilitychange", () => { if (ctx && tocando) document.hidden ? ctx.suspend() : ctx.resume(); });

  window.Musica = { DISCOS, tocar, parar, trocar, get atual() { return tocando && tocando.id; } };
})();
