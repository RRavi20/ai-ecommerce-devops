terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "ecommerce" {
  name         = "ai-ecommerce-devops:1.1"
  keep_locally = true
}
