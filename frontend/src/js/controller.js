var combatTrackerControllers = angular.module('combatTrackerControllers', []);

combatTrackerControllers.controller('PlayerListCtrl', ['$scope', 'Player', 
    function ($scope, Player) {
        $scope.players = Player.query();
    }
]);

combatTrackerControllers.controller('PlayerDetailCtrl', ['$scope', '$routeParams', 'Player', 
    function ($scope, $routeParams, Player) {
        console.log($routeParams);
        $scope.player = Player.get($routeParams);
    }
]);


combatTrackerControllers.controller('NavigationCtrl', ['$scope', '$location', 
    function ($scope, $location)  { 
        $scope.isActive = function (viewLocation) {
            return $location.$$path === viewLocation;
        }
    }
]);
