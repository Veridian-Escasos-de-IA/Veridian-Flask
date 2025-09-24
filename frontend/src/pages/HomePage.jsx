import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Building2, 
  Users, 
  ShieldCheck, 
  BarChart3,
  Settings,
  Bell,
  Calendar,
  FileText,
  ArrowRight,
  Star
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const HomePage = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 opacity-5">
          <svg
            className="absolute inset-0 h-full w-full"
            fill="none"
            viewBox="0 0 400 400"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              <pattern
                id="large-grid"
                width="100"
                height="100"
                patternUnits="userSpaceOnUse"
              >
                <path
                  d="M 100 0 L 0 0 0 100"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1"
                />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#large-grid)" />
          </svg>
        </div>

        <div className="relative px-4 py-12 sm:px-6 sm:py-16 lg:px-8 lg:py-24">
          <div className="mx-auto max-w-none lg:max-w-screen-2xl px-4 lg:px-8">
            <div className="text-center">
              {/* Logo/Icon */}
              <div className="mx-auto h-16 w-16 sm:h-20 sm:w-20 rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center mb-6 sm:mb-8 shadow-lg">
                <Building2 className="h-8 w-8 sm:h-10 sm:w-10 text-white" />
              </div>

              {/* Title */}
              <h1 className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold tracking-tight text-gray-900">
                Sistema de Gestión del{' '}
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Edificio Multifuncional
                </span>
              </h1>

              {/* Subtitle */}
              <p className="mt-4 sm:mt-6 text-base sm:text-lg leading-6 sm:leading-8 text-gray-600 max-w-3xl lg:max-w-5xl mx-auto px-4 sm:px-0">
                Plataforma integral para la administración eficiente de edificios residenciales y comerciales. 
                Gestiona residentes, departamentos, servicios y mucho más desde una sola aplicación.
              </p>

              {/* CTA Buttons */}
              <div className="mt-8 sm:mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-x-6 px-4 sm:px-0">
                {isAuthenticated ? (
                  <Link
                    to="/dashboard"
                    className="w-full sm:w-auto rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-3 text-sm font-semibold text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 text-center"
                  >
                    Ir al Dashboard
                    <ArrowRight className="ml-2 h-4 w-4 inline" />
                  </Link>
                ) : (
                  <>
                    <Link
                      to="/register"
                      className="w-full sm:w-auto rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-3 text-sm font-semibold text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 text-center"
                    >
                      Comenzar Ahora
                      <ArrowRight className="ml-2 h-4 w-4 inline" />
                    </Link>
                    <Link
                      to="/login"
                      className="w-full sm:w-auto text-sm font-semibold leading-6 text-gray-700 hover:text-gray-900 transition-colors duration-200 text-center py-3"
                    >
                      Iniciar Sesión <span aria-hidden="true">→</span>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 sm:py-24 lg:py-32">
        <div className="mx-auto max-w-none lg:max-w-screen-2xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl lg:max-w-4xl text-center">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-gray-900">
              Características Principales
            </h2>
            <p className="mt-4 sm:mt-6 text-base sm:text-lg leading-6 sm:leading-8 text-gray-600">
              Todo lo que necesitas para gestionar tu edificio de manera eficiente y profesional.
            </p>
          </div>

          <div className="mx-auto mt-12 sm:mt-16 lg:mt-24 max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-6 gap-y-12 sm:gap-x-8 sm:gap-y-16 lg:max-w-none lg:grid-cols-3 xl:grid-cols-3 2xl:grid-cols-3">
              {/* Feature 1 */}
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <div className="h-10 w-10 rounded-lg bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center">
                    <Users className="h-5 w-5 text-white" />
                  </div>
                  Gestión de Residentes
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">
                    Administra la información completa de todos los residentes, incluyendo datos personales, 
                    contactos y asignación de departamentos.
                  </p>
                </dd>
              </div>

              {/* Feature 2 */}
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <div className="h-10 w-10 rounded-lg bg-gradient-to-r from-purple-500 to-purple-600 flex items-center justify-center">
                    <ShieldCheck className="h-5 w-5 text-white" />
                  </div>
                  Seguridad Avanzada
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">
                    Autenticación segura con soporte para OAuth de Google, control de acceso por roles 
                    y protección de datos sensibles.
                  </p>
                </dd>
              </div>

              {/* Feature 3 */}
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <div className="h-10 w-10 rounded-lg bg-gradient-to-r from-indigo-500 to-indigo-600 flex items-center justify-center">
                    <BarChart3 className="h-5 w-5 text-white" />
                  </div>
                  Reportes y Analytics
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">
                    Genera reportes detallados, estadísticas de ocupación y análisis de datos 
                    para una toma de decisiones informada.
                  </p>
                </dd>
              </div>

              {/* Feature 4 */}
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <div className="h-10 w-10 rounded-lg bg-gradient-to-r from-green-500 to-green-600 flex items-center justify-center">
                    <Bell className="h-5 w-5 text-white" />
                  </div>
                  Notificaciones
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">
                    Sistema de notificaciones en tiempo real para mantener informados a residentes 
                    y administradores sobre eventos importantes.
                  </p>
                </dd>
              </div>

              {/* Feature 5 */}
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <div className="h-10 w-10 rounded-lg bg-gradient-to-r from-orange-500 to-orange-600 flex items-center justify-center">
                    <Calendar className="h-5 w-5 text-white" />
                  </div>
                  Gestión de Eventos
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">
                    Programa y gestiona eventos del edificio, reservas de espacios comunes 
                    y coordinación de actividades.
                  </p>
                </dd>
              </div>

              {/* Feature 6 */}
              <div className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <div className="h-10 w-10 rounded-lg bg-gradient-to-r from-pink-500 to-pink-600 flex items-center justify-center">
                    <FileText className="h-5 w-5 text-white" />
                  </div>
                  Documentación
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">
                    Almacena y organiza documentos importantes, contratos, reglamentos 
                    y comunicaciones oficiales del edificio.
                  </p>
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 py-16 sm:py-24 lg:py-32">
        <div className="mx-auto max-w-none lg:max-w-screen-2xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl lg:max-w-none">
            <div className="text-center">
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white">
                Datos del Sistema
              </h2>
              <p className="mt-4 text-base sm:text-lg leading-6 sm:leading-8 text-blue-200">
                Estadísticas actuales de nuestro sistema de gestión
              </p>
            </div>
            <dl className="mt-12 sm:mt-16 grid grid-cols-2 gap-0.5 overflow-hidden rounded-2xl text-center lg:grid-cols-4">
              <div className="flex flex-col bg-white/5 p-4 sm:p-6 lg:p-8">
                <dt className="text-xs sm:text-sm font-semibold leading-6 text-blue-200">Usuarios Registrados</dt>
                <dd className="order-first text-2xl sm:text-3xl font-bold tracking-tight text-white">150+</dd>
              </div>
              <div className="flex flex-col bg-white/5 p-4 sm:p-6 lg:p-8">
                <dt className="text-xs sm:text-sm font-semibold leading-6 text-blue-200">Departamentos</dt>
                <dd className="order-first text-2xl sm:text-3xl font-bold tracking-tight text-white">85</dd>
              </div>
              <div className="flex flex-col bg-white/5 p-4 sm:p-6 lg:p-8">
                <dt className="text-xs sm:text-sm font-semibold leading-6 text-blue-200">Eventos Gestionados</dt>
                <dd className="order-first text-2xl sm:text-3xl font-bold tracking-tight text-white">120+</dd>
              </div>
              <div className="flex flex-col bg-white/5 p-4 sm:p-6 lg:p-8">
                <dt className="text-xs sm:text-sm font-semibold leading-6 text-blue-200">Uptime</dt>
                <dd className="order-first text-2xl sm:text-3xl font-bold tracking-tight text-white">99.9%</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="py-16 sm:py-24 lg:py-32">
        <div className="mx-auto max-w-none lg:max-w-screen-2xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:max-w-3xl text-center">
            <h2 className="text-base sm:text-lg font-semibold leading-8 tracking-tight text-blue-600">Testimonios</h2>
            <p className="mt-2 text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-gray-900">
              Lo que dicen nuestros usuarios
            </p>
          </div>
          <div className="mx-auto mt-12 sm:mt-16 lg:mt-20 flow-root max-w-none">
            <div className="grid grid-cols-1 gap-6 sm:gap-8 lg:grid-cols-3 xl:gap-10">
              {/* Testimonial 1 */}
              <div className="rounded-2xl bg-white p-6 sm:p-8 shadow-lg ring-1 ring-gray-200">
                <div className="flex items-center gap-x-1">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-3 w-3 sm:h-4 sm:w-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <blockquote className="mt-4 sm:mt-6 text-gray-900">
                  <p className="text-sm sm:text-base">
                    "El sistema ha revolucionado la manera en que gestionamos nuestro edificio. 
                    Todo es más eficiente y organizado."
                  </p>
                </blockquote>
                <figcaption className="mt-4 sm:mt-6 flex items-center gap-x-4">
                  <div className="h-8 w-8 sm:h-10 sm:w-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                    <span className="text-xs sm:text-sm font-semibold text-white">AM</span>
                  </div>
                  <div>
                    <div className="text-sm sm:text-base font-semibold">Ana Martínez</div>
                    <div className="text-xs sm:text-sm text-gray-600">Administradora</div>
                  </div>
                </figcaption>
              </div>

              {/* Testimonial 2 */}
              <div className="rounded-2xl bg-white p-6 sm:p-8 shadow-lg ring-1 ring-gray-200">
                <div className="flex items-center gap-x-1">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-3 w-3 sm:h-4 sm:w-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <blockquote className="mt-4 sm:mt-6 text-gray-900">
                  <p className="text-sm sm:text-base">
                    "La interfaz es muy intuitiva y el soporte para Google OAuth hace 
                    que sea súper fácil acceder al sistema."
                  </p>
                </blockquote>
                <figcaption className="mt-4 sm:mt-6 flex items-center gap-x-4">
                  <div className="h-8 w-8 sm:h-10 sm:w-10 rounded-full bg-gradient-to-r from-green-500 to-blue-500 flex items-center justify-center">
                    <span className="text-xs sm:text-sm font-semibold text-white">CL</span>
                  </div>
                  <div>
                    <div className="text-sm sm:text-base font-semibold">Carlos López</div>
                    <div className="text-xs sm:text-sm text-gray-600">Residente</div>
                  </div>
                </figcaption>
              </div>

              {/* Testimonial 3 */}
              <div className="rounded-2xl bg-white p-6 sm:p-8 shadow-lg ring-1 ring-gray-200">
                <div className="flex items-center gap-x-1">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-3 w-3 sm:h-4 sm:w-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <blockquote className="mt-4 sm:mt-6 text-gray-900">
                  <p className="text-sm sm:text-base">
                    "Los reportes y estadísticas nos han ayudado mucho a tomar mejores 
                    decisiones para el edificio."
                  </p>
                </blockquote>
                <figcaption className="mt-4 sm:mt-6 flex items-center gap-x-4">
                  <div className="h-8 w-8 sm:h-10 sm:w-10 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center">
                    <span className="text-xs sm:text-sm font-semibold text-white">MR</span>
                  </div>
                  <div>
                    <div className="text-sm sm:text-base font-semibold">María Rodríguez</div>
                    <div className="text-xs sm:text-sm text-gray-600">Propietaria</div>
                  </div>
                </figcaption>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      {!isAuthenticated && (
        <div className="bg-gray-50">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16 sm:py-24 lg:py-32">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-gray-900">
                ¿Listo para comenzar?
              </h2>
              <p className="mx-auto mt-4 sm:mt-6 max-w-xl text-base sm:text-lg leading-6 sm:leading-8 text-gray-600">
                Únete a nuestra plataforma y lleva la gestión de tu edificio al siguiente nivel.
              </p>
              <div className="mt-8 sm:mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-x-6">
                <Link
                  to="/register"
                  className="w-full sm:w-auto rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-3 text-sm font-semibold text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 text-center"
                >
                  Crear Cuenta Gratis
                </Link>
                <Link
                  to="/login"
                  className="w-full sm:w-auto text-sm font-semibold leading-6 text-gray-900 hover:text-gray-700 text-center py-3"
                >
                  Iniciar Sesión <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-900">
        <div className="mx-auto max-w-none lg:max-w-screen-2xl px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="order-2 md:order-1">
              <p className="text-center md:text-left text-xs leading-5 text-gray-400">
                &copy; 2025 Sistema de Gestión del Edificio Multifuncional. Todos los derechos reservados.
              </p>
            </div>
            <div className="order-1 md:order-2">
              <p className="text-center md:text-right text-xs leading-5 text-gray-400">
                Sistema desarrollado con tecnologías modernas: React, Flask, PostgreSQL
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
