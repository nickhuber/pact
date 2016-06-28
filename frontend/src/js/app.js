var app = angular.module('combatTracker', [
    'ngAnimate',
    'ngRoute',
    'ngResource',

    'angular-loading-bar',

    'applicationControllers',

    'navigationControllers',

    'characterControllers',
    'characterServices',

    'encounterControllers',
    'encounterServices',
]);


app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {
            templateUrl: 'templates/home.html'
        }).


        when('/characters', {
            templateUrl: 'templates/characters-list.html',
            controller: 'CharacterListCtrl',
            resolve: {
                characters: function(Character) {
                    return Character.query().$promise;
                }
            }
        }).
        when('/characters/create', {
            templateUrl: 'templates/characters-create.html',
            controller: 'CharacterCreateCtrl'
        }).
        when('/characters/:id', {
            templateUrl: 'templates/characters-detail.html',
            controller: 'CharacterDetailCtrl',
            resolve: {
                character: function($route, Character) {
                    return Character.get($route.current.params).$promise;
                }
            }
        }).


        when('/encounters', {
            templateUrl: 'templates/encounters-list.html',
            controller: 'EncounterListCtrl',
            resolve: {
                encounters: function(Encounter) {
                    return Encounter.query().$promise;
                }
            }
        }).
        when('/encounters/create', {
            templateUrl: 'templates/encounters-create.html',
            controller: 'EncounterCreateCtrl'
        }).
        when('/encounters/:id', {
            templateUrl: 'templates/encounters-detail.html',
            controller: 'EncounterDetailCtrl',
            resolve: {
                encounter: function($route, Encounter) {
                    return Encounter.get($route.current.params).$promise;
                },
                characters: function(Character) {
                    return Character.query().$promise;
                }
            }
        }).
        when('/encounters/:id/mobile', {
            templateUrl: 'templates/encounter-initiative.html',
            controller: 'EncounterDetailCtrl',
            resolve: {
                encounter: function($route, Encounter) {
                    return Encounter.get($route.current.params).$promise;
                },
                characters: function(Character) {
                    return Character.query().$promise;
                }
            }
        }).

        otherwise({
            redirectTo: '/'
        });
    }
]);
