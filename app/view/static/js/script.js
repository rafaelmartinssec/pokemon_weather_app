// static/js/script.js
(function () {
  const form = document.getElementById("form_busca");
  const input = document.getElementById("input_cidade");

  const lblPokemon = document.getElementById("lblPokemon");
  const lblTemperatura = document.getElementById("lblTemperatura");
  const lblChuva = document.getElementById("lblChuva"); // backend não envia; mostramos "—"
  const lblCidade = document.getElementById("lblCidade");
  const imgPokemon = document.getElementById("img_pokemon");

  function setText(el, text) {
    if (el) el.textContent = text;
  }

  function setLoading(isLoading) {
    const btn = form?.querySelector("button[type='submit']") || form?.querySelector("button");
    if (!btn) return;
    btn.disabled = isLoading;
    btn.textContent = isLoading ? "Buscando..." : "Buscar";
  }

  async function consultar(cidade) {
    const resp = await fetch("/api/consulta", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cidade }),
    });

    // Se der ruim, tenta extrair a mensagem do backend
    if (!resp.ok) {
      let msg = `Falha (${resp.status})`;
      try {
        const j = await resp.json();
        if (j?.error) msg = j.error;
        if (j?.detalhe) msg += `: ${j.detalhe}`;
      } catch {}
      throw new Error(msg);
    }

    return resp.json();
  }

  async function onSubmit(e) {
    e.preventDefault();
    const cidade = (input?.value || "").trim();
    if (!cidade) {
      alert("Digite o nome de uma cidade.");
      input?.focus();
      return;
    }

    setLoading(true);
    try {
      const dados = await consultar(cidade);

      // Esperado do backend:
      // { cidade, temperatura, tipo, pokemon, imagem }
      setText(lblCidade, dados.cidade ?? "—");
      setText(lblTemperatura, dados.temperatura != null ? `${dados.temperatura}°C` : "—");
      setText(lblPokemon, dados.pokemon ?? "—");

      // O backend não retorna info de chuva; exibimos "—"
      setText(lblChuva, "—");

      if (imgPokemon) {
        imgPokemon.alt = dados.pokemon ? `Imagem de ${dados.pokemon}` : "Imagem do Pokémon";
        imgPokemon.src = dados.imagem || "";
      }
    } catch (err) {
      console.error(err);
      alert(`Não foi possível completar a consulta.\n${err.message || err}`);
      // Limpa/neutraliza os campos
      setText(lblCidade, "—");
      setText(lblTemperatura, "—");
      setText(lblPokemon, "—");
      setText(lblChuva, "—");
      if (imgPokemon) {
        imgPokemon.alt = "Imagem do Pokémon";
        imgPokemon.src = "";
      }
    } finally {
      setLoading(false);
    }
  }

  // liga o listener quando o DOM estiver pronto
  document.addEventListener("DOMContentLoaded", () => {
    form?.addEventListener("submit", onSubmit);
  });
})();
