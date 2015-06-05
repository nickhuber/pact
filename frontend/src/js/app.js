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
            when('/players/add', {
                templateUrl: 'partials/players-add.html',
                controller: 'PlayerAddCtrl'
            }).
            when('/players/:playerID', {
                templateUrl: 'partials/players-detail.html',
                controller: 'PlayerDetailCtrl'
            }).


            when('/npcs', {
                templateUrl: 'partials/npcs-list.html',
                controller: 'NPCListCtrl'
            }).
            when('/npcs/add', {
                templateUrl: 'partials/npcs-add.html',
                controller: 'NPCAddCtrl'
            }).
            when('/npcs/:NPCID', {
                templateUrl: 'partials/npcs-detail.html',
                controller: 'NPCDetailCtrl'
            }).


            otherwise({
                redirectTo: '/'
            });
        }
]);
