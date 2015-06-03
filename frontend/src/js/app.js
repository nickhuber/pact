var app = angular.module('combatTracker', [
    'ngRoute',
    'combatTrackerControllers',
    'combatTrackerServices'
]);


app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: 'partials/home.html'
            }).
            when('/players', {
                templateUrl: 'partials/players-list.html',
                controller: 'PlayerListCtrl'
            }).
            when('/players/:playerID', {
                templateUrl: 'partials/players-detail.html',
                controller: 'PlayerDetailCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
        }
]);
