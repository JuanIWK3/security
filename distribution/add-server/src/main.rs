use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() {
    let addr = "127.0.0.1:8060";

    let listener = TcpListener::bind(addr).await.unwrap();
    println!("Addition server listening on: {}", addr);

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

                let result = (n1 + n2).to_string() + "\n";

                println!("{} + {} = {}", n1, n2, result.trim());

                socket
                    .write_all(result.to_string().as_bytes())
                    .await
                    .expect("failed to write data to socket");
            }
        });
    }
}
