use axum::extract::ConnectInfo;
use axum::routing::get;
use axum::Router;
use ngrok::prelude::*;
use std::net::SocketAddr;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // build our application with a single route
    let app = Router::new().route(
        "/",
        get(
            |ConnectInfo(remote_addr): ConnectInfo<SocketAddr>| async move {
                format!("Hello, {remote_addr:?}!\r\n")
            },
        ),
    );

    let tun = ngrok::Session::builder()
        // Read the token from the NGROK_AUTHTOKEN environment variable
        .authtoken_from_env()
        // Connect the ngrok session
        .connect()
        .await?
        // Start a tunnel with an HTTP edge
        .http_endpoint()
        .listen()
        .await?;

    println!("Tunnel started on URL: {:?}", tun.url());

    // Instead of binding a local port like so:
    // axum::Server::bind(&"0.0.0.0:8000".parse().unwrap())
    // Run it with an ngrok tunnel instead!
    axum::Server::builder(tun)
        .serve(app.into_make_service_with_connect_info::<SocketAddr>())
        .await
        .unwrap();

    Ok(())
}
