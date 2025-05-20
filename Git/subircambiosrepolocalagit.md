## Subir cambios del repositorio local al repositorio de gitlab
```console
git config --global user.name "ramalave"
git config --global user.email "ramalave@ramalave.com.ar"
git init
git status
git add .
git commit -m "Comentario del commit a subir"
git push
git tag -a v1.4 -m 'mi version 1.4'
```

## Primer commit en GitHub
```console
git init
git add .
git config --global user.name "Rafael Malavé"
git config --global user.email "ramalave@ramalave.com.ar"
git commit -m "Mi primer commit"
git remote add origin https://github.com/NOMBRE_USUARIO/NOMBRE_PROYECTO.git
git push -u origin master
```