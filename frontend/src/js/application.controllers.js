var applicationControllers = angular.module('applicationControllers', []);


applicationControllers.controller('ApplicationCtrl', function ($scope)  {
    $scope.show = true;
    $scope.action = 'Hide';

    $scope.toggleSidebar = function() {
        $scope.show = !$scope.show;
        if ($scope.show) {
            $scope.action = 'Hide';
        } else {
            $scope.action = 'Show';
        }
    };
});
