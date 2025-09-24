import React from 'react';
import { Layout } from '../../shared/components/Layout';
import { useAuth } from '../../context/AuthContext';

export function Dashboard() {
  const { user, isAdmin } = useAuth();

  return (
    <Layout>
      <div className="max-w-none lg:max-w-screen-2xl mx-auto py-4 sm:py-6 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div className="flex-1 min-w-0">
            <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold leading-7 text-gray-900">
              Dashboard
            </h2>
            <p className="mt-1 text-sm text-gray-500">
              Bienvenido/a, {user?.nombre_completo}
            </p>
          </div>
          {isAdmin() && (
            <div className="mt-2 sm:mt-0 sm:ml-4">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Administrador
              </span>
            </div>
          )}
        </div>

        {/* Main content */}
        <div className="mt-6 sm:mt-8">
          <div className="grid grid-cols-1 gap-4 sm:gap-5 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
            {/* Card 1 - Información del Usuario */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-4 sm:p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 sm:h-8 sm:w-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3 sm:ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Mi Perfil
                      </dt>
                      <dd className="text-base sm:text-lg font-medium text-gray-900">
                        {user?.nombre_completo}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 sm:px-5 py-3">
                <div className="text-sm">
                  <p className="text-gray-900">CI: {user?.ci}</p>
                  <p className="text-gray-500">{user?.correo}</p>
                </div>
              </div>
            </div>

            {/* Card 2 - Próximas funcionalidades */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-4 sm:p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 sm:h-8 sm:w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                  <div className="ml-3 sm:ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Espacios
                      </dt>
                      <dd className="text-base sm:text-lg font-medium text-gray-900">
                        Próximamente
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 sm:px-5 py-3">
                <div className="text-sm">
                  <p className="text-gray-500">Gestión de espacios del edificio</p>
                </div>
              </div>
            </div>

            {/* Card 3 - Reservas */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Reservas
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        Próximamente
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-5 py-3">
                <div className="text-sm">
                  <p className="text-gray-500">Sistema de reservas de salas</p>
                </div>
              </div>
            </div>
          </div>

          {/* Información adicional */}
          <div className="mt-8">
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Estado del Sistema
                </h3>
                <div className="mt-2 max-w-xl text-sm text-gray-500">
                  <p>
                    Sistema en desarrollo activo. Nuevas funcionalidades se implementarán cada semana.
                  </p>
                </div>
                <div className="mt-5">
                  <div className="rounded-md bg-green-50 p-4">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-green-800">
                          Autenticación JWT implementada
                        </h3>
                        <div className="mt-2 text-sm text-green-700">
                          <p>
                            Sistema de registro y login funcionando correctamente.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
