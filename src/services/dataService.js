export async function cleaningDatas(data) {
    const newData = data.map(item => ({
            "CodigoTuss": item["Código"],
            "Preco": Number(item["Preço Máximo Intercâmbio Nacional"].replace(',', '.')) || 0,
            "NomeComercial": item["Nome e Apresentação Comercial"],
            "NomeBrasindice": item["Apresentação Brasindice"]
    }))

    const procedimentoComValorZero = newData.filter(item => item.Preco <= 0);
    const procedimentoVerificado = newData.filter(item => item.Preco > 0);

    return { procedimentoVerificado, procedimentoComValorZero };
};