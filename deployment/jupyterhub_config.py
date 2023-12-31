# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub

import os

c = get_config()  # noqa: F821


#c.Spawner.cmd = ['sudo', '-E', 'start-singleuser.sh']

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"


# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.

notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jupyter/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Montar los volumenes de cada usuario en la máquina local, puedes cambiar /home por otra ruta (solo acepta rutas absolutas)
#c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}
c.DockerSpawner.volumes = {"/home/jupyterhub-volumes/jupyterhub-user-{username}": notebook_dir}

## Default URL

c.JupyterHub.default_url = "/hub/home"

## Templates
c.JupyterHub.default_lang = 'es'  # Reemplaza 'es' con el código del idioma que desees (por ejemplo, 'en' para inglés).


c.JupyterHub.template_paths = ['/usr/local/share/jupyterhub/templates']
c.JupyterHub.template_paths = ['/usr/local/share/jupyterhub/static']
#c.JupyterHub.template_vars = {'custom_login_template': 'login.html'}

# Fuentes

c.NotebookApp.font_family = 'Arial, sans-serif'
c.NotebookApp.font_size = 14


# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = True

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]
