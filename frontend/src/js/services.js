var combatTrackerServices = angular.module('combatTrackerServices', ['ngResource']);

combatTrackerServices.factory('Character', ['$resource', function($resource) {
    return $resource('api/characters/:characterID', {characterID: '@id'});
}]);

combatTrackerServices.factory('Encounter', ['$resource', function($resource) {
    return $resource('api/encounters/:encounterID', {encounterID: '@id'})
}]);
