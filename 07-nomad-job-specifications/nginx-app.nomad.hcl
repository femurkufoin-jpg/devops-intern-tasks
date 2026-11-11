job "nginx-app" {
  datacenters = ["dc1"]
  type        = "service"
  group "nginx-group" {
    count = 1
    network {
      port "http" {
        to = 80
      }
    }
    task "nginx" {
      driver = "docker"
      config {
        image = "nginx:alpine"
        ports = ["http"]
      }
      resources {
        cpu    = 100
        memory = 128
      }
    }
  }
}
