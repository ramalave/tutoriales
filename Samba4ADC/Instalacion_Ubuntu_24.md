# Instalación de Directorio activo basado en Samba en Ubuntu 24.04
## Introducción
Estaba en la búsqueda de un Directorio Activo basado en open-source para sustituir el AD de Windows, cabe a destacar,
que la iniciativa nace en la necesidad de adquiir un componente que cumpla los requisitos de Directorio Activo,
cojuntmante con servidor de dominios usando las herramientas administrativas que proporciona Windows, de esta
forma se puede configurar usando las mismas reglas del AD de Windows.

## Prerrequisito
* Servidor Ubuntu (22.04/24.04)
* Una cuenta de usuario con privilegios de sudo, en nuestro caso 
* Una computadora con Windows 10 o 11 PRO en la misma red
* Un escritorio Linux en el mismo servidor (basado en Fedora o Ubuntu)

En este ejemplo, se usará Ubuntu 24.04 Server para Active Directory. Nos conectaremos a él con un cliente Windows 10 PRO y Ubuntu server como cliente basado en Linux.

## Configuración del servidor de CC
### Establecer el nombre de host del servidor
Para esta demostración, utilizaremos el nombre de host adc para el servidor Ubuntu.

```console
# set up the hostname
hostnamectl set-hostname adc
```
### Agregar servidor al archivo Hosts
También necesitaremos modificar el archivo hosts, agregar la siguiente línea a:
```
/etc/hosts
```

### Configure FQDN adc.ramalave.ar

```console
172.28.25.55 adc.ramalave.ar adc
```

### Verificar nombre de host
Puedes verificar rápidamente que todo funcionó con el siguiente comando

```console
# Verificando FQDN
hostname -f
 
# Verificando FQDN si resuelve a la dirección IP de Samba
ping -c3 adc.ramalave.ar
```

## Deshabilitar el solucionador de DNS
### Deshabilitar el solucionador DNS y desvincular la configuración

```console
# Parando y desactivando systemd-resolved service
sudo systemctl disable --now systemd-resolved
 
# Removiendo el archivo del enlace simbólico /etc/resolv.conf
sudo unlink /etc/resolv.conf
```

### Crea nuestro propio Resolv.conf
```console
# Crea un nuevo archivo /etc/resolv.conf
touch /etc/resolv.conf
```

### Introduzca lo siguiente en /etc/resolv.conf
```console
# Servidor Samba dirección IP
nameserver 172.28.25.55
 
# DNS fallback o secundario
nameserver 1.1.1.1
 
# Servidor principal de samba
search ramalave.ar
```

### Hace que el archivo no se sobreescriba
Como no queremos que nada cambie este archivo automáticamente, lo hacemos que no sobreescriba para que no se modifique.

# Añade el atributo que no sobreescriba a /etc/resolv.conf
```console
sudo chattr +i /etc/resolv.conf
```

## Instalando Samba
```console
sudo apt update
sudo apt install -y acl attr samba samba-dsdb-modules samba-vfs-modules smbclient winbind libpam-winbind libnss-winbind libpam-krb5 krb5-config krb5-user dnsutils chrony net-tools
```

### Ingrese la información apropiada
```console
# Default Kerberos Version 5 Realm:
ramalave.ar
 
# Kerberos Servers for your realm:
ramalave.ar
 
# Administrative server for your Kerberos realm:
acd.ramalave.ar
```

## Desactivando servicios de Samba
```console
# Parando y desactivando servicios de samba - smbd, nmbd, and winbind
sudo systemctl disable --now smbd nmbd winbind
```

## Activate `samba-ad-dc`
```console
# Activando servicio samba-ad-dc
sudo systemctl unmask samba-ad-dc
 
# Habilitando servicio samba-ad-dc service
sudo systemctl enable samba-ad-dc
```

## Configuring Directorio Activo de Samba
Primero haga una copia de seguridad del archivo smb.conf original
```console
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.bak
```

### Aprovisionar el Directorio Activo
```console
# Aprovisionamiento del Directorio Activo de Samba
sudo samba-tool domain provision
```

Ingrese la siguiente información
-------------------------------
1. On Realm prompte – <Enter>
2. On Domian Promp – <Enter>
3. On Server Roll – <Enter>
4. On DNS Backend – <Enter>
5. DNS Forwarding IP – 1.1.1.1
6. Enter an Admin Password

### Realice una copia de seguridad y reemplace la configuración de Kerberos
```console
# Realice una copia del archivo original de krb5.conf.orig
sudo mv /etc/krb5.conf /etc/krb5.conf.orig
 
# Copiar la configuración de Kerberos generada por la herramienta samba
sudo cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
```

### Iniciar samba-ad-dc
```console
# Iniciando el servicio de samba-ad-dc
sudo systemctl start samba-ad-dc
 
# Verificando el servicio samba-ad-dc
sudo systemctl status samba-ad-dc
```

