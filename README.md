# Oficinas ABAI — FastAPI + Scraper + DEPLOY +Worker programado
crud basico para oficinas de abai prueba tecnica


## ¿Qué es este proyecto?
Este proyecto resuelve una tarea muy concreta:

1. **Extraer (scrapear)** las oficinas publicadas en  
   https://www.abaigroup.com/donde-encontrarnos/
2. **Guardar** esa información en una “tabla” llamada `oficinas` (SQLite).
3. Exponerlo por una **API REST** (FastAPI):
   - `GET /oficinas` (con filtros por `pais` y/o `ciudad`)
   - `POST /oficinas` (para insertar oficinas)
4. Incluir un proceso automatizado (**worker**) que ejecute el scraping cada cierto intervalo configurable.

---

## URL de acceso (producción)
**API en Render:**  
`https://oficinasabai.onrender.com`

Endpoints principales:
- `GET  https://oficinasabai.onrender.com/health`
- `GET  https://oficinasabai.onrender.com/oficinas?pais=Colombia`
- `GET  https://oficinasabai.onrender.com/oficinas?ciudad=Bogota`
- `POST https://oficinasabai.onrender.com/oficinas` *(requiere token y rol writer/admin)*
- `POST https://oficinasabai.onrender.com/auth/token` *(login)*
- `POST https://oficinasabai.onrender.com/admin/scrape/run` *(dispara scraping manual; requiere admin)*

Documentación Swagger:
- `https://oficinasabai.onrender.com/docs`

---

## Parámetros de entrada necesarios
### 1) Autenticación (JWT)
Para ejecutar endpoints protegidos necesito obtener un token:

**Request**
`POST /auth/token`  
`Content-Type: application/x-www-form-urlencoded`

Campos:
- `username`
- `password`

**Ejemplo**
```bash
curl -X POST "https://oficinasabai.onrender.com/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ADMIN_USER&password=ADMIN_PASS"