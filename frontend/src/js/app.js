var app = angular.module('combatTracker', [
    'ngAnimate',
    'ngRoute',
    'ngResource',

    'angular-loading-bar',

    'applicationControllers',

    'navigationControllers',

    'characterControllers',
    'characterServices',

    'userControllers',

    'authInterceptor',

    'encounterControllers',
    'encounterServices',

    'directives',
]);


app.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.interceptors.push('authenticationChecker');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $routeProvider.
        when('/', {
            redirectTo: '/characters'
        }).


        when('/login', {
            templateUrl: 'templates/login.html',
            controller: 'LoginCtrl',
        }).


        when('/register', {
            templateUrl: 'templates/register.html',
            controller: 'RegisterCtrl',
        }).


        when('/registered', {
            templateUrl: 'templates/registered.html',
        }).


        when('/characters', {
            templateUrl: 'templates/characters-list.html',
            controller: 'CharacterListCtrl',
            resolve: {
                players: function(PlayerCharacter) {
                    return PlayerCharacter.query().$promise;
                },
                npcs: function(NonPlayerCharacter) {
                    return NonPlayerCharacter.query().$promise;
                }
            }
        }).
        when('/characters/create', {
            templateUrl: 'templates/characters-create.html',
            controller: 'CharacterCreateCtrl'
        }).
        when('/characters/:uuid', {
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
        when('/encounters/:uuid', {
            templateUrl: 'templates/encounters-detail.html',
            controller: 'EncounterDetailCtrl',
            resolve: {
                encounter: function($route, Encounter) {
                    return Encounter.get($route.current.params).$promise;
                },
                players: function(PlayerCharacter) {
                    return PlayerCharacter.query().$promise;
                },
                npcs: function(NonPlayerCharacter) {
                    return NonPlayerCharacter.query().$promise;
                }
            }
        }).

        otherwise({
            redirectTo: '/'
        });
    }
]);
