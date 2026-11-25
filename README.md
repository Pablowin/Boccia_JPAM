# Boccia_JPAM

## Ejecutar la aplicación

Instala las dependencias y arranca Streamlit desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
streamlit run app\Inicio.py
```

La pantalla **Inicio** da acceso a las distintas secciones. En **Reglamento** se
muestra el PDF español `World-Boccia-Rules-2025-2028-v1.1-Spanish-Spain.pdf`.
La aplicación lo busca en `docs`, `data/raw` y la carpeta `Downloads` del
usuario; si no está en esas ubicaciones, permite cargarlo desde la propia
pantalla. El PDF se visualiza en la aplicación y no se copia al repositorio.