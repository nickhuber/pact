var navigationControllers = angular.module('navigationControllers', []);


navigationControllers.controller('NavigationCtrl', function ($scope, $http, $location)  {
    $scope.rollQuery = '';
    $scope.rollResult = '';

    $scope.isActive = function (viewLocation) {
        return $location.$$path === viewLocation;
    };

    $scope.rollDice = function() {
        $http.post(
            '/api/roll',
            {query: $scope.rollQuery}
        )
        .then(function(response) {
            $scope.rollResult = response.data.total;
        });
    };
});
