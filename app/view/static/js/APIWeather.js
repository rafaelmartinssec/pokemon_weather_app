class PegaCidade {
  //Função class para api clima
  constructor(nomeCidade) {
    // classe construtora o metodo é criado para direcionar a string nome cidade como atributo
    this.nomecidade = nomeCidade; // referenciando a instancia do metedo
    let key = "6ce079aa71a79c95ed661ab729f8f323"; //chave de acesso para realizar as requisições Rest para as API(s
    let urlstr = "https://api.openweathermap.org/data/2.5/weather?q=" + nomeCidade + "&appid=" + key + "&units=metric"; // acesso a api pela url
    console.log("PegaCidade"); //mostra no conslo PegaCidade
    fetch(`${urlstr}`, options) //manipulação e utilização da api
      .then((response) => {
        // retorna promise com jason do pokemon
        response.json().then((data) => mostrarDados(data)); //promise com os dados
      })
      .catch((e) => console.log("Deu erro: " + e, message)); // mensagem de erro caso não adquirir dados
  }
}
function mostrarDados(data) {
  // função que apresenta o que mostraras os dados
  let t, weather, main, chuva; // declarando as variaveis do tipo let não serão alteradas
  if (data) {
    console.log(data);
    //se for data  rodar o script abaixo
    t = data.main.temp; // armazenando no objeto t =  data.main.temp
    weather = data.weather[0].main; //armazenando na variavel weather o clima atual
    chuva = weather == "Rain" ? "Sim" : "Não";
    document.getElementById("lblTemperatura").innerHTML = t; //aqui se obtem o parametro partindo do atributo
    document.getElementById("lblChuva").innerHTML = chuva;
    document.getElementById("lblCidade").innerHTML = data.name;
    PegaPokemon(); // função PokeAPI                                      //chama função PegaPokemon
  }
}

const options = {
  method: "GET",
  mode: "cors",
  cache: "default",
};