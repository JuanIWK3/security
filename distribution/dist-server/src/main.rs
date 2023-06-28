use tokio::{
    io::{AsyncBufReadExt, AsyncWriteExt, BufReader},
    net::TcpListener,
    sync::broadcast,
};

#[tokio::main]
async fn main() {
    // A TCP server listening at 8080
    let listener = TcpListener::bind("localhost:8080").await.unwrap();

    let (tx, _rx) = broadcast::channel(10);

    loop {
        // Accepting connections
        let (mut socket, addr) = listener.accept().await.unwrap();

        let tx = tx.clone();
        let mut rx = tx.subscribe();

        // Multiple connections asynchronously
        tokio::spawn(async move {
            // Separating the socket
            let (reader, mut writer) = socket.split();

            let mut reader = BufReader::new(reader);
            let mut line = String::new();

            // return the sum of two numbers
            loop {
                tokio::select! {
                    result = reader.read_line(&mut line) => {
                        if result.unwrap() == 0 {
                            break;
                        }

                        tx.send((line.clone(), addr)).unwrap();
                        line.clear();
                    }
                    result = rx.recv() => {
                        let (msg, _other_addr) = result.unwrap();


                        let num1 = msg.split_whitespace().nth(0).unwrap().parse::<i32>().unwrap();
                        let symbol = msg.split_whitespace().nth(1).unwrap();
                        let num2 = msg.split_whitespace().nth(2).unwrap().parse::<i32>().unwrap();

                        let res;

                        match symbol {
                            "+" => res = num1 + num2,
                            "-" => res = num1 - num2,
                            "*" => res = num1 * num2,
                            "/" => res = num1 / num2,
                            _ => res = 0,
                        };

                        let res = res.to_string() + "\n";

                        writer.write_all(&res.as_bytes()).await.unwrap();
                    }
                }
            }
        });
    }
}