## Configurar la sincronización horaria
### Establecer permisos
```console
# Permitir que el grupo _chrony lea el directorio ntp_signd
sudo chown root:_chrony /var/lib/samba/ntp_signd/
 
# Cambiar el permiso del directorio ntp_signd
sudo chmod 750 /var/lib/samba/ntp_signd/
```

### Actualizar Chrony
Agregue lo siguiente a /etc/chrony/chrony.conf
```console
# Vincular el servicio chrony a la dirección IP del AD Samba
bindcmdaddress 172.28.25.55
 
# Permitir que los clientes de la red se conecten al servidor NTP de Chrony
allow 10.20.20.0/24
 
# Permitir que los clientes de la red se conecten al servidor NTP de Chrony
ntpsigndsocket /var/lib/samba/ntp_signd
```

### Luego reinicia Chrony y obtén su estado.
```console
# Reiniciamos el servicio chronyd
sudo systemctl restart chronyd
 
# Verificamos el estado del servicio chronyd
sudo systemctl status chronyd
```

## Verificación de Samba Active Directory
### Ejecute lo siguiente para verificar
```console
# Verificando el dominio ramalave.ar
host -t A ramalave.ar
 
# Verficiando el subdominio adc.ramalave.ar
host -t A .adc.ramalave.ar
```

## Luego verifique los servicios Kerberos y ldap
```console
# Verificar el registro SRV para _kerberos
host -t SRV _kerberos._udp.ramalave.ar
 
# Verificar registro SRV para _ldap
host -t SRV _ldap._tcp.ramalave.ar
```

## Luego verifique los recursos de Samba
```console
# Verificar registro SRV para _kerberos
host -t SRV _kerberos._udp.ramalave.ar
 
# Verificar el registro SRV para _ldap
host -t SRV _ldap._tcp.ramalave.ar
```

## Último KINIT
```console
# Autenticarse en Kerberos mediante el administrador (DEBE ESTAR EN MAYÚSCULAS)
kinit administrator@RAMALAVE.AR
 
# Verificar la lista de tickets Kerberos almacenados en caché
klist
```

## Crea tu primer usuario (Opcional)
La razón por la que esto es opcional es que tienes más opciones al agregar un usuario a través de las Herramientas de administración del servidor remoto (RSAT) en Windows.
```console
# Crea un nuevo usaurio en Smaba
sudo samba-tool user create rmalave
 
# Reviando los usuarios en Samba
sudo samba-tool user list
```

## Configuración de Windows
Comprobación previa
------------------
1. Establecer el nombre de la computadora
2. Configurar DNS/IP. El primer DNS debe ser el servidor Samba configurado anteriormente.

## Verificar el solucionador de DNS
```powershell
# En Powershell
Get-DnsClientServerAddress
 
# ping the AD domain adc.ramalave.ar
ping adc.ramalave.ar
 
# ping the AD domain ramalave.ar
ping ramalave.ar
```

## Agregar servidor al ADC
```powershell
# En Powershell
# Agregar Windows 10/11 en el Active Directory usando POWERSHELL
Add-Computer -DomainName "ramalave.ar" -Restart
```

After restart login as domain user

## Instalar RSAT para administrar el dominio desde Windows
[Descargar herramientas RSAT](https://www.microsoft.com/en-us/download/details.aspx?id=45520) <– Para Windows 11

La otra opcion es ir a Características opciones en Configuracion de sistemas, en agregar característica opcional y en el recuadro de búsqueda escribir RSAT,
te va a mostrar todas las herramientas vinculadas y seleccionar todas e instalar, para tener el acceso total a las herramientas.

## Configuración en Linux
### Prechequeo
En Ubuntu, usted necesita agregar los repositorios universales
```console
sudo add-apt-repository universe
sudo add-apt-repository multiverse
sudo apt update
```

## Establecer nombre de host
```console
sudo hostnamectl set-hostname neo.ramalave.ar
```

## Modifique la info de su Resolv
Necesita cambiar la configuración en /etc/resolv.conf file
```console
nano /etc/systemd/resolved.conf
 
#Agrega lo siguiente
[Resolve]
DNS=172.28.25.55 1.1.1.1 8.8.8.8
 
sudo systemctl restart systemd-resolved
```

## Instalar los paquetes necesarios (sólo Ubuntu)
### Para Ubuntu solamente
```console
sudo apt -y install realmd libnss-sss libpam-sss sssd sssd-tools adcli samba-common-bin oddjob oddjob-mkhomedir packagekit
```

## Descubra el dominio (Opcional)
```console
sudo realm discover ramalave.ar
```

## Únete al dominio
```console
sudo realm join -U Administrator ramalave.ar
```

Reinicie y podrá iniciar sesión como usuario del dominio.

Fuente: [Samba Based Active Directory on Ubuntu 22.04](https://www.considerednormal.com/2022/11/samba-based-active-directory-on-ubuntu-22-04/)
