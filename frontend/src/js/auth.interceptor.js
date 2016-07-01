var authInterceptor = angular.module('authInterceptor', []);


authInterceptor.factory('authenticationChecker', ['$q', '$location', function($q, $location) {
    return {
        responseError: function(response) {
            // User not authenticated
            // TODO: maybe handle these differently
            if (response.status == 401 || response.status == 403) {
                $location.path('/login/');
            }
            return $q.reject(response);
        }
    };
}]);
