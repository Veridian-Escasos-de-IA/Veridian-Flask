# Veridian — Backend (Flask) + Frontend (React/Vite)

Guía rápida para que todo el equipo pueda **clonar**, **configurar** y **ejecutar** el proyecto con buenas prácticas de entornos, ramas y *pull requests*.

> **Stack:** Flask 3.x (API), React 18 + Vite, Node 20 LTS, Python 3.11+

---

## 🧱 Estructura del repo (monorepo)

```
Veridian-Flask-React/
├── backend/                  # API Flask
│   ├── app/                  # blueprints, models, etc.
│   ├── requirements.txt
│   ├── .env.example
│   └── main.py               # punto de entrada
├── frontend/                 # Web (React + Vite)
│   ├── src/
│   ├── package.json
│   ├── .env.example
│   └── index.html
├── .github/workflows/        # CI (opcional)
└── README.md
```

---

## ✅ Requisitos

- **Git** 2.40+
- **Python** 3.11+ (recomendado 3.11.x)
- **Node.js** 20 LTS (usa `nvm` si puedes)
- **Pip** / **venv**
- **Make** (opcional, Linux/Mac) ó PowerShell (Windows)

### Versiones recomendadas
```bash
python --version
node -v
npm -v
```

> En Windows: usa **PowerShell**. En Linux/Mac: usa **bash/zsh**.

---

## 🚀 Quick Start (todo el repo)

```bash
# 1) Clonar
git clone <URL_DEL_REPO.git>
cd Veridian-Flask-React

# 2) Levantar backend y frontend (ver detalles abajo)
# Backend (en otra terminal): cd backend && ...
# Frontend (en otra terminal): cd frontend && ...
```

---

# 🐍 Backend (Flask)

### 1) Crear entorno virtual

**Linux/Mac**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Variables de entorno

Copia el ejemplo y ajusta tus valores:

```bash
cp .env.example .env
```

`.env.example` (referencia):
```
# Flask
FLASK_ENV=development
SECRET_KEY=change_me_please

# CORS
CORS_ORIGINS=http://localhost:5173

# Base de datos (elige una)
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/veridian
# DATABASE_URL=sqlite:///veridian.db

# JWT (si aplica)
JWT_SECRET_KEY=change_me_too

# Otros
PORT=8000
```

> Si usas **PostgreSQL**, asegúrate de tenerlo corriendo y con la DB creada.

### 3) Ejecutar en desarrollo

```bash
# Estando en backend con el venv activado
python main.py
# o, si tienes un script CLI:
# flask --app app/app.py run --debug --port=8000
```

La API por defecto escuchará en `http://localhost:8000` (ajustable con `PORT`).

### 4) Migraciones / Base de datos (opcional)

Si usas **Flask-Migrate / Alembic**:
```bash
flask db upgrade      # aplica migraciones
flask db migrate -m "mensaje"
flask db downgrade    # revertir
```

### 5) Pruebas y lint

```bash
pytest -q
ruff check .     # o flake8/black según convenga
```

> Recomendado: **pre-commit** para formatear y lint automático.

---

# ⚛️ Frontend (React + Vite)

### 1) Instalar dependencias

**Con npm** (o usa pnpm/yarn si el repo lo estandariza):
```bash
cd ../frontend
npm ci   # o npm install
```

> **Node 20 LTS** recomendado. Si usas `nvm`:
```bash
nvm install 20
nvm use 20
```

### 2) Variables de entorno

Copia el ejemplo y ajusta la URL de la API:

```bash
cp .env.example .env
```

`.env.example` (referencia):
```
VITE_API_URL=http://localhost:8000
```

### 3) Ejecutar en desarrollo

```bash
npm run dev
```
Vite abrirá `http://localhost:5173`.

### 4) Build y preview

```bash
npm run build
npm run preview
```

### 5) Lint / Formato

```bash
npm run lint
npm run format
```

---

## 🔗 Conexión Frontend ↔ Backend

- El frontend lee `VITE_API_URL` para apuntar a la API.
- Asegura **CORS** en el backend (`CORS_ORIGINS=http://localhost:5173` por defecto).

---

## 🔐 Entornos

- **Desarrollo**: `.env` locales, ejecutar con hot reload.
- **Producción**: variables en el servidor/CI, nunca subir secretos.

---

# 🌿 Git Flow con Pull Requests

### Ramas
- `main` → producción (estable, versionada).
- `dev` → integración (merge de features).
- `feature/<tarea>` → trabajo diario desde `dev`.
- `hotfix/<bug>` → sale desde `main`.

### Primer setup
```bash
git checkout main && git pull origin main
git checkout -b dev
git push -u origin dev
```

### Trabajo diario
```bash
git checkout dev && git pull
git checkout -b feature/login
# ... commits ...
git push -u origin feature/login
```
- Abrir **PR: feature/login → dev**.
- Al preparar release: **PR: dev → main** (o `release/x.y.z → main`).  
- Hotfix urgente: `hotfix/* → main`, luego **merge back: main → dev**.

### Protecciones de rama (GitHub → Settings → Branches → Add rule)
- `main` (y opcional `dev`):
  - ✅ Require a pull request before merging
  - ✅ Require approvals (≥1)
  - ✅ Require status checks to pass (CI)
  - ✅ Restrict who can push (bloquear push directo)

---

## 🤝 Convenciones de equipo

- **Conventional Commits**: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`…
- **PR template** (añade en `.github/pull_request_template.md`):
  ```md
  ## Descripción
  <!-- Qué cambia y por qué -->

  ## Cómo probar
  <!-- Pasos, datos de prueba -->

  ## Checklist
  - [ ] Lint/Tests OK
  - [ ] Sin secretos en el diff
  - [ ] Docs/ENV actualizados si aplica
  ```
- **Codeowners** en `.github/CODEOWNERS` para revisores por carpeta.

---

## 🛠️ Troubleshooting rápido

- **No levanta Flask / “ModuleNotFoundError”**: activa el venv y revisa `PYTHONPATH`/imports relativos; confirma `pip install -r requirements.txt`.
- **CORS**: revisa `CORS_ORIGINS` y `VITE_API_URL`.
- **Node/ESLint**: usa Node 20 LTS; elimina `node_modules` y `npm ci` si hay conflictos.
- **.env**: nunca lo subas; usa `.env.example` como plantilla.

---

## 📦 Scripts útiles (opcional)

**Linux/Mac `Makefile`:**
```makefile
backend-venv:
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

backend-run:
	cd backend && . .venv/bin/activate && python main.py

frontend-deps:
	cd frontend && npm ci

frontend-dev:
	cd frontend && npm run dev
```

**Windows (PowerShell) – `scripts/dev.ps1`:**
```powershell
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\main.py
```

---

## 📜 Licencia

Este proyecto es de uso interno/educativo. Ajusta esta sección según corresponda (MIT/GPL/Propietaria).