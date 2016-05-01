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
            templateUrl: 'partials/home.html'
        }).


        when('/characters', {
            templateUrl: 'partials/characters-list.html',
            controller: 'CharacterListCtrl',
            resolve: {
                characters: function(Character) {
                    return Character.query().$promise;
                }
            }
        }).
        when('/characters/create', {
            templateUrl: 'partials/characters-create.html',
            controller: 'CharacterCreateCtrl'
        }).
        when('/characters/:id', {
            templateUrl: 'partials/characters-detail.html',
            controller: 'CharacterDetailCtrl',
            resolve: {
                character: function($route, Character) {
                    return Character.get($route.current.params).$promise;
                }
            }
        }).


        when('/encounters', {
            templateUrl: 'partials/encounters-list.html',
            controller: 'EncounterListCtrl',
            resolve: {
                encounters: function(Encounter) {
                    return Encounter.query().$promise;
                }
            }
        }).
        when('/encounters/create', {
            templateUrl: 'partials/encounters-create.html',
            controller: 'EncounterCreateCtrl'
        }).
        when('/encounters/:id', {
            templateUrl: 'partials/encounters-detail.html',
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
            templateUrl: 'partials/encounter-initiative.html',
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
