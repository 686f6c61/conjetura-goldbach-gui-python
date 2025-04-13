#!/bin/bash

#######################################################################
# Script de inicialización para la aplicación de Conjetura de Goldbach
#
# Este script automatiza el proceso de configuración del entorno y
# ejecución de la aplicación. Realiza las siguientes tareas:
# 1. Detecta la versión de Python disponible en el sistema
# 2. Verifica las dependencias necesarias
# 3. Crea y configura un entorno virtual aislado
# 4. Instala las dependencias requeridas
# 5. Ejecuta la aplicación
#
# Autor: https://github.com/686f6c6
# Fecha: 2025-04-13
#######################################################################

# Detección inteligente de la versión de Python
# Primero intentamos con python3, luego con python (verificando que sea 3.x)
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    # Extraemos la versión principal de Python y verificamos que sea 3.x
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d '.' -f 1)
    if [ "$PYTHON_VERSION" -eq 3 ]; then
        PYTHON_CMD="python"
    else
        echo "Se requiere Python 3.x para ejecutar esta aplicación."
        echo "Por favor, instale Python 3.x y vuelva a intentarlo."
        exit 1
    fi
else
    echo "No se encontró Python. Por favor, instale Python 3.x y vuelva a intentarlo."
    exit 1
fi

echo "Usando $PYTHON_CMD para ejecutar la aplicación..."

# Verificación de dependencias del sistema
# Tkinter es una dependencia crítica para la interfaz gráfica
# Intentamos importar tkinter y proporcionamos instrucciones específicas por distribución si falla
echo "Verificando dependencias del sistema..."
$PYTHON_CMD -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter no está instalado. Es necesario para la interfaz gráfica."
    echo "En sistemas basados en Debian/Ubuntu, instale con: sudo apt-get install python3-tk"
    echo "En sistemas basados en Fedora/RHEL, instale con: sudo dnf install python3-tkinter"
    echo "En sistemas basados en Arch, instale con: sudo pacman -S tk"
    exit 1
fi

# Configuración de rutas y entorno
# Obtenemos la ruta absoluta del directorio del script para garantizar
# que todas las operaciones se realicen en el directorio correcto,
# independientemente de dónde se invoque el script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Configuración del entorno virtual
# Utilizamos un entorno virtual para aislar las dependencias de la aplicación
# del entorno global de Python, evitando conflictos de versiones
VENV_NAME="venv"

# Detección y reparación de entornos virtuales corruptos
# Verificamos si el directorio del entorno virtual existe pero los archivos
# de activación no están presentes, lo que indica un entorno corrupto
if [ -d "$VENV_NAME" ] && ! [ -f "$VENV_NAME/bin/activate" ] && ! [ -f "$VENV_NAME/Scripts/activate" ]; then
    echo "Entorno virtual corrupto detectado. Eliminando..."
    rm -rf "$VENV_NAME"
fi

# Creación del entorno virtual con manejo de fallos
# Si el módulo venv falla (común en algunas distribuciones), intentamos con virtualenv
# Este enfoque de degradación elegante garantiza la máxima compatibilidad entre sistemas
if [ ! -d "$VENV_NAME" ]; then
    echo "Creando entorno virtual..."
    $PYTHON_CMD -m venv $VENV_NAME
    if [ $? -ne 0 ]; then
        echo "Error al crear el entorno virtual. Intentando con virtualenv..."
        # Estrategia de fallback: intentar con virtualenv si venv falla
        # Primero verificamos si pip3 está disponible, luego pip
        if command -v pip3 &>/dev/null; then
            pip3 install virtualenv
            $PYTHON_CMD -m virtualenv $VENV_NAME
        elif command -v pip &>/dev/null; then
            pip install virtualenv
            $PYTHON_CMD -m virtualenv $VENV_NAME
        else
            echo "No se pudo crear el entorno virtual. Asegúrese de tener instalado pip o virtualenv."
            exit 1
        fi
    fi
fi

# Activación del entorno virtual con compatibilidad multiplataforma
# Detectamos automáticamente la ubicación del script de activación según el sistema operativo
# Soportamos tanto sistemas Unix/Linux (/bin/activate) como Windows (/Scripts/activate)
if [ -f "$VENV_NAME/bin/activate" ]; then
    source "$VENV_NAME/bin/activate"
elif [ -f "$VENV_NAME/Scripts/activate" ]; then
    # Para entornos Windows (útil en WSL o MSYS2/Git Bash)
    source "$VENV_NAME/Scripts/activate"
else
    echo "No se pudo activar el entorno virtual."
    exit 1
fi

# Actualización de herramientas de gestión de paquetes
# Actualizamos pip para evitar problemas de compatibilidad con paquetes más recientes
echo "Actualizando pip..."
pip install --upgrade pip

# Instalación de dependencias desde el archivo de requisitos
# El archivo requirements.txt contiene todas las dependencias necesarias
# con sus versiones específicas para garantizar la reproducibilidad del entorno
echo "Instalando dependencias..."
pip install -r requirements.txt

# Verificación post-instalación de dependencias críticas
# Comprobamos que las bibliotecas esenciales se hayan instalado correctamente
# Si la verificación falla, intentamos una instalación manual como fallback
echo "Verificando instalación de dependencias..."
$PYTHON_CMD -c "import matplotlib, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: No se pudieron instalar todas las dependencias correctamente."
    echo "Intentando instalación manual de dependencias críticas..."
    pip install matplotlib numpy
fi

# Ejecución de la aplicación principal
# Iniciamos la aplicación desde el punto de entrada principal (main.py)
echo "Iniciando la aplicación de Conjetura de Goldbach..."
python main.py

# Limpieza del entorno
# Desactivamos el entorno virtual para restaurar el entorno Python original
# Esto es importante para evitar conflictos si se ejecutan otros scripts de Python
deactivate
