README - Proyecto Visiona

Requisitos de Instalacion:
	1. Instalar Python
	2. Instalar MongoDB
	3. Crear entorno virtual
	4. Instalar Django y otras librerias en el entorno virtual
	5. Migrar el proyecto y crear un superusuario
	6. Instalar VMWare
	7. Crear maquina virtual con Mininet
	8. Crear maquina virtual con Ubuntu 14
	9. Instalar OpenDayLight (ODL) en la maquina virtual de Ubuntu	

PASO 1: Instalar Python
	Se debe utilizar la version 3.6 o superior
	Enlace de descarga: https://www.python.org/downloads/
	
	En mi caso, he utilizado la version 3.6
	Enlace de descarga: https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe
	IMPORTANTE: Al instalar aceptar la opción "Añadir Python 3.6 al PATH"

PASO 2: Instalar MongoDB
	Se debe utilizar la version 3.6 o superior
	Enlace de descarga: https://www.mongodb.com/try/download/community
	IMPORTANTE: Al descargar escoger el tipo de paquete MSI (mejor que el ZIP)
	
	En mi caso, he utilizado la version 4.4.2 para Windows
	Enlace de descarga: https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.3-signed.msi
	
	Para instalar MongoDB en Windows, les dejo el siguiente enlace
	Manual de instalacion: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
	IMPORTANTE: Para hacer funcionar MongoDB es necesario crear un directorio "data/db"
		En mi caso lo he creado en C:\data\db

PASO 3: Crear entorno virtual
	Abrir un terminal y seguir los siguientes pasos:
		1. Instalar virtualenv
			Comando: python -m pip install virtualenv
		2. Comprobar que virtualenv se ha instalado
			Comando: python -m pip freeze
		3. Crear un entorno virtual llamado "django_venv"
			Comando: python -m venv django_venv
	En mi caso, al utilizar Windows, un terminal puede ser CMD o PowerShell

PASO 4: Instalar Django y otras librerias en el entorno virtual
	Se debe utilizar la version 2.1.2 de Django
	Abrir un terminal y seguir los siguientes pasos:
		1. Ir a la siguiente ruta del entorno virtual: django_venv\Scripts
			Comando: cd .\django_venv\Scripts
		2. Activar el entorno virtual
			Comando: activate
		3. Instalar Django (y otras librerias necesarias como Djongo)
			Comandos:
				- pip install django==2.1.2
				- pip install djongo
				- pip install djangorestframework==3.7.2
				- pip install simplejson
		4. Comprobar librerias instaladas
			Comando: pip freeze
			El resultado debe ser como este:
				dataclasses==0.8
				Django==2.1.2
				djangorestframework==3.7.2
				djongo==1.3.3
				pymongo==3.11.2
				pytz==2020.5
				simplejson==3.17.2
				sqlparse==0.2.4

PASO 5: Migrar el proyecto y crear un superusuario
	Abrir un terminal y seguir los siguientes pasos:
		1. Descargar el proyecto de Github
			Comando: git clone https://github.com/rubenamador/ProyectoVisiona.git
		2. Activar el entorno virtual
			Comandos: 
				- cd .\django_venv\Scripts
				- activate
		3. Ir a la ruta del proyecto Visiona (contiene el fichero "manage.py")
			Comando: cd .\ProyectoVisiona
		4. Ejecutar MongoDB
			Comandos:
				- cd C:\Program Files\MongoDB\Server\4.4\bin
				- mongod
				IMPORTANTE: Dejar la terminal abierta para configurar la aplicacion en Django
		5. Migrar el proyecto
			Comandos:
				- cd .\ProyectoVisiona
				- manage.py makemigrations
				- manage.py migrate
		6. Crear un superusuario
			Comandos:
				- manage.py createsuperuser
				- manage.py runserver
				IMPORTANTE: Introducir credenciales en la siguiente URL
					URL: http://127.0.0.1:8000/admin/
		7. Desactivar el entorno virtual
			Comandos: 
				- cd .\django_venv\Scripts
				- deactivate

PASO 6: Instalar VMWare
	Se ha utilizado la version 15.5.7 de VMWare
	Enlace de descarga: https://my.vmware.com/en/web/vmware/free#desktop_end_user_computing/vmware_workstation_player/15_0
	
PASO 7: Crear maquina virtual con Mininet
	Se ha utilizado la version 2.2.2 para Ubuntu 14.04 
	Enlace de descarga: https://github.com/mininet/mininet/releases/download/2.2.2/mininet-2.2.2-170321-ubuntu-14.04.4-server-i386.zip
	
	Tras descargar Mininet, abrir VMWare y seguir los siguientes pasos:
		1. Descomprimir el ZIP descargado de la Mininet
		2. Crear maquina virtual de Mininet
			Pulsar en 'Open a Virtual Machine'
			Seleccionar el paquete OVF descomprimido de la Mininet

PASO 8: Crear maquina virtual con Ubuntu
	Se ha utilizado la version 14.04 de Ubuntu
	Enlace de descarga: https://releases.ubuntu.com/trusty/ubuntu-14.04.6-desktop-amd64.iso
	
	Tras descargar Ubuntu, abrir VMWare y seguir los siguientes pasos:
		1. Crear maquina virtual de Ubuntu
			Pulsar en 'Create a New Virtual Machine'
			Importar la imagen ISO descargada de Ubuntu

