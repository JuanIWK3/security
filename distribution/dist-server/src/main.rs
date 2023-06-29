use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() {
    let addr = "127.0.0.1:8080";

    let listener = TcpListener::bind(addr).await.unwrap();
    println!("Listening on: {}", addr);

    loop {
        let (mut socket, _) = listener.accept().await.unwrap();

        tokio::spawn(async move {
            let mut buf = vec![0; 1024];

            loop {
                let n = socket
                    .read(&mut buf)
                    .await
                    .expect("failed to read data from socket");

                if n == 0 {
                    return;
                }

                let msg = String::from_utf8_lossy(&buf[..n]);

                let parts = msg.split_whitespace().collect::<Vec<&str>>();

                let n1 = parts[0].parse::<i32>().unwrap();
                let n2 = parts[2].parse::<i32>().unwrap();
                let symbol = parts[1].chars().nth(0).unwrap();

                let mut result = String::new();

                match symbol {
                    '+' => {
                        result = addition(n1, n2).await;

                        println!("{} + {} = {}", n1, n2, result.trim());
                    }
                    '-' => {
                        result = subtraction(n1, n2).await;

                        println!("{} - {} = {}", n1, n2, result.trim());
                    }
                    _ => {
                        let result = "Invalid symbol\n";

                        println!("{} {} {} = {}", n1, symbol, n2, result.trim());

                        socket
                            .write_all(result.to_string().as_bytes())
                            .await
                            .expect("failed to write data to socket");
                    }
                }

                socket
                    .write_all(result.as_bytes())
                    .await
                    .expect("failed to write data to socket");
            }
        });
    }
}

async fn subtraction(n1: i32, n2: i32) -> String {
    let addr = "127.0.0.1:8070";

    let mut stream = TcpStream::connect(addr).await.expect("Failed to connect");

    let msg = format!("{} - {}", n1, n2);

    stream
        .write_all(msg.as_bytes())
        .await
        .expect("Failed to write");

    let mut buf = vec![0; 1024];

    let n = stream
        .read(&mut buf)
        .await
        .expect("failed to read data from socket");

    let msg = String::from_utf8_lossy(&buf[..n]);

    msg.to_string()
}

async fn addition(n1: i32, n2: i32) -> String {
    let addr = "127.0.0.1:8060";

    let mut stream = TcpStream::connect(addr).await.expect("Failed to connect");

    let msg = format!("{} + {}", n1, n2);

    stream
        .write_all(msg.as_bytes())
        .await
        .expect("Failed to write");

    let mut buf = vec![0; 1024];

    let n = stream
        .read(&mut buf)
        .await
        .expect("failed to read data from socket");

    let msg = String::from_utf8_lossy(&buf[..n]);

    msg.to_string()
}
