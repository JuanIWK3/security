use std::thread::sleep;
use std::time::Duration;

use rand::Rng;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;

#[tokio::main]
async fn main() {
    let addr = "127.0.0.1:8080";

    let mut stream = TcpStream::connect(addr).await.expect("Failed to connect");

    loop {
        let n1 = rand::thread_rng().gen_range(1..100);
        let n2 = rand::thread_rng().gen_range(1..100);
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

        println!("{n1} + {n2} = {}", msg.trim());

        sleep(Duration::from_secs(2))
    }
}
