var userControllers = angular.module('userControllers', []);


userControllers.controller('LoginCtrl', function ($scope, $location, $http) {
    $scope.username = '';
    $scope.password = '';
    $scope.error = '';

    $scope.login = function() {
        $http.post('/api/auth/', {username: $scope.username, password: $scope.password})
            .then(function() {
                $location.path('/');
            }).catch(function(errorResponse) {
                $scope.username = '';
                $scope.password = '';
                if (errorResponse.status == 400) {
                    $scope.error = errorResponse.data['error'];
                } else {
                    $scope.error = 'An unknown error occured'
                }
            });
    };
});


userControllers.controller('RegisterCtrl', function ($scope, $location, $http) {
    $scope.username = '';
    $scope.email = '';
    $scope.password = '';
    $scope.errors = {};

    $scope.register = function() {
        $http.post('/api/register/', {username: $scope.username, email: $scope.email, password: $scope.password})
            .then(function() {
                $location.path('/registered');
            }).catch(function(errorResponse) {
                $scope.errors = errorResponse.data;
            });
    };
});
