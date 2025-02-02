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
- `moveit-sim-280`: empezar la simulación y el brazo configurado en `moveit` con el modelo `mycobot_280`.
- `moveit-sim-320`: empezar la simulación y el brazo configurado en `moveit` con el modelo `mycobot_320`.
- `dev`: empezar el entorno para modificarlo y trabajar con el, como se explica mas adelante. 


## Como usar este repositorio para desarrollo:

Recontruimos la imagen e inicializamos una nueva imagen:
```
$ docker compose build --no-cache
$ xhost + && docker compose up dev --force-recreate
```

En una terminal separada nos introducimos en el container.
```
$ docker exec -it robotica_cese_env-dev-1 /bin/bash
```

En esta forma, cualquier cambio en la carpeta `./src/third-party/mycobot-ros2` se reflejan en la carpeta `/root/ros2_ws/src/mycobot_ros2` adentro de la imagen.
Asi podemos hacer cualquier cambio que querramos dentro de esa carpeta y ejecutar los cambios en el sistema con el comando desde la segunda terminal:

```
$ ROBOT_MODEL=mycobot_320 /root/ros2_ws/src/mycobot_ros2/mycobot_bringup/scripts/mycobot_gazebo_and_moveit.sh
```