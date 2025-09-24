import { useAuth } from '../context/AuthContext';

export function useAuthRedirect() {
  const { isAuthenticated, loading } = useAuth();
  
  return {
    isAuthenticated,
    loading,
    shouldRedirectToLogin: !loading && !isAuthenticated,
    shouldRedirectToDashboard: !loading && isAuthenticated,
  };
}
