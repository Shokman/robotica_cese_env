# Mycobot

## Pre requisitos

Este entorno de simulación debería funcionar en cualquier versión de Ubuntu posterior a 20.04.

El uso de Ubuntu no es obligatorio, cualquier entorno que pueda compartir el acceso a la placa de video debería funcionar.
Sin embargo debido a las complejidades que involucra es altamente recomendado utilizar dicha distribución.

### Instalar docker
```
sudo apt install curl
curl -sSL https://get.docker.com/ | sh
sudo usermod -aG docker $(whoami)
```

Cualquier consulta: https://docs.docker.com/get-started/get-docker/

Es importante asegurarse que el sistema tiene el plugin para `docker compose`.
https://docs.docker.com/compose/install/linux/

```
 sudo apt-get update
 sudo apt-get install docker-compose-plugin
```

## Para configurar el espacio:
```
git clone https://github.com/Shokman/robotica_cese_env.git
cd robotica_cese_env
docker compose build
```

## Para ejecutar una de las simulaciones:
```
xhost + && docker compose up [OPTION] --force-recreate
```

Las opciones disponibles son:
- `dev`: empezar el entorno para modificarlo y trabajar con el.
- `moveit-sim-280`: empezar la simulación y el brazo configurado en `moveit` con el modelo `mycobot_280`.
- `moveit-sim-320`: empezar la simulación y el brazo configurado en `moveit` con el modelo `mycobot_320`.