PASO 9: Configurar maquina virtual de Ubuntu para OpenDayLight
	Abrir VMWare y seguir los siguientes pasos:
		1. Abrir la maquina virtual de Ubuntu
		2. Abrir un terminal y descargar ODL (OpenDayLight)
			Comandos:
				- wget https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.4.2-Beryllium-SR2/distribution-karaf-0.4.2-Beryllium-SR2.zip
				- unzip distribution-karaf-0.4.2-Beryllium-SR2.zip
				- mv distribution-karaf-0.4.2-Beryllium-SR2 ODL
		3. Abrir un terminal e instalar Java, Nmap y SSH
			Comandos:
				- sudo apt-get update
				- sudo apt-get install openjdk-7-jdk
				- sudo apt-get install nmap
				- sudo apt-get install openssh-server
		4. Abrir una terminal para ODL
			Comandos: 
				- cd ./ODL/bin/
				- ./karaf -of13
		5. Instalar los siguientes features
			Comandos:
				- feature:install odl-l2switch-all
				- feature:install odl-dlux-all
				- feature:install odl-restconf
				
	URL TUTORIAL ODL CON MININET: https://www.youtube.com/watch?v=K5E6_eik23k

Pasos de Uso:
	1. Ejecutar MongoDB
	2. Correr servidor de Django
	3. Abrir la maquina virtual de Mininet
	4. Generar una red con OpenDayLight en la maquina virtual de Ubuntu
	5. Importar una red generada en la Mininet con OpenDayLight

PASO 1: Ejecutar MongoDB
	Abrir un terminal y seguir los siguientes pasos:
		1. Ir a la ruta donde se instalo MongoDB
			Ejemplo: C:\Program Files\MongoDB\Server\4.4
		2. Ir al directorio "bin" de MongoDB 
			Comando: cd C:\Program Files\MongoDB\Server\4.4\bin
		3. Ejecutar MongoDB
			Comando: mongod
			IMPORTANTE: Dejar la terminal abierta para levantar la aplicacion en Django

PASO 2: Correr servidor de Django
	Abrir un terminal y seguir los siguientes pasos:
		1. Activar el entorno virtual
			Comandos: 
				- cd .\django_venv\Scripts
				- activate
		2. Ir a la ruta del proyecto Django (contiene el fichero "manage.py")
			Comando: cd .\ProyectoVisiona
		3. Correr el servidor de Django
			Comando: manage.py runserver
			Por defecto, te devuelve una URL (http://127.0.0.1:8000/)
		4. Abrir un navegador web (como Google Chrome)
		5. Introducir las credenciales del superusuario
			URL: http://127.0.0.1:8000/admin/
		6. Navegar por la aplicacion
			URL: http://127.0.0.1:8000/
			
PASO 3: Abrir la maquina virtual de Mininet
	Abrir VMWare y seguir los siguientes pasos:
		1. Abrir maquina virtual de Mininet
		2. Introducir credenciales	
			Usuario: mininet
			Contraseña: mininet
		3. Buscar direccion IP de la maquina Mininet
			Comando: ifconfig eth0
			En mi caso, la ip es 192.168.38.129

PASO 4: Generar una red con OpenDayLight en la maquina virtual de Ubuntu
	Abrir VMWare y seguir los siguientes pasos:
		1. Abrir la maquina virtual de Ubuntu
		2. Abrir una terminal para ODL (Terminal 1)
			Comandos: 
				- cd ./ODL/bin/
				- ./karaf -of13
			IMPORTANTE: Dejar la terminal abierta para generar la aplicacion en Django
		3. Abrir una terminal para Mininet (Terminal 2)
			Buscar direccion IP de la maquina Ubuntu
				Comando: ifconfig
				En mi caso, la ip es 192.168.38.128
			Conectar a mininet por ssh
				Comando: ssh -X mininet@192.168.38.129
			Crear topología en mininet
				Ejemplo (topologia tipo-arbol): sudo mn --controller=remote,ip=192.168.38.128 --topo=tree,4,4
				Ejemplo (topologia tipo-lineal): sudo mn --controller=remote,ip=192.168.38.128 --topo=linear,4
				Ejemplo (topologia tipo-single): sudo mn --controller=remote,ip=192.168.38.128 --topo=single,3
			Se pueden crear nuevas topologias, siguiendo los modelos en la carpeta /mininet/custom
				Tutorial: http://mininet.org/walkthrough/
				Ejemplo (topologia personalizada): sudo mn --controller=remote,ip=192.168.38.128 --custom ~/mininet/custom/custom_topology.py --topo mytopo
	Abrir un navegador fuera de la maquina virtual (por ejemplo, Google Chrome)
		1. Ir a la siguiente URL: http://192.168.38.128:8181/index.html
		2. Introducir credenciales
			Usuario: admin
			Contraseña: admin

PASO 5: Importar una red generada en la Mininet con OpenDayLight
	Abrir la aplicacion en Django desde un navegador (como Google Chrome)
	URL: http://127.0.0.1:8000/nodes/listNode
	
	Seguir los siguientes pasos:
		1. Seleccionar la opcion "Obtener json de URL"
		2. Seleccionar la opcion "Importar json"
		3. Visualizar en la siguiente vista
			URL: http://127.0.0.1:8000/links/graphLink
