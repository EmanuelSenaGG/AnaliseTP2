

function formatarCPF(input) {
    let cpf = input.value.replace(/\D/g, '');

    if (cpf.length > 11) cpf = cpf.slice(0, 11);

    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

    input.value = cpf;
}
function formatarCNPJ(input) {
    let cnpj = input.value.replace(/\D/g, '');

    if (cnpj.length > 14) cnpj = cnpj.slice(0, 14);

    cnpj = cnpj.replace(/^(\d{2})(\d)/, '$1.$2');
    cnpj = cnpj.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
    cnpj = cnpj.replace(/\.(\d{3})(\d)/, '.$1/$2');
    cnpj = cnpj.replace(/(\d{4})(\d)/, '$1-$2');

    input.value = cnpj;
}
function formatarTelefone(input) {
    let tel = input.value.replace(/\D/g, '');

    if (tel.length > 11) tel = tel.slice(0, 11);

    if (tel.length <= 10) {
        tel = tel.replace(/^(\d{2})(\d{4})(\d{0,4})$/, '($1) $2-$3');
    } else {
        tel = tel.replace(/^(\d{2})(\d{5})(\d{0,4})$/, '($1) $2-$3');
    }

    input.value = tel.trim();
}
function openTab(evt, tabName) {
    let i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}
function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}
function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}

function cadastrarFornecedor(event) {
    event.preventDefault();

    const form = document.getElementById('formCadastroFornecedor');
    const formData = new FormData(form); // já inclui arquivos

    Swal.fire({
        title: 'Cadastrando...',
        text: 'Por favor, aguarde.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch('http://127.0.0.1:5000/api/fornecedor/cadastrar', {
        method: 'POST',
        body: formData // não mexa no content-type
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw errorData;
                });
            }
            return response.json();
        })
        .then(result => {
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Fornecedor cadastrado com sucesso!',
                allowOutsideClick: true,
                allowEscapeKey: true,
                showConfirmButton: true
            }).then(() => {
                form.reset();
                closeModal('cadastroFornecedorModal');
                setTimeout(() => {
                    atualizarTabelaFornecedores();
                }, 300);

            });
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: `Erro ao cadastrar: ${error.erro || 'Falha de comunicação com o servidor.'}`
            });
        });


    return false;
}

function cadastrarLicitacao(event) {
    event.preventDefault();
    const form = document.getElementById('formCadastroLicitacao');
    const formData = new FormData(form);
    Swal.fire({
        title: 'Cadastrando...',
        text: 'Por favor, aguarde.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    fetch('http://127.0.0.1:5000/api/licitacao/cadastrar', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw errorData;
                });
            }
            return response.json();
        })
        .then(result => {
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Licitação cadastrada com sucesso!',
                allowOutsideClick: true,
                allowEscapeKey: true,
                showConfirmButton: true
            }).then(() => {
                    form.reset();
                    closeModal('cadastroLicitacaoModal');
                    setTimeout(() => {
                        atualizarTabelaLicitacoes();
                    }, 400);           
            });
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Erro ao cadastrar',
                text: `${error.erro || 'Falha na comunicação com o servidor.'}`
            });
        });

    return false;
}
function atualizarTabelaLicitacoes() {
    fetch("http://127.0.0.1:5000/api/licitacao/listar")
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#licitacoes tbody");
            if (!tbody) {
                console.error("Elemento tbody não encontrado");
                return;
            }
            tbody.innerHTML = "";

            data.forEach(licitacao => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${licitacao.empresa}</td>
                    <td>${licitacao.responsavel}</td>
                    <td>${licitacao.cnpj}</td>
                    <td>${licitacao.objeto}</td>
                    <td>
                        <button onclick="abrirModalVincular('${licitacao.id}','${licitacao.empresa}')" class="btn-vincular">
                            Vincular Fornecedores
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error("Erro ao atualizar a lista de licitações:", error);
        });
}
function atualizarTabelaFornecedores() {
    fetch("http://127.0.0.1:5000/api/fornecedor/listar")
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#fornecedor tbody");
            tbody.innerHTML = "";

            data.forEach(fornecedor => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${fornecedor.razao_social}</td>
                    <td>${fornecedor.cnpj}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error("Erro ao atualizar a lista de licitações:", error);
        });
}
let fornecedoresModal = [];
async function listarFornecedores() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/fornecedor/listar");
        if (!response.ok) throw new Error("Erro na resposta da API");
        fornecedoresModal = await response.json();
    } catch (error) {
        console.error("Erro ao buscar fornecedores:", error);
    }
}
async function abrirModalVincular(licitacaoId, licitacaoEmpresa) {
    await listarFornecedores();
    document.getElementById("licitacaoId").value = licitacaoId;
    document.getElementById("nomeEmpresaModal").textContent = licitacaoEmpresa;
    const tbody = document.getElementById("tbodyFornecedoresModal");
    tbody.innerHTML = "";

    fornecedoresModal.forEach(fornecedor => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><input type="checkbox" name="fornecedores" value="${fornecedor.id}"></td>
            <td>${fornecedor.razao_social}</td>
            <td>${fornecedor.cnpj}</td>
        `;
        tbody.appendChild(tr);
    });

    openModal('vincularFornecedorModal');
}
function registrarVinculos(event) {
    event.preventDefault(); // evita reload da página
    const licitacaoId = document.getElementById("licitacaoId").value;
    const checkboxes = document.querySelectorAll("#tbodyFornecedoresModal input[type='checkbox']:checked");
    const fornecedoresSelecionados = Array.from(checkboxes).map(cb => cb.value);

    if (fornecedoresSelecionados.length === 0) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Selecione pelo menos um fornecedor para vincular.',
            allowOutsideClick: true,
            allowEscapeKey: true,
            showConfirmButton: true
        });
        return;
    }

    fetch("/api/licitacao/registrarvinculos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            licitacao_id: licitacaoId,
            fornecedores: fornecedoresSelecionados
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao salvar vínculos.");
            }
            return response.json();
        })
        .then(data => {
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Fornecedores vinculados com sucesso!',
                allowOutsideClick: true,
                allowEscapeKey: true,
                showConfirmButton: true
            })
            closeModal("vincularFornecedorModal");
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Que pena...',
                text: `Ocorreu um erro ao vincular os fornecedores. ${error}`,
                allowOutsideClick: true,
                allowEscapeKey: true,
                showConfirmButton: true
            });

        });
}
