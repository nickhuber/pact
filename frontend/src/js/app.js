var app = angular.module('combatTracker', [
    'ngRoute',
    'combatTrackerControllers',
    'combatTrackerServices',
    'combatTrackerFilters'
]);


app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: 'partials/home.html'
            }).


            when('/characters', {
                templateUrl: 'partials/characters-list.html',
                controller: 'CharacterListCtrl'
            }).
            when('/characters/create', {
                templateUrl: 'partials/characters-create.html',
                controller: 'CharacterCreateCtrl'
            }).
            when('/characters/:characterID', {
                templateUrl: 'partials/characters-detail.html',
                controller: 'CharacterDetailCtrl'
            }).


            when('/encounters', {
                templateUrl: 'partials/encounters-list.html',
                controller: 'EncounterListCtrl'
            }).
            when('/encounters/create', {
                templateUrl: 'partials/encounters-create.html',
                controller: 'EncounterCreateCtrl'
            }).
            when('/encounters/:encounterID', {
                templateUrl: 'partials/encounters-detail.html',
                controller: 'EncounterDetailCtrl'
            }).


            otherwise({
                redirectTo: '/'
            });
        }
]);
