function gerarPropostaTabela(apiUrl) {
    const tabela = document.getElementById("tabela");

    Swal.fire({
        title: 'Analisando Edital...',
        html: 'Por favor, aguarde enquanto os dados são processados.',
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading()
    });

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) throw new Error("Erro na requisição");
            return response.json();
        })
        .then(json => {
            json.forEach(item => {
                const descricao = item.descricao || item.item || "";
                const unidade = item.unidade || "";
                const quantidade = parseFloat(item.quantidade) || 0;
                const preco = parseFloat(item.preco) || 0;
                const total = quantidade * preco;

                inserirLinha(
                    descricao,
                    unidade,
                    quantidade,
                    preco,
                    total
                );
            });

            ordenarTabela();
            Swal.close();
            tabela.style.display = "table";
        })
        .catch(err => {
            console.error("Erro ao processar proposta:", err);

            inserirLinha(
                "ITEM EXEMPLO - ERRO AO CARREGAR",
                "UND",
                1,
                99.90,
                99.90
            );

            ordenarTabela();
            Swal.fire(
                "Erro",
                "❌ Não conseguimos analisar o edital. Uma linha de exemplo foi adicionada.",
                "error"
            );
            tabela.style.display = "table";
        });
}



function inserirLinha(descricao, unidade, quantidade, preco, total) {
    const tbody = document.getElementById("tabela-body");
    const row = document.createElement("tr");

    row.innerHTML = `
        <td class="item-numero"></td>
        <td contenteditable="true">${descricao}</td>
        <td contenteditable="true">${unidade}</td>
        <td contenteditable="true" class="editavel-quantidade">${quantidade}</td>
        <td contenteditable="true" class="editavel-preco">${preco}</td>
        <td contenteditable="false" class="valor-total">${formatarNumero(total)}</td>
        <td>
            <button onclick="removerLinha(this)" class="botaoRemover" title="Remover item">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#e74c3c" viewBox="0 0 24 24">
                    <path d="M3 6h18v2H3V6zm2 3h14l-1.5 13H6.5L5 9zm5 2v8h2v-8H10zm4 0v8h2v-8h-2z"/>
                </svg>
            </button>
        </td>
    `;

    tbody.appendChild(row);
    atualizarNumeracao();
    atualizarTotalGeral();
    ativarAtualizacaoAutomatica(row);
}



function adicionarItem() {
    const desc = document.getElementById("desc").value.trim();
    const unid = document.getElementById("unid").value.trim();
    const qtd = parseFloat(document.getElementById("qtd").value);
    const preco = parseFloat(document.getElementById("preco").value);
    const total = (qtd * preco);

    if (!desc || !unid || isNaN(qtd) || isNaN(preco)) {
        Swal.fire("Erro", "Preencha todos os campos corretamente.", "warning");
        return;
    }

    inserirLinha(desc, unid, qtd, preco, total);
    ordenarTabela();
    limparCampos();
   
}

function limparCampos() {
    document.getElementById("desc").value = "";
    document.getElementById("unid").value = "";
    document.getElementById("qtd").value = "";
    document.getElementById("preco").value = "";
}

function removerLinha(btn) {
    const row = btn.closest("tr");
    row.remove();
    atualizarTotalGeral();
    ordenarTabela();
    atualizarNumeracao();

}

function ordenarTabela() {
    const tbody = document.getElementById("tabela-body");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    rows.sort((a, b) => {
        const aText = a.cells[0].textContent.trim().toLowerCase();
        const bText = b.cells[0].textContent.trim().toLowerCase();
        return aText.localeCompare(bText);
    });

    rows.forEach(row => tbody.appendChild(row));
    atualizarNumeracao();
}

function ativarAtualizacaoAutomatica(row) {
    const qtdCell = row.querySelector(".editavel-quantidade");
    const precoCell = row.querySelector(".editavel-preco");
    const totalCell = row.querySelector(".valor-total");

    const recalcular = () => {
        const qtd = parseFloat(qtdCell.textContent.replace(",", ".")) || 0;
        const preco = parseFloat(precoCell.textContent.replace(",", ".")) || 0;
        const total = qtd * preco;

        totalCell.textContent = formatarNumero(total);
            atualizarTotalGeral();
    };

    qtdCell.addEventListener("input", recalcular);
    precoCell.addEventListener("input", recalcular);
}




function formatarNumero(valor) {
    return new Intl.NumberFormat('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 10
    }).format(valor);
}

function atualizarTotalGeral() {
    const totalGeralEl = document.getElementById("linha-total-geral");
    const totais = Array.from(document.querySelectorAll(".valor-total"));
    
    let soma = 0;
    totais.forEach(cell => {
        const texto = cell.textContent.replace("R$", "").trim().replace(/\./g, "").replace(",", ".");
        const valor = parseFloat(texto) || 0;
        soma += valor;
    });

    if (totalGeralEl) {
        totalGeralEl.querySelector("td.valor-soma").textContent = "R$ " + formatarNumero(soma);
    } else {
        const tbody = document.getElementById("tabela-body");
        const row = document.createElement("tr");
        row.id = "linha-total-geral";
        row.innerHTML = `
            <td colspan="4" style="text-align:right; font-weight:bold;">Total da Proposta:</td>
            <td class="valor-soma" style="font-weight:bold;">R$ ${formatarNumero(soma)}</td>
            <td></td>
        `;
        tbody.appendChild(row);
    }
}

function atualizarNumeracao() {
    const rows = document.querySelectorAll("#tabela-body tr");
    rows.forEach((row, index) => {
        const numeroCell = row.querySelector(".item-numero");
        if (numeroCell) {
            numeroCell.textContent = index + 1;
        }
    });
}


function enviarProposta(btn) {
    const idLicitacao = btn.getAttribute("data-idlicitacao");
    const idFornecedor = btn.getAttribute("data-idfornecedor");
    const apiUrl = btn.getAttribute("data-apiurl");

    const itens = [];
    let valorTotalGeral = 0;

    const linhas = document.querySelectorAll("#tabela-body tr");

    linhas.forEach(linha => {
        const colunas = linha.querySelectorAll("td");
        if (colunas.length >= 6) {
            const numero = colunas[0].innerText.trim();
            const descricao = colunas[1].innerText.trim();
            const unidade = colunas[2].innerText.trim();
            const quantidade = parseFloat(colunas[3].innerText.trim().replace(',', '.'));
            const preco = parseFloat(colunas[4].innerText.trim().replace(',', '.'));
            const valor_total = quantidade * preco;   
            valorTotalGeral += valor_total;

            itens.push({
                numero,
                descricao,
                unidade,
                quantidade,
                preco,
                valor_total
            });
        }
    });

    const payload = {
        idLicitacao,
        idFornecedor,
        itens,
        valor_total_geral: valorTotalGeral
    };

    Swal.fire({
        title: 'Gerando proposta...',
        text: 'Aguarde enquanto processamos os dados.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(res => {
        if (!res.ok) throw new Error("Erro ao enviar proposta");
        return res.json();
    })
    .then(dados => {
        Swal.close();
         Swal.fire("Sucesso!", "Proposta gerada com sucesso!", "success").then((result) => {
        if (result.isConfirmed && dados.url) {
            window.open(dados.url, '_blank');
        }
    });
    })
    .catch(err => {
        Swal.fire("Erro", err.message, "error");
        console.error(err);
    });
}
