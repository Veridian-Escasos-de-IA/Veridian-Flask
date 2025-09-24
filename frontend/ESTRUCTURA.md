# Estructura del Proyecto Frontend

Este proyecto utiliza una arquitectura moderna y escalable basada en features y componentes compartidos.

## 📁 Estructura de Directorios

```
src/
├── assets/                 # Recursos estáticos (imágenes, iconos, etc.)
├── context/               # Context providers de React
├── features/              # Funcionalidades organizadas por módulos
│   ├── auth/             # Autenticación
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── LoginForm.jsx
│   │   ├── RegisterForm.jsx
│   │   └── index.js
│   └── dashboard/        # Dashboard principal
│       ├── Dashboard.jsx
│       └── index.js
├── pages/                 # Páginas principales y punto de entrada
│   ├── HomePage.jsx
│   └── index.js
├── services/             # Servicios para API calls
├── shared/               # Código compartido entre features
│   ├── components/       # Componentes reutilizables
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── Layout.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── index.js
│   ├── hooks/           # Custom hooks compartidos
│   │   ├── useAuth.js
│   │   └── index.js
│   ├── utils/           # Utilidades y constantes
│   │   ├── constants.js
│   │   └── index.js
│   └── index.js
├── App.jsx              # Componente raíz
├── main.jsx             # Punto de entrada
├── App.css              # Estilos globales
└── index.css            # Estilos base con Tailwind
```

## 🏗️ Principios de Arquitectura

### **1. Feature-Based Organization**
- Cada feature contiene todos sus componentes, páginas y lógica relacionada
- Facilita el desarrollo en equipo y la escalabilidad
- Reduce acoplamiento entre diferentes funcionalidades

### **2. Shared Resources**
- Componentes reutilizables en `shared/components`
- Hooks personalizados en `shared/hooks`
- Utilidades y constantes en `shared/utils`

### **3. Clean Imports**
- Cada directorio tiene un archivo `index.js` para exports organizados
- Imports limpios usando destructuring
- Evita imports relativos profundos

## 📝 Convenciones de Nomenclatura

### **Archivos y Componentes**
- Componentes: `PascalCase.jsx` (ej: `LoginPage.jsx`)
- Hooks personalizados: `camelCase.js` con prefijo `use` (ej: `useAuth.js`)
- Utilidades: `camelCase.js` (ej: `constants.js`)

### **Exports/Imports**
```javascript
// ✅ Correcto - Usar exports nombrados
export { LoginPage, RegisterPage } from '../features/auth';

// ✅ Correcto - Import limpio
import { LoginPage, ProtectedRoute } from './pages';

// ❌ Evitar - Imports relativos profundos
import LoginPage from '../../../features/auth/LoginPage';
```

## 🚀 Comandos de Desarrollo

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Compilar para producción
npm run build

# Previsualizar build de producción
npm run preview
```

## 🔧 Tecnologías Utilizadas

- **React 19** - Biblioteca principal
- **Vite** - Build tool y dev server
- **React Router** - Enrutamiento
- **Tailwind CSS** - Framework de estilos
- **Lucide React** - Iconos
- **React Hook Form** - Manejo de formularios
- **React Hot Toast** - Notificaciones
- **JS Cookie** - Manejo de cookies

## 📋 Guías de Contribución

### **Añadir Nueva Feature**
1. Crear directorio en `src/features/[feature-name]`
2. Añadir componentes, páginas y lógica relacionada
3. Crear archivo `index.js` para exports
4. Actualizar imports en archivos principales

### **Añadir Componente Compartido**
1. Crear componente en `src/shared/components/`
2. Añadir export en `src/shared/components/index.js`
3. Documentar props y uso

### **Añadir Hook Personalizado**
1. Crear hook en `src/shared/hooks/`
2. Seguir convención `use[HookName].js`
3. Añadir export en `src/shared/hooks/index.js`

## 🔍 Arquitectura de Estados

- **Context API** para estado global (autenticación)
- **useState/useReducer** para estado local de componentes
- **React Hook Form** para estado de formularios

Esta estructura promueve:
- ✅ Código mantenible y escalable
- ✅ Separación clara de responsabilidades
- ✅ Reutilización de componentes
- ✅ Fácil testing y debugging
- ✅ Desarrollo en equipo eficiente