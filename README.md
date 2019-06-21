# Análisis de Datos de dispositivos IoT
## aws-tf-iot-analysis

Proyecto para la transmisión y el análisis de datos desde dispositivos IoT con core Linux hacia AWS.

En este proyecto se pretende transmitir información haciendo uso del [protocolo MQTT](http://mqtt.org/) utilizando los servicios de nube ofertados por [Amazon Web Services para IoT](https://aws.amazon.com/es/iot/), almacenarlos en una base de dato no relacional haciendo uso del servicio [MongoDB Atlas](https://www.mongodb.com/cloud/atlas?lang=es-es) y posteriormente analizarlos en una instancia EC2 de AWS utilizando el framework de [TensorFlow](https://www.tensorflow.org/).

En las carpetas *server-side* y *client-side* se encuentran los scripts escritos en Python que realizan la transmisión de la información haciendo uso del protocolo MQTT y se deben cambiar los archivos de configuración (config.json, configDB.json) con los valores propios de cada entorno, previamente se debe tener configurado el servicio de [AWS IoT Core](https://aws.amazon.com/es/iot-core/).

Los scripts de transmisión _del lado del cliente_ han sido probados en entornos Windows y Raspbian. Los scripts de transmisión del lado del servidor han sido probados en entornos Linux y Windows.

En el archivo **requirements.txt** podrá encontrar las librerías adicionales de Python que deben ser instaladas.

Versión de Pyhton > 3.6.x
